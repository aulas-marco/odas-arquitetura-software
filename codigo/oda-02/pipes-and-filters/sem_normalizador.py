"""Variante do fluxo de main.py sem o NormalizadorDeCampos.

Os filtros são os mesmos e nenhum arquivo de filtros/ foi alterado. A única
diferença é a montagem do pipeline, e ela basta para mudar o resultado:
o CalculadorDeScore compara habilidades em minúsculas, e quem as deixava em
minúsculas era o filtro retirado.
"""

from dominio import Vaga
from framework import Pipeline
from filtros.consumer import RelatorioDeTriagem
from filtros.producer import LeitorDeCurriculos
from filtros.testers import (
    FiltroPorExperienciaMinima,
    FiltroPorPretensaoSalarial,
    ValidadorDeCurriculo,
)
from filtros.transformers import CalculadorDeScore


def main() -> None:
    vaga = Vaga(
        titulo="Engenheiro(a) de Software Backend",
        anos_minimos=3,
        teto_salarial=18000,
        habilidades=("Python", "PostgreSQL", "Docker", "REST"),
    )
    relatorio = RelatorioDeTriagem()
    pipeline = (
        Pipeline()
        .adicionar(ValidadorDeCurriculo())
        .adicionar(FiltroPorExperienciaMinima(vaga))
        .adicionar(FiltroPorPretensaoSalarial(vaga))
        .adicionar(CalculadorDeScore(vaga))
        .adicionar(relatorio)
    )
    print(f"Pipeline: LeitorDeCurriculos → {str(pipeline)[9:-1]}\n")
    pipeline.executar(LeitorDeCurriculos().ler())
    relatorio.imprimir()


if __name__ == "__main__":
    main()
