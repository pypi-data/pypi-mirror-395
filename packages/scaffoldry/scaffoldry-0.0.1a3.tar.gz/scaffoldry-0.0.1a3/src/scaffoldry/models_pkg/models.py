"""Models for putting the input of the desired content"""

from typing import Optional

from pydantic import BaseModel, field_validator

from scaffoldry.models_pkg.enum_values import (
    FrameworkUsed,
    ProgrammingLanguage,
    RelationshipValue,
)


class Author(BaseModel):
    first_name: Optional[str] = ""
    middle_name: Optional[str] = ""
    last_name: Optional[str] = ""
    email: Optional[str] = ""


class Version(BaseModel):
    major: int
    minor: int
    patch: int


class VersionLanguage(Version):
    relationship: RelationshipValue = RelationshipValue.EQUAL


class VersionRelease(Version):
    finalacronym: Optional[str] = None


class LanguageEnvironment(BaseModel):
    programming_language: ProgrammingLanguage
    framework_language: Optional[FrameworkUsed] = None
    version_language: Optional[VersionLanguage] = None


class BaseTemplate(BaseModel):
    language_environment: LanguageEnvironment
    description: str
    package_name: str
    repository_name: str
    author_repository: str
    author: Author
    version: Version

    @field_validator("package_name")
    def check_spaces(cls, in_str: str) -> str:
        if " " in in_str:
            raise ValueError("there are spaces into package name")
        return in_str
