from urllib.request import urlopen

from bs4 import BeautifulSoup

from .models import Page, Tag
from .exceptions import (
    IncorrectUrlException, UnableToParseException, PageDoesNotExistException
)

KEYS = ['h1', 'h2', 'h3', 'a']


class PageBackend:
    def __parse_page(self, url):
        try:
            content = urlopen(url).read()
            soup = BeautifulSoup(content, 'lxml')
        except ValueError:
            raise IncorrectUrlException()
        except Exception:
            raise UnableToParseException()

        tags = {key: [] for key in KEYS}

        for child in soup.recursiveChildGenerator():
            if child.name in KEYS:
                tags[child.name].append(child.text)
        return tags

    def __save_page_tags(self, page, tags):
        if not tags:
            return

        for tag_name in tags:
            if not tags[tag_name]:
                continue
            Tag.objects.bulk_create([Tag(type=tag_name, value=value, page_id=page) for value in tags[tag_name]])

    def get_page_tags(self, url):
        tags = self.__parse_page(url)

        page = Page.objects.create()
        self.__save_page_tags(page, tags)
        return page.pk, tags

    def is_existing_page(self, page_id):
        return Page.objects.filter(pk=page_id).exists()

    def get_page_tags_by_id(self, page_id):
        if not self.is_existing_page(page_id):
            raise PageDoesNotExistException()

        tags = Tag.objects.filter(page_id=page_id)
        result = {'h1': tags.filter(type='h1').count(),
                  'h2': tags.filter(type='h2').count(),
                  'h3': tags.filter(type='h3').count(),
                  'a': [tag.value for tag in tags.filter(type='a').all()]}
        return result
