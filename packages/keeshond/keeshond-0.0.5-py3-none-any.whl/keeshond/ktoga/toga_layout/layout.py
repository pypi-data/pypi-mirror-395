from keeshond import logging_logger

log = logging_logger.getlogger(__name__, logging_logger.ERROR)

import toga
import yaml
from toga.style.pack import Pack
import inspect
from keeshond.ktoga.toga_layout import utils


class Layout:

    def __init__(self, layout=None):
        self._styles = []
        self._events = []
        self.widgets = []
        self.layout = {}

    def load(self, layout_path):
        with open(layout_path, 'r') as f:
            layout_data = yaml.safe_load(f)
        self.layout = layout_data
        self.widgets = self._create_layout(self.layout)
        return self.widgets

    @property
    def styles(self):
        return self._styles

    @styles.setter
    def styles(self, styles):
        self._styles = styles

    @property
    def events(self):
        return self._events

    @events.setter
    def events(self, events):
        self._events = events

    def _create_widget(self, layout, parent=None):
        if isinstance(layout, dict):
            if len(layout) == 1:
                key, value = next(iter(layout.items()))
                log.debug(f"{value=}")
                if 'CLASS' in value:
                    widget_class = getattr(toga, value['CLASS'])
                    layout_copy = value.copy()
                    layout_copy.pop('CLASS')
                    if 'SUB-LIST-OF-CHILDREN-WIDGETS' in layout_copy:
                        children = layout_copy.pop('SUB-LIST-OF-CHILDREN-WIDGETS')
                    else:
                        children = []

                    # Create a new dictionary for widget properties
                    widget_props = {}
                    log.debug(f"{widget_props=}, {layout_copy.items()=}")
                    for prop_key, prop_value in layout_copy.items():
                        if prop_key not in ['args', 'type', 'SUB-LIST-OF-CHILDREN-WIDGETS']:
                            widget_props[prop_key] = prop_value

                    log.debug(f"{widget_props=}")
                    # Handle special cases like 'on_' events and 'style'
                    for prop_key, prop_value in widget_props.items():
                        log.debug(f"{prop_key=}, {prop_value=}")
                        if prop_key.startswith('on_'):
                            for event_lib in self._events:
                                if hasattr(event_lib, prop_value):
                                    widget_props[prop_key] = getattr(event_lib, prop_value)
                                    break
                        elif prop_key in ('style', 'validators'):
                            # Handle style processing
                            # look for a style in style libs
                            log.debug(f"75::style {prop_value=}")
                            # check if widget has one style or multiple
                            # and build an array for applying styles later
                            apply_props = []
                            if isinstance(prop_value, str):
                                # only one prop row
                                apply_props.append(widget_props[prop_key])
                            elif isinstance(prop_value, list):
                                # multiple prop rows
                                for prop in widget_props[prop_key]:
                                    apply_props.append(prop)

                            result_style = None
                            for prop_value in apply_props:
                                for style_lib in self._styles:
                                    if getattr(style_lib, prop_value, None):
                                        if result_style != None:
                                            # mix styles, apply new styles to existing ones
                                            old_styles = {k: v for k, v in result_style.items()}
                                            new_styles = {k: v for k, v in getattr(style_lib, prop_value).items()}
                                            result_style = Pack(**old_styles, **new_styles)
                                        else:
                                            result_style = getattr(style_lib, prop_value)
                                        break

                            widget_props[prop_key] = result_style

                    # Filter valid keys for the widget
                    valid_keys = utils.get_valid_keys(widget_class)
                    log.debug(f"104::{widget_class=}, {valid_keys=}")
                    filtered_props = {k: v for k, v in widget_props.items() if k in valid_keys}
                    wrong_props = {k: v for k, v in widget_props.items() if k not in valid_keys}
                    if wrong_props:
                        log.debug(f"Wrong keys in widget properties: {wrong_props=}; {valid_keys=}; {layout=}")
                        raise SystemExit(111)

                    # Create the widget
                    try:
                        widget = widget_class(id=key, **filtered_props)
                    except Exception as e:
                        log.error(f"Failed to create widget: {widget_class=}(id={key=}, **{filtered_props=}, {e=}")
                        raise SystemExit(120)

                    # Handle children
                    if isinstance(widget, toga.ScrollContainer):
                        if children:
                            widget.content = self._create_layout(children[0], widget)
                    else:
                        for child in children:
                            child_widget = self._create_layout(child, widget)
                            if child_widget:
                                widget.add(child_widget)

                    return widget
                else:
                    log.error(f"Missing 'CLASS' key in YAML node of {layout}")
                    raise SystemExit(61)
            else:
                log.error(f"Invalid YAML node of {layout}; {len(layout)=} != 1")
                raise SystemExit(64)
        elif isinstance(layout, list):
            return [self._create_widget(item, parent) for item in layout]
        else:
            log.error(f"Invalid YAML node of {layout}, {type(layout)=} != dict or list")
            raise SystemExit(70)

    def _create_layout(self, layout, parent=None):
        if isinstance(layout, dict):
            return self._create_widget(layout, parent)
        elif isinstance(layout, list):
            widgets = []
            for item in layout:
                widgets.append(self._create_layout(item, parent))
            log.debug(f"({widgets=}")
            for name, value in inspect.getmembers(widgets):
                log.debug(f"96::{widgets}:{name}={value}")
            return widgets

    def get_substance_by_id(self, _search_id):

        # if root has a var children or _children or content or with values, then put this values to elements.
        # in this example of ScrollContainer, the solution has to use _content, and not _children, because _childen is None.

        return search_in_elements(self.widgets, _search_id)


def search_in_elements(_top_widget, _search_id):
    if _top_widget.id == _search_id:
        return _top_widget
    else:
        children = getattr(_top_widget, 'children', None)
        if not children:
            object_dict = getattr(_top_widget, '__dict__', {})
            children = object_dict.get('_children', None)
            if not children:
                content = getattr(_top_widget, 'content', None)
                if not content:
                    content = object_dict.get('_content', None)

        sub_widgets = children if children else [content] if content else []

        # log.debug(f"{sub_widgets=}")
        for sub_widget in sub_widgets:
            result = search_in_elements(sub_widget, _search_id)
            if result:
                return result

        return None  # not found in this branch
