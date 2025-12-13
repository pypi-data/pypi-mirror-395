from scaffoldry.models_pkg.enum_values import ProgrammingLanguage
from scaffoldry.models_pkg.models import (
    BaseTemplate,
    LanguageEnvironment,
    VersionLanguage,
    Author,
)


def create_model() -> BaseTemplate:
    return BaseTemplate(
        repository_name="packagerepository",
        author_repository="author",
        language_environment=LanguageEnvironment(
            programming_language=ProgrammingLanguage.PYTHON,
            version_language=VersionLanguage(major=3, minor=10, patch=1),
        ),
        description="Put here your definition of package",
        package_name="packagename",
        author=Author(
            first_name="firstname",
            last_name="lastname",
            middle_name="middlename",
            email="yourmail@domain.com",
        ),
        version=VersionLanguage(major=0, minor=0, patch=0),
    )
