"""Modelo de comando das solicitações de exame.

O comando expressa uma intenção e preserva as invariantes. Cada mudança aceita
grava a solicitação no banco do serviço e acrescenta um fato à lista de fatos,
que a projeção de leitura consome depois.
"""


class ComandoRecusado(Exception):
    """A intenção violaria uma invariante da solicitação."""


class SolicitacoesDeExame:
    def __init__(self):
        self._banco = {}  # modelo de escrita: solicitação -> dados
        self.fatos = []  # fatos publicados, em ordem

    def solicitar(self, solicitacao_id, codigo_exame, unidade):
        if solicitacao_id in self._banco:
            raise ComandoRecusado(f"{solicitacao_id} já existe")
        self._banco[solicitacao_id] = {"exame": codigo_exame, "unidade": unidade, "situacao": "solicitada"}
        self.fatos.append({"tipo": "ExameSolicitado", "id": solicitacao_id, "exame": codigo_exame, "unidade": unidade})

    def cancelar(self, solicitacao_id):
        atual = self._banco.get(solicitacao_id)
        if atual is None or atual["situacao"] != "solicitada":
            raise ComandoRecusado(f"{solicitacao_id} não pode ser cancelada")
        atual["situacao"] = "cancelada"
        self.fatos.append({"tipo": "ExameCancelado", "id": solicitacao_id, "unidade": atual["unidade"]})
