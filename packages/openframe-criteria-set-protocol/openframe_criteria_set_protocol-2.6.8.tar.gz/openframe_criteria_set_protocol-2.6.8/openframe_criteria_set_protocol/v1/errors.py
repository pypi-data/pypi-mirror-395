import typing
from dataclasses import dataclass, field
from typing import Optional


ValidationErrorType = typing.Literal['data', 'parameter']


@dataclass(frozen=True)
class ValidationError(Exception):
    errorType: ValidationErrorType
    code: str
    path: Optional[str]
    arguments: Optional[dict[str, str]]


@dataclass(frozen=True)
class DataValidationError(ValidationError):
    errorType: ValidationErrorType = field(init=False, default='data')


@dataclass(frozen=True)
class ParameterValidationError(ValidationError):
    errorType: ValidationErrorType = field(init=False, default='parameter')


# Helper errors
class CriteriaSetIdNotFoundError(Exception):
    pass


class CriteriaSetVersionNotFoundError(Exception):
    pass
