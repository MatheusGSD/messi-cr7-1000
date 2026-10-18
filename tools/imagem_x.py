"""Cartão 1600 x 900 para o X e prévia de link (imagem_x.png, na raiz, para o GitHub Pages servir).

Fotografa tools/cartao.html com o Chrome (ou o Edge) sem janela. O cartão roda a mesma simulação da página, com o
retrato de data/data.js, então rode depois do build_data.py.

Uso:  python -I tools/imagem_x.py
"""
import os
import subprocess
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'imagem_x.png')
BROWSERS = [
    r'C:\Program Files\Google\Chrome\Application\chrome.exe',
    r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
    '/usr/bin/google-chrome', '/usr/bin/chromium',
]

exe = next(b for b in BROWSERS if os.path.exists(b))
page = 'file:///' + os.path.join(ROOT, 'tools', 'cartao.html').replace('\\', '/')
with tempfile.TemporaryDirectory() as profile:  # perfil limpo: não mexe no Chrome aberto do usuário
    args = [exe, '--headless=new', '--disable-gpu', '--hide-scrollbars', f'--user-data-dir={profile}',
            '--window-size=1600,900', '--virtual-time-budget=15000', f'--screenshot={OUT}', page]
    if os.name != 'nt':
        args.insert(1, '--no-sandbox')  # o Ubuntu do GitHub Actions bloqueia o sandbox do Chrome
    subprocess.run(args, check=True, capture_output=True)
print(OUT)
