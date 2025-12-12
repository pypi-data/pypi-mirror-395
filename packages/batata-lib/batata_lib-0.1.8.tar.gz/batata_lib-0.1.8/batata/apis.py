import requests
from typing import Any
from difflib import get_close_matches
from requests.exceptions import ConnectionError, Timeout, HTTPError

__all__ = ['get', 'post', 'API', 'PokeAPI', 'TranslatorAPI', 'DogAPI', 'RandomUF', 'DarkJoke', 'CatAAS']

TRANSLATOR: str = 'https://tradutor-pq-sim.onrender.com'


class API:
    """
    Classe base para usar APIs
    """

    def __init__(self, url: str, headers: dict[str, str] | None = None) -> None:
        if headers is None:
            headers = {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                ),
                "Accept": "*/*",
                "Accept-Language": "en-US,en;q=0.9,pt-BR;q=0.8",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive",
            }

        self.url = url
        self.headers = headers

    def get(self, endpoint: str, **payload) -> requests.Response:
        return requests.get(
            url=f'{self.url}/{endpoint}',
            headers=self.headers,
            timeout=10,
            **payload
        )

    def post(self, endpoint: str, data: Any | None = None, json: list[dict[str, Any]] | None = None,
             **payload) -> requests.Response:
        return requests.post(
            url=f'{self.url}/{endpoint}',
            headers=self.headers,
            data=data,
            json=json,
            **payload
        )


class TranslatorAPI(API):
    def __init__(self, url: str = TRANSLATOR, endpoint: str = 'translate') -> None:
        super().__init__(url)
        self.endpoint = endpoint

    def translate(self, payload: dict[str, Any]) -> dict[str, Any] | None:
        try:
            return post(
                url=self.url,
                endpoint=self.endpoint,
                payload=payload
            )
        except (ConnectionError, Timeout, HTTPError, Exception):
            return None


class PokeAPI(API):
    """
    API simples que usa o PokéAPI
    """

    def __init__(self):
        super().__init__(url='https://pokeapi.co/api/v2')

    def get_pokemon_info(self, name: str) -> dict[str, dict[str, Any]]:  # Pega alguns dados brutos do pokemon
        pokemons_name: list[Any] = find_pokemon(name)
        pokemons_data: dict[str, dict[str, Any]] = {}

        for pokemon in pokemons_name:
            data = self.get(endpoint=f'/pokemon/{pokemon}').json()
            habilidades: list[dict[str, Any]] = data['abilities']
            pokemons_data[pokemon] = {}

            for habilidade in habilidades:
                pokemons_data[pokemon].setdefault('abilidades', [])
                pokemons_data[pokemon]['abilidades'].append(habilidade['ability'])

        return pokemons_data


class DogAPI(API):
    def __init__(self, quota: int) -> None:
        if quota > 50:
            quota = 50

        if quota < 1:
            quota = 1

        super().__init__(url=f'https://dogapi.dog')
        self.quota = quota

    def get_facts(self) -> list[dict[str, Any]]:
        facts = self.get(endpoint=f'api/v2/facts?limit={self.quota}').json()

        return facts['data']


class RandomUF(API):
    def __init__(self) -> None:
        super().__init__(url='https://uselessfacts.jsph.pl')

    def get_fact(self, include_id: bool = False, include_source: bool = False, translate: bool = True) -> dict[str, Any]:
        data: dict[str, Any] = self.get('api/v2/facts/random').json()
        if translate:
            translator: TranslatorAPI = TranslatorAPI()

            traduction: dict[str, Any] | None = translator.translate({
                "text": data['text'],
                "to": "pt"
            })
            if not traduction:
                result: dict[str, Any] = {'fact': data['text']}
            else:
                result: dict[str, Any] = {'fact': traduction['translatedText']}
        else:
            result: dict[str, Any] = {'fact': data['text']}

        if include_id:
            result['id'] = data['id']

        if include_source:
            result['source'] = data['source']

        return result


class DarkJoke(API):
    def __init__(self) -> None:
        super().__init__('https://v2.jokeapi.dev/joke')

    def get_darkjoke(self) -> str:
        data = self.get('Any?lang=pt&blacklistFlags=nsfw,political,racist,sexist,explicit').json()

        return '\n'.join([data['setup'], data['delivery']])


class CatAAS(API):
    """
    Uma classe para consumir a API Cat as a service(https://cataas.com)
    """

    def __init__(self):
        super().__init__(url='https://cataas.com')

    def get_cat_data(self) -> dict[str, Any]:
        return self.get(
            endpoint='cat?json=true'
        ).json()

    def get_img_url(self) -> str:
        return self.get_cat_data()['url']

    def get_img_type(self) -> str:
        return self.get_cat_data()['mimetype']

    def get_cat_id(self) -> str:
        return self.get_cat_data()['id']

    def img_saying(self, sentence: str) -> str:
        return f'{self.url}/cat/says/{sentence.replace(" ", "%20")}'

    def total_imgs(self) -> int:
        return self.get('api/count').json()['count']


def get(url: str, endpoint: str = '') -> dict[str, Any] | str:
    if url.endswith('/'):
        if endpoint.startswith('/'):
            endpoint = endpoint[1:]

    try:
        return requests.get(f'{url}/{endpoint}').json()
    except requests.exceptions.JSONDecodeError:
        return requests.get(f'{url}/{endpoint}').text
    except ConnectionError:
        return requests.get(f'{url}{endpoint}').json()


def post(url: str, endpoint: str = '', payload: dict[str, Any] | None = None) -> dict[str, Any]:
    return requests.post(f'{url}/{endpoint}', json=payload).json()


def find_pokemon(query: str) -> list[Any]:
    r: dict[str, Any] | str = get('https://pokeapi.co/api/v2/pokemon?limit=10000')
    names: list[str] = [p['name'] for p in r['results']]  # type: ignore
    matchs: list[Any] = get_close_matches(query, names, n=3, cutoff=0.6)

    return matchs
