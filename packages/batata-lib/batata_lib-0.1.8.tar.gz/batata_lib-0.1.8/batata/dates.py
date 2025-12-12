from datetime import date


def dias_para(dia: int, mes: int) -> str:
    hoje = date.today()
    alvo = date(hoje.year, mes, dia)

    if alvo < hoje:
        alvo = date(hoje.year + 1, mes, dia)

    dias = (alvo - hoje).days

    if dias == 0:
        return f'E hoje! (ou daqui a 365 dias)'
    if dias < 10:
        return f'Faltam só {dias} dias!'

    return f'Faltam {dias} dias'
