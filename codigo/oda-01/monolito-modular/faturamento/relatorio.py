"""Forma correta: o Faturamento consome o contrato público da Agenda."""

from agenda.api import AgendaAPI


class RelatorioFaturamento:
    def __init__(self, agenda: AgendaAPI) -> None:
        self._agenda = agenda

    def gerar(self) -> tuple[int, float]:
        consultas = self._agenda.consultas_faturaveis()
        return len(consultas), sum(c.valor for c in consultas)
