import unittest
from datetime import datetime

from openframe_criteria_set_protocol.v1 import types as v1


class TestTypes(unittest.TestCase):
    def test_pdf_documentation_item_has_pdf_type(self):
        documentation_item = v1.PdfDocumentationItem(
            label="PDF",
            text="PDF description",
            url="https://pdf.com"
        )

        self.assertIsInstance(documentation_item, v1.DocumentationItem)
        self.assertIsInstance(documentation_item, v1.PdfDocumentationItem)
        self.assertEqual(documentation_item.type, "pdf")
        self.assertEqual(documentation_item.label, "PDF")
        self.assertEqual(documentation_item.text, "PDF description")
        self.assertEqual(documentation_item.url, "https://pdf.com")

    def test_inline_documentation_item_has_inline_type(self):
        documentation_item = v1.InlineDocumentationItem(
            label="Text",
            text="Inline description"
        )

        self.assertIsInstance(documentation_item, v1.DocumentationItem)
        self.assertIsInstance(documentation_item, v1.InlineDocumentationItem)
        self.assertEqual(documentation_item.type, "text")
        self.assertEqual(documentation_item.label, "Text")
        self.assertEqual(documentation_item.text, "Inline description")
        self.assertIsNone(documentation_item.url)

    def test_link_documentation_item_has_link_type(self):
        documentation_item = v1.LinkDocumentationItem(
            label="Link",
            text="Link description",
            url="https://link.com"
        )

        self.assertIsInstance(documentation_item, v1.DocumentationItem)
        self.assertIsInstance(documentation_item, v1.LinkDocumentationItem)
        self.assertEqual(documentation_item.type, "link")
        self.assertEqual(documentation_item.label, "Link")
        self.assertEqual(documentation_item.text, "Link description")
        self.assertEqual(documentation_item.url, "https://link.com")

    def test_point_option(self):
        point_option = v1.PointOption(
            text="Point",
            value=1.0,
            id="point_id"
        )

        self.assertEqual(point_option.text, "Point")
        self.assertEqual(point_option.value, 1.0)
        self.assertEqual(point_option.id, "point_id")

    def test_select_single_type(self):
        select_single_type = v1.SelectSingleType(
            options=[
                v1.PointOption(
                    text="Point",
                    value=1.0,
                    id="point_id"
                ),
                v1.PointOption(
                    text="Point 2",
                    value=2.0,
                    id="point_id_2"
                )
            ]
        )

        self.assertEqual(select_single_type.type, "select-single")
        self.assertEqual(len(select_single_type.options), 2)
        self.assertIsInstance(select_single_type.options[0], v1.PointOption)
        self.assertEqual(select_single_type.options[0].text, "Point")
        self.assertEqual(select_single_type.options[0].value, 1.0)
        self.assertEqual(select_single_type.options[0].id, "point_id")
        self.assertIsInstance(select_single_type.options[1], v1.PointOption)
        self.assertEqual(select_single_type.options[1].text, "Point 2")
        self.assertEqual(select_single_type.options[1].value, 2.0)
        self.assertEqual(select_single_type.options[1].id, "point_id_2")

    def test_select_multiple_type(self):
        select_multiple_type = v1.SelectMultipleType(
            options=[
                v1.PointOption(
                    text="Point",
                    value=1.0,
                    id="point_id"
                ),
                v1.PointOption(
                    text="Point 2",
                    value=2.0,
                    id="point_id_2"
                )
            ]
        )

        self.assertEqual(select_multiple_type.type, "select-multiple")
        self.assertEqual(len(select_multiple_type.options), 2)
        self.assertIsInstance(select_multiple_type.options[0], v1.PointOption)
        self.assertEqual(select_multiple_type.options[0].text, "Point")
        self.assertEqual(select_multiple_type.options[0].value, 1.0)
        self.assertEqual(select_multiple_type.options[0].id, "point_id")
        self.assertIsInstance(select_multiple_type.options[1], v1.PointOption)
        self.assertEqual(select_multiple_type.options[1].text, "Point 2")
        self.assertEqual(select_multiple_type.options[1].value, 2.0)
        self.assertEqual(select_multiple_type.options[1].id, "point_id_2")

    def test_number_type(self):
        number_type = v1.NumberType(
            minimum=1.0,
            maximum=2.0,
            step=1.0
        )

        self.assertEqual(number_type.type, "number")
        self.assertEqual(number_type.minimum, 1.0)
        self.assertEqual(number_type.maximum, 2.0)
        self.assertEqual(number_type.step, 1.0)

    def test_number_type_optional_fields(self):
        number_type = v1.NumberType()
        self.assertIsNone(number_type.minimum)
        self.assertIsNone(number_type.maximum)
        self.assertIsNone(number_type.step)

    def test_boolean_type(self):
        boolean_type = v1.BooleanType()

        self.assertEqual(boolean_type.type, "boolean")

    def test_task_item(self):
        task_item = v1.TaskItem(
            id="task_item_id",
            description="Task item description",
            definition=v1.SelectSingleType(
                options=[
                    v1.PointOption(
                        text="Point",
                        value=1.0,
                        id="point_id"
                    ),
                    v1.PointOption(
                        text="Point 2",
                        value=2.0,
                        id="point_id_2"
                    )
                ]
            ),
            label="Task item label",
            tags=["tag1", "tag2"],
            documentation=[
                v1.PdfDocumentationItem(
                    label="PDF",
                    text="PDF description",
                    url="https://pdf.com"
                )
            ]
        )

        self.assertEqual(task_item.type, "task-item")
        self.assertEqual(task_item.id, "task_item_id")
        self.assertIsInstance(task_item.definition, v1.SelectSingleType)
        self.assertEqual(task_item.definition.type, "select-single")
        self.assertEqual(len(task_item.definition.options), 2)
        self.assertIsInstance(task_item.definition.options[0], v1.PointOption)
        self.assertEqual(task_item.description, "Task item description")
        self.assertEqual(task_item.label, "Task item label")
        self.assertEqual(task_item.tags, ["tag1", "tag2"])
        self.assertEqual(len(task_item.documentation), 1)
        self.assertIsInstance(task_item.documentation[0], v1.PdfDocumentationItem)

    def test_task_item_optional_fields(self):
        task_item = v1.TaskItem(id='task_item_id', definition=v1.BooleanType())
        self.assertIsNone(task_item.label)
        self.assertIsNone(task_item.tags)
        self.assertIsNone(task_item.documentation)

    def test_task(self):
        task = v1.Task(
            id="task_id",
            title="Task title",
            label="Task label",
            documentation=[
                v1.PdfDocumentationItem(
                    label="PDF",
                    text="PDF description",
                    url="https://pdf.com"
                )
            ],
            tags=["tag1", "tag2"],
            items=[],
            description="Task description"
        )

        self.assertEqual(task.type, "task")
        self.assertEqual(task.id, "task_id")
        self.assertEqual(task.title, "Task title")
        self.assertEqual(task.label, "Task label")
        self.assertEqual(len(task.documentation), 1)
        self.assertIsInstance(task.documentation[0], v1.PdfDocumentationItem)
        self.assertEqual(task.tags, ["tag1", "tag2"])
        self.assertEqual(len(task.items), 0)
        self.assertEqual(task.description, "Task description")

    def test_task_optional_values(self):
        task = v1.Task(id='task_id', title='Task title')
        self.assertIsNone(task.label)
        self.assertIsNone(task.documentation)
        self.assertIsNone(task.tags)
        self.assertIsInstance(task.items, list)
        self.assertEqual(len(task.items), 0)
        self.assertIsNone(task.description)

    def test_criterion(self):
        criterion = v1.Criterion(
            id="criterion_id",
            title="Criterion title",
            label="Criterion label",
            documentation=[
                v1.PdfDocumentationItem(
                    label="PDF",
                    text="PDF description",
                    url="https://pdf.com"
                )
            ],
            tags=["tag1", "tag2"],
            items=[]
        )

        self.assertEqual(criterion.type, "criterion")
        self.assertEqual(criterion.id, "criterion_id")
        self.assertEqual(criterion.title, "Criterion title")
        self.assertEqual(criterion.label, "Criterion label")
        self.assertEqual(len(criterion.documentation), 1)
        self.assertIsInstance(criterion.documentation[0], v1.PdfDocumentationItem)
        self.assertEqual(criterion.tags, ["tag1", "tag2"])
        self.assertEqual(len(criterion.items), 0)

    def test_criterion_optional_values(self):
        criterion = v1.Criterion(id='criterion_id', title='Criterion title')
        self.assertIsNone(criterion.label)
        self.assertIsNone(criterion.documentation)
        self.assertIsNone(criterion.tags)
        self.assertIsInstance(criterion.items, list)
        self.assertEqual(len(criterion.items), 0)

    def test_theme(self):
        theme = v1.Theme(
            code="ECO",
            title="Økologi",
            documentation=[
                v1.PdfDocumentationItem(
                    label="PDF",
                    text="PDF description",
                    url="https://pdf.com"
                )
            ],
            tags=["tag1", "tag2"],
            items=[]
        )

        self.assertEqual(theme.type, "theme")
        self.assertEqual(theme.code, "ECO")
        self.assertEqual(theme.title, "Økologi")
        self.assertEqual(len(theme.documentation), 1)
        self.assertIsInstance(theme.documentation[0], v1.PdfDocumentationItem)
        self.assertEqual(theme.tags, ["tag1", "tag2"])
        self.assertEqual(len(theme.items), 0)

    def test_theme_optional_values(self):
        theme = v1.Theme(code='ECO', title='Økologi')
        self.assertIsNone(theme.documentation)
        self.assertIsNone(theme.tags)
        self.assertIsInstance(theme.items, list)
        self.assertEqual(len(theme.items), 0)

    def test_color(self):
        color = v1.RgbColor(red=255, green=0, blue=0)

        self.assertIsInstance(color, v1.Color)
        self.assertEqual(color.red, 255)
        self.assertEqual(color.green, 0)
        self.assertEqual(color.blue, 0)

        color = '#ff0000'
        self.assertIsInstance(color, v1.Color)
        self.assertEqual(color, '#ff0000')

    def test_metadata(self):
        metadata = v1.Metadata(
            id='criteria_set_id_1',
            name='Criteria set name',
            date=datetime.now(),
            version='1.0.0',
            description='Criteria set description',
            documentation='http://documentation.doc'
        )

        self.assertEqual(metadata.id, 'criteria_set_id_1')
        self.assertEqual(metadata.name, 'Criteria set name')
        self.assertIsInstance(metadata.date, datetime)
        self.assertEqual(metadata.version, '1.0.0')
        self.assertEqual(metadata.description, 'Criteria set description')
        self.assertEqual(metadata.documentation, 'http://documentation.doc')
