"""Portões de qualidade do catálogo, das ODAs e do código executável."""

from pathlib import Path
import subprocess
import sys
import unittest

import yaml

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))

from hooks.catalogo import carregar_catalogo, validar_catalogo  # noqa: E402
from scripts.gerar_odas import ABAS, validar_oda  # noqa: E402

CATALOGO = carregar_catalogo(RAIZ / "catalogo" / "odas.yml")


def odas():
    for arquivo in sorted((RAIZ / "odas").glob("*/oda.yml")):
        yield arquivo, yaml.safe_load(arquivo.read_text(encoding="utf-8"))


class TestCatalogo(unittest.TestCase):
    def test_catalogo_valido(self):
        self.assertEqual(validar_catalogo(CATALOGO, RAIZ), [])

    def test_cada_oda_tem_25_minutos(self):
        self.assertTrue(all(o["minutos"] == 25 for o in CATALOGO["odas"]))


class TestOdas(unittest.TestCase):
    def test_odas_validas(self):
        for arquivo, dados in odas():
            with self.subTest(oda=arquivo.parent.name):
                self.assertEqual(validar_oda(dados, CATALOGO), [])

    def test_quatro_abas(self):
        self.assertEqual(ABAS, ("objetivo", "conceitos", "laboratorio", "verificacao"))

    def test_toda_aba_cita_o_material_oficial(self):
        for arquivo, dados in odas():
            for aba in dados["abas"]:
                with self.subTest(oda=arquivo.parent.name, aba=aba["id"]):
                    urls = [l["url"] for b in aba["blocos"] if b.get("titulo") == "📚 No material oficial" for l in b["links"]]
                    self.assertTrue(urls)
                    self.assertTrue(all(u.startswith("https://marco-mendes.github.io/arquitetura-software/") for u in urls))

    def test_trechos_de_arquivo_correspondem_ao_codigo(self):
        for arquivo, dados in odas():
            for aba in dados["abas"]:
                for b in aba["blocos"]:
                    if b.get("tipo") == "editor" and b.get("rotulo") == "arquivo":
                        with self.subTest(caminho=b["caminho"]):
                            codigo = (RAIZ / b["caminho"]).read_text(encoding="utf-8").splitlines()
                            inicio = b.get("inicio", 1)
                            self.assertEqual(codigo[inicio - 1:inicio - 1 + len(b["linhas"])], b["linhas"])


class TestCodigo(unittest.TestCase):
    """As saídas marcadas como executadas nas ODAs precisam ser as saídas reais dos programas."""

    def executar(self, pasta: str, script: str) -> str:
        r = subprocess.run([sys.executable, "-B", script], cwd=RAIZ / pasta, capture_output=True, text=True)
        return r.stdout.rstrip("\n")

    def test_saidas_dos_terminais_simulados(self):
        for arquivo, dados in odas():
            for aba in dados["abas"]:
                for b in aba["blocos"]:
                    if b.get("tipo") != "terminal":
                        continue
                    pasta = b["titulo"].split("pasta ")[1]
                    for c in b["comandos"]:
                        script = c["entrada"].split()[-1]
                        with self.subTest(pasta=pasta, script=script):
                            self.assertEqual(self.executar(pasta, script), c["saida"])

    def test_verificador_de_ambiente(self):
        r = subprocess.run([sys.executable, "-B", "codigo/modulo-0/verificar_ambiente.py"], cwd=RAIZ, capture_output=True, text=True)
        self.assertIn("[OK] Repositório clonado", r.stdout)


if __name__ == "__main__":
    unittest.main()
