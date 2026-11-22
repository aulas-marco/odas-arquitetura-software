"""Políticas para a chamada síncrona: nova tentativa e disjuntor (circuit breaker).

As duas recebem a chamada como função e não conhecem o domínio. O relógio e a
espera são injetados para que a demonstração seja igual em cada execução.
"""


def com_novas_tentativas(tentativas, espera_inicial, dormir, relatar=print):
    def politica(chamada):
        espera = espera_inicial
        for numero in range(1, tentativas + 1):
            try:
                resultado = chamada()
                relatar(f"  tentativa {numero}: respondeu {resultado[0]}")
                return resultado
            except ConnectionError as erro:
                relatar(f"  tentativa {numero}: falhou ({erro})")
                if numero == tentativas:
                    raise
                dormir(espera)
                espera *= 2  # espera exponencial: 0,1 s, depois 0,2 s, depois 0,4 s
    return politica


class Disjuntor:
    def __init__(self, limite_falhas, tempo_aberto, relogio):
        self.limite_falhas = limite_falhas
        self.tempo_aberto = tempo_aberto
        self.relogio = relogio
        self.estado = "fechado"
        self.falhas = 0
        self.aberto_em = None

    def __call__(self, chamada):
        if self.estado == "aberto":
            if self.relogio() - self.aberto_em < self.tempo_aberto:
                raise ConnectionError("disjuntor aberto, chamada recusada sem usar a rede")
            self.estado = "meio_aberto"  # o prazo passou: uma chamada de teste é liberada
        try:
            resultado = chamada()
        except ConnectionError:
            self.falhas += 1
            if self.estado == "meio_aberto" or self.falhas >= self.limite_falhas:
                self.estado, self.aberto_em = "aberto", self.relogio()
            raise
        self.estado, self.falhas = "fechado", 0
        return resultado
