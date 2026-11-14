"""Percorre a API REST de elegibilidades sem iniciar um servidor.

O TestClient faz as chamadas HTTP dentro do próprio processo. O protocolo e o
horário são fixados para que a saída seja igual em cada execução.
"""

import json
import warnings
from datetime import datetime

warnings.filterwarnings("ignore", message=".*httpx.*")  # aviso da biblioteca, sem efeito aqui
from fastapi.testclient import TestClient  # noqa: E402

import main

main.uuid4 = lambda: "550e8400-e29b-41d4-a716-446655440000"


class RelogioFixo:
    @staticmethod
    def now(fuso):
        return datetime(2026, 7, 17, 13, 30, tzinfo=fuso)


main.datetime = RelogioFixo


def mostrar(metodo, rota, resposta):
    print(f"{metodo} {rota} -> {resposta.status_code}")
    if "location" in resposta.headers:
        print(f"Location: {resposta.headers['location']}")
    print(json.dumps(resposta.json(), ensure_ascii=False, indent=2))
    print()


if __name__ == "__main__":
    cliente = TestClient(main.app)
    pedido = {
        "cpf": "12345678901",
        "codigo_operadora": "OPS-001",
        "matricula_plano": "MAT-2026-001",
    }

    # 1. Caminho feliz: o pedido é aceito e guardado em memória.
    resposta = cliente.post("/elegibilidades", json=pedido)
    mostrar("POST", "/elegibilidades", resposta)

    # 2. A consulta usa o endereço devolvido no cabeçalho Location.
    endereco = resposta.headers["location"]
    mostrar("GET", endereco, cliente.get(endereco))

    # 3. Protocolo que a API nunca emitiu devolve 404.
    mostrar("GET", "/elegibilidades/protocolo-inexistente",
            cliente.get("/elegibilidades/protocolo-inexistente"))

    # 4. Pedido com cpf fora do padrão de onze dígitos é recusado antes de a rota rodar.
    cpf_curto = dict(pedido, cpf="123")
    mostrar("POST", "/elegibilidades (cpf com 3 dígitos)",
            cliente.post("/elegibilidades", json=cpf_curto))

    # 5. Tamanho do corpo enviado no caminho feliz, para comparar com o gRPC.
    corpo = json.dumps(pedido, separators=(",", ":")).encode("utf-8")
    print(f"Corpo do pedido em JSON: {len(corpo)} bytes")
