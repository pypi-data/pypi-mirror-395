import pathlib
import click
from dotenv import dotenv_values

def clean_empty_lines(input_str: str):
    return "\n".join(filter(None, input_str.splitlines()))


def warn_non_wolfi_distro(config_json: dict) -> None:
    """Show warning if image_distro is not set to 'wolfi'."""
    image_distro = config_json.get("image_distro", "debian")  # Default is debian
    if image_distro != "wolfi":
        click.secho(
            "⚠️  安全建议:考虑切换至Wolfi Linux以增强安全性。",
            fg="yellow",
            bold=True,
        )
        click.secho(
            "   Wolfi 是一款面向容器的安全导向型极简 Linux 发行版。",
            fg="yellow",
        )
        click.secho(
            '   要切换，请在您的 orcaagent.json 配置文件中添加 \'"image_distro": "wolfi"\'。',
            fg="yellow",
        )
        click.secho("")  # Empty line for better readability

def _load_env_vars(env_config: object, base_dir: pathlib.Path) -> dict[str, str]:
    if env_config is None:
        return {}

    if isinstance(env_config, str):
        env_path = (base_dir / env_config).resolve()
        if not env_path.exists():
            raise click.UsageError(f"找不到 env 文件: {env_path}")
        values = {
            key: value
            for key, value in dotenv_values(env_path).items()
            if value is not None
        }
        return values

    if isinstance(env_config, dict):
        return {str(key): "" if value is None else str(value) for key, value in env_config.items()}

    raise click.UsageError("env 配置必须是字符串路径或键值映射。")