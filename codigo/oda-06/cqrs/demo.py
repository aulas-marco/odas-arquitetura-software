"""Separa o comando da consulta nas solicitações de exame.

O programa envia comandos, consulta o painel antes e depois de processar os
fatos e reconstrói a projeção do zero.
"""

from comandos import ComandoRecusado, SolicitacoesDeExame
from projecao import PainelGerencial


def mostrar(titulo, painel, solicitacoes):
    contagem, defasagem = painel.consultar(len(solicitacoes.fatos))
    print(f"{titulo}: {contagem} | fatos aplicados {painel.posicao} de {len(solicitacoes.fatos)} | defasagem {defasagem}")


if __name__ == "__main__":
    solicitacoes = SolicitacoesDeExame()
    painel = PainelGerencial()

    # 1. Quatro comandos aceitos e um recusado pela invariante.
    solicitacoes.solicitar("EX-1", "hemograma", "Centro")
    solicitacoes.solicitar("EX-2", "raio-x", "Centro")
    solicitacoes.solicitar("EX-3", "hemograma", "Barreiro")
    solicitacoes.cancelar("EX-2")
    try:
        solicitacoes.cancelar("EX-2")
    except ComandoRecusado as recusa:
        print(f"Comando recusado: {recusa}")
    print("Fatos publicados:")
    for posicao, fato in enumerate(solicitacoes.fatos, 1):
        print(f"  {posicao}. {fato['tipo']} {fato['id']} ({fato['unidade']})")
    print()

    # 2. A projeção processou só os dois primeiros fatos. A consulta mostra dado defasado.
    painel.processar(solicitacoes.fatos, limite=2)
    mostrar("Consulta com atraso", painel, solicitacoes)

    # 3. A projeção alcança o último fato e converge.
    painel.processar(solicitacoes.fatos)
    mostrar("Consulta convergida", painel, solicitacoes)

    # 4. A projeção é descartada e reconstruída a partir da lista de fatos.
    painel.ativas_por_unidade = {"Centro": 99}
    mostrar("Projeção corrompida", painel, solicitacoes)
    painel.reconstruir(solicitacoes.fatos)
    mostrar("Projeção reconstruída", painel, solicitacoes)
