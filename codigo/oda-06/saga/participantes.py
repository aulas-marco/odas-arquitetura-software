"""Participantes da SAGA de agendamento de exame.

Cada participante guarda o próprio estado num dicionário privado, que faz o papel
do banco do serviço. Nenhum participante lê o banco de outro.
"""


class FalhaNoPasso(Exception):
    """Recusa de negócio ou indisponibilidade de um participante."""


class Participante:
    nome = "participante"

    def __init__(self, falhar_em=()):
        self._banco = {}  # banco local: agendamento -> situação
        self._processados = set()  # comandos já aplicados, para a idempotência
        self._falhar_em = set(falhar_em)  # operações que falham nesta execução

    def _aplicar(self, comando_id, operacao, agendamento_id, situacao):
        if comando_id in self._processados:
            return "comando_repetido_sem_efeito"
        if operacao in self._falhar_em:
            raise FalhaNoPasso(f"{self.nome} não conseguiu {operacao}")
        self._banco[agendamento_id] = situacao  # transação local confirmada
        self._processados.add(comando_id)
        return situacao

    def situacao(self, agendamento_id):
        return self._banco.get(agendamento_id, "sem registro")


class Agenda(Participante):
    nome = "Agenda"

    def executar(self, comando_id, agendamento_id):
        return self._aplicar(comando_id, "reservar horário", agendamento_id, "horario_reservado")

    def compensar(self, comando_id, agendamento_id):
        return self._aplicar(comando_id, "liberar horário", agendamento_id, "horario_liberado")


class Autorizacao(Participante):
    nome = "Autorização"

    def executar(self, comando_id, agendamento_id):
        return self._aplicar(comando_id, "autorizar procedimento", agendamento_id, "procedimento_autorizado")

    def compensar(self, comando_id, agendamento_id):
        return self._aplicar(comando_id, "cancelar autorização", agendamento_id, "autorizacao_cancelada")


class PreparoDeSala(Participante):
    nome = "Preparo de Sala"

    def executar(self, comando_id, agendamento_id):
        return self._aplicar(comando_id, "reservar sala", agendamento_id, "sala_reservada")

    def compensar(self, comando_id, agendamento_id):
        return self._aplicar(comando_id, "liberar sala", agendamento_id, "sala_liberada")
