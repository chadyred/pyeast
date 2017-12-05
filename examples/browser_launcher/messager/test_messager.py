import pytest
import abc
from .messager import *

def test_implement_interface():
    assert type(Messager) == type(Messagerable)

def test_implement_interface_abc():
    assert type(Messagerable) == abc.ABCMeta

