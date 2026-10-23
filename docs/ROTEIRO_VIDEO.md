# Roteiro — Vídeo Pitch (até 4 minutos)

**Título sugerido no YouTube:**  
`Rota Inteligente: Otimização de Entregas com IA | Artificial Intelligence Fundamentals`

**Formato:** tela compartilhada (código + gráficos) + narração  
**Duração alvo:** 3 min 30 s – 3 min 50 s  
**Privacidade:** Não listado

---

## Antes de gravar (checklist)

- [ ] Rodar `python3 -m src.main` e deixar abertas as imagens em `outputs/`
- [ ] Abrir `README.md` e `resultado.json`
- [ ] Fechar abas/notificações; áudio do microfone ok
- [ ] Falar em ritmo calmo; olhar para os gráficos ao citar números

---

## Bloco 1 — Abertura e problema (0:00 – 0:40)

**Na tela:** capa mental / README com o título do projeto.

**Fala:**

> Olá! Meu nome é André e este é o pitch do projeto **Rota Inteligente: Otimização de Entregas com Algoritmos de IA**, da disciplina Artificial Intelligence Fundamentals.
>
> O cenário é a **Sabor Express**, uma empresa de delivery na região central. Nos horários de pico, as rotas eram definidas **manualmente**, só com a experiência dos entregadores. Isso gerava caminhos longos, atraso, mais combustível e cliente insatisfeito.
>
> Minha missão foi criar uma solução baseada em IA para sugerir **melhores rotas**, tratando a cidade como um **grafo**.

---

## Bloco 2 — Modelagem (0:40 – 1:20)

**Na tela:** `outputs/01_grafo_cidade.png` e trecho de `data/bairros.csv` / `ruas.csv`.

**Fala:**

> Modelei a cidade como um grafo: **vértices** são bairros ou pontos de entrega, **arestas** são as ruas, e o **peso** é a distância em quilômetros — também temos tempo estimado.
>
> O **Centro** é o hub, de onde saem e para onde voltam os entregadores. Os dados estão em CSV: bairros com coordenadas, ruas com pesos e a lista de pedidos do dia.
>
> Com isso, qualquer deslocamento entre dois pontos pode ser calculado com algoritmos de busca em grafo.

---

## Bloco 3 — Abordagem de IA (1:20 – 2:20)

**Na tela:** `outputs/02_clusters_kmeans.png`, depois código de `clustering.py` / `pathfinding.py` (rápido).

**Fala:**

> A solução tem **duas etapas de IA clássica**.
>
> Primeiro, uso **K-Means**, aprendizado não supervisionado, para **agrupar as entregas em zonas**. Cada cluster vira a carteira de um entregador. Assim evitamos que uma única pessoa atravesse a cidade inteira.
>
> Depois, **dentro de cada zona**, monto a sequência de visitas com a heurística do **vizinho mais próximo**. Entre um bairro e o próximo, o caminho real no mapa é encontrado com **A\***, usando heurística euclidiana — admissível, então o A\* encontra o menor caminho em custo.
>
> Também implementei **BFS** como referência didática, para contrastar busca por número de saltos versus busca com pesos.

---

## Bloco 4 — Resultados (2:20 – 3:20)

**Na tela:** `03_rotas_otimizadas.png` → `04_comparativo_distancia.png` → `resultado.json`.

**Fala (ajuste os números se o `resultado.json` mudar):**

> Rodando o pipeline, o sistema divide **25 pedidos** entre **três entregadores** e gera a rota de cada um, saindo e voltando ao Centro.
>
> Comparando com uma rota **manual** — seguir a ordem do arquivo de pedidos — a solução com IA reduz a distância total. No experimento: baseline **70,0 km** versus solução IA **48,3 km**, uma economia de **31%**.
>
> Exemplos rápidos: o entregador 0 faz Centro → Liberdade → Santa Clara → Estação → Centro (14,1 km); o 1 cobre a zona norte/oeste (16,1 km); o 2 a zona sul/industrial (18,1 km).
>
> Os gráficos mostram as zonas do K-Means, as rotas no grafo e o comparativo de distância. Tudo isso fica versionado no repositório GitHub, com instruções no README.

---

## Bloco 5 — Limitações, melhorias e fechamento (3:20 – 3:50)

**Na tela:** README (seção limitações) ou estrutura de pastas.

**Fala:**

> Entre as limitações: o grafo é estático, sem trânsito em tempo real; o vizinho mais próximo é uma heurística e não garante o ótimo global do caixeiro-viajante; e não modelei janelas de horário dos clientes.
>
> Como evolução, daria para integrar trânsito ao peso das arestas, testar algoritmos genéticos ou reinforcement learning, e usar mais clusters conforme a frota.
>
> Em resumo: **grafo + K-Means + A\*** transformam a operação manual da Sabor Express em rotas mais curtas e organizadas por zona.
>
> Obrigado! Link do repositório na descrição do vídeo.

---

## Texto curto para a descrição do YouTube

```text
Projeto da disciplina Artificial Intelligence Fundamentals (UniFECAF).

Rota Inteligente: otimização de entregas da Sabor Express com:
- Grafo da cidade (bairros e ruas)
- K-Means para zonas de entregadores
- A* + vizinho mais próximo para rotas

Repositório GitHub: <COLE_O_LINK_AQUI>
```

---

## Dicas de edição (opcional)

- Cortar silêncios longos (>1,5 s)
- Zoom leve nos gráficos ao citar economia %
- Não precisa aparecer no vídeo; voz + tela basta
- Se passar de 4:00, corte detalhes do BFS ou da lista de CSVs
