"""Envia seis operações GraphQL ao mesmo endereço POST /graphql.

O TestClient faz as chamadas HTTP dentro do próprio processo, sem iniciar um
servidor. A operação muda no corpo da requisição, e o endereço permanece igual.
"""

import json
import logging
import warnings

warnings.filterwarnings("ignore", message=".*httpx.*")  # aviso da biblioteca, sem efeito aqui
logging.getLogger("ariadne").setLevel(logging.CRITICAL)  # o erro já aparece na resposta
from starlette.testclient import TestClient  # noqa: E402

from api import app  # noqa: E402

cliente = TestClient(app)


def executar(titulo, operacao, variaveis=None):
    print(f"--- {titulo}")
    corpo = {"query": operacao, "variables": variaveis or {}}
    resposta = cliente.post("/graphql", json=corpo)
    texto = json.dumps(resposta.json(), ensure_ascii=False, separators=(",", ":"))
    print(f"POST /graphql -> {resposta.status_code} ({len(texto.encode('utf-8'))} bytes na resposta)")
    print(json.dumps(resposta.json(), ensure_ascii=False, indent=2))
    print()


if __name__ == "__main__":
    # 1. O aplicativo móvel pede só a situação.
    executar("Consulta do aplicativo móvel",
             '{ elegibilidade(protocolo: "ELG-001") { situacao } }')

    # 2. O painel administrativo pede mais campos e os dados da operadora na mesma consulta.
    executar("Consulta do painel administrativo",
             '{ elegibilidade(protocolo: "ELG-001") { protocolo situacao criadoEm '
             'operadora { nome prazoRespostaHoras } } }')

    # 3. Uma lista com a operadora de cada item executa o resolver uma vez por item.
    executar("Lista com a operadora de cada elegibilidade",
             "{ elegibilidades { protocolo operadora { nome } } }")

    # 4. Um protocolo que não existe devolve null no campo, com status 200.
    executar("Protocolo inexistente",
             '{ elegibilidade(protocolo: "ELG-999") { situacao } }')

    # 5. Um campo que o schema não declara é recusado antes de qualquer resolver executar.
    executar("Campo inexistente no schema",
             '{ elegibilidade(protocolo: "ELG-001") { situacao senhaDoPaciente } }')

    # 6. Uma mutation altera dados e também escolhe os campos da resposta.
    executar("Mutation que solicita uma elegibilidade",
             "mutation Solicitar($pedido: PedidoElegibilidade!) "
             "{ solicitarElegibilidade(pedido: $pedido) { protocolo situacao } }",
             {"pedido": {"cpf": "12345678901", "codigoOperadora": "OPS-002",
                         "matriculaPlano": "MAT-2026-004"}})
