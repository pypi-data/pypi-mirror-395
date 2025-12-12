import traceback
import sys
from collections import deque
from pyxavi import TerminalColor

# Constants for customisation
ENTER_DICT = "{"
LEAVE_DICT = "}"
ENTER_LIST = "["
LEAVE_LIST = "]"
SEPARATOR = ","
SPACES_PER_TAB = 2

# Max depth for all recursivity
DEFAULT_MAX_DEPTH = 200

# Max depth only for non built-in objects, like user created classes,
#   which ignores DEFAULT_MAX_DEPTH.
NON_BUILTIN_OBJECTS_MAX_DEPTH = 10


def dd(what: any, export: bool = False, colorise: bool = True, max_depth: int = None):
    """Function to recursively print the value of a variable

    You know you're a php developer when the first thing you ask for
    when learning a new language is "Where's the `var_dump`?"

    :param any what: The variable to inspect
    :param bool export: Should I return the inspection or print? Defaults to False
    :param bool colorise: Should the inspection be colorised? Defaults to True
    :param int max_depth: The maximum inspection depth allowed.
        Defaults to 10 for non built-in objects and 200 for the rest.
    :returns: A (possibly) pretty long string with the variable inspection

    :Authors:
        Xavier Arnaus <xavi@arnaus.net>

    """
    max_depth = DEFAULT_MAX_DEPTH if max_depth is None else max_depth
    is_complex, result = dump(what=what, max_deep_level=max_depth, colorise=colorise)
    if export:
        return result
    else:
        print(result)


def dump(
    what: any,
    level: int = 0,
    content: str = "",
    max_deep_level: int = 200,
    colorise: bool = True
) -> None:

    # Colors
    class COLOR:
        VALUE_TYPE = TerminalColor.YELLOW if colorise else ""
        INT = TerminalColor.GREEN if colorise else ""
        STR = TerminalColor.ORANGE_BRIGHT if colorise else ""
        BOOL = TerminalColor.BLUE if colorise else ""
        DICT_KEY = TerminalColor.CYAN if colorise else ""
        LIST_KEY = TerminalColor.MAGENTA if colorise else ""
        ERROR = TerminalColor.RED_BRIGHT if colorise else ""
        END = TerminalColor.END if colorise else ""

    # Local functions to easy my life
    def needs_recursivity(element) -> bool:
        return True if isinstance(element, (list, dict, tuple, set, deque))\
            or hasattr(element, "__dict__") else False

    def has_length(element) -> bool:
        try:
            len(element)
            return True
        except TypeError:
            return False

    def justify(line: str, tabs: int = 0) -> str:
        spaces = ""
        spaces += " " * (tabs * SPACES_PER_TAB)
        return f"{spaces}{line}"

    # Preparing the info string about the type
    type_name = what.__class__.__name__
    type_length = f"[{str(len(what))}]" if has_length(what) else ""
    type_string = f"{COLOR.VALUE_TYPE}({type_name}{type_length}){COLOR.END}"

    # Complexity flags and stacks for template choosing
    i_am_complex = sub_is_complex = False
    sub_complexity = []
    sub_content = []

    # The "primitives" dump
    if not needs_recursivity(what):
        if type(what) is str:
            value = f"{COLOR.STR}\"{what}\"{COLOR.END}"
        elif type(what) in (int, float):
            value = f"{COLOR.INT}{what}{COLOR.END}"
        elif type(what) in (bool, type(None)):
            value = f"{COLOR.BOOL}{what}{COLOR.END}"
        else:
            value = f"{what}"
        content += f"{type_string}{value}"
    # Needs recursivity but it's already too much
    elif level >= max_deep_level:
        content += f"{type_string}"
        content += f"{COLOR.ERROR}Max recursion depth of {max_deep_level} reached.{COLOR.END}"
        i_am_complex = True
    # The non "primitives" are considered "complex"
    else:
        content += f"{type_string}"
        i_am_complex = True
        if isinstance(what, (list, tuple, deque)):
            enter_char = f"{COLOR.LIST_KEY}{ENTER_LIST}{COLOR.END}"
            leave_char = f"{COLOR.LIST_KEY}{LEAVE_LIST}{COLOR.END}"

            try:
                for element in what:
                    sub_is_complex, sub_content_item = dump(
                        what=element,
                        level=level + 1,
                        max_deep_level=max_deep_level,
                        colorise=colorise
                    )
                    sub_content.append(sub_content_item)
                    sub_complexity.append(sub_is_complex)
            except RuntimeError:
                sub_content.append(f"{COLOR.ERROR}Unknown{COLOR.END}")

        elif isinstance(what, set):
            enter_char = f"{COLOR.DICT_KEY}{ENTER_DICT}{COLOR.END}"
            leave_char = f"{COLOR.DICT_KEY}{LEAVE_DICT}{COLOR.END}"

            try:
                for element in what:
                    sub_is_complex, sub_content_item = dump(
                        what=element,
                        level=level + 1,
                        max_deep_level=max_deep_level,
                        colorise=colorise
                    )
                    sub_content.append(sub_content_item)
                    sub_complexity.append(sub_is_complex)
            except RuntimeError:
                sub_content.append(f"{COLOR.ERROR}Unknown{COLOR.END}")

        elif hasattr(what, "__dict__") and type_name != "method":
            enter_char = f"{COLOR.DICT_KEY}{ENTER_DICT}{COLOR.END}"
            leave_char = f"{COLOR.DICT_KEY}{LEAVE_DICT}{COLOR.END}"

            try:
                for key, element in what.__dict__.items():
                    sub_is_complex, sub_content_item = dump(
                        what=element,
                        level=level + 1,
                        max_deep_level=min(max_deep_level, NON_BUILTIN_OBJECTS_MAX_DEPTH),
                        colorise=colorise
                    )
                    sub_content_item = f"{COLOR.STR}\"{key}\"{COLOR.END}: {sub_content_item}"
                    sub_content.append(sub_content_item)
                    sub_complexity.append(sub_is_complex)
            except RuntimeError:
                sub_content.append(f"{COLOR.ERROR}Unknown{COLOR.END}")

            try:
                methods = f"{SEPARATOR} ".join(
                    [
                        a for a in dir(what)
                        if not a.endswith("__") and callable(getattr(what, a))
                    ]
                )
                sub_content.append(f"class methods: {methods}")
            except ModuleNotFoundError:
                sub_content.append(f"class methods: {COLOR.ERROR}Unknown{COLOR.END}")
            except AttributeError:
                sub_content.append(f"class methods: {COLOR.ERROR}Unknown{COLOR.END}")

        elif isinstance(what, dict):
            enter_char = f"{COLOR.DICT_KEY}{ENTER_DICT}{COLOR.END}"
            leave_char = f"{COLOR.DICT_KEY}{LEAVE_DICT}{COLOR.END}"

            try:
                for key, element in what.items():
                    sub_is_complex, sub_content_item = dump(
                        what=element,
                        level=level + 1,
                        max_deep_level=max_deep_level,
                        colorise=colorise
                    )
                    sub_content_item = f"{COLOR.STR}\"{key}\"{COLOR.END}: {sub_content_item}"
                    sub_content.append(sub_content_item)
                    sub_complexity.append(sub_is_complex)
            except RuntimeError:
                sub_content.append(f"{COLOR.ERROR}Unknown{COLOR.END}")

        else:
            enter_char = ""
            leave_char = ""

        # Let's draw
        if sub_content is not None:
            # Template inline for non complex types
            #  or complex types with non-complex sub-elements
            if not any(sub_complexity):
                content += f"{enter_char}"
                content += f"{SEPARATOR} ".join([element for element in sub_content])
                content += f"{leave_char}"
            else:
                content += f"{enter_char}" + "\n"
                content += f"{SEPARATOR}\n".join(
                    [justify(element, level + 1) for element in sub_content]
                )
                content += "\n" + justify(f"{leave_char}", level)
    return i_am_complex, content


def full_stack():
    """
    `print full_stack()` will print the full stack trace up to the top,
    including e.g. IPython's interactiveshell.py calls,
    since there is (to my knowledge) no way of knowing who would catch exceptions.
    It's probably not worth figuring out anyway...

    If `print full_stack()` is called from within an `except` block,
    `full_stack` will include the stack trace down to the raise.
    In the standard Python interpreter, this will be identical to the message
    you receive when not catching the exception (Which is why that del stack[-1] is there,
    you don't care about the except block but about the try block).

    Kindly stolen from:
    https://stackoverflow.com/questions/6086976/how-to-get-a-complete-exception-stack-trace-in-python

    """
    exc = sys.exc_info()[0]
    stack = traceback.extract_stack()[:-1]  # last one would be full_stack()
    # i.e. an exception is present
    if exc is not None:
        # remove call of full_stack, the printed exception
        # will contain the caught exception caller instead
        del stack[-1]

    trc = 'Traceback (most recent call last):\n'
    stackstr = trc + ''.join(traceback.format_list(stack))
    if exc is not None:
        stackstr += '  ' + traceback.format_exc().lstrip(trc)
    return stackstr
