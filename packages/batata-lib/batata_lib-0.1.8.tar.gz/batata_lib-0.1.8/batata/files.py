import json
import csv
from pathlib import Path
from typing import Any
from batata.errors import ParamError
from batata.aliases import err


class FileManager:
    def __init__(self, name: str, path: str = './', indent: int = 2) -> None:
        self.path: Path = Path(path)
        self.name: str = name
        self.indent: int = indent

        self.arquivo: str = str(self.path / self.name)

        self.mode: str
        if self.arquivo.endswith('.csv'):
            self.mode = 'csv'
        elif self.arquivo.endswith('.json'):
            self.mode = 'json'
        elif self.arquivo.endswith('.txt'):
            self.mode = 'txt'
        else:
            self.mode = 'file'

    def creat(self) -> None:
        """
        Essa função apenas cria o arquivo

        :return: None
        """
        try:
            with open(self.arquivo, 'w', encoding='utf-8') as file:
                if self.mode == 'json':
                    file.write(json.dumps([], indent=self.indent))
                elif self.mode == 'csv':
                    writer = csv.writer(file)
                    writer.writerow([])
                return
        except Exception as e:
            err(f'Erro ao criar o arquivo: {e}')

    def read(self) -> str | list[list[str] | dict[str, Any]]:
        """
        Essa função retorna o conteúdo de um arquivo

        :return: O conteúdo do arquivo
        """
        try:
            with open(self.arquivo, 'r', encoding='utf-8') as file:
                if self.mode == 'json':
                    return json.loads(file.read())
                elif self.mode == 'csv':
                    reader = csv.reader(file)
                    return [row for row in reader]
                conteudo: str = file.read()
        except FileNotFoundError:
            err('Arquivo não encontrado!')
            conteudo: str = ''
        except Exception as e:
            err(f'Erro ao criar o arquivo: {e}')
            conteudo: str = ''

        return conteudo

    def write(self, content: str | dict[str, Any] | list[str | Any]) -> None:
        """
        Essa função escreve alguma coisa em um arquivo

        :param content: Contendo a ser adicionado

        :return: None
        """
        try:
            with open(self.arquivo, 'a', encoding='utf-8') as file:
                if self.mode == 'json':
                    if type(content) != dict[str, Any]:
                        raise ParamError(
                            message='\033[1;31mPara o JSON o conteúdo deve ser um dict[str, Any]\033[m',
                            param='content',
                            esperado='dict[str, Any]'
                        )

                    data: list[dict[str, Any]] = self.read()  # type: ignore
                    data.append(content)  # type: ignore
                    json.dump(data, file, indent=self.indent)
                    return
                elif self.mode == 'csv':
                    if type(content) != list[str | Any]:
                        raise ParamError(
                            message='\033[1;31mPara o CSV o conteúdo deve ser um list[str | Any]\033[m',
                            param='content',
                            esperado='list[str | Any]'
                        )
                    writer = csv.writer(file)
                    writer.writerow(content)
                    return
                file.write(str(content))
        except FileNotFoundError:
            self.creat()
            with open(self.arquivo, 'a', encoding='utf-8') as file:
                file.write(str(content))

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(path={self.path}/, name={self.name}, arquivo={self.arquivo}, mode={self.mode})'


class JSONManager(FileManager):
    def __init__(self, name: str, path: str = './', indent: int = 2) -> None:
        super().__init__(path=path, name=name, indent=indent)

    def creat(self) -> None:
        """
        Essa função cria um JSON

        :return: None
        """
        with open(self.arquivo, 'w', encoding='utf-8') as file:
            file.write(json.dumps([], indent=self.indent))

    def read(self) -> list[dict[str, Any]]:
        """
        Essa função le um JSON

        :return: Conteúdo do JSON como uma lista
        """
        try:
            with open(self.arquivo, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            err('Arquivo JSON não encontrado! Criando um novo...')
            self.creat()
            with open(self.arquivo, 'r', encoding='utf-8') as file:
                return json.load(file)
        except Exception as e:
            err(f'Erro ao ler o arquivo JSON: {e}')
            return []

    def write(self, content: dict[str, Any]) -> None:
        """
        Essa função escreve coisas no JSON

        :param content: Contendo a ser escrevido

        :return: None
        """
        data: list[dict[str, Any]] = self.read()

        data.append(content)

        try:
            with open(self.arquivo, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=self.indent)
        except FileNotFoundError as not_file:
            err(f'Arquivo não encontrado: {not_file}! Criando um novo...')
            self.creat()
            with open(self.arquivo, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=self.indent)
        except Exception as e:
            err(f'Erro ao escrever no arquivo JSON: {e}')

    def update(self, filter_key: str, filter_val: Any, update_key: str, new_val: Any):
        """
        Atualiza um item do JSON baseado num filtro.
        Exemplo:
        update('server', 'Survivors', 'status', 'stopped')
        """
        content = self.read()

        for obj in content:
            if obj.get(filter_key) == filter_val:
                obj[update_key] = new_val

        with open(self.arquivo, 'w', encoding='utf-8') as file:
            json.dump(content, file, indent=self.indent)


class CSVManager(FileManager):
    def __init__(self, name: str, path: str = './'):
        super().__init__(name=name, path=path)

    def creat(self, header: list[str] | None = None) -> None:
        """
        Essa função cria um arquivo CSV

        :return: None
        """
        try:
            with open(self.arquivo, 'w', encoding='utf-8') as file:
                writer = csv.writer(file)
                if header:
                    writer.writerow(header)
                return
        except Exception as e:
            err(f'Erro ao criar o arquivo CSV: {e}')

    def read(self) -> list[list[str | Any]]:
        """
        Essa função retorna o conteúdo do CSV

        :return: O conteúdo do CSV
        """
        try:
            with open(self.arquivo, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                return [row for row in reader]
        except FileNotFoundError:
            err('Arquivo CSV não encontrado!')
            return []
        except Exception as e:
            err(f'Erro ao ler o arquivo CSV: {e}')
            return []

    def write(self, content: list[str]) -> None:
        try:
            with open(self.arquivo, 'a', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(content)
        except FileNotFoundError:
            err('Arquivo CSV não encontrado! Criando um novo...')
            self.creat()
            with open(self.arquivo, 'a', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(content)
        except Exception as e:
            err(f'Erro ao escrever no arquivo CSV: {e}')


class NKVManager(FileManager):
    SEPS: list[str] = [
        '|', '/', '\\', ' ', '-'
    ]

    def __init__(self, name: str, path: str = './', sep_type: str = '|'):
        super().__init__(name=name, path=path)
        if sep_type not in self.SEPS:
            raise ParamError(
                message='\033[1;31mERRO! \033[1;34mParametro "sep_type" invalido!',
                param='sep_type',
                esperado=' | '.join(self.SEPS)
            )
        self.sep_type = sep_type
        if path.endswith('/'):
            self.arquivo = f'{path}{name}'
        else:
            self.arquivo = f'{path}/{name}'

    def write(self, key: str, value: Any) -> None:
        try:
            with open(self.arquivo, 'a', encoding='utf-8') as file:
                if type(value) == str:
                    file.write(f'{key}{self.sep_type}"{value}"\n')
                    return
                file.write(f'{key}{self.sep_type}{value}\n')
        except FileNotFoundError:
            self.creat()
            with open(self.arquivo, 'a', encoding='utf-8') as file:
                file.write(f'{key}{self.sep_type}{value}\n')

    def read(self) -> list[dict[str, Any]]:
        try:
            with open(self.arquivo, 'r', encoding='utf-8') as file:
                brute = file.read()
        except FileNotFoundError:
            err('Arquivo não encontrado! Criando novo arquivo...')
            self.creat()
            brute = ''

        content: list[dict[str, Any]] = []
        brute = brute.split('\n')

        for linha in brute:
            data = linha.split(self.sep_type)
            if data.__len__() == 2:
                key, val = data
                if '.' in val:
                    try:
                        val = float(val)
                    except ValueError:
                        pass
                else:
                    try:
                        val = int(val)
                    except ValueError:
                        pass

                content.append({key: val})

        return content

    def get_sep(self) -> str:
        separator: str

        with open(self.arquivo, 'r', encoding='utf-8') as file:
            content = file.read()

        for sep in self.SEPS:
            for char in content:
                if char == sep:
                    return sep

        raise ValueError
