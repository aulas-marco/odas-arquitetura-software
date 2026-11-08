"""Registra um plugin novo, ICMS-MG, e processa uma fatura de Minas Gerais.

nucleo.py não foi alterado: o estado novo entrou por um arquivo em plugins/
e por uma linha de registro aqui.
"""

from dominio import Fatura, Item
from main import imprimir_cabecalho
from nucleo import Nucleo, Registro
from plugins.frete import FretePadrao
from plugins.impostos_mg import IcmsMG
from plugins.impostos_rj import IcmsRJ
from plugins.impostos_sp import IcmsSP, IssSP
from plugins.notificacao import NotificacaoEmail


def main() -> None:
    registro = Registro()
    for plugin in (IcmsSP(), IssSP(), IcmsRJ(), IcmsMG(), FretePadrao(), NotificacaoEmail()):
        registro.registrar(plugin)

    fatura = Fatura(1004, "Mineira Tech", "MG", "contas@mineiratech.com", [
        Item("Notebook Dell", 1, 5000.0, "eletronico"),
    ])
    imprimir_cabecalho(fatura, "Minas Gerais")
    Nucleo(registro).processar(fatura)
    for nome, valor in fatura.ajustes:
        print(f"  {nome}: R${valor:,.2f}")
    print(f"  TOTAL: R${fatura.total:,.2f}")


if __name__ == "__main__":
    main()
