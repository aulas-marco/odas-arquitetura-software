"""Variante de main.py sem o filtro NormalizadorDeCampos.

Os arquivos de filtros/ são os mesmos usados por main.py, e a diferença está
somente na montagem do pipeline. O CalculadorDeScore compara habilidades em
letras minúsculas, e o filtro retirado era o responsável por convertê-las.
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
