# -*- coding: utf-8 -*-
"""Docs are here"""
import os
import pathlib
import typing
import types
from collections import defaultdict
import json

__version__ = "0.1.0"
__author__ = "Md Nazrul Islam <email2nazrul@gmail.com>"


class Configuration:
    """Simple Configuration Class"""

    _initialized: bool
    __storage__: typing.DefaultDict[str, typing.Any]
    __slots__ = ("__storage__", "_initialized")

    def __init__(self, data_dict: typing.Dict[str, typing.Any]):
        """ """
        object.__setattr__(self, "__storage__", defaultdict())
        object.__setattr__(self, "_initialized", False)
        self.init(data_dict)
        object.__setattr__(self, "_initialized", True)
        self.normalize_paths()

    @classmethod
    def from_module(cls, mod: types.ModuleType):
        """ """
        data_dict = mod.__dict__.copy()
        return cls(data_dict)

    @classmethod
    def from_json_file(cls, file: pathlib.Path):
        """ """
        assert file.is_file() and file.exists()

        with open(str(file), "r", encoding="utf-8") as fp:
            data_dict = json.load(fp)
            assert isinstance(data_dict, dict)

        return cls(data_dict)

    @classmethod
    def from_text_file(cls, file: pathlib.Path):
        """KEY=VALUE formatted variables
        @todo: dict type value by dotted path?
        """
        assert file.is_file() and file.exists()
        data_dict = dict()
        with open(str(file), "r", encoding="utf-8") as fp:
            for line in fp:
                ln = line.strip()
                if not ln or ln.startswith("#") or "=" not in ln:
                    continue
                key, val = ln.split("=", 1)
                key = key.strip()
                if not key.isupper():
                    continue
                val = list(map(lambda x: x.strip(), val.split(",")))
                if len(val) == 1:
                    data_dict[key] = val[0]
                else:
                    data_dict[key] = val
        return cls(data_dict)

    def init(self, data_dict: typing.Dict[str, typing.Any]):
        """ """
        init_ = object.__getattribute__(self, "_initialized")
        if init_ is True:
            raise ValueError("Instance has already be initialized!")

        def _add(items):
            """ """
            for key, val in items:
                if key.isupper() is False:
                    continue
                setattr(self, key, val)

        _add(data_dict.items())

    def normalize_paths(self):
        """ """
        init_ = object.__getattribute__(self, "_initialized")
        if init_ is False:
            raise ValueError("Instance has must be initialized!")

        storage = object.__getattribute__(self, "__storage__")
        base_path = storage["BASE_PATH"]
        if not isinstance(base_path, pathlib.PurePath):
            base_path = resolve_path(base_path, None)
            storage["BASE_PATH"] = base_path

        needed_paths = (
            "CACHE_PATH",
            "RESOURCE_TARGET_DIRECTORY",
            "FACTORY_TARGET_NAME",
            "DEPENDENCIES_TARGET_FILE_NAME",
            "UNITTEST_TARGET_DIRECTORY",
            "UNITTEST_COPY_FILES",

        )
        for np in needed_paths:
            val = storage[np]
            if isinstance(val, list):
                new_val = list()
                for p in val:
                    if isinstance(p, pathlib.PurePath):
                        new_val.append(p)
                    else:
                        new_val.append(resolve_path(p, base_path))
                storage[np] = new_val
            else:
                if not isinstance(val, pathlib.PurePath):
                    storage[np] = resolve_path(val, base_path)

        # take care of manual profiles
        new_profiles = list()
        for path, mod_name, values in storage["MANUAL_PROFILES"]:
            if not isinstance(path, pathlib.PurePath):
                path = resolve_path(path, base_path)
            new_profiles.append((path, mod_name, values))

        storage["MANUAL_PROFILES"] = new_profiles

    def __getitem__(self, item):
        """ """
        try:
            return self.__storage__[item]
        except KeyError:
            raise KeyError(f"´item´ is not defined in any configuration.")

    def __getattr__(self, item):
        """ """
        try:
            return self.__storage__[item]
        except KeyError:
            raise AttributeError(f"´item´ is not defined in any configuration.")

    def __setitem__(self, key, value):
        """ """
        storage = object.__getattribute__(self, "__storage__")
        storage[key] = value

    def __setattr__(self, key, value):
        """ """
        self[key] = value


def resolve_path(string_path: str, parent: pathlib.PurePath = None):
    """ """
    if os.path.isabs(string_path):
        return pathlib.Path(string_path)
    elif string_path.startswith("~"):
        return pathlib.Path(os.path.expanduser(string_path))

    if parent is None:
        parent = pathlib.Path(os.getcwd())
    if string_path == ".":
        return parent

    me = parent
    for part in string_path.split(os.sep):
        if not part:
            continue
        if part == ".":
            continue
        elif part == "..":
            me = me.parent
        else:
            me = me / part
    return me
