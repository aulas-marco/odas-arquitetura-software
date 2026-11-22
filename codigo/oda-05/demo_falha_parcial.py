"""Mostra a falha parcial: Exames saudável e incapaz de aceitar solicitações.

Elegibilidade roda como servidor HTTP numa porta livre. A demonstração passa por
três situações da dependência: no ar, fora do ar e lenta.
"""

import time

from elegibilidade import ServidorElegibilidade
from exames import ServicoExames


def mostrar(rotulo, resultado):
    status, corpo = resultado
    print(f"{rotulo} -> {status} {corpo}")


if __name__ == "__main__":
    elegibilidade = ServidorElegibilidade().iniciar()
    exames = ServicoExames(elegibilidade.url, prazo=0.3)

    # 1. Elegibilidade no ar: os três resultados de negócio possíveis.
    print("Elegibilidade no ar")
    mostrar("  POST /exames B-001", exames.solicitar_exame("B-001", "HEMOGRAMA"))
    mostrar("  POST /exames B-002", exames.solicitar_exame("B-002", "HEMOGRAMA"))
    mostrar("  POST /exames B-999", exames.solicitar_exame("B-999", "HEMOGRAMA"))

    # 2. Elegibilidade fora do ar: Exames continua respondendo, mas não registra.
    elegibilidade.parar()
    print("\nElegibilidade fora do ar")
    mostrar("  GET /health       ", exames.health())
    mostrar("  POST /exames B-001", exames.solicitar_exame("B-001", "GLICEMIA"))
    print(f"  solicitações gravadas em Exames: {len(exames.solicitacoes)}")

    # 3. Elegibilidade lenta: responde em 1 s, e Exames espera no máximo 300 ms.
    lenta = ServidorElegibilidade().iniciar()
    lenta.modo = "lenta"
    exames.url_elegibilidade = lenta.url
    print("\nElegibilidade lenta com resposta em 1 s e prazo de 300 ms em Exames")
    inicio = time.monotonic()
    mostrar("  POST /exames B-001", exames.solicitar_exame("B-001", "GLICEMIA"))
    desistiu_cedo = time.monotonic() - inicio < 0.5
    print(f"  Exames desistiu antes de 500 ms: {'sim' if desistiu_cedo else 'não'}")
    lenta.parar()
