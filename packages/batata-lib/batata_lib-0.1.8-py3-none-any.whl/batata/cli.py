import argparse
import sys
from typing import Callable, Any


class CLI:
    """
    Wrapper simplificado pro argparse

    Exemplo:
        cli = CLI("mcmanager", "Gerenciador de servidor Minecraft")
        cli.add_command("start", lambda: print("Iniciando..."))
        cli.add_command("stop", lambda: print("Parando..."))
        cli.run()
    """

    def __init__(self, name: str, description: str = '', version: str = '1.0.0'):
        """
        Inicializa CLI

        Args:
            name: Nome do programa
            description: Descrição do programa
            version: Versão do programa
        """
        self.name = name
        self.description = description
        self.version = version

        # Parser principal
        self.parser = argparse.ArgumentParser(
            prog=name,
            description=description,
            formatter_class=argparse.RawDescriptionHelpFormatter
        )

        # Adiciona versão automaticamente
        self.parser.add_argument(
            '-v', '--version',
            action='version',
            version=f'{name} {version}'
        )

        # Subparsers (pra comandos)
        self.subparsers = self.parser.add_subparsers(
            dest='command',
            help='Comandos disponíveis'
        )

        # Guarda comandos e suas funções
        self.commands: dict[str, Callable] = {}

    def add_argument(
            self,
            *args,
            required: bool = False,
            _help: str = '',
            _type: type = str,
            default: Any = None,
            choices: list = None
    ) -> None:
        """
        Adiciona argumento global

        Exemplo:
            cli.add_argument('--verbose', help='Modo verbose', type=bool)
        """
        kwargs: dict[str, Any] = {
            'required': required,
            'help': _help,
            'type': _type,
        }

        if default is not None:
            kwargs['default'] = default

        if choices:
            kwargs['choices'] = choices

        self.parser.add_argument(*args, **kwargs)

    def add_flag(self, *args, _help: str = '') -> None:
        """
        Adiciona flag (boolean)

        Exemplo:
            cli.add_flag('--verbose', '-v', help='Modo verbose')
        """
        self.parser.add_argument(
            *args,
            action='store_true',
            help=_help
        )

    def add_command(
            self,
            name: str,
            func: Callable,
            _help: str = '',
            aliases: list[str] | None = None
    ) -> argparse.ArgumentParser:
        """
        Adiciona subcomando

        Args:
            name: Nome do comando
            func: Função a ser executada
            _help: Descrição do comando
            aliases: Aliases do comando (ex: ['st'] pra 'start')

        Returns:
            Subparser do comando (pra adicionar args específicos)

        Exemplo:
            def start_server():
                print("Iniciando...")

            cli.add_command("start", start_server, help="Inicia servidor")
        """
        # Cria subparser
        kwargs: dict[str, Any] = {'help': _help}
        if aliases:
            kwargs['aliases'] = aliases

        subparser = self.subparsers.add_parser(name, **kwargs)

        # Guarda função
        self.commands[name] = func

        # Guarda aliases também
        if aliases:
            for alias in aliases:
                self.commands[alias] = func

        return subparser

    def run(self, argv: list[str] | None = None) -> None:
        """
        Executa CLI

        Args:
            argv: Argumentos (default: sys.argv[1:])
        """
        # Parseia argumentos
        args = self.parser.parse_args(argv)

        # Se não tem comando, mostra help
        if not args.command:
            self.parser.print_help()
            sys.exit(0)

        # Executa comando
        if args.command in self.commands:
            try:
                # Passa args pra função se ela aceitar
                func = self.commands[args.command]

                # Tenta passar args
                try:
                    func(args)
                except TypeError:
                    # Se função não aceita args, chama sem
                    func()

            except KeyboardInterrupt:
                print("\n\nInterrompido pelo usuário")
                sys.exit(130)
            except Exception as e:
                print(f"Erro: {e}")
                sys.exit(1)
        else:
            print(f"Comando '{args.command}' não encontrado")
            self.parser.print_help()
            sys.exit(1)
