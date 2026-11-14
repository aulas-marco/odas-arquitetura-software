"""Mostra o canal WebSocket em duas cenas, com servidor e clientes no mesmo processo.

Na primeira cena, dois clientes recebem a mesma mudança sem pedir de novo. Na
segunda, a conexão cai e uma mudança acontece enquanto ninguém está conectado.
"""

import asyncio
import json

from websockets.asyncio.client import connect
from websockets.asyncio.server import serve

from servidor import CentralDeAcompanhamento


async def enviar(nome, conexao, mensagem):
    await conexao.send(json.dumps(mensagem))
    print(f"  [{nome}] enviou: {json.dumps(mensagem, ensure_ascii=False)}")


async def receber(nome, conexao):
    mensagem = json.loads(await conexao.recv())
    print(f"  [{nome}] recebeu: {json.dumps(mensagem, ensure_ascii=False)}")


async def principal():
    central = CentralDeAcompanhamento({"ELG-001": "recebida"})
    async with serve(central.atender, "127.0.0.1", 0) as servidor:  # porta 0: o sistema escolhe uma livre
        url = f"ws://127.0.0.1:{servidor.sockets[0].getsockname()[1]}"

        print("--- Cena 1: painel e aplicativo acompanham ELG-001")
        async with connect(url) as painel, connect(url) as aplicativo:
            await enviar("painel", painel, {"acao": "acompanhar", "protocolo": "ELG-001"})
            await receber("painel", painel)
            await enviar("aplicativo", aplicativo, {"acao": "acompanhar", "protocolo": "ELG-001"})
            await receber("aplicativo", aplicativo)
            await central.publicar("ELG-001", "em_analise")  # a operadora começou a analisar
            await receber("painel", painel)
            await receber("aplicativo", aplicativo)
        print("  [painel] e [aplicativo] fecharam a conexão")
        print()

        await asyncio.sleep(0.2)  # tempo para o servidor registrar o fechamento
        print("--- Cena 2: uma mudança acontece sem nenhuma conexão aberta")
        await central.publicar("ELG-001", "elegivel")  # ninguém recebe esta mensagem
        async with connect(url) as painel:
            await enviar("painel", painel, {"acao": "acompanhar", "protocolo": "ELG-001"})
            await receber("painel", painel)
        print("  O painel recebeu o estado atual. A mensagem de mudança para elegivel não foi entregue.")


if __name__ == "__main__":
    asyncio.run(principal())
