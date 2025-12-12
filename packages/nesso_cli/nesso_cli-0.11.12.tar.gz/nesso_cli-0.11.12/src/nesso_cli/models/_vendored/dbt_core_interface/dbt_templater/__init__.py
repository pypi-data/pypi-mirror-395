"""Defines the hook endpoints for the dbt templater plugin."""
import logging

from sqlfluff.core.plugin import hookimpl

from nesso_cli.models._vendored.dbt_core_interface.dbt_templater.templater import (
    DCIDbtTemplater,
)

LOGGER = logging.getLogger(__name__)


@hookimpl
def get_templaters():
    """Get templaters."""
    def create_templater(**kwargs):
        import nesso_cli.models.dbt_core_interface.state
        assert nesso_cli.models.dbt_core_interface.state.dbt_project_container is not None, "dbt_project_container is None"
        return DCIDbtTemplater(
            dbt_project_container=nesso_cli.models.dbt_core_interface.state.dbt_project_container,
            **kwargs
        )

    create_templater.name = DCIDbtTemplater.name
    return [create_templater]
