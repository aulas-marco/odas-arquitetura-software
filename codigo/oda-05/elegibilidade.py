"""Serviço de Elegibilidade: decide se um beneficiário pode usar o plano.

Roda como servidor HTTP de verdade numa porta livre do computador. O banco é o
dicionário _BANCO, que só este módulo lê. O atributo modo simula três situações
da dependência: normal, lenta e instável.
"""

import json
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

_BANCO = {  # dados sintéticos, acessíveis só a este serviço
    "B-001": {"beneficiario_id": "B-001", "elegivel": True},
    "B-002": {"beneficiario_id": "B-002", "elegivel": False},
}


class ServidorElegibilidade:
    def __init__(self):
        self.modo = "normal"       # normal, lenta ou instavel
        self.atraso = 1.0          # segundos de espera no modo lenta
        self.falhas_restantes = 0  # respostas 503 que ainda serão dadas no modo instavel
        self.chamadas = 0          # requisições que chegaram pela rede
        self._http = None

    @property
    def url(self):
        host, porta = self._http.server_address
        return f"http://{host}:{porta}"

    def iniciar(self):
        servidor = self

        class Tratador(BaseHTTPRequestHandler):
            def do_GET(self):
                servidor.chamadas += 1
                status, corpo = servidor.responder(self.path)
                dados = json.dumps(corpo).encode()
                self.send_response(status)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(dados)))
                self.end_headers()
                self.wfile.write(dados)

            def log_message(self, *args):  # silencia o log de acesso no terminal
                pass

        self._http = ThreadingHTTPServer(("127.0.0.1", 0), Tratador)
        self._http.daemon_threads = True
        threading.Thread(target=self._http.serve_forever, daemon=True).start()
        return self

    def parar(self):
        self._http.shutdown()
        self._http.server_close()

    def responder(self, caminho):
        if self.modo == "lenta":
            time.sleep(self.atraso)
        if self.modo == "instavel" and self.falhas_restantes > 0:
            self.falhas_restantes -= 1
            return 503, {"codigo": "sobrecarga_temporaria"}
        beneficiario_id = caminho.rsplit("/", 1)[-1]
        registro = _BANCO.get(beneficiario_id)
        if registro is None:
            return 404, {"codigo": "beneficiario_nao_encontrado"}
        return 200, registro
