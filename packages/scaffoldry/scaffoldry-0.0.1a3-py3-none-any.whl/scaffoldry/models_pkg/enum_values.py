from enum import Enum


class RelationshipValue(str, Enum):
    EQUAL = "="
    NOT_EQUAL = "!="
    MORE_THAN = ">"
    LESS_THAN = "<"
    MORE_OR_EQUAL_THAN = ">="
    LESS_OR_EQUAL_THAN = "<="


class FrameworkUsed(str, Enum):
    DJANGO = "django"
    FASTAPI = "fastapi"


class ProgrammingLanguage(str, Enum):
    """Programming language in which we want to generate the template."""

    PYTHON = "python"
