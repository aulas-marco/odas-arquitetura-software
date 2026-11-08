"""Verificador de fronteiras: procura imports que entram no interior de outro módulo.

Regra: um módulo só pode importar de outro módulo pelo arquivo api.py dele.
Qualquer import de "<outro_modulo>.interno" é violação. Ferramentas como
import-linter (Python), ArchUnit (Java) e Packwerk (Ruby) aplicam a mesma
ideia na integração contínua.
"""

import ast
import sys
from pathlib import Path

RAIZ = Path(__file__).parent
MODULOS = ("agenda", "faturamento")


def violacoes() -> list[str]:
    encontradas = []
    for modulo in MODULOS:
        for arquivo in sorted((RAIZ / modulo).rglob("*.py")):
            arvore = ast.parse(arquivo.read_text(encoding="utf-8"))
            for no in ast.walk(arvore):
                if isinstance(no, ast.ImportFrom) and no.module:
                    nomes = [no.module]
                elif isinstance(no, ast.Import):
                    nomes = [a.name for a in no.names]
                else:
                    continue
                for nome in nomes:
                    destino = nome.split(".")[0]
                    if destino != modulo and destino in MODULOS and ".interno" in nome:
                        caminho = arquivo.relative_to(RAIZ).as_posix()
                        encontradas.append(f"{caminho}:{no.lineno} importa {nome}")
    return encontradas


def main() -> int:
    encontradas = violacoes()
    if not encontradas:
        print("Fronteiras respeitadas: nenhum módulo importa o interior de outro.")
        return 0
    print(f"{len(encontradas)} violação(ões) de fronteira:")
    for v in encontradas:
        print(f"  {v}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
