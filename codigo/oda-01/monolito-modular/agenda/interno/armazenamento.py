"""Armazenamento interno da Agenda, que em produção corresponderia a uma tabela do banco de dados."""

from agenda.interno.modelos import ReservaModel

RESERVAS: list[ReservaModel] = []
