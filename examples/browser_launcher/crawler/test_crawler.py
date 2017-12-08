import pytest
import abc
import sys
from .crawler import *
from inspect import getsource

from pytest_mock import mocker

def test_implement_interface():
    assert type(OneBodyParser) == type(BodyParser)
    assert type(MyRequester) == type(Requester)
