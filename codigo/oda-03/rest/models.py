"""Contrato REST da elegibilidade, escrito como classes Pydantic.

O tipo declarado em cada campo funciona como regra de validação. Um corpo que
não cumpre o tipo é recusado pelo FastAPI antes de a rota executar.
"""

from datetime import datetime

from pydantic import BaseModel, Field


class PedidoElegibilidade(BaseModel):  # o que o consumidor envia
    cpf: str = Field(pattern=r"^\d{11}$")  # onze dígitos, valor sintético
    codigo_operadora: str
    matricula_plano: str


class ElegibilidadeAceita(BaseModel):  # o que a API devolve
    protocolo: str
    situacao: str  # neste incremento, sempre "recebida"
    criado_em: datetime
