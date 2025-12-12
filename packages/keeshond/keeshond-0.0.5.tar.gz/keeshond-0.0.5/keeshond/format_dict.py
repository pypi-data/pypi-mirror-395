import inspect
import json


def format_dict(_d: dict) -> str:
    """
    Formats a dictionary into a string for logging.
    """

    def get_caller_var_name(var):
        callers_locals = inspect.currentframe().f_back.f_back.f_locals
        for name, val in callers_locals.items():
            if val is var:
                return name
        return "dict"

    return f"{get_caller_var_name(_d)}={json.dumps(_d, indent=2, default=str)}"
