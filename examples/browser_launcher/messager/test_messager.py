import pytest
import abc
import sys
from . import messager
from .messager import *
from inspect import getsource

from pytest_mock import mocker

def test_implement_interface():
    assert type(Messager) == type(Messagerable)

def test_implement_interface_abc():
    assert type(Messagerable) == abc.ABCMeta

def test_print_with_on(mocker):

    # Given
    mocker.patch.object(messager, 'MessageTemplating')
    message = "test"
    messageFormatted = "<foo>test"
    io = sys.stdout
    messager.MessageTemplating.format_message.return_value = message

    # If
    messager.Messager.print_with_on(messager.Messager, message,messager.MessageTemplating, io)

    # Get second argument which is lambda
    lambda_template = messager.MessageTemplating.format_message.call_args[0][1]
    template_content = lambda_template(messageFormatted)
    template_source = getsource(lambda_template)

    # then
    assert messager.MessageTemplating.format_message.call_count == 1
    assert messager.MessageTemplating.format_message.called_with(message, template_source)

