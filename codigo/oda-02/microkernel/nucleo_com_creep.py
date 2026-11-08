"""Contraexemplo do anti-padrão core creep, mantido apenas para leitura.

O programa main.py não usa este arquivo. A regra de cada estado está escrita
como condicional dentro do núcleo, e cada estado novo exige uma nova versão
do núcleo.
"""

from dominio import Fatura


class NucleoComCreep:
    def processar(self, fatura: Fatura) -> None:
        eletronicos = sum(i.total for i in fatura.itens if i.categoria == "eletronico")
        if fatura.estado == "SP":
            fatura.ajustes.append(("ICMS-SP", eletronicos * 0.18))
        elif fatura.estado == "RJ":
            fatura.ajustes.append(("ICMS-RJ", eletronicos * 0.20))
        # Minas Gerais exigiria mais um elif dentro do núcleo.
