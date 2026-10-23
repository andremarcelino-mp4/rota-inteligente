# Rota Inteligente: Otimização de Entregas com Algoritmos de IA

Projeto da disciplina **Artificial Intelligence Fundamentals** (UniFECAF) — solução inteligente de roteamento para a empresa fictícia **Sabor Express**.

---

## 1. Problema, desafio e objetivos

### Contexto

A **Sabor Express** é uma pequena empresa de delivery de alimentos na região central da cidade. Nos horários de pico (almoço e jantar), as rotas dos entregadores eram definidas **manualmente**, apenas com base na experiência. Isso gerava:

- percursos longos e ineficientes;
- atrasos e insatisfação dos clientes;
- aumento de custo com combustível;
- falta de visão sistêmica da operação.

### Desafio

Tratar a cidade como um **grafo** e desenvolver uma solução baseada em algoritmos de Inteligência Artificial capaz de:

1. representar bairros (vértices), ruas (arestas) e distâncias/tempos (pesos);
2. **agrupar** pedidos em zonas para diferentes entregadores;
3. encontrar **caminhos de menor custo** entre pontos de entrega;
4. comparar a solução inteligente com uma rota “manual” de referência.

### Objetivos

- Aplicar **algoritmos de busca com heurística** (A\*) e busca clássica (BFS).
- Aplicar **aprendizado não supervisionado** (K-Means) para zonificação.
- Entregar código executável, dados, visualizações e documentação clara.
- Demonstrar impacto mensurável (redução de quilometragem total).

---

## 2. Abordagem adotada

A solução segue um pipeline em três camadas:

```text
Dados CSV → Grafo da cidade → K-Means (zonas)
                              ↓
                    Rota por zona (vizinho mais próximo)
                              ↓
                    Caminhos reais com A* no grafo
                              ↓
                    Comparativo vs. baseline manual + gráficos
```

### Passo a passo

1. **Modelagem:** carrega `bairros.csv`, `ruas.csv` e `entregas.csv` e monta um grafo não direcionado com NetworkX.
2. **Clustering:** posiciona cada pedido nas coordenadas (x, y) do bairro e aplica **K-Means** (`k=3`) — cada cluster = um entregador.
3. **Roteamento:** em cada zona, a ordem de visitas usa a heurística do **vizinho mais próximo**; o trajeto entre dois bairros é calculado com **A\***.
4. **Retorno ao hub:** toda rota começa e termina no **Centro**.
5. **Baseline:** simula a operação manual percorrendo os pedidos na ordem do CSV (um único percurso), para medir economia.
6. **Saídas:** imagens do grafo, clusters, rotas, comparativo e `resultado.json`.

---

## 3. Algoritmos utilizados

| Algoritmo | Tipo | Papel na solução |
|-----------|------|------------------|
| **K-Means** | Aprendizado não supervisionado | Agrupa entregas em zonas geográficas |
| **A\*** | Busca informada em grafo | Menor caminho entre bairros (peso = km) |
| **Vizinho mais próximo** | Heurística construtiva | Sequência de visitas dentro da zona |
| **BFS** | Busca cega | Referência didática (menos arestas, ignora peso) |

### Por que A\*?

A heurística euclidiana entre coordenadas dos bairros é **admissível** (nunca superestima o custo real nas ruas do mapa simplificado). Assim, o A\* encontra o caminho de **menor distância** no grafo, melhor que BFS quando as arestas têm pesos diferentes.

### Por que K-Means?

Espelha a prática de **territórios de entrega** (como em cases de logística e UPS ORION / clustering + otimização): em vez de um único entregador cruzar a cidade, cada um fica responsável por uma região coerente.

---

## 4. Diagrama do grafo / modelo

O diagrama é gerado automaticamente pelo código:

- `outputs/01_grafo_cidade.png` — vértices, arestas e pesos (km)
- `outputs/02_clusters_kmeans.png` — zonas K-Means + hub
- `outputs/03_rotas_otimizadas.png` — rotas por entregador
- `outputs/04_comparativo_distancia.png` — baseline vs. IA

**Hub (depósito):** bairro `Centro` (id `0`).

---

## 5. Estrutura do repositório

```text
rota-inteligente/
├── README.md
├── requirements.txt
├── data/
│   ├── bairros.csv      # vértices (id, nome, x, y, tipo)
│   ├── ruas.csv         # arestas (origem, destino, km, minutos)
│   └── entregas.csv     # pedidos do dia
├── src/
│   ├── main.py          # pipeline completo
│   ├── graph.py         # modelo do grafo
│   ├── pathfinding.py   # A*, BFS, vizinho mais próximo
│   ├── clustering.py    # K-Means
│   └── visualize.py     # gráficos
├── outputs/             # resultados gerados
└── docs/
    └── ROTEIRO_VIDEO.md # roteiro do pitch (≤4 min)
```

---

## 6. Como executar

### Pré-requisitos

- Python 3.10+ (testado com 3.12)
- pip

### Instalação

```bash
cd rota-inteligente
python3 -m pip install -r requirements.txt
```

### Execução

```bash
python3 -m src.main
```

Ao final, o terminal imprime o resumo das rotas e a economia percentual. Os arquivos em `outputs/` são atualizados.

### Principais saídas

| Arquivo | Conteúdo |
|---------|----------|
| `outputs/resultado.json` | Métricas e rotas detalhadas |
| `outputs/entregas_com_cluster.csv` | Pedidos com label de zona |
| `outputs/01_*.png` … `04_*.png` | Visualizações |

---

## 7. Análise dos resultados

Após executar o pipeline, consulte `outputs/resultado.json` para os números exatos da sua máquina. Em geral a solução apresenta:

- **Divisão territorial** estável em 3 zonas (ajustável via `n_clusters` em `src/main.py`).
- **Redução da distância total** frente ao baseline manual (um único entregador na ordem do CSV).
- Rotas **fechadas** (ida e volta ao hub), alinhadas à operação real de delivery.

### Interpretação

O ganho vem principalmente de dois efeitos combinados:

1. **paralelismo espacial** (vários entregadores em zonas distintas);
2. **ordem inteligente** + **caminhos de menor custo** (A\*) dentro de cada zona.

### Limitações

- Grafo **estático** (sem trânsito em tempo real nem bloqueios).
- Vizinho mais próximo **não garante ótimo global** (problema do caixeiro-viajante é NP-difícil).
- Não há janelas de horário, capacidade da bag, nem prioridade dura na função de custo (prioridade existe no CSV apenas como atributo de negócio).
- Coordenadas são **relativas/sintéticas**, para fins didáticos.

### Sugestões de melhoria

- Incorporar tempo de trânsito dinâmico nos pesos das arestas.
- Trocar a construção da rota por 2-opt, genéticos ou MILP em instâncias pequenas.
- Usar aprendizado por reforço para políticas de despacho online.
- Aumentar/diminuir `k` conforme tamanho da frota.
- Integrar mapa real (OSM) via `osmnx`.

---

## 8. Fontes e inspiração

- Case **UPS ORION** — otimização de rotas com heurísticas e dados operacionais.
- Discussões de **clustering + otimização** em logística (K-Means / DBSCAN + roteamento).
- Conteúdo da disciplina: busca com heurísticas, grafos e aprendizado não supervisionado.

---

## 9. Vídeo pitch

Roteiro completo (blocos por tempo, falas e checklist): [`docs/ROTEIRO_VIDEO.md`](docs/ROTEIRO_VIDEO.md).

---

## 10. Autor

Projeto acadêmico — UniFECAF / Artificial Intelligence Fundamentals.
