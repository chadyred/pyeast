from typing import Callable, IO, cast
import abc

class MessageTemplating(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def format_message(self, message: 'Messagerable') -> str:
        """Message factoring"""

class Messagerable(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def print_with_on(self, message: str, messagerTemplate : 'MessagerTemplate', stream: IO[str]) -> 'Messagerable':
        """Message factoring"""

class Messager(Messagerable):

    def print_with_on(self, message: str, messagerTemplate : 'MessageTemplating', stream: IO[str]) -> str:

        messagerTemplate.format_message(
            message,
            lambda message_formatted: stream.write(message_formatted)
        )

        return self

class MessagerTemplate(MessageTemplating):

    def format_message(self, message: str, action: Callable[[str], None]) -> str:
        """Show notice"""

        action("Notice : " + message + '\n')

        return self
