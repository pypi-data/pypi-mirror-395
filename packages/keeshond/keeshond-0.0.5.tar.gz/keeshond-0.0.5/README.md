# Keeshond

## Name

Software should help so as dogs do. And keeshond is a useful dog race from the Netherlands. So: why not Keeshond?

## Description

Keeshond will become a toolbox of Python functions that can be executed without instantiating any class from different
apps. Here's the structure and a coding approach:

1. **Project Structure**:
   TODO: Add a diagram of the new project structure
   ```
   src
   ├── __init__.py
   └── keeshond
       ├── file_hash_check.py
       ├── __init__.py
       ├── ktoga
       │   ├── __init__.py
       │   ├── keystore
       │   │   ├── auth.py
       │   │   ├── database.py
       │   │   └── __init__.py
       │   └── toga_layout
       │       ├── __init__.py
       │       ├── layout.py
       │       └── utils.py
       ├── log_analyze_object.py
       ├── logging_logger.py
   ```
2. **file_hash_check.py**:
   This file contains the first utility functions.
3. **ktoga** package
   This package supports the use of [Toga](https://toga.readthedocs.io/en/latest/), a GUI framework for Python.
4. **keystore** package
   This package enables the store of a password.
5. **toga_layout** package
   This package structures the use of [Toga](https://toga.readthedocs.io/en/latest/) widgets, the GUI elements of Toga
6. **log_analyze_object**
   Logs the attributes of a Pythonobject.
7. **logging_logger**.
   Logging support.

## Installation

If a project wants to use [Keeshond](https://gitlab.com/pynpakken/keeshond).

Download and for development Keeshond is integrated by:

```bash
poetry add -e ../keeshond
```

When moving to main, this line has to be replaced by:

```bash
poetry add git+https://gitlab.com/pynpakken/keeshond
```

## Usage

To use the functions from Keeshond, you can import them directly from the respective modules:

```python
from keeshond.file_hash_check import check_file

# Example usage
result = check_file("path/to/your/file")
```

This modular structure allows you to easily add, modify, or remove functions without affecting the rest of the toolbox.
It also makes it easy to import and use the functions from different apps, as they are not tied to any specific class or
instance.

### Keystore

```python
from keeshond.ktoga.keystore.auth import Auth

# Initialize database and auth
auth = Auth(path_to_auth_db, pepper_bytecode)

auth.set_password(password)

if auth.verify_password(password):
# The _password is correct
else:
# The _password is incorrect
```

### Toga Layout

### Example screen

![img.png](img.png)

### Layout description in YAML

```yaml
root:
   CLASS: Box
   style: root_style
   SUB-LIST-OF-CHILDREN-WIDGETS:
      - workbench:
           CLASS: ScrollContainer
           style: root_style
           SUB-LIST-OF-CHILDREN-WIDGETS:
              - main_box:
                   CLASS: Box
                   style: main_box
                   SUB-LIST-OF-CHILDREN-WIDGETS:
                      - filler15:
                           CLASS: Box
                           style: filler1_style
                      - pw_in_box:
                           CLASS: Box
                           style: row_with_widget
                           SUB-LIST-OF-CHILDREN-WIDGETS:
                              - filler22:
                                   CLASS: Box
                                   style: filler1_style
                              - pw_input:
                                   style: input
                                   placeholder: Password (min 12 characters)
                                   CLASS: PasswordInput
                              - filler29:
                                   CLASS: Box
                                   style: filler1_style
                      - pw_confirm_box:
                           CLASS: Box
                           style: row_with_widget
                           SUB-LIST-OF-CHILDREN-WIDGETS:
                              - filler36:
                                   CLASS: Box
                                   style: filler1_style
                              - confirm_pw_input:
                                   style: input
                                   CLASS: PasswordInput
                                   placeholder: Confirm Password
                                   validators: pw_input_validator
                              - filler43:
                                   CLASS: Box
                                   style: filler1_style
                      - filler16:
                           CLASS: Box
                           style: filler1_style
                      - row_with_button:
                           CLASS: Box
                           style: row_with_widget
                           SUB-LIST-OF-CHILDREN-WIDGETS:
                              - filler33:
                                   CLASS: Box
                                   style: filler1_style
                              - submit_pw:
                                   CLASS: Button
                                   text: Submit
                                   on_press: submit_pw
                                   style: button
                              - filler41:
                                   CLASS: Box
                                   style: filler1_style
                      - filler24:
                           CLASS: Box
                           style: filler1_style
      - user_info:
           CLASS: TextInput
           style: full_width
           value: None
           readonly: True
```

| YAMAL structural element     | YAML element type | Description                                                    |
|------------------------------|-------------------|----------------------------------------------------------------|
| root                         | list              | Name of widget or container                                    |
| - workbench                  | list element      | Name of widget or container                                    |
| CLASS                        | mapping           | Class of widget or container                                   |
| style                        | mapping           | Style of widget or container; link to styles_and_validators.py |
| SUB-LIST-OF-CHILDREN-WIDGETS | dictionary        | List of next level of widgets or containers                    |
| placeholder, text, ...       | mapping           | Attributes of widget or container                              |
| validators                   | mapping           | Link to validator in styles_and_validators.py                  |
| on_press                     | mapping           | Link to function in events.py                                  |

```python 
# your_app_styles.py
from toga.style.pack import Pack, COLUMN, ROW, TOP, LEFT, BOTTOM
from toga.validators import MinLength

from .your_app_events import *

# https://toga.readthedocs.io/en/stable/reference/style/pack.html
# padding = (top, right, bottom, left)
# Styles
root_style = Pack(direction=COLUMN, flex=1, padding=0, visibility="visible", color="#C6E2B5")
row_with_widget = Pack(direction=ROW, flex=1, padding=0, visibility="visible")
main_box = Pack(direction=COLUMN, alignment=TOP, flex=1, padding=1, visibility="visible")
filler1_style = Pack(direction=ROW, alignment=TOP, flex=1, padding=7, visibility="hidden")
input = Pack(direction=ROW, flex=10, padding=7, visibility="visible", alignment=TOP)
button = Pack(direction=ROW, flex=1, padding=(0, 8, 0, 8), visibility="visible", alignment=TOP)
# Validators
pw_input_validator = [pw_validator, MinLength(12,
                                              error_message="Password must be at least 12 characters long.",
                                              allow_empty=False)]
```

```python 
# your_app_events.py
import platform

from keeshond import logging_logger

from . import globals

log = logging_logger.getlogger(__name__, logging_logger.DEBUG)

import asyncio


def submit_pw(Button):
   asyncio.create_task(Button.app.store_pw(Button))
   # because of async program flow goes on
   pass


def pw_validator(_validator):
   try:
      if _validator != globals.xoloitzcuintle_layout.get_substance_by_id('pw_input').value:
         log.debug(f"FUTURE not valid runs with every hit of tastature key {_validator=}")
         return "FUTURE 21: PW != confirm PW"
   except AttributeError as e:
      if platform.system() == "Android":
         log.debug(f"known Android attribut error {e=}")
      else:
         log.error(f"{platform.system()=} {e=}")
         raise SystemExit(45)
   except Exception as e:
      log.error(f"{platform.system()=} {e=}")
      raise SystemExit(48)

   return None  # Validation passed

```

```python 
# __main__.py
def main():
   return YourApp("YourApp", "de.model-enact-analyze-manage.your_app",
                  startup=YourApp.your_app_build)


if __name__ == "__main__":
   main().main_loop()
```

```python 
# your_app.py
from keeshond.ktoga.toga_layout.layout import layout


def your_app_build():
   globals.your_app_layout = layout.Layout()
   globals.your_app_layout.styles = [your_app_styles]
   globals.your_app_layout.events = [your_app_events]

   # Load the layout using the full path ans store the window(!)
   globals.your_app_layout.load("/path/to/layout.yaml")

   user_info = globals.your_app_layout.get_substance_by_id('user_info')
   user_info.text = f"enter your _password"

   # Initialize database and auth
   return globals.your_app_layout.widgets


async def store_pw(self, _button_widget):
   password_widget = globals.your_app_layout.get_substance_by_id('confirm_pw_input')
   if not password_widget.is_valid:
      await main_window.dialog(toga.InfoDialog("Error", "\n".join(
         list(filter(None, (validator(password_widget.value) for validator in password_widget.validators))))))
      return  # within the current _password-layout
```

### Widget Manipulation in Toga-Layout

This section explains how to manipulate widgets in a Toga application after the Toga layout has been loaded.
Prerequisites

    The layout has been loaded using layout.load('layout.yaml').

    Widgets are stored in layout._widgets.

Accessing and Modifying Widgets

To access and modify a specific widget, you can use the get_substance_by_id utility function. This function allows
you to retrieve a widget or container by its ID and then modify its properties.
Example: see above

Notes

    Always check if the widget exists and is of the expected type before modifying it to avoid errors.

    This approach allows for dynamic updates to your UI based on user interactions or application logic.

---

Dieser Artikel wurde mit maschineller Unterstützung (KI) erstellt und vor der Veröffentlichung sorgfältig geprüft.