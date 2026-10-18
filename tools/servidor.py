"""Serve a corrida Messi × CR7 (index.html) com o histórico de agora do messivsronaldo.app.

Por que um servidor: o messivsronaldo.app não libera CORS, então o navegador não pode ler o histórico direto de lá.

  /api/corrida  -> messivsronaldo.app, jogo a jogo dos dois, passado pelo build() de tools/build_data.py
                   com a data de hoje; é o mesmo formato de data/data.js

O endereço do messivsronaldo.app não é documentado: pode mudar ou ser bloqueado sem aviso.

Uso:  python -I tools/servidor.py      (abre http://localhost:8765/)
"""
import datetime
import importlib.util
import http.server
import json
import os
import socketserver
import threading
import time
import urllib.parse
import urllib.request
import webbrowser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# python -I não põe a pasta do script no sys.path, então o build_data é carregado pelo caminho
_spec = importlib.util.spec_from_file_location('build_data', os.path.join(ROOT, 'tools', 'build_data.py'))
build_data = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(build_data)
CORRIDA_TTL = 120
PORT = 8765
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) gol1000'
cache = {}
lock = threading.Lock()


def fetch(url, ttl, timeout):
    with lock:
        hit = cache.get(url)
        if hit and time.time() - hit[0] < ttl:
            return hit[1]
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    for attempt in range(3):  # uma ou outra conexão cai; tenta de novo antes de desistir
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                body = r.read()
            break
        except Exception:
            if attempt == 2:
                raise
            time.sleep(0.8 * (attempt + 1))
    with lock:
        cache[url] = (time.time(), body)
    return body



def corrida():
    """Dados da corrida com o histórico de agora; guardados por CORRIDA_TTL segundos."""
    with lock:
        hit = cache.get('corrida')
        if hit and time.time() - hit[0] < CORRIDA_TTL:
            return hit[1]
    raws = {p: json.loads(fetch(build_data.MVR_URL.format(slug), CORRIDA_TTL, 40)) for p, slug in build_data.MVR_SLUG.items()}
    data = build_data.build(raws, datetime.date.today().isoformat())
    data['aoVivo'] = {'fonte': 'messivsronaldo.app', 'consultadoEm': datetime.datetime.now().astimezone().isoformat(timespec='seconds')}
    body = json.dumps(data, ensure_ascii=False, separators=(',', ':')).encode()
    with lock:
        cache['corrida'] = (time.time(), body)
    return body


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=ROOT, **kw)

    def do_GET(self):
        u = urllib.parse.urlparse(self.path)
        parts = u.path.strip('/').split('/')
        if parts[0] != 'api':
            return super().do_GET()
        if parts[1:] != ['corrida']:
            return self.send_error(404)
        self.reply(corrida)

    def reply(self, get):
        try:
            body, status = get(), 200
        except Exception as e:  # a página cai no retrato de data/data.js
            body, status = json.dumps({'erro': str(e)}).encode(), 502
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        if '/api/' in str(args[0] if args else ''):
            print(time.strftime('%H:%M:%S'), fmt % args, flush=True)


class Server(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True


if __name__ == '__main__':
    url = f'http://localhost:{PORT}/'
    with Server(('127.0.0.1', PORT), Handler) as srv:
        print('No ar:', url, '(Ctrl+C para parar)', flush=True)
        if os.environ.get('SEM_NAVEGADOR') != '1':
            threading.Timer(0.6, lambda: webbrowser.open(url)).start()
        srv.serve_forever()
