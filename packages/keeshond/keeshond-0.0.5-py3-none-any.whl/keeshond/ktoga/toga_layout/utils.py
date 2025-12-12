from keeshond import logging_logger

log = logging_logger.getlogger(__name__, logging_logger.DEBUG)

import inspect

def print_all_widgets_with_attributes(_window):
    def print_widget(widget, indent=0):
        log.debug(f"{widget=}, {indent=}")
        print('  ' * indent + str(widget))
        for attr in dir(widget):
            if not attr.startswith('_'):
                print('  ' * (indent + 1) + f"{attr}: {getattr(widget, attr)}")
        if hasattr(widget, 'content'):
            print_widget(widget.content, indent + 1)
        if hasattr(widget, 'children'):
            for child in widget.children:
                print_widget(child, indent + 1)

    if _window is not None:
        print_widget(_window)
        for attr in dir(_window):
            if not attr.startswith('_'):
                log.debug(f"{attr}: {getattr(_window, attr)}")


def get_valid_keys(widget_class):
    base_keys = set()

    # Use dir() to get all attributes and methods
    base_keys.update(dir(widget_class))

    # Use vars() to get all instance variables
    base_keys.update(vars(widget_class))

    # Iterate through the class hierarchy
    for cls in inspect.getmro(widget_class):
        base_keys.update(dir(cls))
        base_keys.update(vars(cls))

        # Explicitly check for properties
        base_keys.update(name for name, value in cls.__dict__.items()
                         if isinstance(value, property))

    # Ensure common Toga attributes are included
    common_toga_attrs = {'style', 'id', 'enabled', 'visible'}
    base_keys.update(common_toga_attrs)

    # Filter out private attributes and 'impl'
    valid_keys = [key for key in base_keys if not key.startswith('_') and key != 'impl']

    return valid_keys
