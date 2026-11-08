"""Forma errada: o Faturamento lê o modelo interno da Agenda.

O atalho foi escrito quando a Agenda gravava a situação como texto. Desde a
versão 2 da Agenda a comparação abaixo é sempre falsa, e o relatório devolve
zero sem mensagem de erro.
"""

from agenda.interno.armazenamento import RESERVAS


class RelatorioFaturamentoComAtalho:
    def gerar(self) -> tuple[int, float]:
        realizadas = [r for r in RESERVAS if r.situacao == "realizada"]
        return len(realizadas), sum(r.valor_centavos for r in realizadas) / 100
