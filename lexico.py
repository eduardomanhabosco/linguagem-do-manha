"""
lexico.py — 1ª estação: o analisador léxico (scanner).

Lê o código-fonte caractere por caractere e devolve a lista de tokens.

Como funciona (a "cascata" do separador de moedas):
  Em cada posição do texto, as REGRAS abaixo são testadas EM ORDEM, e a
  primeira que casar ganha. O pedaço casado (o lexema) "cai no buraco" do seu
  tipo de token. Depois o dedo anda para depois do lexema e tudo recomeça.

Três cuidados que o enunciado e o EI03 cobram:
  1. Maior casamento (longest match): '==' vem ANTES de '=' na lista; senão
     '==' cairia no buraco errado e viraria dois '='.  (EI03 P2b)
  2. Palavra reservada × identificador: "se" casa com a regra de identificador
     e depois consultamos PALAVRAS_RESERVADAS.  (EI03 P2a)
  3. Erro léxico: as regras de ERRO (no fim da lista, ou logo depois da regra
     certa que falhou) guardam o erro com linha, coluna e lexema, e a leitura
     CONTINUA.  (EI03 P3c)

Uso isolado (só o léxico, útil para o EI03):
    python lexico.py testes/06_lexico_todos_tokens.gam
"""

import re
import sys

from erros import ErroLexico
from tokens import PALAVRAS_RESERVADAS, TipoToken, Token


# ---------------------------------------------------------------------------
# Tabela de regras: (nome da regra, expressão regular).
# A ORDEM IMPORTA: é testada de cima para baixo.
# Nomes que são um TipoToken viram token; os outros têm tratamento especial
# (ignorar ou registrar erro) na função analisar().
# ---------------------------------------------------------------------------
REGRAS = [
    # --- ignorados: espaços, quebras de linha e comentários ---
    ("ESPACO",          r"[ \t\r\n]+"),
    ("COMENT_LINHA",    r"//[^\n]*"),                 # // até o fim da linha
    ("COMENT_BLOCO",    r"/\*[\s\S]*?\*/"),           # /* ... */ (o '?' pega o PRIMEIRO */)
    ("ERRO_COMENT",     r"/\*[\s\S]*"),               # /* sem */ até o fim do arquivo

    # --- texto: aspas duplas, sem quebra de linha, escapes \n \t \" \\ ---
    ("TEXTO",           r'"(?:\\[nt"\\]|[^"\\\n])*"'),
    ("ERRO_ESCAPE",     r'"(?:\\.|[^"\\\n])*"'),      # fechou, mas tem escape inválido (ex.: \q)
    ("ERRO_TEXTO",      r'"[^\n]*'),                  # abriu aspas e a linha acabou

    # --- números: o (?![\w.]) exige que o número termine ali ---
    #     sem ele, "2abc" viraria NUM(2) ID(abc) e "3.4.5" viraria NUM(3.4) ...
    ("NUM_REAL",        r"[0-9]+\.[0-9]+(?![\w.])"),  # 10.5  (real ANTES do inteiro)
    ("NUM_INT",         r"[0-9]+(?![\w.])"),          # 10
    ("ERRO_NUMERO",     r"[0-9][\w.]*|\.[0-9][\w.]*"),# 2abc, 3.4.5, 5., .5

    # --- identificador (e palavra reservada, decidida depois) ---
    #     (?!\w) recusa um nome colado a letra acentuada: "preço"
    ("ID",              r"[A-Za-z_][A-Za-z0-9_]*(?!\w)"),
    ("ERRO_ID",         r"\w+"),                      # nome com acento ou outro caractere fora de Σ

    # --- operadores de DOIS caracteres: antes dos de um (maior casamento) ---
    ("IGUAL_IGUAL",     r"=="),
    ("DIFERENTE",       r"!="),
    ("MAIOR_IGUAL",     r">="),
    ("MENOR_IGUAL",     r"<="),
    ("E_LOGICO",        r"&&"),
    ("OU_LOGICO",       r"\|\|"),

    # --- operadores e delimitadores de UM caractere ---
    ("ATRIB",           r"="),
    ("NAO_LOGICO",      r"!"),
    ("MAIOR",           r">"),
    ("MENOR",           r"<"),
    ("MAIS",            r"\+"),
    ("MENOS",           r"-"),
    ("VEZES",           r"\*"),
    ("DIVIDE",          r"/"),
    ("RESTO",           r"%"),
    ("ABRE_PAREN",      r"\("),
    ("FECHA_PAREN",     r"\)"),
    ("ABRE_CHAVE",      r"\{"),
    ("FECHA_CHAVE",     r"\}"),
    ("PONTO_VIRGULA",   r";"),
    ("VIRGULA",         r","),

    # --- "pega-tudo": qualquer outro caractere é ERRO (nunca vira token) ---
    ("ERRO_CARACTERE",  r"."),
]

# Compila uma vez só (mais rápido e deixa o laço principal limpo).
REGRAS_COMPILADAS = [(nome, re.compile(padrao)) for nome, padrao in REGRAS]

# Regras que só consomem texto, sem gerar token.
IGNORADAS = {"ESPACO", "COMENT_LINHA", "COMENT_BLOCO"}

# Mensagem de cada regra de erro.
MENSAGENS_ERRO = {
    "ERRO_COMENT":    "comentário de bloco '/*' aberto e nunca fechado com '*/'",
    "ERRO_ESCAPE":    "texto com sequência de escape inválida (valem só \\n, \\t, \\\" e \\\\)",
    "ERRO_TEXTO":     "texto sem fechar aspas (o texto não pode quebrar linha)",
    "ERRO_NUMERO":    "número malformado (inteiro: 10; real: 10.5; nome não começa com dígito)",
    "ERRO_ID":        "identificador com caractere inválido (use só letras sem acento, dígitos e _)",
    "ERRO_CARACTERE": "caractere que não pertence à linguagem",
}


def analisar(codigo):
    """
    Varre o código e devolve (tokens, erros).

    tokens: lista de Token, terminando SEMPRE com um token FIM.
    erros:  lista de ErroLexico (vazia se deu tudo certo).
    """
    tokens = []
    erros = []
    pos = 0          # o "dedo": índice do caractere atual no texto
    linha = 1        # controle de posição (EI03 P2c)
    coluna = 1

    while pos < len(codigo):
        # Testa as regras em ordem; fica a PRIMEIRA que casar.
        for nome, regex in REGRAS_COMPILADAS:
            casamento = regex.match(codigo, pos)
            if casamento:
                break
        # A última regra ('.') casa com qualquer caractere menos '\n', e o '\n'
        # é pego por ESPACO; então sempre há casamento aqui.
        lexema = casamento.group()

        if nome in IGNORADAS:
            pass
        elif nome.startswith("ERRO_"):
            erros.append(ErroLexico(f"{MENSAGENS_ERRO[nome]}: {mostrar_lexema(lexema)}", linha, coluna))
        else:
            tokens.append(criar_token(nome, lexema, linha, coluna))

        # Anda o dedo e atualiza linha/coluna contando as quebras de linha do lexema.
        quebras = lexema.count("\n")
        if quebras:
            linha += quebras
            coluna = len(lexema) - lexema.rfind("\n")   # caracteres depois do último '\n', +1
        else:
            coluna += len(lexema)
        pos = casamento.end()

    tokens.append(Token(TipoToken.FIM, "", None, linha, coluna))
    return tokens, erros


def criar_token(nome, lexema, linha, coluna):
    """Transforma o lexema casado em Token, já convertendo o valor."""
    if nome == "ID":
        # Palavra reservada × identificador: consulta a tabela.
        tipo = PALAVRAS_RESERVADAS.get(lexema, TipoToken.ID)
        return Token(tipo, lexema, None, linha, coluna)
    if nome == "NUM_INT":
        return Token(TipoToken.NUM_INT, lexema, int(lexema), linha, coluna)
    if nome == "NUM_REAL":
        return Token(TipoToken.NUM_REAL, lexema, float(lexema), linha, coluna)
    if nome == "TEXTO":
        # Guardamos o texto SEM as aspas. Os escapes ficam como estão (\n
        # continua sendo barra + n), porque o C entende os mesmos escapes.
        return Token(TipoToken.TEXTO, lexema, lexema[1:-1], linha, coluna)
    return Token(TipoToken[nome], lexema, None, linha, coluna)


def mostrar_lexema(lexema, limite=30):
    """Lexema para a mensagem de erro: entre aspas simples e cortado se for longo."""
    primeira_linha = lexema.split("\n", 1)[0]
    if len(primeira_linha) > limite:
        primeira_linha = primeira_linha[:limite] + "..."
    return f"'{primeira_linha}'"


def tabela_tokens(tokens):
    """Texto com um token por linha: posição, tipo e lexema (a saída do EI03, P3b)."""
    linhas = [f"{'LIN:COL':<9}{'TIPO':<15}LEXEMA"]
    for t in tokens:
        linhas.append(f"{f'{t.linha}:{t.coluna}':<9}{t.tipo.name:<15}{t.lexema}")
    return "\n".join(linhas)


# Rodando este arquivo sozinho: mostra os tokens e os erros léxicos de um arquivo.
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("uso: python lexico.py <arquivo.gam>")
        sys.exit(1)
    sys.stdout.reconfigure(encoding="utf-8")
    with open(sys.argv[1], encoding="utf-8-sig") as arquivo:     # -sig: ignora o BOM
        lista, problemas = analisar(arquivo.read())
    print(tabela_tokens(lista))
    for erro in problemas:
        print(erro)
    sys.exit(1 if problemas else 0)
