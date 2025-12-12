class ErroGenerico(Exception):
    """
    Classe base para erros genéricos
    """
    def __init__(self, message: str, code: int | None = None) -> None:
        super().__init__(message)
        self.message: str = message
        self.code: int | None = code

    def __str__(self) -> str:
        if self.code:
            return f'{self.message}: {self.code}'
        return f'{self.message}'


class ParamError(ErroGenerico):
    """
    Erro para parâmetros inválidos
    """

    def __init__(self, message: str = '\033[1;31mERRO! \033[1;34mParâmetro invalido!', code: int | None = None,
                 param: str = '', esperado: str = '') -> None:
        """
        Inicializa a exceção ParamError

        :param message: A mensagem de erro
        :param code: O código do erro
        :param param: O parâmetro inválido
        :param esperado: O valor esperado para o parâmetro
        """
        super().__init__(message)
        self.code: int | None = code
        self.message: str = message
        self.param: str = param
        self.esperado: str = esperado

        if param and esperado:
            self.message = f"{message}\n{param} -> {esperado}"
        elif param or esperado:
            if param and not esperado:
                self.message = f"{message}\n{param}"
            elif esperado and not param:
                self.message = f"{message}\nEsperado: {esperado}"

    def __str__(self) -> str:
        if self.code:
            return f'{self.code}: {self.message}'
        return f'{self.message}'


class ScrapingError(ErroGenerico):
    """
    Erro para operações de scraping
    """

    def __init__(self, message: str = 'Erro durante a operação de scraping.', code: int | None = None) -> None:
        super().__init__(message)
        self.code: int | None = code
        self.message: str = message

    def __str__(self) -> str:
        if self.code:
            return f'{self.code}: {self.message}'
        return f'{self.message}'
