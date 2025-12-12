import typer
from typing_extensions import Annotated

from nesso_cli.models.common import call_shell, wrapper_context_settings

app = typer.Typer()


@app.command(context_settings=wrapper_context_settings)
def generate(
    ctx: typer.Context,
    select: Annotated[
        str, typer.Option("--select", "-s", help="The model(s) to select.")
    ] = None,
):
    """Generate metadata for the project."""
    # Process arguments.
    args = []
    if select:
        args.extend(["-s", select])
    if ctx.args:
        args.extend(ctx.args)

    call_shell("dbt docs generate", args=args, print_logs=True)
