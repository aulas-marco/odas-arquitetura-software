"""API GraphQL de elegibilidades da plataforma hospitalar.

O schema vem do arquivo schema.graphql. Cada resolver é a função que busca o
valor de um campo, e só executa quando a consulta pede esse campo.
"""

from pathlib import Path

from ariadne import MutationType, ObjectType, QueryType, make_executable_schema
from ariadne.asgi import GraphQL

from dados import ELEGIBILIDADES, OPERADORAS

query = QueryType()
mutation = MutationType()
elegibilidade = ObjectType("Elegibilidade")


@query.field("elegibilidade")
def resolver_elegibilidade(_, info, protocolo):
    return ELEGIBILIDADES.get(protocolo)


@query.field("elegibilidades")
def resolver_elegibilidades(_, info):
    return list(ELEGIBILIDADES.values())


@elegibilidade.field("operadora")
def resolver_operadora(registro, info):
    # Executa uma vez para cada elegibilidade que a consulta devolve.
    print(f"  [resolver] cadastro de operadoras consultado para {registro['codigoOperadora']}")
    return OPERADORAS[registro["codigoOperadora"]]


@mutation.field("solicitarElegibilidade")
def resolver_solicitar(_, info, pedido):
    protocolo = f"ELG-{len(ELEGIBILIDADES) + 1:03d}"
    ELEGIBILIDADES[protocolo] = {
        "protocolo": protocolo,
        "situacao": "recebida",
        "criadoEm": "2026-07-17T15:00:00Z",
        "matriculaPlano": pedido["matriculaPlano"],
        "codigoOperadora": pedido["codigoOperadora"],
    }
    return ELEGIBILIDADES[protocolo]


SDL = (Path(__file__).parent / "schema.graphql").read_text(encoding="utf-8")
schema = make_executable_schema(SDL, query, mutation, elegibilidade)
app = GraphQL(schema)  # aplicação web que atende POST /graphql
