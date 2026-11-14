"""Dados em memória usados pela API GraphQL.

As operadoras ficam num cadastro separado das elegibilidades, como ficariam num
serviço ou numa tabela própria. Cada elegibilidade guarda só o código da operadora.
"""

OPERADORAS = {
    "OPS-001": {"codigo": "OPS-001", "nome": "Saúde Mais", "prazoRespostaHoras": 24},
    "OPS-002": {"codigo": "OPS-002", "nome": "Vida Plena", "prazoRespostaHoras": 48},
}

ELEGIBILIDADES = {
    "ELG-001": {"protocolo": "ELG-001", "situacao": "recebida", "criadoEm": "2026-07-17T13:30:00Z",
                "matriculaPlano": "MAT-2026-001", "codigoOperadora": "OPS-001"},
    "ELG-002": {"protocolo": "ELG-002", "situacao": "em_analise", "criadoEm": "2026-07-17T13:42:00Z",
                "matriculaPlano": "MAT-2026-002", "codigoOperadora": "OPS-002"},
    "ELG-003": {"protocolo": "ELG-003", "situacao": "elegivel", "criadoEm": "2026-07-17T14:05:00Z",
                "matriculaPlano": "MAT-2026-003", "codigoOperadora": "OPS-001"},
}
