from typing import Any

from nesso_cli.models.common import get_current_dbt_project_path

project_path = get_current_dbt_project_path()
ctx = {
    "PROJECT_DIR": project_path,
    "DBT_PROJECT": None,
    "PROJECT_NAME": project_path.name,
}


def set(key: str, value: Any) -> None:
    global context
    ctx.update({key: value})


def get(key: str) -> Any:
    global context
    return ctx.get(key)
