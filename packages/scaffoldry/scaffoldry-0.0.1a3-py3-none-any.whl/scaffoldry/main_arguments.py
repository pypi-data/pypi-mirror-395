import typer


class CommandAppGenerate:
    path_definition = typer.Argument(..., help="Path with the definition file")
    path_location = typer.Argument(
        ..., help="Output root path in which the project is generated"
    )


class CommandAppCreate:
    path_loc = typer.Argument(help="Path to store the template")
