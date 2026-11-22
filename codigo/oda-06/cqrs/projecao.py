"""Projeção de leitura do painel gerencial.

A projeção conta solicitações ativas por unidade. Ela guarda a posição do último
fato aplicado, o que torna a defasagem visível e permite reconstruir o painel
a partir da lista de fatos.
"""


class PainelGerencial:
    def __init__(self):
        self.ativas_por_unidade = {}  # modelo de leitura, pronto para a consulta
        self.posicao = 0  # quantos fatos já foram aplicados

    def processar(self, fatos, limite=None):
        fim = len(fatos) if limite is None else min(limite, len(fatos))
        for fato in fatos[self.posicao:fim]:
            unidade = fato["unidade"]
            atual = self.ativas_por_unidade.get(unidade, 0)
            if fato["tipo"] == "ExameSolicitado":
                self.ativas_por_unidade[unidade] = atual + 1
            elif fato["tipo"] == "ExameCancelado":
                self.ativas_por_unidade[unidade] = atual - 1
        self.posicao = max(self.posicao, fim)

    def reconstruir(self, fatos):
        self.ativas_por_unidade = {}  # descarta a projeção e aplica todos os fatos de novo
        self.posicao = 0
        self.processar(fatos)

    def consultar(self, total_de_fatos):
        defasagem = total_de_fatos - self.posicao
        return dict(sorted(self.ativas_por_unidade.items())), defasagem
