"""Demonstração do professor: o que o armazenamento faz durante uma partição.

Três réplicas guardam a lista de alergias de um paciente. A partição separa as
réplicas A e B da réplica C. O programa compara três comportamentos: recusar a
escrita do lado sem quórum, aceitar dos dois lados e resolver por última escrita
vence, e aceitar dos dois lados e resolver por uma função de mesclagem do domínio.
Os carimbos de tempo são fixos para que a saída seja igual em cada execução.
"""


class Replica:
    def __init__(self, nome):
        self.nome = nome
        self.alergias = ["látex"]
        self.carimbo = 0  # carimbo de tempo da última escrita aceita


def escrever(lado, total_replicas, alergias, carimbo, exigir_quorum):
    if exigir_quorum and len(lado) <= total_replicas // 2:
        nomes = "+".join(r.nome for r in lado)
        return f"recusada em {nomes}: {len(lado)} de {total_replicas} réplicas, sem quórum"
    for replica in lado:
        replica.alergias = list(alergias)
        replica.carimbo = carimbo
    return f"aceita em {'+'.join(r.nome for r in lado)}"


def ultima_escrita_vence(replicas):
    vencedora = max(replicas, key=lambda r: r.carimbo)
    return vencedora.alergias


def mesclar_alergias(replicas):
    # Regra do domínio: nenhuma alergia registrada em qualquer unidade é descartada.
    return sorted({a for r in replicas for a in r.alergias})


def cenario(titulo, exigir_quorum, resolver=None):
    a, b, c = Replica("A"), Replica("B"), Replica("C")
    maioria, minoria = [a, b], [c]
    print(f"== {titulo}")
    # Durante a partição, a unidade Centro escreve na maioria e a unidade Barreiro na minoria.
    print("Centro grava dipirona:", escrever(maioria, 3, ["látex", "dipirona"], 10, exigir_quorum))
    print("Barreiro grava penicilina:", escrever(minoria, 3, ["látex", "penicilina"], 11, exigir_quorum))
    print(f"Durante a partição: A={a.alergias} C={c.alergias}")
    if resolver is not None:
        final = resolver([a, b, c])
        print(f"Depois da partição: {final}")
    print()


if __name__ == "__main__":
    # 1. Preservar a visão única: o lado sem quórum recusa a escrita.
    cenario("1. Recusar sem quórum", exigir_quorum=True)

    # 2. Continuar respondendo e resolver pelo carimbo mais recente: a dipirona some.
    cenario("2. Aceitar e aplicar última escrita vence", exigir_quorum=False, resolver=ultima_escrita_vence)

    # 3. Continuar respondendo e resolver pela regra do domínio: as duas alergias ficam.
    cenario("3. Aceitar e mesclar pela regra do domínio", exigir_quorum=False, resolver=mesclar_alergias)
