from pathlib import Path

from scaffoldry.templates import core


current_folder = Path(__file__).parent.relative_to(core._path)
pyproject_toml_j2_path = current_folder / "pyproject.toml.j2"
gitignore_j2_path = current_folder / ".gitignore.j2"
checks_sh_j2_path = current_folder / "checks.sh.j2"
ci_yml_j2 = current_folder / "ci.yml.j2"
release_yml_j2 = current_folder / "release.yml.j2"
flake8_j2 = current_folder / ".flake8.j2"
package_base_name = current_folder / "main.py.j2"
pre_commit_config_yaml_j2 = current_folder / ".pre-commit-config.yaml.j2"
