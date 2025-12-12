# batata/__init__.py
from batata.geral import mostra, get_num, par, primo, divisivel, raiz_qdd
from batata.aliases import info, warn, err, out, perguntar
from batata.mat import fat, soma, area, produto
from batata.formas import Retangulo, Circulo, Triangulo, FormaQualquer, FormaGeometrica
from batata.errors import ParamError, ScrapingError
from batata.scraping import Scraper
from batata.files import FileManager, JSONManager, CSVManager
from batata.colors import COLORS, MODES, Color
from batata.cli import CLI
from batata.apis import get, post, API, PokeAPI
from batata.mcoptions import start_server, save_servers, load_servers, list_servers, get_server, list_mods
from batata.PyDown import PyDown

__version__ = '0.1.7'
__all__ = [
    '__version__',
    'mostra', 'get_num', 'par', 'primo',
    'info', 'warn', 'err', 'out', 'perguntar',
    'fat', 'soma', 'area', 'divisivel', 'raiz_qdd', 'produto',
    'Retangulo', 'Circulo', 'Triangulo', 'FormaQualquer', 'FormaGeometrica',
    'ParamError', 'ScrapingError',
    'Scraper',
    'FileManager', 'JSONManager', 'CSVManager',
    'COLORS', 'MODES', 'Color',
    'CLI',
    'get', 'post', 'API', 'PokeAPI',
    'start_server', 'save_servers', 'load_servers', 'list_servers', 'get_server', 'list_mods',
    'PyDown'
]
