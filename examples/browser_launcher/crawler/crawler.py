#!/usr/bin/python3

import abc
from typing import Callable, IO, cast
from urllib.request import urlopen
from pyeast import *
import attr
from bs4 import BeautifulSoup
import pandas as pd


@attr.s
class BodyValue(object):

    body = attr.ib(default='')
    tree = attr.ib(default='')

@attr.s
class TemplateValue(object):

    bodyTemplatize = attr.ib(default='')

class ScrapperTemplating(metaclass=abc.ABCMeta):

    def templatize_tree_with(self, bodyValue: 'BodyValue', action: Callable[['TemplateValue'], None]) -> 'ScrapperTemplating':
        """Scrap page"""

    def dataframe_tree_with(self, bodyValue: 'BodyValue', action: Callable[['TemplateValue'], None]) -> 'ScrapperTemplating':
        """Pandas dataframe with whole value"""

class Scrapper(metaclass=abc.ABCMeta):

    def scrap_with(self, bodyValue: 'BodyValue', action: Callable[['BodyValue'], None]) -> 'Scrapper':
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

class ScrapperTemplate(ScrapperTemplating):

    def templatize_tree_with(self, bodyValue: 'BodyValue', action: Callable[['TemplateValue'], None]) -> 'ScrapperTemplating':
        """"""

        templateValue = TemplateValue()

        title = bodyValue.tree.title.get_text()
        pics = [pic.get('src') for pic in bodyValue.tree.findAll('img')]
        titresSect = [title.get_text() for title in bodyValue.tree.findAll(('h1','h2','h3','h4','h5'))]

        templateValue.bodyTemplatize = "Title : " + str(bodyValue.tree.title) + " => " + title + '\n'
        templateValue.bodyTemplatize += "Image : " + str(bodyValue.tree.findAll('img')) + '\n'
        templateValue.bodyTemplatize += "Image link " + str(pics) + '\n'
        templateValue.bodyTemplatize += "Whole title" + str(titresSect) + '\n'

        action(templateValue)

        return self

    def dataframe_tree_with(self, bodyValue: 'BodyValue', action: Callable[['TemplateValue'], None]) -> 'ScrapperTemplating':

        templateValue = TemplateValue()
        titresSect = [title.get_text() for title in bodyValue.tree.findAll(('h1','h2','h3','h4','h5'))]
        pics = [pic.get('src') for pic in bodyValue.tree.findAll('img')]

        matrix = pd.Series([titresSect, pics])
        dataframe = pd.DataFrame(matrix)
        dataframe = dataframe.rename(columns = {0:"titreSect", 1:"pics"})

        templateValue.bodyTemplatize = dataframe
        action(templateValue)

        return self

class ExampleScrapper(Scrapper):

    def scrap_with(self, bodyValue: 'BodyValue', action: Callable[['BodyValue'], None]) -> 'Scrapper':
        """Scrap page"""

        bodyValue.tree = BeautifulSoup(bodyValue.body, "lxml")

        action(bodyValue)

        return self

    def if_templatize_do(self, bodyValue: 'BodyValue', scrapperTemplate: 'ScrapperTemplating', action: Callable[['TemplateValue'], None]) -> 'Scrapper':

        scrapperTemplate.templatize_tree_with(bodyValue, lambda result : action(result))

        return self

    def if_templatize_with_dataframe_do(self, bodyValue: 'BodyValue', scrapperTemplate: 'ScrapperTemplating', action: Callable[['TemplateValue'], None]) -> 'Scrapper':

        scrapperTemplate.dataframe_tree_with(bodyValue, lambda result : action(result))

        return self


class MyRequester(Requester):

    def do_request_with(self, url: 'Url', action: Callable[['BodyValue'], None]) -> 'Requester':

        # Request to external site and whole information is here
        html = urlopen(url._url).read()
        bodyValue = BodyValue()
        bodyValue.body = html

        action(bodyValue)

        return self
