"""Contraexemplo para leitura: o núcleo que acumulou regra de plugin (core creep).

Este arquivo não é usado por main.py. Ele mostra o que acontece quando a regra
de cada estado é escrita como condicional dentro do núcleo: cada estado novo
exige alterar, testar e implantar o núcleo de novo.
"""

from dominio import Fatura


class NucleoComCreep:
    def processar(self, fatura: Fatura) -> None:
        eletronicos = sum(i.total for i in fatura.itens if i.categoria == "eletronico")
        if fatura.estado == "SP":
            fatura.ajustes.append(("ICMS-SP", eletronicos * 0.18))
        elif fatura.estado == "RJ":
            fatura.ajustes.append(("ICMS-RJ", eletronicos * 0.20))
        # Minas Gerais exigiria mais um elif aqui, dentro do núcleo.
