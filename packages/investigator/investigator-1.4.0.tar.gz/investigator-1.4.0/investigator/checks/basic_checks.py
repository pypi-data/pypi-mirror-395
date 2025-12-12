from typing import Any


def check_obj_is_int(obj: Any) -> bool:
    """
    Checks if object is type integer

    :param obj: Any Python object
    :return: bool
    """
    return isinstance(obj, int)


def check_obj_is_str(obj: Any) -> bool:
    """
    Checks if object is type string

    :param obj: Any Python object
    :return: bool
    """
    return isinstance(obj, str)
