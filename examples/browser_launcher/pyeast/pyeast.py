#!/usr/bin/python3

import abc
import time, json, sys
from typing import Callable, IO, cast
import shutil
import webbrowser
from messager import Messager, MessagerTemplate
from crawler import *

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

class UrlNormalizer(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def normalize_url(self, url: 'Url') -> 'UrlNormalizer':
        """Normalize url given"""

class SimpleJsonFormatter(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def format_url(self, url: 'Url', action: Callable[['Url'], None]) -> str:
        """Message factoring"""

    @abc.abstractmethod
    def format_body(self, body: 'BodyValue', action: Callable[['BodyParser'], None]) -> 'SimpleJsonFormatter':
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

    def if_format_do(self, jsonFormatter: 'SimpleJsonFormatter', action: Callable[['Url'], None]) -> 'Url':

        self.format_json_with(jsonFormatter, action) # We could happen url directly or attr.s

        return self

    def normalize_with(self, normalizer: 'UrlNormalizer'):

        normalizer.normalize_url(self) # Rules 2 : commands

        return self # Rules 1 : return self

    def format_json_with(self, jsonFormatter: 'SimpleJsonFormatter',  action: Callable[['Url'], None]) -> 'Url':

        jsonFormatter.format_url(self, lambda result: action(result)) # Rules 2 : commands

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

    def format_url(self, url: 'Url', action: Callable[[str], None]) -> 'SimpleJsonFormatter':

        url.formatted_json = json.dumps({'url': url._url }) + '\n'

        action(url)

        return self # Todo : use action to pass value and change header for caller to give value through action

    def format_body(self, body: 'BodyValue', action: Callable[['BodyParser'], None]) -> 'SimpleJsonFormatter':

        Messager().print_with_on(
            "Body type: " + str(type(body)),
            MessagerTemplate(),
            sys.stdout
        )

        action(json.dumps({'body': str(body.body) }) + '\n')

        return self

class Print(Printer):

    def print_url_with(self, url : 'Url', stream: IO[str]) -> 'Printer':

        stream.write(url.formatted_json)

        return self

    def print_with(self, string : str, stream: IO[str]) -> 'Printer':

        stream.write(string)

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

    def crawle_body(self, urlSearch: str):
        """Use it to parse body"""

        OneBodyParser().get_page_with(
            ExampleUrl(urlSearch),
            MyRequester(),
            lambda result : ExampleScrapper().scrap_with(
                result,
                lambda result: ExampleScrapper().if_templatize_do(
                        result,
                        ScrapperTemplate(),
                        lambda templateValue: Print().print_with(
                            templateValue.bodyTemplatize,
                            sys.stdout
                    )
                )
            )
        )

    def crawle_body_dataframe(self, urlSearch: str):
        """Use it to parse body"""

        OneBodyParser().get_page_with(
            ExampleUrl(urlSearch),
            MyRequester(),
            lambda result : ExampleScrapper().scrap_with(
                result,
                lambda result: ExampleScrapper().if_templatize_with_dataframe_do(
                        result,
                        ScrapperTemplate(),
                        lambda templateValue:
                            (lambda listImage : Print().print_with(
                                str(listImage),
                                sys.stdout)
                            )(
                                [templateValue.bodyTemplatize.iloc[1][0][i] for i in range(0, len(templateValue.bodyTemplatize.iloc[1][0]) - 1) ]
                        )
                    )
                )
            )

        return self
