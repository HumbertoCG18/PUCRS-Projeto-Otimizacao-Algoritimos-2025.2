import sys as sys_
import re as re_
from typing import Dict as Dict_, List as List_, Tuple as Tuple_

# -----------------------------
# Tabelas Morse (International Morse)
# -----------------------------
AZ_ = {
    'A': '.-',   'B': '-...', 'C': '-.-.', 'D': '-..',  'E': '.',    'F': '..-.',
    'G': '--.',  'H': '....', 'I': '..',   'J': '.---', 'K': '-.-',  'L': '.-..',
    'M': '--',   'N': '-.',   'O': '---',  'P': '.--.', 'Q': '--.-', 'R': '.-.',
    'S': '...',  'T': '-',    'U': '..-',  'V': '...-', 'W': '.--',  'X': '-..-',
    'Y': '-.--', 'Z': '--..',
}

DIGITS_ = {
    '1': '.----','2': '..---','3': '...--','4': '....-','5': '.....',
    '6': '-....','7': '--...','8': '---..','9': '----.','0': '-----',
}

# Extensões usuais para letras acentuadas
ACCENTS_ = {
    'Ç': '-.-..',              # pt-BR
    'Ä': '.-.-', 'Æ': '.-.-', 'Ą': '.-.-',
    'Á': '.--.-','Å': '.--.-',
    'É': '..-..',
    'È': '.-..-',
    'Ñ': '--.--',
    'Ö': '---.',
    'Ü': '..--',
    'CH': '----',              # letra composta (tradicional em alguns alfabetos)
}

def build_table_(mode_: str='AZ_CEDILLA') -> Dict_[str,str]:
    """
    mode_:
      - 'AZ'            : apenas A..Z
      - 'AZ_CEDILLA'    : A..Z + Ç  (padrão)
      - 'AZ_DIGITS'     : A..Z + 0..9
      - 'FULL'          : A..Z + 0..9 + acentuadas (inclui Ç, Ä, Á, É, Ö, Ü, Ñ, È, CH)
    """
    table_ = dict(AZ_)
    if mode_ == 'AZ':
        return table_
    if mode_ == 'AZ_CEDILLA':
        table_.update({'Ç': ACCENTS_['Ç']})
        return table_
    if mode_ == 'AZ_DIGITS':
        table_.update(DIGITS_)
        return table_
    if mode_ == 'FULL':
        table_.update(DIGITS_)
        table_.update(ACCENTS_)
        return table_
    raise ValueError(f"Modo de tabela desconhecido: {mode_}")

# -----------------------------
# Trie para matching eficiente
# -----------------------------
class _TrieNode:
    __slots__ = ('children_', 'end_')
    def __init__(self) -> None:
        self.children_: Dict_[str, _TrieNode] = {}
        self.end_: bool = False

def build_trie_(codes_: List_[str]) -> _TrieNode:
    root_ = _TrieNode()
    for code_ in codes_:
        node_ = root_
        for ch_ in code_:
            node_ = node_.children_.setdefault(ch_, _TrieNode())
        node_.end_ = True
    return root_

# -----------------------------
# DP por segmento (sem espaços)
# -----------------------------
def count_decodings_segment_(segment_: str, trie_root_: _TrieNode) -> int:
    n_ = len(segment_)
    dp_: List_[int] = [0]*(n_+1)
    dp_[0] = 1
    for i_ in range(n_):
        if dp_[i_] == 0:
            continue
        node_ = trie_root_
        j_ = i_
        while j_ < n_ and segment_[j_] in node_.children_:
            node_ = node_.children_[segment_[j_]]
            j_ += 1
            if node_.end_:
                dp_[j_] += dp_[i_]
    return dp_[n_]

def count_total_(message_: str, table_mode_: str='AZ_CEDILLA', verbose_: bool=False) -> Tuple_[int, List_[Tuple_[str,int]]]:
    # qualquer quantidade de espaço = uma quebra obrigatória
    segments_: List_[str] = [s for s in re_.split(r'\s+', message_.strip()) if s != '']
    table_ = build_table_(table_mode_)
    trie_ = build_trie_(list(set(table_.values())))
    per_seg_: List_[Tuple_[str,int]] = []
    total_: int = 1
    for seg_ in segments_:
        ways_ = count_decodings_segment_(seg_, trie_)
        per_seg_.append((seg_, ways_))
        total_ *= ways_
        if verbose_:
            print(f"[debug] segmento='{seg_}' -> {ways_} maneiras")
    return total_, per_seg_

# -----------------------------
# CLI
# -----------------------------
USAGE_ = f"""Uso:
  python morse_count.py "<mensagem_em_morse>"
  echo "<mensagem_em_morse>" | python morse_count.py
Opções:
  --mode=AZ|AZ_CEDILLA|AZ_DIGITS|FULL    (padrão: AZ_CEDILLA)
  --verbose
Exemplos:
  python morse_count.py "..-  --..-.-.-...  --  -  --...-"
  python morse_count.py --mode=FULL "..-  --..-.-.-...  --  -  --...-"
"""

def main_() -> None:
    args_ = sys_.argv[1:]
    mode_ = 'AZ_CEDILLA'
    verbose_ = False
    msg_ = None

    # flags simples
    rest_ = []
    for a_ in args_:
        if a_.startswith('--mode='):
            mode_ = a_.split('=',1)[1].strip().upper()
        elif a_ == '--verbose':
            verbose_ = True
        else:
            rest_.append(a_)

    if rest_:
        msg_ = ' '.join(rest_).strip()
    else:
        data_ = sys_.stdin.read()
        msg_ = data_.strip()

    if not msg_:
        print(USAGE_)
        sys_.exit(1)

    total_, per_seg_ = count_total_(msg_, mode_, verbose_)
    print(total_)

    if verbose_:
        for seg_, ways_ in per_seg_:
            print(f"segmento: {seg_:>20s} | {ways_:>10d}")

if __name__ == '__main__':
    main_()