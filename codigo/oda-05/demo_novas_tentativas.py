"""Mostra a nova tentativa numa falha transitória e o risco de repetir uma escrita.

Elegibilidade fica instável: responde 503 nas duas primeiras chamadas e depois
volta ao normal. A segunda parte repete um POST cuja resposta se perdeu.
"""

import time

from elegibilidade import ServidorElegibilidade
from exames import ServicoExames
from resiliencia import com_novas_tentativas

if __name__ == "__main__":
    elegibilidade = ServidorElegibilidade().iniciar()

    # 1. Sem política: a primeira falha transitória vira 503 para a recepção.
    elegibilidade.modo, elegibilidade.falhas_restantes = "instavel", 2
    exames = ServicoExames(elegibilidade.url, prazo=0.3)
    print("Sem nova tentativa")
    print(f"  POST /exames B-001 -> {exames.solicitar_exame('B-001', 'HEMOGRAMA')[0]}")

    # 2. Três tentativas com espera exponencial: a terceira encontra o serviço de volta.
    elegibilidade.falhas_restantes, elegibilidade.chamadas = 2, 0
    exames.politica = com_novas_tentativas(tentativas=3, espera_inicial=0.1, dormir=time.sleep)
    print("\nCom até três tentativas")
    print(f"  POST /exames B-001 -> {exames.solicitar_exame('B-001', 'HEMOGRAMA')[0]}")
    print(f"  chamadas que chegaram a Elegibilidade: {elegibilidade.chamadas}")
    elegibilidade.parar()

    # 3. A recepção repete o POST porque a resposta se perdeu na rede.
    #    A primeira resposta é descartada para simular a perda.
    elegibilidade = ServidorElegibilidade().iniciar()
    print("\nRecepção repete o POST sem chave de idempotência")
    exames = ServicoExames(elegibilidade.url)
    exames.solicitar_exame("B-001", "RAIO-X")  # resposta perdida
    exames.solicitar_exame("B-001", "RAIO-X")  # repetição
    print(f"  solicitações gravadas: {len(exames.solicitacoes)}")

    print("\nRecepção repete o POST com a chave de idempotência req-7f3a")
    exames = ServicoExames(elegibilidade.url)
    exames.solicitar_exame("B-001", "RAIO-X", chave="req-7f3a")  # resposta perdida
    status, corpo = exames.solicitar_exame("B-001", "RAIO-X", chave="req-7f3a")
    print(f"  segunda resposta -> {status} {corpo}")
    print(f"  solicitações gravadas: {len(exames.solicitacoes)}")
    elegibilidade.parar()
