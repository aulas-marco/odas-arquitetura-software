"""Confere se o ambiente do Módulo 0 está pronto para as ODAs.

Execute a partir da raiz do repositório clonado:
    Windows:          py codigo/modulo-0/verificar_ambiente.py
    macOS e Linux:    python3 codigo/modulo-0/verificar_ambiente.py
"""

import shutil
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]


def conferir() -> list[tuple[bool, str]]:
    versao = sys.version_info
    return [
        (versao >= (3, 10), f"Python {versao.major}.{versao.minor}.{versao.micro} (mínimo 3.10)"),
        (shutil.which("git") is not None, "Git encontrado no PATH"),
        ((RAIZ / "codigo" / "oda-01").is_dir() and (RAIZ / "codigo" / "oda-02").is_dir(),
         "Repositório clonado, com as pastas codigo/oda-01 e codigo/oda-02"),
    ]


def main() -> int:
    resultados = conferir()
    for ok, descricao in resultados:
        print(f"  [{'OK' if ok else 'FALTA'}] {descricao}")
    if shutil.which("code") is None:
        print("  [AVISO] Comando 'code' não encontrado. O VS Code pode estar instalado sem o atalho de terminal.")
    if all(ok for ok, _ in resultados):
        print("\nAmbiente pronto.")
        return 0
    print("\nAmbiente incompleto: revise os itens marcados com FALTA no Módulo 0.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
