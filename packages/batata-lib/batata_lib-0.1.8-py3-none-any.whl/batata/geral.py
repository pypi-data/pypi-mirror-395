from typing import Any
from batata.errors import ParamError
from batata.colors import COLORS, MODES

__all__ = ['mostra', 'get_num', 'par', 'primo', 'divisivel', 'raiz_qdd', 'get_inp']


def mostra(*valor: Any, end: str | None = '\n', sep: str = ' ', color: str = '', mode: str = '') -> None:
    """
    Print so que traduzido

    :param sep: O separador das strings
    :param end: O que vai estar no final
    :param valor: O que vai ser imprimido
    :param color: Cor opcional
    :param mode: Tipo opcional

    :return: None

    Cores disponíveis:
    BLACK, RED, GREEN, YELLOW, BLUE, PURPLE, CYAN, GRAY, WHITE \n
    Tipos de texto:
    BOLD, NOR, ITAL, UND
    """

    if color or mode:
        color = color.upper()
        mode = mode.upper()

        if color and mode:
            if mode not in COLORS:
                raise ParamError('\033[1;31mERRO! \033[1;34mModo inválido!')

            if color not in COLORS[mode]:
                raise ParamError('\033[1;31mERRO! \033[1;34mCor inválida!')

            print(COLORS[mode][color], end='')
        elif mode and not color:
            mode = mode.upper()

            if mode not in MODES:
                raise ParamError('\033[1;31mERRO! \033[1;34mModo não disponível')

            print(COLORS[mode], end='')
        elif color and not mode:
            if color not in COLORS['NOR']:
                raise ParamError('\033[1;31mERRO! \033[1;34mCor inválida!')

            print(COLORS['NOR'][color], end='')
        else:
            raise ParamError(
                '\033[1;31mERRO! \033[1;34mParâmetros de cor e modo inválidos!',
                param='color | mode',
                esperado=f'{", ".join(key for key in COLORS)} | {", ".join(color for color in COLORS["NOR"])}'
            )

    print(sep.join(str(s) + '\033[m' for s in valor), end=end, sep=sep)


def get_num(prompt: str, erro_msg: str = 'Número invalido!', retry: bool = False,
            num_type: str = 'int') -> int | float | None:
    """
    Função para pegar um número

    :param num_type: O tipo do valor a ser retornado deve ser int | float
    :param prompt: O prompt para o usuário
    :param erro_msg: A mensagem de erro
    :param retry: Parametro para verificar se vai se repetir

    :return: Retorna o tipo número do parâmetro do num_type
    """
    while True:
        try:
            match num_type:
                case 'int':
                    return int(input(prompt))
                case 'float':
                    return float(input(prompt))
                case _:
                    raise ParamError(
                        message=f'{COLORS["BOLD"]["RED"]}ERRO! {COLORS["BOLD"]["BLUE"]}Parametro num_type deve ser: ’int’ ou ‘float’',
                        param='num_type',
                        esperado='int | float'
                    )
        except ValueError:
            print(erro_msg)
            if not retry:
                break


def get_inp(prompt: str, color: str | None = None,
            mode: str | None = None) -> str | None:
    if color or mode:
        if color and not mode:
            mostra(prompt, color=color, mode='bold', end='')
        elif mode and not color:
            mostra(prompt, color='blue', mode=mode, end='')
        elif mode and color:
            mostra(prompt, color=color, mode=mode, end='')

    return input(prompt)


def par(num: int) -> bool:
    """
    Verifica se um número e par ou não

    :param num: O número para ser verificado

    :return: Retorna True se o número for par e False se for impar
    """
    return num % 2 == 0


def primo(num: int) -> bool:
    """
    Verifica se um número e primo

    :param num: O número para ser verificado

    :return: Retorna True se o número for primo e False se o número não for primo
    """

    if num == 2:
        return True

    if num < 2 or par(num):
        return False

    for in_num in range(3, int(raiz_qdd(num)) + 1, 2):
        if divisivel(num, in_num):
            return False

    return True


def divisivel(num1: int | float, num2: int | float) -> bool:
    return num1 % num2 == 0


def raiz_qdd(num: int | float) -> float:
    """
    Essa função calcula a raiz quadrada de um número

    :param num: Número para calcular a raiz quadrada

    :return: Retorna a raiz quadrada
    """
    return num ** (1 / 2)
