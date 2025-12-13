import json
import pathlib
import shutil
from typing import Literal, NamedTuple, Optional

import click.exceptions

from orcaagent_cli.exec import subp_exec
from orcaagent_cli.config import validate_config_file, config_to_docker,default_base_image
from orcaagent_cli.util import _load_env_vars
ROOT = pathlib.Path(__file__).parent.resolve()
POSTGRES_HOST = "orcakit-postgres"
POSTGRES_PORT = "5432"
POSTGRES_DB = "postgres"
POSTGRES_USER = "postgres"
POSTGRES_PASSWORD = "postgres"
DEFAULT_POSTGRES_URI = (
    f"postgres://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}?sslmode=disable"
)


class Version(NamedTuple):
    major: int
    minor: int
    patch: int


DockerComposeType = Literal["plugin", "standalone"]


class DockerCapabilities(NamedTuple):
    version_docker: Version
    version_compose: Version
    healthcheck_start_interval: bool
    compose_type: DockerComposeType = "plugin"


def _parse_version(version: str) -> Version:
    parts = version.split(".", 2)
    if len(parts) == 1:
        major = parts[0]
        minor = "0"
        patch = "0"
    elif len(parts) == 2:
        major, minor = parts
        patch = "0"
    else:
        major, minor, patch = parts
    return Version(
        int(major.lstrip("v")), int(minor), int(patch.split("-")[0].split("+")[0])
    )


def check_capabilities(runner) -> DockerCapabilities:
    # check docker available
    if shutil.which("docker") is None:
        raise click.UsageError("Docker not installed") from None

    try:
        stdout, _ = runner.run(
            subp_exec("docker", "info", "-f", "{{json .}}", collect=True)
        )
        info = json.loads(stdout)
    except (click.exceptions.Exit, json.JSONDecodeError):
        raise click.UsageError("Docker not installed or not running") from None

    if not info["ServerVersion"]:
        raise click.UsageError("Docker not running") from None

    compose_type: DockerComposeType
    try:
        compose = next(
            p for p in info["ClientInfo"]["Plugins"] if p["Name"] == "compose"
        )
        compose_version_str = compose["Version"]
        compose_type = "plugin"
    except (KeyError, StopIteration):
        if shutil.which("docker-compose") is None:
            raise click.UsageError("Docker Compose not installed") from None

        compose_version_str, _ = runner.run(
            subp_exec("docker-compose", "--version", "--short", collect=True)
        )
        compose_type = "standalone"

    # parse versions
    docker_version = _parse_version(info["ServerVersion"])
    compose_version = _parse_version(compose_version_str)

    # check capabilities
    return DockerCapabilities(
        version_docker=docker_version,
        version_compose=compose_version,
        healthcheck_start_interval=docker_version >= Version(25, 0, 0),
        compose_type=compose_type,
    )


def debugger_compose(
    *, port: Optional[int] = None, base_url: Optional[str] = None
) -> dict:
    if port is None:
        return ""

    config = {
        "orcakit-debugger": {
            "image": "langchain/langgraph-debugger",
            "restart": "on-failure",
            "depends_on": {
                "orcakit-postgres": {"condition": "service_healthy"},
            },
            "ports": [f'"{port}:3968"'],
        }
    }

    if base_url:
        config["orcakit-debugger"]["environment"] = {
            "VITE_STUDIO_LOCAL_GRAPH_URL": base_url
        }

    return config


# Function to convert dictionary to YAML
def dict_to_yaml(d: dict, *, indent: int = 0) -> str:
    """Convert a dictionary to a YAML string."""
    yaml_str = ""

    for idx, (key, value) in enumerate(d.items()):
        # Format things in a visually appealing way
        # Use an extra newline for top-level keys only
        if idx >= 1 and indent < 2:
            yaml_str += "\n"
        space = "    " * indent
        if isinstance(value, dict):
            yaml_str += f"{space}{key}:\n" + dict_to_yaml(value, indent=indent + 1)
        elif isinstance(value, list):
            yaml_str += f"{space}{key}:\n"
            for item in value:
                yaml_str += f"{space}    - {item}\n"
        else:
            # Handle multiline strings properly
            if isinstance(value, str) and '\n' in value:
                # Use YAML literal block scalar for multiline strings
                yaml_str += f"{space}{key}: |\n"
                for line in value.split('\n'):
                    yaml_str += f"{space}    {line}\n"
            else:
                yaml_str += f"{space}{key}: {value}\n"
    return yaml_str


def compose_as_dict(
    capabilities: DockerCapabilities,
    *,
    port: int,
    debugger_port: Optional[int] = None,
    debugger_base_url: Optional[str] = None,
    # postgres://user:password@host:port/database?option=value
    postgres_uri: Optional[str] = None,
    # If you are running against an already-built image, you can pass it here
    image: Optional[str] = None,
    # Base image to use for the LangGraph API server
    base_image: Optional[str] = None,
    # API version of the base image
    api_version: Optional[str] = None,
    # Chat UI options
    enable_chat_ui: bool = False,
    chat_ui_context: Optional[str] = None,
    chat_ui_port: int = 3000,
    # Config integration options
    config_path: Optional[pathlib.Path] = None,
    config: Optional[dict] = None,
    watch: bool = False,
    langsmith_key: Optional[str] = None,
    assistant_id: Optional[str] = None,
) -> dict:
    """Create a docker compose file as a dictionary in YML style."""
    if postgres_uri is None:
        include_db = True
        postgres_uri = DEFAULT_POSTGRES_URI
    else:
        include_db = False

    # The services below are defined in a non-intuitive order to match
    # the existing unit tests for this function.
    # It's fine to re-order just requires updating the unit tests, so it should
    # be done with caution.

    # Define the Redis service first as per the test order
    services = {
        "orcakit-redis": {
            "image": "redis:6",
            "healthcheck": {
                "test": "redis-cli ping",
                "interval": "5s",
                "timeout": "1s",
                "retries": 5,
            },
        }
    }

    # Add Postgres service before orcakit-api if it is needed
    if include_db:
        services["orcakit-postgres"] = {
            "image": "pgvector/pgvector:pg16",
            "ports": ['"5433:5432"'],
            "environment": {
                "POSTGRES_DB": "postgres",
                "POSTGRES_USER": "postgres",
                "POSTGRES_PASSWORD": "postgres",
            },
            "command": ["postgres", "-c", "shared_preload_libraries=vector"],
            "volumes": ["orcakit-data:/var/lib/postgresql/data"],
            "healthcheck": {
                "test": "pg_isready -U postgres",
                "start_period": "10s",
                "timeout": "1s",
                "retries": 5,
            },
        }
        if capabilities.healthcheck_start_interval:
            services["orcakit-postgres"]["healthcheck"]["interval"] = "60s"
            services["orcakit-postgres"]["healthcheck"]["start_interval"] = "1s"
        else:
            services["orcakit-postgres"]["healthcheck"]["interval"] = "5s"

    # Add optional debugger service if debugger_port is specified
    if debugger_port:
        services["orcakit-debugger"] = debugger_compose(
            port=debugger_port, base_url=debugger_base_url
        )["orcakit-debugger"]

    # Add orcakit-api service
    services["orcakit-api"] = {
        "ports": [f'"127.0.0.1:{port}:{port}"'],
        "depends_on": {
            "orcakit-redis": {"condition": "service_healthy"},
        },
        "environment": {
            "REDIS_URI": "redis://orcakit-redis:6379",
            "POSTGRES_URI": postgres_uri,
            "ORCAKIT_SERVER_HOST": "0.0.0.0",
            "ORCAKIT_SERVER_PORT": str(port),
            "PORT": str(port),
        },
    }
    if image:
        services["orcakit-api"]["image"] = image

    # If Postgres is included, add it to the dependencies of orcakit-api
    if include_db:
        services["orcakit-api"]["depends_on"]["orcakit-postgres"] = {
            "condition": "service_healthy"
        }

    # Additional healthcheck for orcakit-api - use curl for reliability
    if capabilities.healthcheck_start_interval:
        services["orcakit-api"]["healthcheck"] = {
            "test": f'["CMD", "curl", "-f", "http://localhost:{port}/ok"]',
            "interval": "10s",
            "start_interval": "2s",
            "start_period": "30s",
            "timeout": "5s",
            "retries": 5,
        }

    # Integrate config-based build configuration if provided
    if config_path and config and not image:
        _integrate_config_build(services["orcakit-api"], config_path, config, base_image, api_version, watch)
    # Add agent-chat-ui service if enabled
    if enable_chat_ui and chat_ui_context:
        services["agent-chat-ui"] = _create_chat_ui_service_dict(
            chat_ui_context, 
            chat_ui_port, 
            port,
            config_path
        )

    # Final compose dictionary with volumes included if needed
    compose_dict = {}
    if include_db:
        compose_dict["volumes"] = {"orcakit-data": {"driver": "local"}}
    compose_dict["services"] = services

    return compose_dict


def compose(
    capabilities: DockerCapabilities,
    *,
    port: int,
    debugger_port: Optional[int] = None,
    debugger_base_url: Optional[str] = None,
    # postgres://user:password@host:port/database?option=value
    postgres_uri: Optional[str] = None,
    image: Optional[str] = None,
    base_image: Optional[str] = None,
    api_version: Optional[str] = None,
    # Chat UI options
    enable_chat_ui: bool = False,
    chat_ui_context: Optional[str] = None,
    chat_ui_port: int = 3000,
    # Config integration options
    config_path: Optional[pathlib.Path] = None,
    config: Optional[dict] = None,
    watch: bool = False,
    langsmith_key: Optional[str] = None,
    assistant_id: Optional[str] = None,
) -> str:
    """Create a docker compose file as a string."""
    compose_content = compose_as_dict(
        capabilities,
        port=port,
        debugger_port=debugger_port,
        debugger_base_url=debugger_base_url,
        postgres_uri=postgres_uri,
        image=image,
        base_image=base_image,
        api_version=api_version,
        enable_chat_ui=enable_chat_ui,
        chat_ui_context=chat_ui_context,
        chat_ui_port=chat_ui_port,
        config_path=config_path,
        config=config,
        watch=watch,
        langsmith_key=langsmith_key,
        assistant_id=assistant_id,
    )
    print(f"compose_content "+ str(compose_content))
    compose_str = dict_to_yaml(compose_content)
    return compose_str


def _create_chat_ui_service_dict(
    context: str, 
    ui_port: int, 
    api_port: int,
    config: pathlib.Path,
) -> dict:
    """生成写死配置的 agent-chat-ui 服务定义"""

    config_json = validate_config_file(config)
    env_config = config_json.get("env")
    env_vars = _load_env_vars(env_config, config.parent)
    langsmith_key = env_vars.get("LANGSMITH_API_KEY", "")
    assistant_id = None
    graphs = config_json.get("graphs", {})
    if graphs:
        assistant_id = list(graphs.keys())[0]
        click.secho(f"🔍 检测到 assistant_id: {assistant_id}", fg="cyan")
    else:
        raise click.UsageError("配置文件中未找到任何 graph")

    
    return {
        "ports": [f"{ui_port}:3000"],
        "depends_on": {
            "orcakit-api": {"condition": "service_healthy"}
        },
        "build": {
            "context": context,
            "dockerfile": "Dockerfile",
            "args": {
                "NEXT_PUBLIC_API_URL": f"http://localhost:{api_port}",
                "NEXT_PUBLIC_ASSISTANT_ID": assistant_id,
                "LANGSMITH_API_KEY": langsmith_key
            }
        },
        "environment": {
            "NEXT_PUBLIC_API_URL": f"http://localhost:{api_port}",
            "NEXT_PUBLIC_ASSISTANT_ID": assistant_id
        },
        "healthcheck": {
            "test": ["CMD", "curl", "-f", "http://localhost:3000"],
            "interval": "60s", 
            "timeout": "10s",
            "retries": 5,
            "start_period": "120s"
        }
    }


def _integrate_config_build(
    orcakit_api_service: dict,
    config_path: pathlib.Path,
    config: dict,
    base_image: Optional[str],
    api_version: Optional[str],
    watch: bool
) -> None:
    """将 config 中的 build 配置集成到 orcakit-api 服务中"""
    import orcaagent_cli.config
    
    # 获取默认 base_image
    base_image = base_image or default_base_image(config)
    
    # 添加环境变量
    env_vars = config.get("env", {})
    if isinstance(env_vars, dict):
        orcakit_api_service["environment"].update(env_vars)
    elif isinstance(env_vars, str):
        orcakit_api_service["env_file"] = env_vars
    
    # 添加 build 配置
    orcakit_api_service["pull_policy"] = "build"
    
    # 生成 dockerfile
    dockerfile, additional_contexts = config_to_docker(
        config_path, config, base_image, api_version
    )
    
    build_config = {
        "context": ".",
        "dockerfile_inline": dockerfile
    }
    
    # 添加额外的构建上下文
    if additional_contexts:
        build_config["additional_contexts"] = [
            f"{name}: {path}" for name, path in additional_contexts.items()
        ]
    
    orcakit_api_service["build"] = build_config
    
    # 添加 watch 配置
    if watch:
        dependencies = config.get("dependencies") or ["."]
        watch_paths = [config_path.name] + [
            dep for dep in dependencies if dep.startswith(".")
        ]
        watch_actions = [
            {"path": path, "action": "rebuild"} for path in watch_paths
        ]
        orcakit_api_service["develop"] = {
            "watch": watch_actions
        }
