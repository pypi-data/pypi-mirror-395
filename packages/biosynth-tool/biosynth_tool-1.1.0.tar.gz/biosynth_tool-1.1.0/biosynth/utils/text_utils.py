
import sys
from enum import Enum
from biosynth.utils.output_utils import Logger


class OutputFormat(Enum):
    TEST = -1
    NONE = 0
    TERMINAL = 1
    GUI = 2

output_format = OutputFormat.NONE

def set_output_format(o_format):
    global output_format
    try:
        output_format = o_format
    except KeyError:
        Logger.error("Invalid output format. Supported formats: 'TEST', 'NONE', 'TERMINAL', and 'GUI'.")


def format_text_bold_for_output(text):
    if output_format in (OutputFormat.TERMINAL, OutputFormat.TEST):
        return f"\033[1m{text}\033[0m"
    elif output_format == OutputFormat.GUI:
        return f"<b>{text}</b>"
    else:
        Logger.error("Invalid output format. Supported formats: 'TERMINAL' and 'GUI'.")
        return ""

def handle_critical_error(message: str):
    """
    Handles critical errors differently depending on the output format.
    GUI -> Raise ValueError
    Terminal -> Log and exit
    """
    if output_format == OutputFormat.GUI:
        raise ValueError(message)
    elif output_format == OutputFormat.TERMINAL:
        Logger.error(message)
        Logger.space()
        sys.exit(2)
    else:
        sys.exit(2)

def get_execution_mode():
    if output_format == OutputFormat.GUI:
        return "GUI"
    elif output_format == OutputFormat.TERMINAL:
        return "Terminal"
    else:
        return "Unknown"