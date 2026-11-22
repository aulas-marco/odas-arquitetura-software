"""Mostra o disjuntor abrindo, recusando chamadas sem usar a rede e fechando.

Elegibilidade começa fora do ar. O relógio é simulado: a demonstração avança 30
segundos sem esperar de verdade.
"""

from elegibilidade import ServidorElegibilidade
from exames import ServicoExames
from resiliencia import Disjuntor


class RelogioSimulado:
    def __init__(self):
        self.agora = 0.0

    def __call__(self):
        return self.agora


if __name__ == "__main__":
    relogio = RelogioSimulado()
    disjuntor = Disjuntor(limite_falhas=3, tempo_aberto=30, relogio=relogio)

    # Elegibilidade sobe e para logo em seguida: o endereço existe e ninguém atende.
    elegibilidade = ServidorElegibilidade().iniciar()
    url = elegibilidade.url
    elegibilidade.parar()
    exames = ServicoExames(url, prazo=0.3, politica=disjuntor)

    # 1. Cinco pedidos com Elegibilidade fora do ar.
    print("Elegibilidade fora do ar, limite de 3 falhas")
    tentativas_na_rede = 0
    for pedido in range(1, 6):
        usou_rede = disjuntor.estado != "aberto"
        tentativas_na_rede += usou_rede
        status = exames.solicitar_exame("B-001", "HEMOGRAMA")[0]
        print(f"  pedido {pedido}: {status}, usou a rede: {'sim' if usou_rede else 'não'}, "
              f"disjuntor {disjuntor.estado}")
    print(f"  tentativas de conexão: {tentativas_na_rede} de 5 pedidos")

    # 2. Trinta segundos depois, Elegibilidade volta ao ar.
    relogio.agora = 30.0
    elegibilidade = ServidorElegibilidade().iniciar()
    exames.url_elegibilidade = elegibilidade.url
    print("\n30 s depois, Elegibilidade de volta")
    status = exames.solicitar_exame("B-001", "HEMOGRAMA")[0]
    print(f"  pedido 6: {status}, chamada de teste liberada, disjuntor {disjuntor.estado}")
    print(f"  chamadas que chegaram a Elegibilidade: {elegibilidade.chamadas}")
    elegibilidade.parar()
