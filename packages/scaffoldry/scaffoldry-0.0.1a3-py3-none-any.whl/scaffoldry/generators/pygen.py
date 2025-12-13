from pathlib import Path

from scaffoldry.models_pkg.models import BaseTemplate
from scaffoldry.templates.pypackage import paths
from scaffoldry.templates.core import (
    TemplateConfigElement,
    generate_final_files,
)


def prepare_project_python(
    root_location: Path, in_project: BaseTemplate
) -> None:
    """Prepare all the files from a project in python."""
    root_location.mkdir(parents=True, exist_ok=True)

    generate_final_files(
        in_project,
        root_location,
        [
            TemplateConfigElement(
                in_path_template=paths.pyproject_toml_j2_path
            ),
            TemplateConfigElement(in_path_template=paths.gitignore_j2_path),
            TemplateConfigElement(
                in_path_template=paths.pre_commit_config_yaml_j2
            ),
            TemplateConfigElement(
                in_path_template=paths.checks_sh_j2_path,
                out_relative_folder=Path("scripts"),
            ),
            TemplateConfigElement(
                in_path_template=paths.ci_yml_j2,
                out_relative_folder=Path(".github", "workflows"),
            ),
            TemplateConfigElement(
                in_path_template=paths.release_yml_j2,
                out_relative_folder=Path(root_location, ".github", "workflows"),
            ),
            TemplateConfigElement(
                in_path_template=paths.flake8_j2,
            ),
            TemplateConfigElement(
                in_path_template=paths.package_base_name,
                out_relative_folder=Path(
                    root_location, "src", in_project.package_name
                ),
                out_base_name="main.py",
            ),
        ],
    )
    Path(root_location, "src", in_project.package_name, "__init__.py").touch()
