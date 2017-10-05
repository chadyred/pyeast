#!/usr/bin/python3

import abc
import time
from typing import Callable

class StartableClient(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def start(self, message) -> str:
        """when start show message"""

class StartableClientEnginify(StartableClient):

    @abc.abstractmethod
    def if_warmup_do(self, url: str, action: Callable[[StartableClient], None]) -> StartableClient:
        """check the warmup and path it througth action to handle behavior for recipient"""

class EngineMakerInterface(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def warmup_engine(self) -> 'EngineMakerInterface':
        """Allow warmup to not ript engine"""

class Messagerable(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def message(self, message) -> str:
        """Message factoring"""


class MessageFactoring(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def message(self, message) -> str:
        """Message factoring"""

class Browserify(metaclass=abc.ABCMeta):
    def naviguate(self):
        """Naviguate"""

class StarterClient(StartableClient):

    def start(self, url) -> str:
        print(url)

class Messager(Messagerable):

    def message(self, message) -> str:
        print(message)

class MessagerFactory(MessageFactoring):

    def __init__(self, messager: Messagerable):
        """"""
        self.messager = messager

    def message(self, message):
        self.messager.message(message)

class EngineMaker(EngineMakerInterface):

    def __init__(self, messagerFactory: MessageFactoring):
        self.messagerFactory = messagerFactory

    def warmup_engine(self, time: int):
        self.if_time_do(time, lambda message, timeSleep : self.messagerFactory.message(message + str(timeSleep)))

        return self

    def if_time_do(self, timeSleep: int, action: Callable[[str, int], None]):
        time.sleep(timeSleep) # Like a if
        action("Go !!", timeSleep)

        return self

class SimpleStarterclient(StartableClient):
    """Class to know version which is startable"""

    def start(self, url, version) -> str:
        print("Version is " + version)

class StarterClientEngine(StartableClientEnginify):

    def __init__(self, engineMaker: EngineMakerInterface):
        self.engineMaker = engineMaker

    def if_warmup_do(self, url: str, action: Callable[[StartableClientEnginify], None]) -> StartableClientEnginify:

        action(self)
        return self

    def start(self, url, version) -> str:
        print("Browser launch through " + url + " on " + version)

class BrowserNiviguate(Browserify):

    def __init__(self, version="Firefox"):
        self.client = client
        self.version = version

class LighterBrowser(Browserify):

    def __init__(self, url, client: StartableClient, version="Firefox"):
        self.client = client
        self.url = url
        self.version = version

    def naviguate(self):
        self.client.start(self.url, self.version)

class Naviguate():

    def browse(self, url):
        """Little call """

        StarterClientEngine(BrowserNiviguate("Internet Exlorer") ).if_warmup_do(url, lambda browser: )

        return self

    def simple_browser(self, url):

        LighterBrowser(
            url,
            SimpleStarterclient()
        ).naviguate()


        return self
