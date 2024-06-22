from dataclasses import dataclass
from functools import wraps
from inspect import isclass
from typing import TypeVar, Generic, List, Dict, Any, get_type_hints, Callable

from flask import Flask, request
from werkzeug.datastructures.file_storage import FileStorage

T = TypeVar('T')


@dataclass
class _Type(Generic[T]):
    value: T


@dataclass
class Object:
    pass


@dataclass
class Array(_Type[List[Any]]):
    pass


@dataclass
class String(_Type[str]):
    pass


@dataclass
class Integer(_Type[int]):
    pass


@dataclass
class Float(_Type[float]):
    pass


@dataclass
class Boolean(_Type[bool]):
    pass


@dataclass
class Dict(_Type[Dict[Any, Any]]):
    pass


@dataclass
class FormText(_Type[str]):
    pass


@dataclass
class FormFile(_Type[FileStorage]):
    pass


class TJFUBody:
    def __init__(
            self,
            app: Flask
    ):
        self._app = app

        self._on_from_json_missing_attribute = None
        self._on_from_json_invalid_attribute_type = None
        self._on_from_form_data_invalid_attribute_type = None

    def on_from_json_missing_attribute(
            self,
            callback: Callable[[str, Any, Any, int], Any]  # attr, type, class, status code
    ):
        self._on_from_json_missing_attribute = callback

    def on_from_json_invalid_attribute_type(
            self,
            callback: Callable[[str, Any, Any, int], Any]  # attr, type, invalid type, status code
    ):
        self._on_from_json_invalid_attribute_type = callback

    def on_from_form_data_invalid_attribute_type(
            self,
            callback: Callable[[str, Any, Any, int], Any]  # attr, type, status code
    ):
        self._on_from_form_data_invalid_attribute_type = callback

    def _json_to_class(
            self,
            json_body,
            cls
    ):
        json = {}
        type_hints = get_type_hints(cls)
        for attribute, typ in type_hints.items():
            if not isclass(typ):
                continue

            if attribute not in json_body:
                return {
                    "msg": f'Missing attribute `{attribute}`:{typ} in {cls}',
                    "status_code": 400
                } if self._on_from_json_missing_attribute is None else self._on_from_json_missing_attribute(
                    attribute, typ, cls, 400
                )

            if issubclass(typ, Object):
                if not isinstance(json_body[attribute], dict):
                    return {
                        "msg": f'Attribute `{attribute}` in body requires {typ} found {type(json_body[attribute])}',
                        "status_code": 400
                    } if self._on_from_json_invalid_attribute_type is None else self._on_from_json_invalid_attribute_type(
                        attribute, typ, type(json_body[attribute]), 400
                    )

                sub_cls = self._json_to_class(
                    json_body[attribute],
                    typ
                )
                if not isinstance(sub_cls, typ):
                    return sub_cls
                json[attribute] = sub_cls
                continue

            type_mapping = {
                String: str,
                Integer: int,
                Float: float,
                Boolean: bool,
                Array: list,
                Dict: dict
            }

            type_of_value = type_mapping.get(typ)
            if type_of_value is None:
                raise ValueError(f'Invalid type: {typ} requires: {list(type_mapping.keys())}')

            if not isinstance(json_body[attribute], type_of_value):
                return {
                    "msg": f'Attribute `{attribute}` in body requires {typ} found {type(json_body[attribute])}',
                    "status_code": 400
                } if self._on_from_json_invalid_attribute_type is None else self._on_from_json_invalid_attribute_type(
                    attribute, typ, type(json_body[attribute]), 400
                )

            json[attribute] = typ(json_body[attribute])

        return cls(**json)

    def from_json(
            self,
            t: T
    ):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                json_body: dict = request.json

                cls = self._json_to_class(json_body, t)

                if not isinstance(cls, t):
                    return cls

                return func(*args, cls, **kwargs)

            return wrapper

        return decorator

    def from_form_data(
            self,
            t: T
    ):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                params = []
                type_hints = get_type_hints(t)
                for attribute, typ in type_hints.items():
                    if not typ == FormFile and not typ == FormText:
                        raise TypeError(f'Invalid type: {typ} requires: {[FormFile, FormText]}')
                    if attribute in request.files and typ == FormFile:
                        params.append(FormFile(request.files[attribute]))
                    elif attribute in request.form and typ == FormText:
                        params.append(FormText(request.form[attribute]))
                    else:
                        return {
                            "msg": f'Attribute `{attribute} requires {typ}`',
                            "status_code": 400
                        } if self._on_from_form_data_invalid_attribute_type is None else self._on_from_form_data_invalid_attribute_type(
                            attribute, typ, type(request.form[attribute]), 400
                        )

                cls_body = t(*params)
                return func(*args, cls_body, **kwargs)

            return wrapper

        return decorator
