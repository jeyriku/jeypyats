#!/Users/jeremierouzet/Documents/Dev/pyats/pyats-jeyws01/bin/python
# -*- coding:utf-8 -*-
########################################################################################################################
#
# File: utils.py
# This file is a part of Netalps.fr
#
# Created: 2025/06/25 13:41:04
# Author: Jeremie Rouzet
#
# Last Modified: 26.01.2026 14:01:10
# Modified By: Jeremie Rouzet
#
# Copyright (c) 2025 Netalps.fr
########################################################################################################################

__author__ = ["Jeremie Rouzet"]
__contact__ = 'jeremie.rouzet@netalps.fr'
__copyright__ = 'Netalps, 2026'
__license__ = "Netalps, Copyright 2026. All rights reserved."

'''
Utility functions and classes for JeyPyats
This module provides various utility functions and custom exceptions
used across the JeyPyats framework.
'''

import importlib
import logging
from packaging import version
from lxml import etree

# create a logger for this module
log = logging.getLogger(__name__)


class JeyPyatsBaseException(Exception):
    """Base exception for all JeyPyats errors."""


class JeyPyatsValueError(JeyPyatsBaseException):
    """Exception raised for errors in the input value."""


class JeyPyatsTypeError(JeyPyatsBaseException):
    """Exception raised for errors in the input type."""


class JeyPyatsNotFoundError(JeyPyatsBaseException):
    """Exception raised when an item is not found."""


class JeyPyatsNotImplementedError(JeyPyatsBaseException):
    """Exception raised when an item is not implemented"""


class JeyPyatsNotConnectedError(JeyPyatsBaseException):
    """Exception raised when a device is not connected"""


class JeyPyatsStateError(JeyPyatsBaseException):
    """Exception raised when a the returned state is not the expected one"""


def apply_mixin(obj, mixin_class):
    """
    Applies methods from a mixin class to an object.

    Args:
        obj (object): The object to which the mixin methods will be applied.
        mixin_class (class): The class containing the mixin methods.

    Returns:
        None

    Raises:
        None

    Example:
        class MyMixin:
            def my_method(self):
                print("Hello from mixin!")

        class MyClass:
            pass

        my_instance = MyClass()
        apply_mixin(my_instance, MyMixin)

        my_instance.my_method()  # This will correctly print "Hello from mixin!"
    """
    def _remove_duplicate_methods(objects):
        # maybe this can be done smarter?
        highest_version = {}

        for obj in objects:
            name = obj[0]
            ver = obj[2]

            if name not in highest_version or ver > highest_version[name][2]:
                highest_version[name] = obj

        return set(highest_version.values())

    empty_dict = {}
    mixin_items = empty_dict.items()
    try:
        obj_version = obj.os_version
    except AttributeError:
        log.warning(f"{obj} has no os_version")
        log.warning("Loading the newest mixins")
        obj_version = version.parse("65000")

    for cls in mixin_class.__mro__:
        try:
            cls_version = cls.__os_version__
        except AttributeError:
            log.debug(f"{cls.__name__} has no os_version")
            cls_version = version.parse("0")
        if obj_version >= cls_version:
            class_methods = vars(cls).items()
            class_methods = [
                (method_name, method, cls_version)
                for method_name, method in class_methods
                # don't load the protected methods
                if not method_name.startswith("__") and not method_name.startswith("_")
            ]
            mixin_items = mixin_items | set(class_methods)
    mixin_items = _remove_duplicate_methods(mixin_items)
    for name, method, _ in mixin_items:
        if callable(method) and name not in vars(obj):
            try:
                setattr(obj, name, method.__get__(obj))
            except AttributeError as err:
                log.debug(f"Could not load method {name}")
                log.debug(err)


def guess_and_load_mixin(obj, mixin_type, mixin_name=None):
    """
    Dynamically loads and applies a mixin class to the given object based on its connection information.

    Parameters:
        obj (object): The object to which the mixin will be applied. The object must have a 'connection_info' attribute
                    with 'os' and 'device_type' attributes.
        mixin_type (str): The type of mixin to load. It should be either 'parsers' or 'configs'.
        mixin_name (str, optional): The name of the mixin class to load. If not provided, it defaults to 'ParsersMixin'
                                    for 'parsers' type and 'ConfigsMixin' for 'configs' type.

    Raises:
        JeyPyatsTypeError: If the object does not have the required 'connection_info' attribute with 'os' and 'device_type'.
        ModuleNotFoundError: If the specified module path does not exist.
        AttributeError: If the specified mixin class is not found in the module.

    Returns:
        None
    """

    if (
        not hasattr(obj, "connection_info")
        or not hasattr(obj.connection_info, "os")
        or not hasattr(obj.connection_info, "device_type")
    ):
        raise JeyPyatsTypeError(
            "Object must have 'connection_info' with 'os' and 'device_type' attributes"
        )

    mixin = {"parsers": "ParsersMixin", "configs": "ConfigsMixin"}

    module_path = f"jeypyats.{mixin_type}.libs.{obj.connection_info.os}.{obj.connection_info.device_type}"
    mixin_name = mixin[mixin_type] if mixin_name is None else mixin_name
    # It will raise an ModuleNotFoundError if module is not found
    module = importlib.import_module(module_path)
    mixin_class = getattr(module, mixin_name)
    apply_mixin(obj, mixin_class)
    # try to see we can load some waits
    module_path = f"jeypyats.{mixin_type}.libs.{obj.connection_info.os}.waits"
    mixin_name = "WaitsMixin"
    try:
        module = importlib.import_module(module_path)
        mixin_class = getattr(module, mixin_name)
        apply_mixin(obj, mixin_class)
    except ModuleNotFoundError:
        log.debug(f"Could not load waits for {obj.connection_info.os}")


def sanitize_xml(xml_string):
    """Removes all whitespaces from an XML string
    Parameters:
        xml_string (str): The XML string for which to remove whitespaces

    Retruns:
        str: the same XML string without any whitespace
    """
    parser = etree.XMLParser(remove_blank_text=True)
    try:
        root = etree.fromstring(xml_string, parser)
    except etree.XMLSyntaxError as e:
        logging.error(f"Failed to parse XML for sanitizing: {e}")
        logging.error(f"Input was:\n{xml_string}")
        raise
    sanitized_xml = etree.tostring(root, encoding="utf-8").decode()
    return sanitized_xml


def xml_insert_after(element, new_element):
    """Inserts an xml element after another one

    Args:
        element (_type_): lxml element
        new_element (_type_): lxml element
    """
    parent = element.getparent()
    parent.insert(parent.index(element) + 1, new_element)


def xml_insert_in(parent_element, new_element):
    """Inserts an xml element inside another element

    Args:
        parent_element (_type_): lxml element
        new_element (_type_): lxml element
    """
    parent_element.append(new_element)


def dict_intersection(dict1, dict2):
    """
    Compute the intersection of two dictionaries, including nested dictionaries.
    This function returns a new dictionary that contains only the key-value pairs
    that are present in both input dictionaries. If the values corresponding to a
    common key are dictionaries themselves, the function will recursively compute
    the intersection of these nested dictionaries.
    Args:
        dict1 (dict): The first dictionary.
        dict2 (dict): The second dictionary.
    Returns:
        dict: A dictionary containing the intersection of the two input dictionaries.
              Only key-value pairs that are present in both dictionaries and have
              the same value are included in the result. For nested dictionaries,
              the intersection is computed recursively.
    """

    def recursive_intersection(d1, d2):
        common_keys = d1.keys() & d2.keys()
        intersection = {}
        for key in common_keys:
            if isinstance(d1[key], dict) and isinstance(d2[key], dict):
                intersection[key] = recursive_intersection(d1[key], d2[key])
            elif d1[key] == d2[key]:
                intersection[key] = d1[key]
        return intersection

    return recursive_intersection(dict1, dict2)
