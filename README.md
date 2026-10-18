# Corrida ao Gol 1000

Messi ou Cristiano Ronaldo: quem chega primeiro ao milésimo gol oficial, e quando? Este repositório simula a corrida
milhares de vezes, com o ritmo de gols de cada um pelo clube e os jogos reais do calendário.

**Página:** https://matheusgsd.github.io/messi-cr7-1000/

## O que os números mostram

Dados de 18/10/2026, na publicação, recorte padrão da página (ponderado ótimo, 10.000 simulações). A página se atualiza toda semana; estes números, não.

- **Placar:** CR7 tem 981 gols oficiais e precisa de mais 19. Messi tem 936 e precisa de 64.
- **CR7 chega primeiro em todas as 10.000 simulações.** O milésimo dele sai, na mediana, em abril de 2027 (80% das
  simulações entre fevereiro e maio de 2027), em cerca de 24 jogos do Al-Nassr.
- **Messi:** mediana em novembro de 2028 (80% entre agosto de 2028 e agosto de 2029), em cerca de 73 jogos do Inter
  Miami.
- **Messi marca mais por jogo** (0,87 contra 0,78 no recorte padrão), mas a vantagem de 45 gols do CR7 pesa mais. Só o
  recorte pós-Copa, de poucos jogos, dá alguma chance ao Messi: 7,8%.

## Como foi feito

Cada simulação sorteia um ritmo de gols por jogo para cada jogador (posteriori Gamma de um modelo Poisson, com priori
de Jeffreys) e depois os gols de cada jogo futuro do clube, em ordem, até chegar a 1000. O recorte padrão usa todos os
jogos de clube desde julho de 2019, com peso que cai pela metade a cada 365 dias; essa meia-vida foi a que melhor
previu, no passado, os gols dos 20 jogos seguintes. A página explica o resto e deixa trocar o recorte.

Premissas: os dois jogam todos os jogos do clube, sem lesão, aposentadoria ou queda por idade. Gols por seleção contam
no total, mas não entram na projeção. O calendário só tem jogos garantidos; depois da última data publicada, segue o
formato de cada liga. Os detalhes estão no cabeçalho de `tools/build_data.py`.

| Arquivo | O que faz |
| --- | --- |
| `index.html`, `app.js` | A página: placar, gráficos, replay de uma simulação |
| `sim.js` | Motor da simulação, com semente fixa (a mesma simulação sempre se repete igual) |
| `tools/build_data.py` | Monta `data/data.js` com o histórico e o calendário; `--baixar` busca o histórico de agora |
| `tools/servidor.py` | Serve a página com o histórico ao vivo do messivsronaldo.app (`/api/corrida`) |
| `tools/imagem_x.py` | Cartão 1600 × 900 para redes sociais e prévia de link (`imagem_x.png`), a partir de `tools/cartao.html` |
| `tools/build_artifact.py` | Versão da página para publicar como Artifact no claude.ai (`dist/index.html`) |

Dados em `data/sources/`: histórico jogo a jogo do messivsronaldo.app, calendário futuro (`fixtures.csv`, levantado em
10/10/2026 e revisto em 18/10/2026) e notas sobre o calendário de cada liga.

## Atualizar

```
python -I tools/build_data.py --baixar   # histórico de agora e data/data.js
python -I tools/imagem_x.py              # cartão
python -I tools/build_artifact.py        # opcional: versão Artifact
```

Uma GitHub Action (`.github/workflows/atualizar.yml`) roda esses três passos toda segunda de manhã e sobe o que mudou; dá para disparar à mão na aba Actions. O calendário futuro (`data/sources/fixtures.csv`) é editado à mão. Os jogos disputados saem sozinhos, mas jogos novos,
adiados ou de mata-mata precisam entrar no arquivo. No GitHub Pages a página usa o retrato de `data/data.js`; para ver
os dados de agora, rode `python -I tools/servidor.py`. O endereço do histórico no messivsronaldo.app é um JSON interno
do site, sem documentação, e pode mudar sem aviso.

Precisa de Python 3. O cartão precisa do Chrome ou do Edge.

## Fontes

- Gols jogo a jogo: [messivsronaldo.app](https://www.messivsronaldo.app/), a contagem da imprensa (Opta, AFP, AP/ESPN,
  EFE), conferida com o [Transfermarkt](https://www.transfermarkt.com/).
- Calendário: Transfermarkt, ESPN, Wikipedia e MLS. Cada jogo de `fixtures.csv` tem as fontes na própria linha.

## Licença

Código sob a licença MIT (`LICENSE`). Os dados montados aqui (`data/data.json`, `data/data.js` e
`data/sources/fixtures.csv`) ficam sob [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.pt-br): pode
reusar, citando Matheus Dalmolin e o messivsronaldo.app. Os arquivos `data/sources/mvr_*.json` são cópia do que o
messivsronaldo.app publica e seguem as condições do site.

A calculadora do gol 1000 para qualquer jogador, que começou aqui, virou outro projeto.
