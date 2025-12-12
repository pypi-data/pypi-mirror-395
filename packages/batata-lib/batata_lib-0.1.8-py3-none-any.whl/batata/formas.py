from math import pi
from batata.errors import ParamError


class FormaQualquer:
    def area(self) -> float:
        pass

    def __repr__(self) -> str:
        pass


class Retangulo(FormaQualquer):
    def __init__(self, largura: float, altura: float) -> None:
        if largura < 0 or altura < 0:
            raise ParamError(
                "Largura e altura devem ser valores positivos.",
                param='largura | altura',
                esperado='valor positivo'
            )
        self.largura = largura
        self.altura = altura

    def area(self) -> float:
        return self.largura * self.altura

    def __repr__(self) -> str:
        return f'Retangulo(largura={self.largura}, altura={self.altura}, area={self.area()})'


class Circulo(FormaQualquer):
    def __init__(self, raio: float) -> None:
        self.raio = raio

    def area(self) -> float:
        return round(pi * self.raio ** 2, 1)

    def __repr__(self) -> str:
        return f'Circulo(raio={self.raio}, area={self.area()})'


class Triangulo(FormaQualquer):
    def __init__(self, base: float, altura: float) -> None:
        self.base = base
        self.altura = altura

    def area(self) -> float:
        return (self.base * self.altura) / 2

    def __repr__(self) -> str:
        return f'Triangulo(base={self.base}, altura={self.altura}, area={self.area()})'


class Quadrado(Retangulo):
    def __init__(self, lado: float) -> None:
        super().__init__(lado, lado)

    def area(self) -> float:
        return self.largura * self.largura

    def __repr__(self) -> str:
        return f'Quadrado(lado={self.largura}, area={self.area()})'


class Trapezio(FormaQualquer):
    def __init__(self, base_grande: float, base: float, altura: float) -> None:
        self.base_grande = base_grande
        self.base = base
        self.altura = altura

    def area(self) -> float:
        return ((self.base_grande + self.base) * self.altura) / 2

    def __repr__(self) -> str:
        return f'Trapezio(base_grande={self.base_grande}, base={self.base}, altura={self.altura}, area={self.area()})'


class Losangulo(FormaQualquer):
    def __init__(self, diagonal: float, diagonal_maior: float) -> None:
        self.diagonal = diagonal
        self.diagonal_maior = diagonal_maior

    def area(self) -> float:
        return (self.diagonal * self.diagonal_maior) / 2

    def __repr__(self) -> str:
        return f'Losangulo(diagonal={self.diagonal}, diagonal_maior={self.diagonal_maior}, area={self.area()})'


type FormaGeometrica = Retangulo | Circulo | Triangulo | Quadrado | Trapezio | Losangulo
