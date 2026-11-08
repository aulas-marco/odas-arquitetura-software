"""Regra tributária de Minas Gerais, acrescentada sem alterar o núcleo.

A alíquota é ilustrativa e serve apenas ao exemplo.
"""

from dominio import Fatura
from nucleo import Plugin

ALIQUOTA_ICMS = 0.18


class IcmsMG(Plugin):
    nome = "ICMS-MG"
    categoria = "impostos"

    def aplica_se(self, fatura: Fatura) -> bool:
        return fatura.estado == "MG"

    def executar(self, fatura: Fatura) -> None:
        base = sum(i.total for i in fatura.itens if i.categoria == "eletronico")
        if base:
            fatura.ajustes.append(("ICMS-MG", base * ALIQUOTA_ICMS))
