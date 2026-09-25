"""
tokens.py — Os tipos de token da Gambiarra e a tabela de palavras reservadas.

Token = par [tipo, lexema]. Aqui ele também leva o valor já convertido
(ex.: o lexema "10" vira o valor 10) e a posição (linha e coluna).
"""

from dataclasses import dataclass
from enum import Enum, auto


class TipoToken(Enum):
    # --- palavras reservadas ---
    GAMBIARRA = auto()   # gambiarra   início do programa
    REMENDO = auto()     # remendo     declaração de variável
    MOSTRA = auto()      # mostra      saída
    PEGA = auto()        # pega        entrada
    SE = auto()          # se          if
    SENAO = auto()       # senao       else
    ENQUANTO = auto()    # enquanto    while
    FIRME = auto()       # firme       verdadeiro
    QUEBRADO = auto()    # quebrado    falso

    # --- classes de token (o lexema varia) ---
    ID = auto()          # fita, total_1
    NUM_INT = auto()     # 10
    NUM_REAL = auto()    # 10.5
    TEXTO = auto()       # "oi\n"

    # --- operadores aritméticos ---
    MAIS = auto()        # +
    MENOS = auto()       # -
    VEZES = auto()       # *
    DIVIDE = auto()      # /
    RESTO = auto()       # %

    # --- atribuição e operadores relacionais ---
    ATRIB = auto()       # =
    IGUAL_IGUAL = auto() # ==
    DIFERENTE = auto()   # !=
    MAIOR = auto()       # >
    MAIOR_IGUAL = auto() # >=
    MENOR = auto()       # <
    MENOR_IGUAL = auto() # <=

    # --- operadores lógicos ---
    E_LOGICO = auto()    # &&
    OU_LOGICO = auto()   # ||
    NAO_LOGICO = auto()  # !

    # --- delimitadores ---
    ABRE_PAREN = auto()  # (
    FECHA_PAREN = auto() # )
    ABRE_CHAVE = auto()  # {
    FECHA_CHAVE = auto() # }
    PONTO_VIRGULA = auto()  # ;
    VIRGULA = auto()     # ,

    FIM = auto()         # fim do arquivo (não tem lexema; o parser usa para saber que acabou)


# Palavra reservada × identificador (EI03, P2a): o léxico casa "se" como
# identificador e DEPOIS consulta esta tabela. Se estiver aqui, vira palavra reservada.
PALAVRAS_RESERVADAS = {
    "gambiarra": TipoToken.GAMBIARRA,
    "remendo": TipoToken.REMENDO,
    "mostra": TipoToken.MOSTRA,
    "pega": TipoToken.PEGA,
    "se": TipoToken.SE,
    "senao": TipoToken.SENAO,
    "enquanto": TipoToken.ENQUANTO,
    "firme": TipoToken.FIRME,
    "quebrado": TipoToken.QUEBRADO,
}


# Como cada tipo aparece nas mensagens de erro ("esperava ';'").
DESCRICAO = {
    TipoToken.ID: "um nome de variável",
    TipoToken.NUM_INT: "um número inteiro",
    TipoToken.NUM_REAL: "um número real",
    TipoToken.TEXTO: "um texto",
    TipoToken.FIM: "o fim do arquivo",
    TipoToken.MAIS: "'+'", TipoToken.MENOS: "'-'", TipoToken.VEZES: "'*'",
    TipoToken.DIVIDE: "'/'", TipoToken.RESTO: "'%'", TipoToken.ATRIB: "'='",
    TipoToken.IGUAL_IGUAL: "'=='", TipoToken.DIFERENTE: "'!='",
    TipoToken.MAIOR: "'>'", TipoToken.MAIOR_IGUAL: "'>='",
    TipoToken.MENOR: "'<'", TipoToken.MENOR_IGUAL: "'<='",
    TipoToken.E_LOGICO: "'&&'", TipoToken.OU_LOGICO: "'||'", TipoToken.NAO_LOGICO: "'!'",
    TipoToken.ABRE_PAREN: "'('", TipoToken.FECHA_PAREN: "')'",
    TipoToken.ABRE_CHAVE: "'{'", TipoToken.FECHA_CHAVE: "'}'",
    TipoToken.PONTO_VIRGULA: "';'", TipoToken.VIRGULA: "','",
}
for _palavra, _tipo in PALAVRAS_RESERVADAS.items():
    DESCRICAO[_tipo] = f"'{_palavra}'"


@dataclass(frozen=True)
class Token:
    tipo: TipoToken
    lexema: str     # o pedaço do código-fonte, exatamente como estava escrito
    valor: object   # o valor convertido: int, float ou str; None quando não se aplica
    linha: int
    coluna: int

    def descricao(self):
        """Como o token aparece numa mensagem: "'mostra'", "'x'", "o fim do arquivo"."""
        if self.tipo == TipoToken.FIM:
            return "o fim do arquivo"
        return f"'{self.lexema}'"
