"""
ast_nos.py — Os nós da AST (árvore sintática abstrata).

A AST é a versão "enxuta" da árvore de derivação: só fica o que importa para
entender e traduzir o programa. Somem ';', parênteses, chaves e as variáveis
intermediárias da gramática (Termo, Fator...).

Exemplo:  remendo total = 2 + 3 * 4;
  vira    Declaracao(total, Binario(+, 2, Binario(*, 3, 4)))
  A precedência já está na FORMA da árvore: o '*' ficou mais fundo, então é
  calculado primeiro. O gerador de C não precisa "consertar" nada.

Todo nó guarda linha e coluna, para a semântica apontar onde está o erro.
Os campos 'tipo' e 'nome_c' começam vazios e são preenchidos pela semântica.
"""

from dataclasses import dataclass, field


# ============================ programa e blocos ============================

@dataclass
class Programa:
    corpo: "Bloco"
    linha: int = 1
    coluna: int = 1


@dataclass
class Bloco:
    instrucoes: list        # Declaracao, Atribuicao, Leitura, Escrita, Se, Enquanto
    linha: int
    coluna: int


# ================================ comandos =================================

@dataclass
class Declaracao:           # remendo nome = valor;
    nome: str
    valor: object           # uma expressão
    linha: int
    coluna: int
    tipo: str = None        # semântica: tipo deduzido do valor ('inteiro', 'real', 'logico')
    nome_c: str = None      # semântica: nome da variável no C (ex.: v_fita)


@dataclass
class Atribuicao:           # nome = valor;
    nome: str
    valor: object
    linha: int
    coluna: int
    nome_c: str = None


@dataclass
class Leitura:              # pega(nome);
    nome: str
    linha: int
    coluna: int
    tipo: str = None        # semântica: tipo da variável (decide %d ou %f no scanf)
    nome_c: str = None


@dataclass
class Escrita:              # mostra(item, item, ...);
    itens: list             # cada item é Texto ou uma expressão
    linha: int
    coluna: int


@dataclass
class Se:                   # se (condicao) { ... } senao { ... }
    condicao: object
    entao: Bloco
    senao: Bloco            # None quando não há 'senao'
    linha: int
    coluna: int


@dataclass
class Enquanto:             # enquanto (condicao) { ... }
    condicao: object
    corpo: Bloco
    linha: int
    coluna: int


# =============================== expressões ================================

@dataclass
class Binario:              # esquerda op direita   (op: '+', '<=', '&&', ...)
    op: str
    esquerda: object
    direita: object
    linha: int
    coluna: int
    tipo: str = None


@dataclass
class Unario:               # op operando   (op: '-' ou '!')
    op: str
    operando: object
    linha: int
    coluna: int
    tipo: str = None


@dataclass
class NumeroInt:            # 10
    valor: int
    linha: int
    coluna: int
    tipo: str = "inteiro"


@dataclass
class NumeroReal:           # 10.5
    valor: float
    lexema: str             # guardamos o texto original para escrever igual no C
    linha: int
    coluna: int
    tipo: str = "real"


@dataclass
class Logico:               # firme / quebrado
    valor: bool
    linha: int
    coluna: int
    tipo: str = "logico"


@dataclass
class Variavel:             # fita
    nome: str
    linha: int
    coluna: int
    tipo: str = None
    nome_c: str = None


@dataclass
class Texto:                # "oi\n"  (só aparece como item do mostra)
    valor: str              # sem as aspas; escapes como no fonte
    linha: int
    coluna: int
    tipo: str = "texto"


# ============================ mostrar a AST ================================

def ast_para_texto(no):
    """Desenha a AST com ├─ e └─, no estilo do enunciado."""
    linhas = [rotulo(no)]
    _desenhar_filhos(no, "", linhas)
    return "\n".join(linhas)


def _desenhar_filhos(no, prefixo, linhas):
    filhos = filhos_de(no)
    for i, filho in enumerate(filhos):
        ultimo = i == len(filhos) - 1
        linhas.append(prefixo + ("└─ " if ultimo else "├─ ") + rotulo(filho))
        _desenhar_filhos(filho, prefixo + ("   " if ultimo else "│  "), linhas)


def rotulo(no):
    """O texto de um nó: comandos mostram a forma; expressões pequenas cabem numa linha."""
    if isinstance(no, Programa):
        return "Programa"
    if isinstance(no, Declaracao):
        return f"Declaracao({no.nome} = {expr_texto(no.valor)})"
    if isinstance(no, Atribuicao):
        return f"Atrib({no.nome} = {expr_texto(no.valor)})"
    if isinstance(no, Leitura):
        return f"Leitura({no.nome})"
    if isinstance(no, Escrita):
        return "Print(" + ", ".join(expr_texto(i) for i in no.itens) + ")"
    if isinstance(no, Se):
        return f"If({expr_texto(no.condicao)})"
    if isinstance(no, Enquanto):
        return f"While({expr_texto(no.condicao)})"
    if isinstance(no, tuple):          # ("Senao", bloco): rótulo do ramo senao
        return "Else"
    return expr_texto(no)


def filhos_de(no):
    """Os filhos que o desenho mostra. Expressões não abrem galhos (ficam no rótulo)."""
    if isinstance(no, Programa):
        return no.corpo.instrucoes
    if isinstance(no, Se):
        filhos = list(no.entao.instrucoes)
        if no.senao is not None:
            filhos.append(("Senao", no.senao))
        return filhos
    if isinstance(no, tuple):
        return no[1].instrucoes
    if isinstance(no, Enquanto):
        return no.corpo.instrucoes
    return []


def expr_texto(no):
    """Expressão com parênteses em TODA operação: mostra a precedência que a árvore guardou.
    Ex.: 2 + 3 * 4  →  (2 + (3 * 4))"""
    if isinstance(no, Binario):
        return f"({expr_texto(no.esquerda)} {no.op} {expr_texto(no.direita)})"
    if isinstance(no, Unario):
        return f"({no.op}{expr_texto(no.operando)})"
    if isinstance(no, NumeroInt):
        return str(no.valor)
    if isinstance(no, NumeroReal):
        return no.lexema
    if isinstance(no, Logico):
        return "firme" if no.valor else "quebrado"
    if isinstance(no, Variavel):
        return no.nome
    if isinstance(no, Texto):
        return f'"{no.valor}"'
    return repr(no)
