from batata.errors import ParamError
from batata.formas import FormaGeometrica

pi = 3.141592653589793

__all__ = ['produto', 'fat', 'soma', 'area', 'pi']


def produto(*valores: int) -> int:
    """
    Retorna o produto (multiplicação) de todos os valores

    :param valores: Valores para calcular as combinações

    :return: Retorna o total de combinações possíveis
    """
    tot: int = 1
    num: int
    for valor in valores:
        tot *= valor

    return tot


def fat(num: int, verbose: bool = False) -> int:
    """
    Calcula o fatorial de um número

    :param verbose: Parametro para verificar se vai mostrar o número durante o cálculo
    :param num: O número para pegar o fatorial

    :return: Retorna o número do fatorial
    """

    if num < 0:
        raise ParamError(
            'Não é possível calcular o fatorial de um número negativo.',
            param='num',
            esperado='valor positivo'
        )
    if num <= 1:
        return 1

    fatorial: int = 1
    i: int = num
    while i >= 2:
        fatorial *= i
        if verbose:
            print(fatorial)
        i -= 1

    return fatorial


def soma(*nums: int) -> int:
    """
    Retorna a soma de todos os números fornecidos

    :param nums: Números para somar

    :return: Retorna a soma dos números
    """
    return sum(nums)


def area(formato: FormaGeometrica) -> float:
    """
    Calcula a área de uma forma geométrica

    :param formato: O tipo da forma geométrica

    :return: Retorna a área da forma geométrica
    """
    return formato.area()
