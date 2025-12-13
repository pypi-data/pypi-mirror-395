import json
from pathlib import Path

import typer

from scaffoldry.generators.core import prepare_project
from scaffoldry.init_template_objs.python_pkg import create_model
from scaffoldry.main_arguments import CommandAppGenerate, CommandAppCreate
from scaffoldry.models_pkg.models import BaseTemplate

app = typer.Typer()


@app.command()
def generate(
    path_definition: str = CommandAppGenerate.path_definition,
    path_location: str = CommandAppGenerate.path_location,
) -> None:
    """Generate all the content related with the input file provided"""
    with open(path_definition, "r") as f_r:
        model_obj = json.load(f_r)
    prepare_project(Path(path_location), BaseTemplate.model_validate(model_obj))


@app.command()
def create_template(
    path_loc: str = CommandAppCreate.path_loc,
) -> None:
    """Create a template in json in order to modify it."""
    var_model = create_model()
    Path(path_loc).parent.mkdir(parents=True, exist_ok=True)
    Path(path_loc).write_text(var_model.model_dump_json(indent=2))


def main() -> None:
    app()


if __name__ == "__main__":
    main()
