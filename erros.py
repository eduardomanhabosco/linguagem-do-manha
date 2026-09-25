"""
erros.py — As três classes de erro do transpilador.

Cada estação tem o seu tipo de erro (enunciado §7):
  - ErroLexico:    um caractere ou lexema que não casa com nenhum token (ex.: '@').
  - ErroSintatico: tokens válidos numa ordem que a gramática não gera (ex.: falta ';').
  - ErroSemantico: forma certa, mas sem sentido (ex.: variável não declarada).

Todas guardam a linha e a coluna, para a mensagem dizer ONDE está o problema.
"""


class ErroGambiarra(Exception):
    """Base comum: linha, coluna e mensagem. As subclasses só mudam o nome da estação."""

    estacao = "Erro"

    def __init__(self, mensagem, linha, coluna):
        super().__init__(mensagem)
        self.mensagem = mensagem
        self.linha = linha
        self.coluna = coluna

    def __str__(self):
        return f"{self.estacao} [linha {self.linha}, coluna {self.coluna}]: {self.mensagem}"


class ErroLexico(ErroGambiarra):
    # O léxico NÃO lança este erro: ele guarda numa lista e continua lendo (EI03, P3c).
    estacao = "Erro léxico"


class ErroSintatico(ErroGambiarra):
    # O parser LANÇA este erro (raise) e para no primeiro (enunciado §4).
    estacao = "Erro sintático"


class ErroSemantico(ErroGambiarra):
    # A semântica guarda todos numa lista e, no fim, não deixa gerar o C.
    estacao = "Erro semântico"
