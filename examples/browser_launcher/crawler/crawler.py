#!/usr/bin/python3

import abc
from typing import Callable, IO, cast
from urllib.request import urlopen
from pyeast import *
import attr
from bs4 import BeautifulSoup


@attr.s
class BodyValue(object):

    body = attr.ib(default='')
    tree = attr.ib(default='')

class Scrapper(metaclass=abc.ABCMeta):

    def scrap_with(self, bodyParser: 'BodyParser', action: Callable[['BodyValue'], None]) -> 'Scrapper':
        """Scrap page"""

class Requester(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def do_request_with(self, url: 'Url', action: Callable[['BodyValue'], None]) -> 'Requester':
        """Request website with a given Url and give result (str result)"""

class BodyParser(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def format_body_json_with(self, body: 'BodyValue', jsonFormatter: 'SimpleJsonFormatter', action: Callable[[str], None]) -> 'BodyParser':
        """Append body receive on a Json array"""

    @abc.abstractmethod
    def get_page_with(self, url: 'Url', requester: 'Requester', action: Callable[[str], None]) -> 'BodyParser':
        """Get page request as is"""

class OneBodyParser(BodyParser):

    def get_page_with(self, url: 'Url', requester: 'Requester', action: Callable[[str], None]) -> 'BodyParser':
        """Request page to get content"""

        requester.do_request_with(url, lambda html: action(html))

        return self

    def format_body_json_with(self, body: 'BodyValue', jsonFormatter: 'SimpleJsonFormatter', action: Callable[[str], None]) -> 'BodyParser':
        """Append body receive on a Json array"""

        jsonFormatter.format_body(body, lambda result: action(result))

        return self

class ExampleScrapper(Scrapper):

    def scrap_with(self, bodyValue: 'BodyValue', bodyParser: 'BodyParser', action: Callable[['BodyValue'], None]) -> 'Scrapper':
        """Scrap page"""

        bodyValue.tree = BeautifulSoup(bodyValue.body, "lxml")
        action(bodyValue)

        return self


class MyRequester(Requester):

    def do_request_with(self, url: 'Url', action: Callable[['BodyValue'], None]) -> 'Requester':

        # Request to external site and whole information is here
        html = urlopen(url._url).read()
        bodyValue = BodyValue()
        bodyValue.body = html

        action(bodyValue)

        return self
