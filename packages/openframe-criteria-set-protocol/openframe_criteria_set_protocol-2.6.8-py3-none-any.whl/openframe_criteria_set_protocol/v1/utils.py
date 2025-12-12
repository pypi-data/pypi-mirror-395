from typing import Optional

from .types import Theme, CriteriaTreeElement, Criterion, TaskGroup, Task, TaskItem, CriteriaTree


def to_color_hex_string(color):
    """
    Convert a color object to a hex string
    """
    if isinstance(color, str):
        return color
    return f"#{color.red:02x}{color.green:02x}{color.blue:02x}"


def should_hide_code(element: CriteriaTreeElement | str | dict) -> bool:
    """
    Check if a tree element should be hidden in the output
    """
    return element.options is not None and element.options.get('hideCode', False)


def get_qualified_name(element: Theme | Criterion | TaskGroup | Task | dict) -> str:
    """
    Get the qualified name of a tree element, which is the title with the code prepended if it is different
    """
    if isinstance(element, dict):
        title, code, options = (element.get('title', None), element.get('code', None), element.get('code', dict()))
        if title is None or code is None:
            raise ValueError("Element must have 'title' and 'code' keys")
    else:
        title, code, options = element.title, element.code, element.options

    if options is not None and options.get('hideCode', False):
        return title

    return f"{code} {element.title}"


def find_in_tree(tree: CriteriaTree, code: str) -> Optional[CriteriaTreeElement]:
    """
    Find an element in the criteria tree by its code
    """
    def _search_elements(elements: list[CriteriaTreeElement]):
        for element in elements:
            if element.code == code:
                return element
            if not isinstance(element, TaskItem):
                element = _search_elements(element.items)
                if element is not None:
                    return element
        return None

    return _search_elements(tree.themes)
