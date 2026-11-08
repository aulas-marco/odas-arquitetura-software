"""Modelo interno do módulo Agenda, de uso exclusivo do próprio módulo.

Na versão 2 da Agenda, a situação da reserva passou a ser gravada como código
de duas letras. A mudança é permitida porque o modelo é interno e o contrato
público em agenda/api.py permaneceu igual.
"""

from dataclasses import dataclass

AGENDADA = "AG"
REALIZADA = "RE"
CANCELADA = "CA"


@dataclass
class ReservaModel:
    id: int
    paciente: str
    procedimento: str
    valor_centavos: int
    situacao: str = AGENDADA
