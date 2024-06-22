# Flask-Tjfu-Body 1.0.0

Effortlessly Handle Request Bodies with Class Definitions in Flask

### Primary Dependencies

1. [Flask](https://pypi.org/project/Flask/)

### Installation

```
pip install flask-tjfu-body
```

### Getting Started

```python
from dataclasses import dataclass

from flask import Flask

from flask_tjfu_body import TJFUBody, String, FormText, FormFile

app = Flask(__name__)
tjfu_body = TJFUBody(app)


@dataclass
class UserLogin:
    username: String
    password: String


@dataclass
class UploadVideo:
    description: FormText
    video: FormFile


@app.route('/login', methods=['POST'])
@tjfu_body.from_json(UserLogin)
def login(cls: UserLogin):
    print(cls.username)
    print(cls.password)
    return "Success"


@app.route('/upload', methods=['POST'])
@tjfu_body.from_form_data(UploadVideo)
def upload_video(cls: UploadVideo):
    desc = cls.description.value
    video = cls.video.value
    video.save(video.filename)
    return "Success"
```

### JSON Data Types

Flask-Tjfu-Body provides 7 JSON data types: `Object`, `Array`, `String`, `Integer`, `Float`, `Boolean`, and `Dict`, corresponding to `class`, `list`, `str`, `int`, `float`, `bool`, and `dict`.

```python
from dataclasses import dataclass
from flask_tjfu_body import Object, String, Integer, Array, Boolean, Float, Dict

@dataclass
class User(Object):
    name: String
    age: Integer

@dataclass
class MyJsonBody:
    user: User
    favorite_foods: Array
    male: Boolean
    bmi: Float
    other: Dict
```

Corresponding JSON:

```json
{
  "user": {
    "name": "John Doe",
    "age": 18
  },
  "favorite_foods": [
    "Apple",
    "Pine Apple"
  ],
  "male": true,
  "bmi": 18.5,
  "other": {}
}
```

### Form Data Types

Flask-Tjfu-Body provides 2 Form Data types: `FormText` and `FormFile`, corresponding to `str` and `werkzeug.datastructures.file_storage.FileStorage`.

```python
from dataclasses import dataclass
from flask_tjfu_body import FormText, FormFile

@dataclass
class UploadVideo:
    description: FormText
    video: FormFile
```

### Requesting Body from Client

Use `from_json` for JSON and `from_form_data` for Form Data, passing the defined class as an argument.

```python
from dataclasses import dataclass

from flask import Flask

from flask_tjfu_body import TJFUBody, String, FormText, FormFile

app = Flask(__name__)
tjfu_body = TJFUBody(app)


@dataclass
class UserLogin:
    username: String
    password: String


@dataclass
class UploadVideo:
    description: FormText
    video: FormFile


@app.route('/login', methods=['POST'])
@tjfu_body.from_json(UserLogin)
def login(cls: UserLogin):
    ...


@app.route('/upload', methods=['POST'])
@tjfu_body.from_form_data(UploadVideo)
def upload_video(cls: UploadVideo):
    ...
```

### Handling Variable Part

Body arguments are placed after Variable Part arguments.

```python
from dataclasses import dataclass
from flask import Flask
from flask_tjfu_body import TJFUBody, String

app = Flask(__name__)
tjfu_body = TJFUBody(app)

@dataclass
class A:
    a: String

@app.route('/user/<user_id>', methods=['POST'])
@tjfu_body.from_json(A)
def user(user_id, a: A):
    ...
```

### Customization

Customize responses for invalid requests with `on_from_json_missing_attribute`, `on_from_json_invalid_attribute_type`, and `on_from_form_data_invalid_attribute_type`.

```python

from flask import Flask

from flask_tjfu_body import TJFUBody

app = Flask(__name__)
tjfu_body = TJFUBody(app)


def on_from_json_missing_attribute(attr, attr_type, on_class, status_code):
    return f"Error: The attribute '{attr}' of type '{attr_type}' is missing in the class '{on_class}'. Status code: {status_code}."


def on_from_json_invalid_attribute_type(attr, attr_type, invalid_type, status_code):
    return f"Error: The attribute '{attr}' is expected to be of type '{attr_type}', but found type '{invalid_type}'. Status code: {status_code}."


def on_from_form_data_invalid_attribute_type(attr, attr_type, invalid_type, status_code):
    return f"Error: The attribute '{attr}' is expected to be of type '{attr_type}', but found type '{invalid_type}'. Status code: {status_code}."


tjfu_body.on_from_json_missing_attribute(on_from_json_missing_attribute)
tjfu_body.on_from_json_invalid_attribute_type(on_from_json_invalid_attribute_type)
tjfu_body.on_from_form_data_invalid_attribute_type(on_from_form_data_invalid_attribute_type)
```

## Changelog

### Version 1.0.0 - Initial Release - June 23, 2024

- Initial release with core functionalities:
    - Define classes and process data from Body into explicitly defined classes.
    - Provide customization functions.

Each section in this changelog provides a summary of what was added, changed, fixed, or removed in each release, helping users and developers understand the evolution of the project and highlighting important updates or improvements.