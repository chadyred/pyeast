#!/usr/bin/python3

import abc
import time, json, sys
from typing import Callable, IO, cast
import shutil
import webbrowser

from urllib.request import urlopen

import attr

@attr.s
class UrlValue(object):

    url = attr.ib(default='')

class StartableClient(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def start_browser_with(self, browser: 'Browserify', url: 'Url') -> 'StartableClient':
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
    def print_with_on(self, message: str, messagerTemplate : 'MessagerTemplate', stream: IO[str]) -> 'Messagerable':
        """Message factoring"""


class MessageTemplating(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def format_message(self, message: 'Messagerable') -> str:
        """Message factoring"""

class UrlNormalizer(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def normalize_url(self, url: 'Url') -> 'UrlNormalizer':
        """Normalize url given"""

class Requester(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def do_request_with(self, url: 'Url') -> 'Requester':
        """Normalize url given"""

class SimpleJsonFormatter(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def format_url(self, url: 'Url', action: Callable[['Url'], None]) -> str:
        """Message factoring"""

    @abc.abstractmethod
    def format_body(self, body: 'BodyParser', action: Callable[['BodyParser'], None]) -> 'SimpleJsonFormatter':
        """Format body of page HTML to Json"""

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

class BodyParser(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def format_body_json_with(self, body: str, jsonFormatter: 'SimpleJsonFormatter', action: Callable[[str], None]) -> 'BodyParser':
        """Format body received to json"""

    def get_page_with(self, url: 'Url', requester: 'Requester', action: Callable[[str], None]) -> 'BodyParser':
        """Get page request as is"""

class Browserify(metaclass=abc.ABCMeta):

    def browse_with(self, client: 'StartableClient', url: 'Url') -> 'Browserify':
        """Naviguate"""

class Printer(metaclass=abc.ABCMeta):

    def print_url_with(self, url : 'Url', stream: IO[str]) -> 'Printer':
        """Print on stream"""

    def print_with(self, string : str, stream: IO[str]) -> 'Printer':
        """Print on stream"""

class StarterClient(StartableClient):

    def start_browser_with(self, browser: 'Browserify', url: 'Url') -> 'StartableClient':
        """Just show URL"""

        print(url)

class Messager(Messagerable):

    def print_with_on(self, message: str, messagerTemplate : 'MessageTemplating', stream: IO[str]) -> str:

        (lambda message_formatted: stream.write(message_formatted))(
            messagerTemplate.format_message(message)
        )

        return self

class MessagerTemplate(MessageTemplating):

    def format_message(self, message: str) -> str:
        """Show """

        return "Notice : " + message + '\n'

class EngineMaker(EngineMakerInterface):

    def warmup_browser(self, browser: 'Browserify', url: 'Url') -> 'EngineMakerInterface':

        self.if_time_do(browser.loadingTime, url)

        return self

    def if_time_do(self, timeSleep: int, url: 'Url'):

        Messager().print_with_on(
            "Lancement avec un temps de démarrage de : " + str(timeSleep),
            MessagerTemplate(),
            sys.stdout
        )

        time.sleep(timeSleep) # Like a if

        return self

class SimpleStarterclient(StartableClient):
    """Class to know version which is startable"""

    def start_browser_with(self, browser: 'Browserify', url: 'Url') -> 'StartableClient':

        Messager().print_with_on(
            str("Browser start through " + url._url + " on " + browser.version),
            MessagerTemplate(),
            sys.stdout
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

    def if_format_do(self, jsonFormatter: 'SimpleJsonFormatter', action: Callable[[str], None]) -> 'Url':

        action(self.format_json_with(jsonFormatter)) # We could happen url directly or attr.s

        return self

    def normalize_with(self, normalizer: 'UrlNormalizer'):

        normalizer.normalize_url(self) # Rules 2 : commands

        return self # Rules 1 : return self

    def format_json_with(self, jsonFormatter: 'SimpleJsonFormatter'):

        self.formatted_json = jsonFormatter.format_url(self) # Rules 2 : commands

        return self # Rules 1 : return self

    def print_with_on(self, printer: 'Printer', stream: IO[str]):

        printer.print_url_with(self, stream) # Rules 2 : commands

        return self # Rules 1 : return self

class UrlNormalize(UrlNormalizer):

    def normalize_url(self, url: 'Url'):

        url._normlized_url = "http://" + str(url._url)

        return self

class StarterClientEngine(StartableClientEnginify):

    def __init__(self, engine : EngineMaker):
        self.engine = engine

    def warm_up_and_do(self, browser: 'Browserify', url: 'Url', action: Callable[['StartableClient', 'Browserify', 'Url'], None ]) -> str:

        self.engine.if_warmup_do(self, browser, url, action)

        return self

    def start_browser_with(self, browser: 'Browserify', url: 'Url') -> 'StartableClient':

        Messager().print_with_on(
            str("Browser start through " + url._normlized_url + " on " + browser.version),
            MessagerTemplate(),
            sys.stdout
        )

        webbrowser.get(shutil.which(browser.version)).open(url._normlized_url)

        return self

class BrowserNaviguate(Browserify):

    def __init__(self, version="firefox", loadingTime=5):
        self.version = version
        self.loadingTime = loadingTime

    def if_warmup_do(self, engineMaker: 'EngineMakerInterface', startableEngine: 'StartableClientEnginify', url: 'Url', action: Callable[['StartableClient', 'Browserify', 'Url'], None]) -> 'Browserify':

        engineMaker.warmup_browser(self, url)
        action(startableEngine, self, url)

        return self

    def browse_with(self, clientStartable: 'StartableClient', url : 'Url'):

        clientStartable.start_browser_with(self, url)

        return self

class JsonFormatter(SimpleJsonFormatter):
    """Class which format url - todo : format result"""

    def format_url(self, url: 'Url') -> str:

        return json.dumps({'url': url._url }) # Todo : use action to pass value and change header for caller to give value through action

    def format_body(self, body: str, action: Callable[['BodyParser'], None]) -> 'SimpleJsonFormatter':

        Messager().print_with_on(
            "Type du body : " + str(type(body)),
            MessagerTemplate(),
            sys.stdout
        )

        action(json.dumps({'body': str(body) }) + '\n')

        return self

class Print(Printer):

    def print_url_with(self, url : 'Url', stream: IO[str]) -> 'Printer':

        stream.write(url.formatted_json)

        return self

    def print_with(self, string : str, stream: IO[str]) -> 'Printer':

        stream.write(string)

        return self

class OneBodyParser(BodyParser):

    def get_page_with(self, url: 'Url', requester: 'Requester', action: Callable[[str], None]) -> 'BodyParser':
        """Request page to get content"""

        requester.do_request_with(url, lambda html: action(html))

        return self

    def format_body_json_with(self, body: str, jsonFormatter: 'SimpleJsonFormatter', action: Callable[[str], None]) -> 'BodyParser':
        """Parse body content"""

        jsonFormatter.format_body(body, lambda result: action(result))

        return self


class MyRequester(Requester):

    def do_request_with(self, url: 'Url', action: Callable[[str], None]) -> 'Requester':

        # Request to external site and whole information is here
        html = urlopen(url._url).read()
        action(html)

        return self

class Naviguate():

    def format(self, naviguator: str, urlSearch: str):
        """Little call """

        BrowserNaviguate(naviguator).if_warmup_do(
            EngineMaker(),
            StarterClientEngine(
                EngineMaker()
            ),
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
        """Use it to do simple search, with normalized URL with 'http://'"""

        BrowserNaviguate(naviguator).if_warmup_do(
            EngineMaker(),
            StarterClientEngine(
                EngineMaker()
            ),
            ExampleUrl(urlSearch),
            lambda starterClient, browser, url: url.if_normalize_do(
                UrlNormalize(),
                lambda urlWellNormalize: browser.browse_with(starterClient, urlWellNormalize)
            )
        )


        return self

    def simple_browser(self, naviguator: str, urlSearch: str):
        """Use it to do simple search, no normalized URL, it's free"""

        BrowserNaviguate(
            naviguator,
            0
        ).browse_with(
            SimpleStarterclient(),
            ExampleUrl(urlSearch)
        )


        return self


    def parse_body(self, urlSearch: str):
        """Use it to parse body"""

        OneBodyParser().get_page_with(
            ExampleUrl(urlSearch),
            MyRequester(),
            lambda result : OneBodyParser().format_body_json_with(
                result,
                JsonFormatter(),
                lambda result: Print().print_with(
                    result,
                    sys.stdout
                )
            )
        )

        return self
