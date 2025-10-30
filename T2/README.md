# O Código Confuso (Morse) — Contagem de Decodificações

Programa em **Python** que conta quantas mensagens diferentes uma string em **Código Morse** pode representar.

- **Quebras obrigatórias**: qualquer espaço (`' '`, tab, quebras de linha) **separa segmentos**; não é permitido atravessar espaços.
- **Sem espaços**: pontos e traços “grudados” podem formar **várias letras** (ex.: `".-"` → `"A"` ou `"E T"`).
- **Tabelas configuráveis**: escolha o alfabeto Morse (A–Z; A–Z+Ç; A–Z+0–9; FULL com acentuadas/CH).

---

## Sumário

- [O Código Confuso (Morse) — Contagem de Decodificações](#o-código-confuso-morse--contagem-de-decodificações)
  - [Sumário](#sumário)
  - [Visão geral](#visão-geral)
  - [Instalação e requisitos](#instalação-e-requisitos)
  - [Uso rápido](#uso-rápido)
    - [Passando a mensagem como argumento](#passando-a-mensagem-como-argumento)
    - [Lendo do `stdin`](#lendo-do-stdin)
  - [Opções de linha de comando](#opções-de-linha-de-comando)
  - [Exemplos](#exemplos)
    - [1) Modo padrão (A–Z+Ç)](#1-modo-padrão-azç)
    - [2) Modo FULL (inclui dígitos e acentuadas)](#2-modo-full-inclui-dígitos-e-acentuadas)
    - [3) Vários segmentos](#3-vários-segmentos)
  - [Saída e modo verboso](#saída-e-modo-verboso)
  - [Algoritmo](#algoritmo)
    - [Ideia](#ideia)
    - [DP por segmento](#dp-por-segmento)
    - [Por que trie?](#por-que-trie)
  - [Complexidade](#complexidade)
  - [Casos de borda](#casos-de-borda)
  - [Testes rápidos](#testes-rápidos)
  - [Benchmark simples](#benchmark-simples)
  - [Estrutura do projeto](#estrutura-do-projeto)

---

## Visão geral

Dada uma mensagem em Morse contendo `.` e `-`, possivelmente com **espaços** entre trechos, o programa:

1. **Divide** a entrada em **segmentos** usando espaços (regex `\s+`).
2. Para cada segmento, **conta** o número de **decomposições válidas** em códigos Morse de letras/dígitos (dependendo do modo).
3. O **total da mensagem** é o **produto** das contagens por segmento.

Ex.:  
Segmento `".."` → 2 maneiras (`"I"` ou `"E E"`).  
Mensagem `"..  --"` → `2 × (#maneiras de "--")`.

---

## Instalação e requisitos

- **Python 3.8+**
- Nenhuma dependência externa.

Clone ou copie o arquivo `morse_count.py` para o seu diretório de trabalho.

---

## Uso rápido

### Passando a mensagem como argumento
```bash
python morse_count.py "..-  --..-.-.-...  --  -  --...-"
```

### Lendo do `stdin`
```bash
echo "..-  --..-.-.-...  --  -  --...-" | python morse_count.py
```

O programa imprime **apenas o total** (ideal para correção automática).  
Use `--verbose` para detalhes por segmento.

---

## Opções de linha de comando

```text
--mode=AZ|AZ_CEDILLA|AZ_DIGITS|FULL   (padrão: AZ_CEDILLA)
--verbose                             (debug por segmento)
```

**Tabelas:**
- `AZ` → A..Z  
- `AZ_CEDILLA` → A..Z + **Ç** (padrão)  
- `AZ_DIGITS` → A..Z + 0..9  
- `FULL` → A..Z + 0..9 + acentuadas comuns (**Ç, Ä/Æ/Ą, Á/Å, É, È, Ñ, Ö, Ü**) e **CH**

> Observação: a escolha da tabela **altera** o total (mais símbolos → mais decodificações possíveis).

---

## Exemplos

### 1) Modo padrão (A–Z+Ç)
```bash
python morse_count.py ".."
# saída: 2
```

### 2) Modo FULL (inclui dígitos e acentuadas)
```bash
python morse_count.py --mode=FULL "----"
# "----" pode ser "CH" (letra composta) ou combinações de T/M etc.
```

### 3) Vários segmentos
```bash
python morse_count.py ".- ..  ---"
# produto das maneiras por segmento ".-", ".." e "---"
```

---

## Saída e modo verboso

- **Padrão**: imprime **um inteiro** (total de decodificações).
- **Com `--verbose`**: além do total, imprime `"segmento -> #maneiras"` para cada trecho.

Ex.:
```bash
python morse_count.py --verbose "..  --"
#  <total>
#  segmento:                 .. |          2
#  segmento:                 -- |          X
```

---

## Algoritmo

### Ideia
- Cada **segmento** (sem espaços) é um **caminho** de `.` e `-` que pode ser “particionado” em múltiplos códigos de letras.
- Usamos **Programação Dinâmica (DP)** para contar as decomposições e uma **trie** para testar **prefixos** de forma eficiente.

### DP por segmento
- `dp[i]` = nº de maneiras de decompor o **prefixo** `segmento[:i]`.
- Base: `dp[0] = 1`.
- Para cada `i` com `dp[i] > 0`, caminhamos na **trie** seguindo `segmento[i], segmento[i+1], ...`.  
  Sempre que alcançamos um nó **final** (fim de algum código), digamos `j`, fazemos:
  ```
  dp[j] += dp[i]
  ```
- No fim, `dp[n]` (n = len(segmento)) é o total de decomposições do segmento.

### Por que trie?
- Cada passo é só seguir ponteiros `.`/`-`, parando assim que o caminho não existe — rápido e local.
- O maior comprimento de um código Morse (letras/dígitos) é pequeno (≤ 5; `CH` tem 4), então o custo é **linear** no tamanho do segmento.

---

## Complexidade

Seja `n` o comprimento do segmento e `L` o comprimento máximo de um código Morse (pequeno e constante):

- **Tempo por segmento**: `O(n · L)` → na prática **O(n)`
- **Memória por segmento**: `O(n)` para a tabela `dp`
- **Trie**: tamanho **constante** para um alfabeto fixo (A–Z, etc.)
- **Mensagem completa**: produto das contagens por segmento (cada um independente)

---

## Casos de borda

- **Espaços múltiplos** / tabs / quebras de linha: contam como **uma** quebra obrigatória (`\s+`).
- **Segmentos vazios** (após split/trim): ignorados.
- **Caracteres inválidos** (além de `.` e `-`): não há match na trie → contagem do segmento vira `0` → total `0`.
- **Números grandes**: Python usa inteiros arbitrários; se necessário, veja `--mod` em [Extensões](#extensões-úteis).

---

## Testes rápidos

Crie um arquivo `tests/test_morse.py` (opcional) e rode com `pytest`:

```python
# tests/test_morse.py
import subprocess, sys, shlex

def run(msg, mode=None):
    cmd = f'{sys.executable} morse_count.py ' + (f'--mode={mode} ' if mode else '') + f'"{msg}"'
    out = subprocess.check_output(shlex.split(cmd), text=True).strip()
    return int(out)

def test_dotdot_default():
    assert run("..") == 2  # "I" ou "E E"

def test_dashdash_full():
    # sanity check; depende da tabela
    assert run("--", "FULL") >= 1

def test_spaces_are_breaks():
    x = run(".-  .-")  # duas letras "A" separadas por espaço
    assert x >= 1
```

Rodar:
```bash
pytest -q
```

---

## Benchmark simples

```bash
python - << 'PY'
from time import perf_counter
import subprocess, sys, shlex

msg = ".-" * 2000  # 4000 símbolos
cmd = f'{sys.executable} morse_count.py "{msg}"'
t0 = perf_counter()
out = subprocess.check_output(shlex.split(cmd), text=True)
t1 = perf_counter()
print("total:", out.strip(), "tempo(s):", round(t1-t0, 3))
PY
```

> Dica: para mensagens muito longas, o tempo cresce ~linearmente no tamanho do segmento (L é pequeno).

---

## Estrutura do projeto

```
.
├── morse_count.py      # script principal (CLI)
├── README.md           # este arquivo
└── tests/
    └── test_morse.py   # (opcional) testes unitários
```

---