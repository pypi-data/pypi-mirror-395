from typing import Any
import requests
from bs4 import BeautifulSoup


class Scraper:
    def __init__(self, url: str) -> None:
        self.url: str = url
        self.html: str = requests.get(url).text
        self.soup: BeautifulSoup = BeautifulSoup(self.html, 'html.parser')

    def scrape(self) -> str:
        return self.soup.prettify()

    def get_content(self, tag: str) -> list[str]:
        elements = self.soup.find_all(tag)

        return [str(element.prettify()) for element in elements]

    def get_title(self) -> str:
        title = self.soup.find('title')

        return title.prettify() if title else 'Titulo não encontrado'

    def get_links(self) -> list[str]:
        links: Any = self.soup.find_all('a')
        return [link.get('href') for link in links if link.get('href')]

    def get_images(self) -> list[str]:
        images: list[str] = self.get_content('img')
        return images

    def get_class(self, classe: str) -> list[str]:
        elements = self.soup.find_all(class_=classe)
        return [str(element.prettify()) for element in elements]

    def clean_tags(self, tag: str) -> str:
        element: Any = self.soup.find_all(tag)

        return element.get_text(strip=True) if element else ''

    def __repr__(self) -> str:
        return f'Scraper(url={self.url})'
