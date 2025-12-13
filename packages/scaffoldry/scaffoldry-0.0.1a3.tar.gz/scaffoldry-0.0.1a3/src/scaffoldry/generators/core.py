from scaffoldry.generators.pygen import prepare_project_python
from scaffoldry.models_pkg.enum_values import ProgrammingLanguage
from scaffoldry.models_pkg.models import BaseTemplate
from pathlib import Path


def prepare_project(root_location: Path, in_project: BaseTemplate) -> None:
    if (
        in_project.language_environment.programming_language
        is ProgrammingLanguage.PYTHON
    ):
        prepare_project_python(root_location, in_project)
