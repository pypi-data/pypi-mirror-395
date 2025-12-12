import datetime
import typing
from abc import ABC
from dataclasses import dataclass, field
from typing import Optional, Literal

from typing_extensions import Required

CertificationDefinitionType = Literal['number', 'percentage']


@dataclass(slots=True)
class CertificationDefinition(ABC):
    code: str
    type: str
    name: str
    rules: Optional[ABC] = None
    rulesText: Optional[str] = None
    icon: Optional[str] = None
    url: Optional[str] = None
    description: Optional[str] = None


@dataclass(slots=True)
class NumberBasedCertificationDefinitionRules:
    minimum: Optional[float] = None
    maximum: Optional[float] = None
    exclusiveMinimum: Optional[float] = None
    exclusiveMaximum: Optional[float] = None


PercentageBasedCertificationDefinitionRules = NumberBasedCertificationDefinitionRules


@dataclass(slots=True)
class NumberBasedCertificationDefinition(CertificationDefinition):
    type: Literal["number"] = field(init=False, default='number')
    rules: NumberBasedCertificationDefinitionRules


@dataclass(slots=True)
class PercentageBasedCertificationDefinition(CertificationDefinition):
    type: Literal["percentage"] = field(init=False, default='percentage')
    rules: PercentageBasedCertificationDefinitionRules


@dataclass(slots=True)
class RgbColor:
    red: int
    green: int
    blue: int


Color = typing.Union[RgbColor, str]


@dataclass(slots=True)
class ThemeStyle:
    primaryColor: Color
    secondaryColor: Color


@dataclass(slots=True)
class DocumentationItem(ABC):
    type: str
    label: str
    text: str
    url: Optional[str] = None


@dataclass(slots=True)
class PdfDocumentationItem(DocumentationItem):
    type: str = field(init=False, default='pdf')


@dataclass(slots=True)
class InlineDocumentationItem(DocumentationItem):
    type: str = field(init=False, default='text')


@dataclass(slots=True)
class LinkDocumentationItem(DocumentationItem):
    type: str = field(init=False, default='link')


TaskItemScalarValue = typing.Union[str, float, bool, None]
TaskItemValue = typing.Union[TaskItemScalarValue, list[TaskItemScalarValue]]
DefinitionType = Literal['select-single', 'select-multiple', 'number', 'boolean']
TaskItemValueMap = dict[str, TaskItemValue]


@dataclass(slots=True)
class PointOption:
    value: TaskItemScalarValue
    text: str
    id: Optional[str] = None
    intro: Optional[str] = None
    outro: Optional[str] = None


@dataclass(slots=True)
class BaseTaskItemDefinition(ABC):
    type: DefinitionType = field(init=True)


@dataclass(slots=True)
class SelectSingleType(BaseTaskItemDefinition):
    type: DefinitionType = field(init=False, default='select-single')
    options: list[PointOption]
    minimum: Optional[float] = None
    maximum: Optional[float] = None
    label: Optional[str] = None
    readOnly: Optional[bool] = None
    defaultValue: Optional[str] = None


@dataclass(slots=True)
class SelectMultipleType(BaseTaskItemDefinition):
    type: DefinitionType = field(init=False, default='select-multiple')
    options: list[PointOption]
    minimum: Optional[float] = None
    maximum: Optional[float] = None
    label: Optional[str] = None
    readOnly: Optional[bool] = None
    defaultValue: Optional[list[str]] = None


@dataclass(slots=True)
class NumberType(BaseTaskItemDefinition):
    type: DefinitionType = field(init=False, default='number')
    minimum: Optional[float] = None
    maximum: Optional[float] = None
    step: Optional[float] = None
    label: Optional[str] = None
    readOnly: Optional[bool] = None
    defaultValue: Optional[float] = None


@dataclass(slots=True)
class BooleanType(BaseTaskItemDefinition):
    type: DefinitionType = field(init=False, default='boolean')
    labels: Optional[dict[str, str]] = None
    label: Optional[str] = None
    readOnly: Optional[bool] = None
    defaultValue: Optional[bool] = None


TaskItemDefinition = typing.Union[SelectSingleType, SelectMultipleType, NumberType, BooleanType]
CriteriaTreeElementType = Literal['theme', 'criterion', 'task-group', 'task', 'task-item']


@dataclass(slots=True)
class ThemeOptions:
    # Whether to hide the theme from the breadcrumbs
    hideFromBreadcrumbs: bool

    # Whether to hide the theme from the document tree structure
    hideFromDocumentTree: bool

    # Whether to hide the theme code in the generated PDF report
    hideCodeInReport: bool

    # The format of the report row text, use ':code:' and ':title:' to define where the code and/or title
    # should be inserted, if not provided only the title will be rendered
    reportTitleTextFormat: Optional[str] = ":title:"

    # The format of the breadcrumb text, use ':code:' and ':title:' to define
    # where the code and/or title should be inserted
    breadcrumbTextFormat: Optional[str] = ":title:"

    # The format of the document tree folder text, use ':code:' and ':title:' to define where the code and/or title
    # should be inserted
    documentTreeFolderTextFormat: Optional[str] = ":code:"


@dataclass(slots=True)
class CriterionOptions:
    # Whether to hide the criterion from the breadcrumbs
    hideFromBreadcrumbs: bool

    # Whether to hide the criterion from the document tree structure
    hideFromDocumentTree: bool

    # Whether to hide the criterion code in the generated PDF report
    hideCodeInReport: bool

    # The format of the report row text, use ':code:' and ':title:' to define where the code and/or title
    # should be inserted, if not provided only the title will be rendered
    reportTitleTextFormat: Optional[str] = ":title:"

    # The format of the breadcrumb text, use ':code:' and ':title:' to define
    # where the code and/or title should be inserted
    breadcrumbTextFormat: Optional[str] = ":title:"

    # The format of the document tree folder text, use ':code:' and ':title:' to define where the code and/or title
    # should be inserted
    documentTreeFolderTextFormat: Optional[str] = ":code:"

    # The format of the criteria tree element text, use ':code:' and ':title:' to define where the code and/or title
    # should be inserted
    criteriaTreeElementTextFormat: Optional[str] = ":code: :title:"


@dataclass(slots=True)
class TaskOptions:
    # The format of the breadcrumb text, use ':code:' and ':title:' to define where the code and/or title
    # should be inserted
    breadcrumbTextFormat: str = ":title:"

    # The format of the document tree folder text, use ':code:' and ':title:' to define where the code and/or title
    # should be inserted
    documentTreeFolderTextFormat: str = ":code:"

    # The format of the report row text, use ':code:' and ':title:' to define where the code and/or title
    # should be inserted, if not provided only the title will be rendered
    reportTitleTextFormat: Optional[str] = ":title:"

    # Whether the title of the indicator task view should show the task code, or the hardcoded description text
    showCodeAsIndicatorTaskViewTitle: bool = False

    # The format of the criteria tree element text, use ':code:' and ':title:' to define where the code and/or title
    # should be inserted
    criteriaTreeElementTextFormat: Optional[str] = ":code: :title:"


@dataclass(slots=True)
class TaskItemOptions:
    # Whether to exclude this task item from the targets page altogether
    excludeFromTargets: Optional[bool] = None


class NumericElementDataValue(typing.TypedDict, total=False):
    value: Required[int | float]
    minimumValue: Optional[int | float]
    maximumValue: Optional[int | float]
    minimumValue: Optional[int | float]
    exclusiveMaximum: Optional[int | float]
    exclusiveMinimum: Optional[int | float]
    weight: Optional[int | float]


class NumberElementDataValue(NumericElementDataValue, total=False):
    type: Literal['number']
    total: Required[int | float]


class PercentageElementDataValue(NumericElementDataValue, total=False):
    type: Required[Literal['percentage']]


class BooleanElementDataValue(typing.TypedDict, total=False):
    type: Required[Literal['boolean']]
    value: Required[bool]


class ElementDataText(typing.TypedDict, total=False):
    text: Required[str]


class NumberElementData(ElementDataText, NumberElementDataValue, total=False):
    pass


class PercentageElementData(ElementDataText, PercentageElementDataValue, total=False):
    pass


class BooleanElementData(ElementDataText, BooleanElementDataValue, total=False):
    pass


ElementData = NumberElementData | PercentageElementData | BooleanElementData


class AbstractTaskItemData(typing.TypedDict, total=False):
    valueReference: Optional[TaskItemValue]
    readOnly: Required[bool]


class NumberTaskItemData(AbstractTaskItemData, ElementDataText, NumberElementDataValue, total=False):
    pass


class PercentageTaskItemData(AbstractTaskItemData, ElementDataText, PercentageElementDataValue, total=False):
    pass


class BooleanTaskItemData(AbstractTaskItemData, ElementDataText, BooleanElementDataValue, total=False):
    pass


TaskItemData = NumberTaskItemData | PercentageTaskItemData | BooleanTaskItemData


class NumberTreeResult(ElementDataText, NumberElementDataValue, total=False):
    pass


class PercentageTreeResult(ElementDataText, PercentageElementDataValue, total=False):
    pass


class BooleanTreeResult(ElementDataText, BooleanElementDataValue, total=False):
    pass


TreeResult = NumberTreeResult | PercentageTreeResult | BooleanTreeResult


@dataclass(slots=True)
class TaskItem:
    type: CriteriaTreeElementType = field(init=False, default='task-item')
    code: str
    definition: TaskItemDefinition
    options: TaskItemOptions
    data: TaskItemData
    tags: Optional[list] = None
    documentation: Optional[list[DocumentationItem]] = None
    description: Optional[str] = None
    sortOrder: Optional[int] = None


@dataclass(slots=True)
class Task:
    type: CriteriaTreeElementType = field(init=False, default='task')
    code: str
    title: str
    longFormTitle: str
    options: TaskOptions
    data: ElementData
    category: Optional[str] = None
    tags: Optional[list] = None
    documentation: Optional[list[DocumentationItem]] = None
    description: Optional[str] = None
    items: list[TaskItem] = field(default_factory=list)
    sortOrder: Optional[int] = None


@dataclass(slots=True)
class TaskGroup:
    type: CriteriaTreeElementType = field(init=False, default='task-group')
    code: str
    title: str
    longFormTitle: str
    tags: Optional[list] = None
    documentation: Optional[list[DocumentationItem]] = None
    description: Optional[str] = None
    items: list[Task] = field(default_factory=list)
    sortOrder: Optional[int] = None


@dataclass(slots=True)
class Criterion:
    type: CriteriaTreeElementType = field(init=False, default='criterion')
    code: str
    title: str
    longFormTitle: str
    options: CriterionOptions
    data: ElementData
    tags: Optional[list] = None
    documentation: Optional[list[DocumentationItem]] = None
    items: list[TaskGroup] = field(default_factory=list)
    sortOrder: Optional[int] = None


@dataclass(slots=True)
class Theme:
    type: CriteriaTreeElementType = field(init=False, default='theme')
    code: str
    title: str
    longFormTitle: str
    options: ThemeOptions
    data: ElementData
    tags: Optional[list] = None
    documentation: Optional[list[DocumentationItem]] = None
    items: list[Criterion] = field(default_factory=list)
    style: Optional[ThemeStyle] = None
    sortOrder: Optional[int] = None


DashboardRenderingType = Literal['per-criteria', 'per-task']


@dataclass(slots=True)
class CriteriaSetOptions:
    dashboardRenderingType: DashboardRenderingType = 'per-task'


@dataclass(slots=True)
class CriteriaTree:
    version: str
    revision: str
    themes: list[Theme] = field(init=False, default_factory=list)
    options: CriteriaSetOptions
    result: TreeResult
    certifications: Optional[list[str]] = None
    certificationDefinitions: Optional[list[CertificationDefinition]] = None


CriteriaTreeElement = typing.Union[Theme, Criterion, TaskGroup, Task, TaskItem]


SchemaDefinition = dict[str, typing.Any]


@dataclass(slots=True)
class SchemaDefinitions:
    properties: Optional[SchemaDefinition] = None
    parameters: Optional[SchemaDefinition] = None


@dataclass(slots=True)
class Metadata:
    id: str
    version: str
    revision: str
    date: datetime.datetime
    name: str
    shortName: str
    group: str
    description: str
    documentation: str
    schemas: Optional[SchemaDefinitions] = None


@dataclass(slots=True)
class DataMap:
    version: str
    revision: str
    elements: dict[str, ElementData | TaskItemData]
    result: TreeResult
    certifications: Optional[list[str]] = None


MetadataResponse = Metadata
DataMapResponse = DataMap
CriteriaSetsAndVersions = dict[str, list[Metadata]]


@dataclass
class CriteriaTreeResponse(CriteriaTree):
    pass


@dataclass(slots=True)
class StreamMatrixResponse:
    filename: str
    content_type: str
    path: str
