"""Armazenamento interno da Agenda. Em produção, seria uma tabela do banco."""

from agenda.interno.modelos import ReservaModel

RESERVAS: list[ReservaModel] = []
