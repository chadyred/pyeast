#!/usr/bin/python3

import abc
import time, json, sys
from typing import Callable, IO, cast
import shutil
import webbrowser

import attr

@attr.s
class UrlValue(object):

    url = attr.ib(default='')

class StartableClient(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def start(self, browser: 'Browserify', url: 'Url') -> 'StartableClient':
        """when start show message"""

class StartableClientEnginify(StartableClient):

    @abc.abstractmethod
    def warm_up_and_do(self, browser: 'Browserify', url: 'Url', action: Callable[['StartableClient', 'Browserify', 'Url'], None ]) -> 'StartableClient':
        """check the warmup and path it througth action to handle behavior for recipient"""

class EngineMakerInterface(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def warmup_browser(self, browser: 'Browserify', url: 'Url') -> 'EngineMakerInterface':
        """Allow warmup to not ript engine"""

class Messagerable(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def message(self, message) -> str:
        """Message factoring"""


class MessageFactoring(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def message(self, message) -> str:
        """Message factoring"""

class UrlNormalizer(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def normalize_url(self, url: 'Url') -> 'UrlNormalizer':
        """Normalize url given"""

class SimpleJsonFormatter(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def format_url(self, url: 'Url', action: Callable[['Url'], None]) -> str:
        """Message factoring"""

class Url(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def if_normalize_do(self, urlNormalizer: 'UrlNormalize', action: Callable[['Url'], None]) -> 'Url':
        """Normalize url entry"""

    @abc.abstractmethod
    def if_format_do(self, jsonFormatter: 'SimpleJsonFormatter', action: Callable[['Url'], None]) -> 'Url':
        """Normalize url entry"""

    @abc.abstractmethod
    def normalize_with(self, normalizer: 'UrlNormalizer') -> 'Url':
        """Normalize"""

    @abc.abstractmethod
    def format_json_with(self, jsonFormatter: 'SimpleJsonFormatter') -> 'Url':
        """Format"""

    @abc.abstractmethod
    def print_with_on(self, printer: 'Printer', stream: IO[str]) -> 'Url':
        """Print"""

class Browserify(metaclass=abc.ABCMeta):

    def naviguate(self):
        """Naviguate"""

class Printer(metaclass=abc.ABCMeta):

    def print_with(self, url : 'Url', stream: IO[str]) -> 'Printer':
        """Print on stream"""

class StarterClient(StartableClient):

    def start(self, browser: 'Browserify', url: 'Url') -> 'StartableClient':
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

    # Move to browser (command)
    def if_warmup_do(self, startableEngine: 'StartableClientEnginify', browser: 'Browserify', url: 'Url', action: Callable[['StartableClient', 'Browserify', 'Url'], None]) -> 'EngineMakerInterface':

        browser.warmup_with(self, url)
        action(startableEngine, browser, url)

        return self

    def warmup_browser(self, browser: 'Browserify', url: 'Url') -> 'EngineMakerInterface':

        self.if_time_do(browser.loadingTime, url)

        return self

    def if_time_do(self, timeSleep: int, url: 'Url'):

        ( lambda message : self.messagerFactory.message(message) )(
            "Lancement avec un temps de démarrage de : " + str(timeSleep)
        )

        time.sleep(timeSleep) # Like a if

        return self

class SimpleStarterclient(StartableClient):
    """Class to know version which is startable"""

    def __init__(self, messageFactory: MessagerFactory):
        self.messagerFactory = messageFactory

    def start(self, browser: 'Browserify', url: 'Url') -> 'StartableClient':

        ( lambda message : self.messagerFactory.message(message) )(
            str("Browser start through " + url._url + " on " + browser.version)
        )

        webbrowser.get(shutil.which(browser.version)).open(url._url)

        return self

class ExampleUrl(Url):

    def __init__(self, url: str):
        self._url = url
        self._normlized_url = url
        self.formatted_json = ''

    def if_normalize_do(self, urlNormalizer: 'UrlNormalize', action: Callable[['Url'], None]) -> 'Url':

        action(self.normalize_with(urlNormalizer)) # We could happen url directly or attr.s

        return self

    def if_format_do(self, jsonFormatter: 'SimpleJsonFormatter', action: Callable[['Url'], None]) -> 'Url':

        action(self.format_json_with(jsonFormatter)) # We could happen url directly or attr.s

        return self

    def normalize_with(self, normalizer: 'UrlNormalizer'):

        normalizer.normalize_url(self) # Rules 2 : commands

        return self # Rules 1 : return self

    def format_json_with(self, jsonFormatter: 'SimpleJsonFormatter'):

        jsonFormatter.to_json(self) # Rules 2 : commands

        return self # Rules 1 : return self

    def print_with_on(self, printer: 'Printer', stream: IO[str]):

        printer.print_with(self, stream) # Rules 2 : commands

        return self # Rules 1 : return self

class UrlNormalize(UrlNormalizer):

    def normalize_url(self, url: 'Url'):

        url._normlized_url = "http://" + str(url._url)

        return self

class StarterClientEngine(StartableClientEnginify):

    def __init__(self, engine : EngineMaker,  messageFactory: MessagerFactory):
        self.engine = engine
        self.messagerFactory = messageFactory

    def warm_up_and_do(self, browser: 'Browserify', url: 'Url', action: Callable[['StartableClient', 'Browserify', 'Url'], None ]) -> str:

        self.engine.if_warmup_do(self, browser, url, action)

        return self

    def start(self, browser: 'Browserify', url: 'Url') -> 'StartableClient':

        ( lambda message : self.messagerFactory.message(message) )(
            str("Browser start through " + url._normlized_url + " on " + browser.version)
        )

        webbrowser.get(shutil.which(browser.version)).open(url._normlized_url)

        return self

class BrowserNiviguate(Browserify):

    def __init__(self, version="Firefox", loadingTime=5):
        self.version = version
        self.loadingTime = loadingTime

    def warmup_with(self, engineMaker: 'EngineMakerInterface', url : 'Url') -> 'Browserify':

        engineMaker.warmup_browser(self, url)

        return self

    def start_with(self, clientStartable: 'StartableClient', url : 'Url'):

        clientStartable.start(self, url)

        return self


class LighterBrowser(Browserify):

    def naviguate(self, client: 'StartableClient', browser: 'Browserify', url: 'Url') -> 'Browserify':

        client.start(browser, url)

        return self

class JsonFormatter(SimpleJsonFormatter):


    def format_url(self, url: 'Url', action: Callable[['Url'], None]) -> str:

        action(url.format_json_with(self)) # Always return self (rule 1)

        return self

    def to_json(self, url: 'Url'):

        url.formatted_json = json.dumps({'url': url._normlized_url }) + '\n'

        return self

class Print(Printer):

    def print_with(self, url : 'Url', stream: IO[str]) -> 'Printer':

        stream.write(url.formatted_json)

        return self

class Naviguate():

    def format(self, naviguator: str, urlSearch: str):
        """Little call """

        StarterClientEngine(
            EngineMaker(
                MessagerFactory(
                    Messager()
                )
            ),
            MessagerFactory(
                Messager()
            )
        ).warm_up_and_do(
                BrowserNiviguate(naviguator),
                ExampleUrl(urlSearch),
                lambda starterClient, browser, url: url.if_normalize_do(
                    UrlNormalize(),
                    lambda urlWellNormalize: urlWellNormalize.if_format_do(
                        JsonFormatter(),
                        lambda urlWellJsonFormat : urlWellJsonFormat.print_with_on(
                            Print(),
                            sys.stdout
                        )
                    )
                )
            )

        return self

    def browse(self, naviguator: str, urlSearch: str):
        """Little call """

        StarterClientEngine(
            EngineMaker(
                MessagerFactory(
                    Messager()
                )
            ),
            MessagerFactory(
                Messager()
            )
        ).warm_up_and_do(
            BrowserNiviguate(naviguator),
            ExampleUrl(urlSearch),
            lambda starterClient, browser, url: url.if_normalize_do(
                UrlNormalize(),
                lambda urlWellNormalize: browser.start_with(starterClient, urlWellNormalize)
            )
        )


        return self

    def simple_browser(self, naviguator: str, urlSearch: str):

        LighterBrowser().naviguate(
            SimpleStarterclient(
                MessagerFactory(
                    Messager()
                )
            ),
            BrowserNiviguate(naviguator),
            ExampleUrl(urlSearch)
        )


        return self
