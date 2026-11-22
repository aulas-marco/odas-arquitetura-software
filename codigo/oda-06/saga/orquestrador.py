"""Orquestrador da SAGA de agendamento de exame.

O orquestrador conhece a sequência dos passos, chama cada participante e, na
falha, aciona as compensações em ordem inversa. A trilha guarda cada evento
para auditoria.
"""

from participantes import FalhaNoPasso


class OrquestradorAgendamento:
    def __init__(self, passos):
        self.passos = passos  # sequência declarada num lugar só
        self.trilha = []  # trilha de auditoria: uma linha por evento

    def _registrar(self, agendamento_id, texto):
        self.trilha.append(f"[{agendamento_id}] {texto}")

    def executar(self, agendamento_id):
        concluidos = []
        for passo in self.passos:
            comando_id = f"{agendamento_id}:{passo.nome}:executar"
            try:
                resultado = passo.executar(comando_id, agendamento_id)
            except FalhaNoPasso as falha:
                self._registrar(agendamento_id, f"falha: {falha}")
                return self._compensar(agendamento_id, concluidos)
            self._registrar(agendamento_id, f"{passo.nome}: {resultado}")
            concluidos.append(passo)
        self._registrar(agendamento_id, "situação final: concluida")
        return "concluida"

    def _compensar(self, agendamento_id, concluidos):
        for passo in reversed(concluidos):  # ordem inversa à da execução
            comando_id = f"{agendamento_id}:{passo.nome}:compensar"
            try:
                resultado = passo.compensar(comando_id, agendamento_id)
            except FalhaNoPasso as falha:
                self._registrar(agendamento_id, f"falha na compensação: {falha}")
                self._registrar(agendamento_id, "situação final: requer_intervencao")
                return "requer_intervencao"
            self._registrar(agendamento_id, f"{passo.nome}: {resultado}")
        self._registrar(agendamento_id, "situação final: compensada")
        return "compensada"
