"""Percorre o serviço gRPC de elegibilidades com um cliente gerado.

O servidor sobe numa porta livre do próprio computador e o cliente chama as
operações pelo stub, que tem um método Python para cada rpc do contrato.
"""

import json
from datetime import datetime, timezone

import grpc

import elegibilidade_pb2 as pb
import elegibilidade_pb2_grpc as pb_grpc
from servidor import ServicoElegibilidades, iniciar_servidor


def mostrar(operacao, resposta):
    print(f"{operacao} -> OK")
    print(f'  protocolo: "{resposta.protocolo}"')
    print(f'  situacao: "{resposta.situacao}"')
    print(f'  criado_em: "{resposta.criado_em}"')
    print()


def mostrar_erro(operacao, erro: grpc.RpcError):
    print(f"{operacao} -> {erro.code().name}")
    print(f"  detalhe: {erro.details()}")
    print()


if __name__ == "__main__":
    # Protocolo e horário fixos tornam a saída igual em cada execução.
    servico = ServicoElegibilidades(
        gerar_protocolo=lambda: "550e8400-e29b-41d4-a716-446655440000",
        agora=lambda: datetime(2026, 7, 17, 13, 30, tzinfo=timezone.utc),
    )
    servidor, porta = iniciar_servidor(servico, porta=0)  # porta 0: o sistema escolhe uma livre

    with grpc.insecure_channel(f"127.0.0.1:{porta}") as canal:
        stub = pb_grpc.ElegibilidadesStub(canal)
        pedido = pb.PedidoElegibilidade(
            cpf="12345678901", codigo_operadora="OPS-001", matricula_plano="MAT-2026-001"
        )

        # 1. Caminho feliz: a chamada remota tem a forma de uma chamada de função.
        aceita = stub.SolicitarElegibilidade(pedido)
        mostrar("SolicitarElegibilidade", aceita)

        # 2. A consulta usa o protocolo devolvido na mensagem de resposta.
        mostrar("ConsultarElegibilidade",
                stub.ConsultarElegibilidade(pb.ConsultaElegibilidade(protocolo=aceita.protocolo)))

        # 3. Protocolo que o serviço nunca emitiu devolve o status NOT_FOUND.
        try:
            stub.ConsultarElegibilidade(pb.ConsultaElegibilidade(protocolo="protocolo-inexistente"))
        except grpc.RpcError as erro:
            mostrar_erro("ConsultarElegibilidade (protocolo inexistente)", erro)

        # 4. Pedido com cpf curto chega ao servidor, que recusa com INVALID_ARGUMENT.
        try:
            stub.SolicitarElegibilidade(pb.PedidoElegibilidade(
                cpf="123", codigo_operadora="OPS-001", matricula_plano="MAT-2026-001"))
        except grpc.RpcError as erro:
            mostrar_erro("SolicitarElegibilidade (cpf com 3 dígitos)", erro)

    servidor.stop(grace=None)

    # 5. O mesmo pedido em JSON e em Protocol Buffers.
    como_json = json.dumps({"cpf": pedido.cpf, "codigo_operadora": pedido.codigo_operadora,
                            "matricula_plano": pedido.matricula_plano},
                           separators=(",", ":")).encode("utf-8")
    binario = pedido.SerializeToString()
    print(f"Corpo do pedido em JSON: {len(como_json)} bytes")
    print(f"Corpo do pedido em Protocol Buffers: {len(binario)} bytes")
    print(f"Primeiros bytes da mensagem binária: {binario[:16]!r}")
