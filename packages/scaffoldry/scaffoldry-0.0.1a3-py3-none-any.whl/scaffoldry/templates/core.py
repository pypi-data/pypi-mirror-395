from pathlib import Path
from typing import Optional, List

from jinja2 import Environment, FileSystemLoader, Template
from pydantic import BaseModel

from scaffoldry.models_pkg.models import BaseTemplate


def get_template(in_path_template: Path) -> Template:
    return _env.get_template(in_path_template.as_posix())


def render_template(
    in_base_obj: BaseTemplate, in_path_template: Path, out_path: Path
) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.open("w").write(
        get_template(in_path_template).render(in_base_obj.model_dump())
    )


def final_basename(template_base: Path) -> str:
    return template_base.name.replace(".j2", "")


def generate_final_file(
    in_base_obj: BaseTemplate,
    in_path_template: Path,
    out_path_folder: Path,
    out_base_name: Optional[str] = None,
) -> None:
    if out_base_name is None:
        out_base_name = final_basename(in_path_template)

    render_template(
        in_base_obj,
        in_path_template,
        out_path_folder / out_base_name,
    )


class TemplateConfigElement(BaseModel):
    in_path_template: Path
    out_relative_folder: Path = Path("")
    out_base_name: Optional[str] = None


def generate_final_files(
    in_base_obj: BaseTemplate,
    common_root_location: Path,
    list_templates_config_elements: List[TemplateConfigElement],
) -> None:
    for in_template in list_templates_config_elements:
        if in_template.out_base_name is None:
            in_template.out_base_name = final_basename(
                in_template.in_path_template
            )

        render_template(
            in_base_obj,
            in_template.in_path_template,
            common_root_location
            / in_template.out_relative_folder
            / in_template.out_base_name,
        )


_path = Path(__file__).parent
_env = Environment(loader=FileSystemLoader(_path.as_posix()))
