###############################################################################
#
#  Welcome to Baml! To use this generated code, please run the following:
#
#  $ pip install baml-py
#
###############################################################################

# This file was generated by BAML: please do not edit it. Instead, edit the
# BAML files and re-generate this code.
#
# ruff: noqa: E501,F401
# flake8: noqa: E501,F401
# pylint: disable=unused-import,line-too-long
# fmt: off
from enum import Enum
from typing import Dict, Generic, List, Literal, Optional, TypeVar, Union

import baml_py
from pydantic import BaseModel, ConfigDict

from . import types
from .types import Check, Checked

###############################################################################
#
#  These types are used for streaming, for when an instance of a type
#  is still being built up and any of its fields is not yet fully available.
#
###############################################################################

T = TypeVar('T')
class StreamState(BaseModel, Generic[T]):
    value: T
    state: Literal["Pending", "Incomplete", "Complete"]


class Answer(BaseModel):
    question: Optional[str] = None
    answer: Optional[str] = None

class Cypher(BaseModel):
    query: Optional[str] = None

class Entity(BaseModel):
    tag: List[str]
