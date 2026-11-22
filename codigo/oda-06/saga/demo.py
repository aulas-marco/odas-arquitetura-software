"""Percorre quatro execuções da SAGA de agendamento de exame.

Cada cenário cria participantes novos, executa o orquestrador e mostra a trilha
de auditoria e a situação gravada no banco de cada participante.
"""

from orquestrador import OrquestradorAgendamento
from participantes import Agenda, Autorizacao, PreparoDeSala


def mostrar(titulo, orquestrador, agendamento_id):
    print(f"== {titulo}")
    for linha in orquestrador.trilha:
        print(linha)
    print("Bancos locais:")
    for passo in orquestrador.passos:
        print(f"  {passo.nome}: {passo.situacao(agendamento_id)}")
    print()


if __name__ == "__main__":
    # 1. Caminho feliz: os três passos confirmam suas transações locais.
    saga = OrquestradorAgendamento([Agenda(), Autorizacao(), PreparoDeSala()])
    saga.executar("AG-101")
    mostrar("1. Agendamento concluído", saga, "AG-101")

    # 2. O Preparo de Sala recusa o recurso. As compensações rodam em ordem inversa.
    saga = OrquestradorAgendamento([Agenda(), Autorizacao(), PreparoDeSala(falhar_em={"reservar sala"})])
    saga.executar("AG-102")
    mostrar("2. Falha no Preparo de Sala", saga, "AG-102")

    # 3. A compensação da Autorização também falha. A SAGA para e pede intervenção.
    saga = OrquestradorAgendamento([
        Agenda(),
        Autorizacao(falhar_em={"cancelar autorização"}),
        PreparoDeSala(falhar_em={"reservar sala"}),
    ])
    saga.executar("AG-103")
    mostrar("3. Falha na compensação", saga, "AG-103")

    # 4. O orquestrador reinicia e reenvia os mesmos comandos. Nenhum passo é aplicado duas vezes.
    saga = OrquestradorAgendamento([Agenda(), Autorizacao(), PreparoDeSala()])
    saga.executar("AG-104")
    saga.trilha.append("[AG-104] -- orquestrador reiniciado, comandos reenviados --")
    saga.executar("AG-104")
    mostrar("4. Comandos repetidos", saga, "AG-104")
