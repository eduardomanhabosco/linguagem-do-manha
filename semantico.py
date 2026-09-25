"""
semantico.py — 3ª estação: a análise semântica.

A gramática confere a FORMA; aqui conferimos o SENTIDO, que depende de
contexto e que o parser não enxerga (enunciado §5, quadro "Importante").
Teste rápido: troque cada nome pelo tipo do token (x → id). Se o erro some,
ele é semântico: "mostra(y);" com y não declarada tem a mesma forma de
"mostra(x);", então só a tabela de símbolos percebe.

O que esta estação faz, percorrendo a AST:
  1. Mantém a TABELA DE SÍMBOLOS (nome → tipo), com uma pilha de escopos.
  2. Confere as regras R1 a R12 (lista abaixo, igual ao docs/ESPECIFICACAO.md).
  3. Anota na AST o tipo de cada expressão e o nome de cada variável no C
     (o gerador usa isso para escolher %d/%g/%f e para o sombreamento).
  4. Junta TODOS os erros numa lista (decisão do grupo) em vez de parar no 1º.

REGRAS SEMÂNTICAS
  R1  variável só pode ser usada depois de declarada.
  R2  não pode declarar duas vezes no MESMO escopo.
  R3  escopo por bloco: se, senao e enquanto têm o seu; ao sair, as variáveis dele somem.
  R4  sombreamento permitido: um bloco pode declarar um nome que já existe fora.
  R5  + - * / : só números; inteiro op inteiro = inteiro; se houver real, dá real.
      % : só entre inteiros.
  R6  > >= < <= : só números, dão lógico. == != : dois números ou dois lógicos.
      && || ! : só lógicos, dão lógico. - (unário): só números.
  R7  atribuição: real ← inteiro vale (promoção); inteiro ← real não;
      número ↔ lógico não.
  R8  / entre inteiros é divisão inteira (7 / 2 = 3), como no C.
  R9  na declaração, o valor é conferido ANTES de o nome existir
      ("remendo x = x + 1;" usa um x que ainda não existe).
  R10 a condição do se/enquanto tem que ser lógica.
  R11 pega só aceita variável inteira ou real, já declarada.
  R12 a variável fica com o tipo do valor inicial, e ele não muda.
"""

from dataclasses import dataclass

from ast_nos import (Atribuicao, Binario, Declaracao, Enquanto, Escrita, Leitura,
                     Logico, NumeroInt, NumeroReal, Se, Texto, Unario, Variavel)
from erros import ErroSemantico

INTEIRO, REAL, LOGICO = "inteiro", "real", "logico"
NUMERICOS = {INTEIRO, REAL}


@dataclass
class Simbolo:
    nome: str       # nome na Gambiarra
    tipo: str       # inteiro, real ou logico (None se o valor inicial tinha erro)
    linha: int      # onde foi declarada (para a mensagem de redeclaração)
    nome_c: str     # nome no C gerado


class TabelaDeSimbolos:
    """Pilha de escopos. Cada escopo é um dicionário nome → Simbolo.

    - declarar olha só o TOPO (R2: "mesmo escopo");
    - procurar vai do topo para baixo (o de dentro esconde o de fora: R4)."""

    def __init__(self):
        self.escopos = []
        self.contagem_nomes = {}    # quantas vezes cada nome já foi declarado (para o nome no C)

    def entrar_escopo(self):
        self.escopos.append({})

    def sair_escopo(self):
        self.escopos.pop()

    def no_escopo_atual(self, nome):
        return self.escopos[-1].get(nome)

    def declarar(self, nome, tipo, linha):
        # Nome no C: v_fita; se o nome for declarado de novo (sombreamento),
        # v_fita_2, v_fita_3... Assim "remendo x = x + 1;" num bloco interno
        # continua lendo o x de FORA também no C (no C, "int v_x = v_x + 1;"
        # leria o x NOVO, ainda sem valor).
        n = self.contagem_nomes.get(nome, 0) + 1
        self.contagem_nomes[nome] = n
        nome_c = f"v_{nome}" if n == 1 else f"v_{nome}_{n}"
        simbolo = Simbolo(nome, tipo, linha, nome_c)
        self.escopos[-1][nome] = simbolo
        return simbolo

    def procurar(self, nome):
        for escopo in reversed(self.escopos):
            if nome in escopo:
                return escopo[nome]
        return None


class AnalisadorSemantico:
    def __init__(self):
        self.tabela = TabelaDeSimbolos()
        self.erros = []

    def erro(self, mensagem, no):
        self.erros.append(ErroSemantico(mensagem, no.linha, no.coluna))

    # =============================== comandos ===============================

    def programa(self, no):
        self.bloco(no.corpo)

    def bloco(self, bloco):
        # R3: cada bloco tem o seu escopo.
        self.tabela.entrar_escopo()
        for instrucao in bloco.instrucoes:
            self.instrucao(instrucao)
        self.tabela.sair_escopo()

    def instrucao(self, no):
        if isinstance(no, Declaracao):
            self.declaracao(no)
        elif isinstance(no, Atribuicao):
            self.atribuicao(no)
        elif isinstance(no, Leitura):
            self.leitura(no)
        elif isinstance(no, Escrita):
            for item in no.itens:
                if not isinstance(item, Texto):
                    self.expressao(item)      # qualquer tipo pode ser mostrado
        elif isinstance(no, Se):
            self.condicao(no.condicao, "se")
            self.bloco(no.entao)
            if no.senao is not None:
                self.bloco(no.senao)
        elif isinstance(no, Enquanto):
            self.condicao(no.condicao, "enquanto")
            self.bloco(no.corpo)

    def declaracao(self, no):
        # R9: primeiro o valor, depois o nome passa a existir.
        tipo = self.expressao(no.valor)
        anterior = self.tabela.no_escopo_atual(no.nome)
        if anterior is not None:
            self.erro(f"a variável '{no.nome}' já foi declarada neste escopo, na linha "
                      f"{anterior.linha} (regra R2: não pode declarar duas vezes no mesmo escopo)", no)
            no.nome_c, no.tipo = anterior.nome_c, anterior.tipo
            return
        # R12: o tipo da variável é o tipo do valor inicial.
        simbolo = self.tabela.declarar(no.nome, tipo, no.linha)
        no.tipo, no.nome_c = tipo, simbolo.nome_c

    def atribuicao(self, no):
        tipo_valor = self.expressao(no.valor)
        simbolo = self.tabela.procurar(no.nome)
        if simbolo is None:
            self.erro(f"atribuição à variável '{no.nome}', que não foi declarada "
                      f"(regra R1: declare antes com 'remendo {no.nome} = ...;')", no)
            return
        no.nome_c = simbolo.nome_c
        if not atribuicao_compativel(simbolo.tipo, tipo_valor):
            self.erro(f"a variável '{no.nome}' é {simbolo.tipo} e não pode receber um valor "
                      f"{tipo_valor} (regra R7)", no)

    def leitura(self, no):
        simbolo = self.tabela.procurar(no.nome)
        if simbolo is None:
            self.erro(f"pega({no.nome}): a variável '{no.nome}' não foi declarada (regras R1 e R11)", no)
            return
        no.tipo, no.nome_c = simbolo.tipo, simbolo.nome_c
        if simbolo.tipo == LOGICO:
            self.erro(f"pega({no.nome}): a variável '{no.nome}' é lógica; pega só lê "
                      f"inteiro ou real (regra R11)", no)

    def condicao(self, expr, comando):
        tipo = self.expressao(expr)
        if tipo is not None and tipo != LOGICO:
            self.erro(f"a condição do '{comando}' tem que ser lógica, mas é {tipo} "
                      f"(regra R10; ex.: use 'x > 0' em vez de 'x')", expr)

    # ============================== expressões ==============================
    # Cada função devolve o TIPO da expressão (e anota no nó).
    # None = tipo desconhecido (já houve um erro ali dentro): não reclamamos de
    # novo, para um único erro não virar uma cascata de mensagens.

    def expressao(self, no):
        if isinstance(no, (NumeroInt, NumeroReal, Logico)):
            return no.tipo                    # literal: o tipo vem do formato
        if isinstance(no, Variavel):
            simbolo = self.tabela.procurar(no.nome)
            if simbolo is None:
                self.erro(f"a variável '{no.nome}' foi usada antes de ser declarada (regra R1)", no)
                return None
            no.tipo, no.nome_c = simbolo.tipo, simbolo.nome_c
            return no.tipo
        if isinstance(no, Unario):
            no.tipo = self.unario(no)
            return no.tipo
        if isinstance(no, Binario):
            no.tipo = self.binario(no)
            return no.tipo
        raise TypeError(f"nó de expressão desconhecido: {no!r}")

    def unario(self, no):
        tipo = self.expressao(no.operando)
        if tipo is None:
            return None
        if no.op == "-":
            if tipo in NUMERICOS:
                return tipo
            self.erro(f"o '-' só vale para números, mas o valor é {tipo} (regra R6)", no)
            return None
        # op == "!"
        if tipo == LOGICO:
            return LOGICO
        self.erro(f"o '!' só vale para valor lógico, mas o valor é {tipo} (regra R6)", no)
        return None

    def binario(self, no):
        esq = self.expressao(no.esquerda)
        dir_ = self.expressao(no.direita)
        if esq is None or dir_ is None:
            return None
        op = no.op

        if op in ("+", "-", "*", "/"):                              # R5
            if esq in NUMERICOS and dir_ in NUMERICOS:
                return REAL if REAL in (esq, dir_) else INTEIRO     # promoção
            self.erro(f"o operador '{op}' só aceita números, mas recebeu {esq} e {dir_} (regra R5)", no)
            return None

        if op == "%":                                               # R5
            if esq == INTEIRO and dir_ == INTEIRO:
                return INTEIRO
            self.erro(f"o operador '%' só aceita inteiros, mas recebeu {esq} e {dir_} (regra R5)", no)
            return None

        if op in (">", ">=", "<", "<="):                            # R6
            if esq in NUMERICOS and dir_ in NUMERICOS:
                return LOGICO
            self.erro(f"o operador '{op}' só compara números, mas recebeu {esq} e {dir_} (regra R6)", no)
            return None

        if op in ("==", "!="):                                      # R6
            if (esq in NUMERICOS and dir_ in NUMERICOS) or (esq == dir_ == LOGICO):
                return LOGICO
            self.erro(f"o operador '{op}' não compara {esq} com {dir_} (regra R6)", no)
            return None

        # && e ||                                                     R6
        if esq == LOGICO and dir_ == LOGICO:
            return LOGICO
        self.erro(f"o operador '{op}' só aceita valores lógicos, mas recebeu {esq} e {dir_} (regra R6)", no)
        return None


def atribuicao_compativel(destino, valor):
    """R7. Tipo desconhecido (None) não gera erro novo."""
    if destino is None or valor is None:
        return True
    if destino == valor:
        return True
    return destino == REAL and valor == INTEIRO     # só a promoção inteiro → real


def analisar(ast):
    """Função de entrada: devolve a lista de ErroSemantico (vazia = tudo certo).
    A AST volta anotada (tipo e nome_c)."""
    analisador = AnalisadorSemantico()
    analisador.programa(ast)
    return analisador.erros
