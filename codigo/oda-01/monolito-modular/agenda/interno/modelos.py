"""Modelo interno do módulo Agenda. Nenhum outro módulo deve importar este arquivo.

Na versão 2 da Agenda, a situação da reserva deixou de ser gravada como texto
("agendada", "realizada", "cancelada") e passou a ser gravada como código de
duas letras. A mudança é legítima porque o modelo é interno: o contrato público,
em agenda/api.py, continuou igual.
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
