"""
parser.py — 2ª estação: o analisador sintático (parser) por DESCIDA RECURSIVA.

Recebe a lista de tokens do léxico, confere se a ORDEM segue a gramática e
monta a AST. Cada regra da gramática (EBNF abaixo) vira UMA função; na EBNF:
    <Nome>   → chamar a função Nome
    { X }    → while (zero ou mais)
    [ X ]    → if (opcional)
    "texto"  → consome(token)

GRAMÁTICA (EBNF) — a mesma do docs/ESPECIFICACAO.md:
  <Programa>    ::= "gambiarra" <Bloco> FIM
  <Bloco>       ::= "{" { <Instrucao> } "}"
  <Instrucao>   ::= <Declaracao> | <Atribuicao> | <Leitura> | <Escrita>
                  | <Condicional> | <Repeticao>
  <Declaracao>  ::= "remendo" id "=" <Expressao> ";"
  <Atribuicao>  ::= id "=" <Expressao> ";"
  <Leitura>     ::= "pega" "(" id ")" ";"
  <Escrita>     ::= "mostra" "(" <Item> { "," <Item> } ")" ";"
  <Item>        ::= texto | <Expressao>
  <Condicional> ::= "se" "(" <Expressao> ")" <Bloco> [ "senao" <Bloco> ]
  <Repeticao>   ::= "enquanto" "(" <Expressao> ")" <Bloco>
  <Expressao>   ::= <ExprE> { "||" <ExprE> }                        ← mais fraco
  <ExprE>       ::= <ExprRel> { "&&" <ExprRel> }
  <ExprRel>     ::= <ExprAdit> [ <OpRel> <ExprAdit> ]
  <OpRel>       ::= "==" | "!=" | ">" | ">=" | "<" | "<="
  <ExprAdit>    ::= <Termo> { ( "+" | "-" ) <Termo> }
  <Termo>       ::= <Unario> { ( "*" | "/" | "%" ) <Unario> }
  <Unario>      ::= ( "!" | "-" ) <Unario> | <Fator>
  <Fator>       ::= num_int | num_real | "firme" | "quebrado" | id
                  | "(" <Expressao> ")"                             ← mais forte

Por que funciona com 1 token de espiada (LL(1)): cada alternativa começa com
um token diferente (remendo, id, pega, mostra, se, enquanto...). Não há
recursão à esquerda: "A → A op B" foi escrito como "A → B { op B }", que vira
um while que junta os termos À ESQUERDA (10 - 3 - 2 = (10 - 3) - 2 = 5).

Erro sintático: o parser PARA no primeiro (raise ErroSintatico) e diz a
linha, a coluna, o token encontrado e o que era esperado.

Além da AST, o parser monta a ÁRVORE DE DERIVAÇÃO (uma folha por token, um nó
por regra chamada), para a opção --derivacao.
"""

from ast_nos import (Atribuicao, Binario, Bloco, Declaracao, Enquanto, Escrita,
                     Leitura, Logico, NumeroInt, NumeroReal, Programa, Se, Texto,
                     Unario, Variavel)
from erros import ErroSintatico
from tokens import DESCRICAO, TipoToken as T


# Os tokens que podem COMEÇAR uma expressão (conjunto PRIMEIROS de <Expressao>).
PRIMEIROS_EXPRESSAO = {T.NUM_INT, T.NUM_REAL, T.FIRME, T.QUEBRADO, T.ID,
                       T.ABRE_PAREN, T.NAO_LOGICO, T.MENOS}

OPERADORES_RELACIONAIS = {T.IGUAL_IGUAL, T.DIFERENTE, T.MAIOR, T.MAIOR_IGUAL,
                          T.MENOR, T.MENOR_IGUAL}


class NoDerivacao:
    """Um nó da árvore de derivação: uma variável da gramática (<Termo>) ou um token (folha)."""

    def __init__(self, rotulo):
        self.rotulo = rotulo
        self.filhos = []

    def para_texto(self):
        linhas = [self.rotulo]
        self._desenhar(self, "", linhas)
        return "\n".join(linhas)

    @staticmethod
    def _desenhar(no, prefixo, linhas):
        for i, filho in enumerate(no.filhos):
            ultimo = i == len(no.filhos) - 1
            linhas.append(prefixo + ("└─ " if ultimo else "├─ ") + filho.rotulo)
            NoDerivacao._desenhar(filho, prefixo + ("   " if ultimo else "│  "), linhas)


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0                      # o "dedo": índice do token atual
        self.derivacao = None             # raiz da árvore de derivação
        self._pilha = []                  # regras abertas no momento (para montar a derivação)

    # ======================= ferramentas básicas =======================

    def atual(self):
        return self.tokens[self.pos]

    def proximo(self):
        """Espia o TIPO do token atual, sem avançar."""
        return self.atual().tipo

    def consome(self, tipo, esperado=None):
        """Confere se o token atual é do tipo pedido e avança o dedo.
        Se não for, é erro sintático."""
        token = self.atual()
        if token.tipo != tipo:
            self.erro(esperado or DESCRICAO[tipo])
        self.pos += 1
        # folha da árvore de derivação: o token consumido
        if self._pilha:
            if token.tipo in (T.ID, T.NUM_INT, T.NUM_REAL, T.TEXTO):
                folha = f"{token.tipo.name.lower()} ({token.lexema})"   # classe + lexema: id (fita)
            elif token.tipo == T.FIM:
                folha = "FIM (fim do arquivo)"
            else:
                folha = token.lexema                                    # terminal fixo: remendo, ;
            self._pilha[-1].filhos.append(NoDerivacao(folha))
        return token

    def erro(self, esperado):
        """Monta a mensagem de erro sintático e PARA o parser.

        Caso especial: faltou ';' no fim da linha. O token encontrado já está na
        linha de baixo, então apontamos o fim do token ANTERIOR (onde o ';'
        deveria estar), que é onde o programador vai procurar."""
        token = self.atual()
        if esperado == "';'" and self.pos > 0:
            anterior = self.tokens[self.pos - 1]
            if anterior.linha < token.linha:
                raise ErroSintatico(
                    f"esperava ';' depois de '{anterior.lexema}' (fim da linha {anterior.linha}), "
                    f"mas encontrei {token.descricao()} na linha {token.linha}",
                    anterior.linha, anterior.coluna + len(anterior.lexema))
        raise ErroSintatico(f"esperava {esperado}, mas encontrei {token.descricao()}",
                            token.linha, token.coluna)

    # --- árvore de derivação: cada função de regra abre e fecha um nó ---

    def _abre(self, regra):
        no = NoDerivacao(f"<{regra}>")
        if self._pilha:
            self._pilha[-1].filhos.append(no)
        else:
            self.derivacao = no
        self._pilha.append(no)

    def _fecha(self):
        self._pilha.pop()

    # ============================ as regras ============================

    def programa(self):
        # <Programa> ::= "gambiarra" <Bloco> FIM
        self._abre("Programa")
        inicio = self.consome(T.GAMBIARRA, "'gambiarra' no início do programa")
        corpo = self.bloco()
        self.consome(T.FIM, "o fim do arquivo depois do '}' que fecha o programa")
        self._fecha()
        return Programa(corpo, inicio.linha, inicio.coluna)

    def bloco(self):
        # <Bloco> ::= "{" { <Instrucao> } "}"
        self._abre("Bloco")
        abre = self.consome(T.ABRE_CHAVE)
        instrucoes = []
        while self.proximo() not in (T.FECHA_CHAVE, T.FIM):      # { <Instrucao> } = while
            instrucoes.append(self.instrucao())
        self.consome(T.FECHA_CHAVE, "'}' para fechar o bloco aberto na linha " + str(abre.linha))
        self._fecha()
        return Bloco(instrucoes, abre.linha, abre.coluna)

    def instrucao(self):
        # <Instrucao>: escolhe a regra pelo PRIMEIRO token (LL(1)).
        self._abre("Instrucao")
        tipo = self.proximo()
        if tipo == T.REMENDO:
            no = self.declaracao()
        elif tipo == T.ID:
            no = self.atribuicao()
        elif tipo == T.PEGA:
            no = self.leitura()
        elif tipo == T.MOSTRA:
            no = self.escrita()
        elif tipo == T.SE:
            no = self.condicional()
        elif tipo == T.ENQUANTO:
            no = self.repeticao()
        else:
            self.erro("um comando (remendo, mostra, pega, se, enquanto ou uma atribuição)")
        self._fecha()
        return no

    def declaracao(self):
        # <Declaracao> ::= "remendo" id "=" <Expressao> ";"
        self._abre("Declaracao")
        self.consome(T.REMENDO)
        nome = self.consome(T.ID, "o nome da variável depois de 'remendo'")
        self.consome(T.ATRIB, "'=' e um valor inicial (o tipo do remendo vem do valor)")
        valor = self.expressao()
        self.consome(T.PONTO_VIRGULA)
        self._fecha()
        return Declaracao(nome.lexema, valor, nome.linha, nome.coluna)

    def atribuicao(self):
        # <Atribuicao> ::= id "=" <Expressao> ";"
        self._abre("Atribuicao")
        nome = self.consome(T.ID)
        self.consome(T.ATRIB)
        valor = self.expressao()
        self.consome(T.PONTO_VIRGULA)
        self._fecha()
        return Atribuicao(nome.lexema, valor, nome.linha, nome.coluna)

    def leitura(self):
        # <Leitura> ::= "pega" "(" id ")" ";"
        self._abre("Leitura")
        self.consome(T.PEGA)
        self.consome(T.ABRE_PAREN)
        nome = self.consome(T.ID, "o nome da variável que vai receber o valor")
        self.consome(T.FECHA_PAREN)
        self.consome(T.PONTO_VIRGULA)
        self._fecha()
        return Leitura(nome.lexema, nome.linha, nome.coluna)

    def escrita(self):
        # <Escrita> ::= "mostra" "(" <Item> { "," <Item> } ")" ";"
        self._abre("Escrita")
        inicio = self.consome(T.MOSTRA)
        self.consome(T.ABRE_PAREN)
        itens = [self.item()]
        while self.proximo() == T.VIRGULA:                        # { "," <Item> } = while
            self.consome(T.VIRGULA)
            itens.append(self.item())
        self.consome(T.FECHA_PAREN, "',' ou ')'")
        self.consome(T.PONTO_VIRGULA)
        self._fecha()
        return Escrita(itens, inicio.linha, inicio.coluna)

    def item(self):
        # <Item> ::= texto | <Expressao>
        self._abre("Item")
        if self.proximo() == T.TEXTO:
            token = self.consome(T.TEXTO)
            no = Texto(token.valor, token.linha, token.coluna)
        else:
            no = self.expressao()
        self._fecha()
        return no

    def condicional(self):
        # <Condicional> ::= "se" "(" <Expressao> ")" <Bloco> [ "senao" <Bloco> ]
        self._abre("Condicional")
        inicio = self.consome(T.SE)
        self.consome(T.ABRE_PAREN, "'(' depois de 'se'")
        condicao = self.expressao()
        self.consome(T.FECHA_PAREN)
        entao = self.bloco()
        senao = None
        if self.proximo() == T.SENAO:                             # [ "senao" <Bloco> ] = if
            self.consome(T.SENAO)
            senao = self.bloco()
        self._fecha()
        return Se(condicao, entao, senao, inicio.linha, inicio.coluna)

    def repeticao(self):
        # <Repeticao> ::= "enquanto" "(" <Expressao> ")" <Bloco>
        self._abre("Repeticao")
        inicio = self.consome(T.ENQUANTO)
        self.consome(T.ABRE_PAREN, "'(' depois de 'enquanto'")
        condicao = self.expressao()
        self.consome(T.FECHA_PAREN)
        corpo = self.bloco()
        self._fecha()
        return Enquanto(condicao, corpo, inicio.linha, inicio.coluna)

    # ======================= expressões (andares) =======================
    # Do mais fraco (perto da raiz) ao mais forte (mais fundo na árvore).

    def expressao(self):
        # <Expressao> ::= <ExprE> { "||" <ExprE> }
        self._abre("Expressao")
        no = self.expr_e()
        while self.proximo() == T.OU_LOGICO:
            op = self.consome(T.OU_LOGICO)
            no = Binario("||", no, self.expr_e(), op.linha, op.coluna)
        self._fecha()
        return no

    def expr_e(self):
        # <ExprE> ::= <ExprRel> { "&&" <ExprRel> }
        self._abre("ExprE")
        no = self.expr_rel()
        while self.proximo() == T.E_LOGICO:
            op = self.consome(T.E_LOGICO)
            no = Binario("&&", no, self.expr_rel(), op.linha, op.coluna)
        self._fecha()
        return no

    def expr_rel(self):
        # <ExprRel> ::= <ExprAdit> [ <OpRel> <ExprAdit> ]
        # Um relacional só (não associativo): "a < b < c" é erro sintático.
        self._abre("ExprRel")
        no = self.expr_adit()
        if self.proximo() in OPERADORES_RELACIONAIS:
            self._abre("OpRel")
            op = self.consome(self.proximo())
            self._fecha()
            no = Binario(op.lexema, no, self.expr_adit(), op.linha, op.coluna)
        self._fecha()
        return no

    def expr_adit(self):
        # <ExprAdit> ::= <Termo> { ( "+" | "-" ) <Termo> }
        # O while junta À ESQUERDA: 10 - 3 - 2 → ((10 - 3) - 2)
        self._abre("ExprAdit")
        no = self.termo()
        while self.proximo() in (T.MAIS, T.MENOS):
            op = self.consome(self.proximo())
            no = Binario(op.lexema, no, self.termo(), op.linha, op.coluna)
        self._fecha()
        return no

    def termo(self):
        # <Termo> ::= <Unario> { ( "*" | "/" | "%" ) <Unario> }
        self._abre("Termo")
        no = self.unario()
        while self.proximo() in (T.VEZES, T.DIVIDE, T.RESTO):
            op = self.consome(self.proximo())
            no = Binario(op.lexema, no, self.unario(), op.linha, op.coluna)
        self._fecha()
        return no

    def unario(self):
        # <Unario> ::= ( "!" | "-" ) <Unario> | <Fator>
        # Recursão à DIREITA (não trava): "- - 5" = -(-5).
        self._abre("Unario")
        if self.proximo() in (T.NAO_LOGICO, T.MENOS):
            op = self.consome(self.proximo())
            no = Unario(op.lexema, self.unario(), op.linha, op.coluna)
        else:
            no = self.fator()
        self._fecha()
        return no

    def fator(self):
        # <Fator> ::= num_int | num_real | "firme" | "quebrado" | id | "(" <Expressao> ")"
        self._abre("Fator")
        tipo = self.proximo()
        if tipo == T.NUM_INT:
            t = self.consome(T.NUM_INT)
            no = NumeroInt(t.valor, t.linha, t.coluna)
        elif tipo == T.NUM_REAL:
            t = self.consome(T.NUM_REAL)
            no = NumeroReal(t.valor, t.lexema, t.linha, t.coluna)
        elif tipo in (T.FIRME, T.QUEBRADO):
            t = self.consome(tipo)
            no = Logico(tipo == T.FIRME, t.linha, t.coluna)
        elif tipo == T.ID:
            t = self.consome(T.ID)
            no = Variavel(t.lexema, t.linha, t.coluna)
        elif tipo == T.ABRE_PAREN:
            self.consome(T.ABRE_PAREN)
            no = self.expressao()                                 # os parênteses "furam" os andares
            self.consome(T.FECHA_PAREN)
        elif tipo == T.TEXTO:
            self.erro("um número, variável, firme/quebrado ou '(' "
                      "(texto só pode aparecer direto dentro do mostra)")
        else:
            self.erro("um valor (número, variável, firme, quebrado ou '(')")
        self._fecha()
        return no


def analisar(tokens):
    """Função de entrada: devolve (ast, arvore_de_derivacao). Lança ErroSintatico."""
    parser = Parser(tokens)
    ast = parser.programa()
    return ast, parser.derivacao
