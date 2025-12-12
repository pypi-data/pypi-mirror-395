from typing import Any
from batata.geral import mostra, get_inp

__all__ = ['info', 'warn', 'err', 'out', 'perguntar']


def info(*informacao: Any, custom_color: str | None = None, custom_mode: str | None = None) -> None:
    """
    Essa função e um atalho para dar informações ao usuário

    :param informacao: O que vai ser mostrado para o usuário
    :param custom_color: Cor personalizada para a informação (opcional)
    :param custom_mode: Modo personalizado para a informação (opcional)

    :return: None
    """
    if custom_color or custom_mode:
        if custom_color and not custom_mode:
            mostra(f'[INFO]: '.join(informacao), color=custom_color, mode='bold')
        elif custom_mode and not custom_color:
            mostra(f'[INFO]: '.join(informacao), color='yellow', mode=custom_mode)
        elif custom_mode and custom_color:
            mostra(f'[INFO]: '.join(informacao), color=custom_color, mode=custom_mode)
        return

    mostra(f'[INFO]: '.join(informacao), color='cyan', mode='bold')


def warn(waring: Any, custom_color: str | None = None, custom_mode: str | None = None) -> None:
    """
    Essa função e um atalho para dar avisos ao usuário

    :param waring: O que vai ser mostrado para o usuário
    :param custom_color: Cor personalizada para o aviso (opcional)
    :param custom_mode: Modo personalizado para o aviso (opcional)

    :return: None
    """
    if custom_color or custom_mode:
        if custom_color and not custom_mode:
            mostra(f'[WARN]: {waring}', color=custom_color, mode='bold')
        elif custom_mode and not custom_color:
            mostra(f'[WARN]: {waring}', color='cyan', mode=custom_mode)
        return

    mostra(f'[WARN]: {waring}', color='yellow', mode='bold')


def err(erro: Any, custom_color: str | None = None, custom_mode: str | None = None) -> None:
    """
    Essa função e um atalho para mostrar um erro ao usuário

    :param erro: O que vai ser mostrado para o usuário
    :param custom_color: Cor personalizada para o erro (opcional)
    :param custom_mode: Modo personalizado para o erro (opcional)

    :return: None
    """

    if custom_color or custom_mode:
        if custom_color and not custom_mode:
            mostra(f'[ERRO]: {erro}', color=custom_color, mode='bold')
        elif custom_mode and not custom_color:
            mostra(f'[ERRO]: {erro}', color='red', mode=custom_mode)
        elif custom_mode and custom_color:
            mostra(f'[ERRO]: {erro}', color=custom_color, mode=custom_mode)
        return

    mostra(f'[ERRO]: {erro}', color='red', mode='bold')


def out(valor: Any, custom_color: str | None = None, custom_mode: str | None = None) -> None:
    """
    Essa função e um atalho para mostrar resultados ao usuário

    :param valor: O que vai ser mostrado para o usuário
    :param custom_color: Cor personalizada para o resultado (opcional)
    :param custom_mode: Modo personalizado para o resultado (opcional)

    :return: None
    """

    if custom_color or custom_mode:
        if custom_color and not custom_mode:
            mostra(valor, color=custom_color, mode='bold')
        elif custom_mode and not custom_color:
            mostra(valor, color='blue', mode=custom_mode)
        elif custom_mode and custom_color:
            mostra(valor, color=custom_color, mode=custom_mode)
        return

    mostra(valor, color='blue', mode='bold')


def perguntar(pergunta: str, custom_color: str | None = None, custom_mode: str | None = None) -> None:
    """
    Essa função e um atalho para fazer perguntas ao usuário

    :param pergunta: O que vai ser perguntado ao usuário
    :param custom_color: Cor personalizada para a pergunta (opcional)
    :param custom_mode: Modo personalizado para a pergunta (opcional)

    :return: None
    """

    get_inp(pergunta, color=custom_color, mode=custom_mode)


