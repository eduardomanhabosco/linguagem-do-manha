"""
gerador.py — 4ª estação: geração de código (AST → C).

Só roda depois que o léxico, o parser e a semântica passaram sem erro. Ele
PERCORRE A AST (não é troca de texto): para cada tipo de nó há uma função que
escreve o C equivalente. A precedência já está na forma da árvore; o gerador
só põe parênteses em toda operação para o C não ter como ler diferente.

Mapa AST → C:
  Programa             →  #include <stdio.h> / int main(void) { ... return 0; }
  Declaracao inteiro   →  int v_x = ...;
  Declaracao real      →  float v_x = ...;
  Declaracao logico    →  int v_x = ...;          (firme = 1, quebrado = 0)
  Atribuicao           →  v_x = ...;
  Leitura              →  scanf("%d", &v_x);  ou  scanf("%f", &v_x);
  Escrita              →  um printf só, com um formato por item e '\n' no fim
  Se / senao           →  if (...) { ... } else { ... }
  Enquanto             →  while (...) { ... }

Formatos do printf: inteiro %d, real %g (10.5 e não 10.500000),
lógico %s com (v ? "firme" : "quebrado"), texto %s (um '%' dentro do texto não
vira formato).

Variáveis ganham o prefixo v_ (uma variável chamada 'int' ou 'printf' não quebra
o C); a semântica já escolheu o nome (nome_c), inclusive v_x_2 no sombreamento.
"""

from ast_nos import (Atribuicao, Binario, Declaracao, Enquanto, Escrita, Leitura,
                     Logico, NumeroInt, NumeroReal, Se, Texto, Unario, Variavel)

TIPO_C = {"inteiro": "int", "real": "float", "logico": "int"}
FORMATO_SCANF = {"inteiro": "%d", "real": "%f"}
INDENTACAO = "    "


class GeradorC:
    def __init__(self):
        self.linhas = []
        self.nivel = 0          # nível de indentação atual

    def emitir(self, texto):
        self.linhas.append(INDENTACAO * self.nivel + texto)

    # ============================== comandos ==============================

    def programa(self, no):
        self.emitir("#include <stdio.h>")
        self.emitir("")
        self.emitir("int main(void) {")
        self.nivel += 1
        self.instrucoes(no.corpo)
        self.emitir("return 0;")
        self.nivel -= 1
        self.emitir("}")
        return "\n".join(self.linhas) + "\n"

    def instrucoes(self, bloco):
        for instrucao in bloco.instrucoes:
            self.instrucao(instrucao)

    def instrucao(self, no):
        if isinstance(no, Declaracao):
            self.emitir(f"{TIPO_C[no.tipo]} {no.nome_c} = {self.expr(no.valor, topo=True)};")
        elif isinstance(no, Atribuicao):
            self.emitir(f"{no.nome_c} = {self.expr(no.valor, topo=True)};")
        elif isinstance(no, Leitura):
            self.emitir(f'scanf("{FORMATO_SCANF[no.tipo]}", &{no.nome_c});')
        elif isinstance(no, Escrita):
            self.escrita(no)
        elif isinstance(no, Se):
            self.emitir(f"if ({self.expr(no.condicao, topo=True)}) {{")
            self.bloco_indentado(no.entao)
            if no.senao is not None:
                self.emitir("} else {")
                self.bloco_indentado(no.senao)
            self.emitir("}")
        elif isinstance(no, Enquanto):
            self.emitir(f"while ({self.expr(no.condicao, topo=True)}) {{")
            self.bloco_indentado(no.corpo)
            self.emitir("}")

    def bloco_indentado(self, bloco):
        self.nivel += 1
        self.instrucoes(bloco)
        self.nivel -= 1

    def escrita(self, no):
        # mostra("total: ", x);  →  printf("%s%d\n", "total: ", v_x);
        formatos = []
        argumentos = []
        for item in no.itens:
            if isinstance(item, Texto):
                formatos.append("%s")
                argumentos.append(f'"{item.valor}"')   # escapes (\n, \t, \", \\) iguais aos do C
            elif item.tipo == "inteiro":
                formatos.append("%d")
                argumentos.append(self.expr(item, topo=True))
            elif item.tipo == "real":
                formatos.append("%g")
                argumentos.append(self.expr(item, topo=True))
            else:  # logico
                formatos.append("%s")
                argumentos.append(f'({self.expr(item)} ? "firme" : "quebrado")')
        self.emitir(f'printf("{"".join(formatos)}\\n", {", ".join(argumentos)});')

    # ============================= expressões =============================

    def expr(self, no, topo=False):
        """Escreve a expressão em C. Toda operação ganha parênteses, menos a
        mais de fora (topo=True), para o C gerado ficar legível."""
        if isinstance(no, NumeroInt):
            return str(no.valor)
        if isinstance(no, NumeroReal):
            return no.lexema + "f"                    # 10.5f: literal float, como o tipo da variável
        if isinstance(no, Logico):
            return "1" if no.valor else "0"
        if isinstance(no, Variavel):
            return no.nome_c
        if isinstance(no, Unario):
            texto = f"{no.op}{self.expr(no.operando)}"
        elif isinstance(no, Binario):
            texto = f"{self.expr(no.esquerda)} {no.op} {self.expr(no.direita)}"
        else:
            raise TypeError(f"nó de expressão desconhecido: {no!r}")
        return texto if topo else f"({texto})"


def gerar(ast):
    """Função de entrada: devolve o código C (texto)."""
    return GeradorC().programa(ast)
