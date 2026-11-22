"""Serviço de Exames: registra uma solicitação depois de consultar Elegibilidade.

Exames tem banco próprio (a lista solicitacoes) e nunca lê o banco de
Elegibilidade. A única ligação entre os dois é a chamada HTTP com prazo de
espera. Cada resultado devolve um par (status HTTP, corpo), como uma API faria.
"""

import json
import urllib.error
import urllib.request


class ServicoExames:
    def __init__(self, url_elegibilidade, prazo=2.0, politica=None):
        self.url_elegibilidade = url_elegibilidade
        self.prazo = prazo  # segundos que Exames aceita esperar por Elegibilidade
        self.politica = politica or (lambda chamada: chamada())  # sem política: uma tentativa
        self.solicitacoes = []
        self._por_chave = {}  # chave de idempotência -> solicitação já registrada

    def health(self):
        return 200, {"status": "ok", "servico": "exames"}

    def consultar_elegibilidade(self, beneficiario_id):
        url = f"{self.url_elegibilidade}/elegibilidades/{beneficiario_id}"
        try:
            with urllib.request.urlopen(url, timeout=self.prazo) as resposta:
                return resposta.status, json.load(resposta)
        except urllib.error.HTTPError as erro:
            if erro.code >= 500:
                raise ConnectionError(f"Elegibilidade respondeu {erro.code}") from erro
            return erro.code, json.load(erro)
        except (urllib.error.URLError, TimeoutError) as erro:
            raise ConnectionError("Elegibilidade não respondeu dentro do prazo") from erro

    def solicitar_exame(self, beneficiario_id, codigo_exame, chave=None):
        if chave in self._por_chave:  # pedido repetido: devolve o que já foi registrado
            return 201, self._por_chave[chave]
        try:
            status, corpo = self.politica(lambda: self.consultar_elegibilidade(beneficiario_id))
        except ConnectionError:
            return 503, {"codigo": "dependencia_indisponivel"}
        if status == 404:
            return 422, {"codigo": "beneficiario_desconhecido"}
        if not corpo["elegivel"]:
            return 422, {"codigo": "beneficiario_inelegivel"}
        solicitacao = {"solicitacao_id": len(self.solicitacoes) + 1,
                       "beneficiario_id": beneficiario_id, "codigo_exame": codigo_exame}
        self.solicitacoes.append(solicitacao)
        if chave is not None:
            self._por_chave[chave] = solicitacao
        return 201, solicitacao
