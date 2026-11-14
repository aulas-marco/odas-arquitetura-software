"""Serviço gRPC de elegibilidades da plataforma hospitalar.

A classe herda de ElegibilidadesServicer, gerada a partir de elegibilidade.proto,
e implementa uma função Python para cada operação declarada no contrato.
"""

from concurrent import futures
from datetime import datetime, timezone
from uuid import uuid4

import grpc

import elegibilidade_pb2 as pb
import elegibilidade_pb2_grpc as pb_grpc


class ServicoElegibilidades(pb_grpc.ElegibilidadesServicer):
    def __init__(self, gerar_protocolo=lambda: str(uuid4()),
                 agora=lambda: datetime.now(timezone.utc)):
        self._elegibilidades: dict[str, pb.ElegibilidadeAceita] = {}
        self._gerar_protocolo = gerar_protocolo
        self._agora = agora

    def SolicitarElegibilidade(self, pedido, context):
        # O .proto declara apenas o tipo string. A regra dos onze dígitos fica no servidor.
        if not (len(pedido.cpf) == 11 and pedido.cpf.isdigit()):
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "cpf deve ter onze dígitos")
        aceita = pb.ElegibilidadeAceita(
            protocolo=self._gerar_protocolo(),
            situacao="recebida",
            criado_em=self._agora().strftime("%Y-%m-%dT%H:%M:%SZ"),
        )
        self._elegibilidades[aceita.protocolo] = aceita
        return aceita

    def ConsultarElegibilidade(self, consulta, context):
        encontrada = self._elegibilidades.get(consulta.protocolo)
        if encontrada is None:
            context.abort(grpc.StatusCode.NOT_FOUND, "Protocolo de elegibilidade não encontrado.")
        return encontrada


def iniciar_servidor(servico: ServicoElegibilidades, porta: int = 50051):
    """Registra o serviço num servidor gRPC e devolve o servidor e a porta em uso."""
    servidor = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    pb_grpc.add_ElegibilidadesServicer_to_server(servico, servidor)
    porta_em_uso = servidor.add_insecure_port(f"127.0.0.1:{porta}")
    servidor.start()
    return servidor, porta_em_uso


if __name__ == "__main__":
    servidor, porta = iniciar_servidor(ServicoElegibilidades())
    print(f"Servidor gRPC atendendo em 127.0.0.1:{porta}. Ctrl+C encerra.")
    servidor.wait_for_termination()
