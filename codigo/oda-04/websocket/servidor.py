"""Servidor WebSocket que avisa mudanças de situação de uma elegibilidade.

O cliente abre uma conexão e pede para acompanhar um protocolo. A partir daí o
servidor envia mensagens pela mesma conexão sempre que a situação muda, sem
esperar uma nova requisição do cliente.
"""

import asyncio
import json

from websockets.asyncio.server import serve
from websockets.exceptions import ConnectionClosed


class CentralDeAcompanhamento:
    def __init__(self, situacoes: dict[str, str]):
        self._situacoes = dict(situacoes)
        self._conexoes: dict[str, set] = {}  # protocolo -> conexões abertas que o acompanham

    async def atender(self, conexao):
        """Executa enquanto a conexão de um cliente permanece aberta."""
        try:
            async for mensagem in conexao:
                pedido = json.loads(mensagem)
                if pedido["acao"] == "acompanhar":
                    protocolo = pedido["protocolo"]
                    self._conexoes.setdefault(protocolo, set()).add(conexao)
                    # Quem chega, ou volta depois de uma queda, recebe primeiro o estado atual.
                    await conexao.send(json.dumps({
                        "tipo": "estado_atual", "protocolo": protocolo,
                        "situacao": self._situacoes[protocolo]}))
        finally:
            for conexoes in self._conexoes.values():
                conexoes.discard(conexao)

    async def publicar(self, protocolo: str, situacao: str):
        """Chamado quando a operadora responde. Envia a mudança às conexões abertas."""
        self._situacoes[protocolo] = situacao
        destinos = list(self._conexoes.get(protocolo, ()))
        print(f"  [servidor] {protocolo} mudou para {situacao}, {len(destinos)} conexão(ões) aberta(s)")
        mensagem = json.dumps({"tipo": "mudanca", "protocolo": protocolo, "situacao": situacao})
        for conexao in destinos:
            try:
                await conexao.send(mensagem)
            except ConnectionClosed:
                pass  # a mensagem não é guardada para quem caiu


async def principal():
    central = CentralDeAcompanhamento({"ELG-001": "recebida"})
    async with serve(central.atender, "127.0.0.1", 8765) as servidor:
        print("Servidor WebSocket atendendo em ws://127.0.0.1:8765. Ctrl+C encerra.")
        await servidor.serve_forever()


if __name__ == "__main__":
    asyncio.run(principal())
