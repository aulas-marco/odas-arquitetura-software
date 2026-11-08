"""Contrato público do módulo Agenda, único ponto de acesso permitido aos outros módulos.

O contrato devolve o tipo próprio ConsultaFaturavel e converte o modelo interno.
Uma mudança no modelo interno exige ajuste somente neste arquivo.
"""

from dataclasses import dataclass

from agenda.interno import armazenamento
from agenda.interno.modelos import CANCELADA, REALIZADA, ReservaModel


@dataclass(frozen=True)
class ConsultaFaturavel:
    reserva_id: int
    paciente: str
    procedimento: str
    valor: float


class AgendaAPI:
    def reservar(self, paciente: str, procedimento: str, valor: float) -> int:
        reserva = ReservaModel(
            id=len(armazenamento.RESERVAS) + 1,
            paciente=paciente,
            procedimento=procedimento,
            valor_centavos=round(valor * 100),
        )
        armazenamento.RESERVAS.append(reserva)
        return reserva.id

    def registrar_realizacao(self, reserva_id: int) -> None:
        self._buscar(reserva_id).situacao = REALIZADA

    def cancelar(self, reserva_id: int) -> None:
        self._buscar(reserva_id).situacao = CANCELADA

    def consultas_faturaveis(self) -> list[ConsultaFaturavel]:
        return [
            ConsultaFaturavel(r.id, r.paciente, r.procedimento, r.valor_centavos / 100)
            for r in armazenamento.RESERVAS
            if r.situacao == REALIZADA
        ]

    @staticmethod
    def _buscar(reserva_id: int) -> ReservaModel:
        return next(r for r in armazenamento.RESERVAS if r.id == reserva_id)
