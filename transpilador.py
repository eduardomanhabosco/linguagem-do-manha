"""
transpilador.py — Liga as estações: fonte → léxico → parser → semântica → C.

Uso:
    python transpilador.py programa.gam [opções]

Opções:
    --tokens       mostra a lista de tokens
    --so-lexico    para depois do léxico (para o EI03)
    --derivacao    mostra a árvore de derivação
    --ast          mostra a AST
    --c            mostra o código C gerado
    --executar     compila o C com o gcc e roda o programa
    --saida PASTA  onde salvar o .c (padrão: gerados/)

Cada estação só roda se a anterior passou. Código de saída do programa:
    0 = tudo certo · 1 = erro léxico · 2 = erro sintático · 3 = erro semântico
    4 = arquivo não encontrado · 5 = falha no gcc
"""

import argparse
import os
import shutil
import subprocess
import sys

import gerador
import lexico
import parser as parser_gambiarra      # o NOSSO parser.py (exige Python 3.10+: antes havia um módulo "parser" embutido)
import semantico
from ast_nos import ast_para_texto
from erros import ErroSintatico


def titulo(texto):
    print(f"\n===== {texto} =====")


def main(argv=None):
    # Acentos e ├─ saem certos mesmo quando a saída vai para um arquivo ou outro programa.
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    opcoes = argparse.ArgumentParser(description="Transpilador Gambiarra → C")
    opcoes.add_argument("arquivo", help="programa na linguagem Gambiarra (.gam)")
    opcoes.add_argument("--tokens", action="store_true", help="mostra os tokens")
    opcoes.add_argument("--so-lexico", action="store_true", help="para depois do léxico")
    opcoes.add_argument("--derivacao", action="store_true", help="mostra a árvore de derivação")
    opcoes.add_argument("--ast", action="store_true", help="mostra a AST")
    opcoes.add_argument("--c", action="store_true", help="mostra o código C gerado")
    opcoes.add_argument("--executar", action="store_true", help="compila com gcc e roda")
    opcoes.add_argument("--saida", default="gerados", help="pasta do .c (padrão: gerados)")
    args = opcoes.parse_args(argv)

    # ---------- leitura do arquivo (EI03 P3a) ----------
    try:
        # utf-8-sig: aceita arquivos com BOM (marca invisível que o Bloco de Notas e o
        # PowerShell põem no início); sem isso, o léxico acusaria um caractere inválido.
        with open(args.arquivo, encoding="utf-8-sig") as arquivo:
            codigo = arquivo.read()
    except FileNotFoundError:
        print(f"Arquivo não encontrado: {args.arquivo}")
        return 4

    # ---------- 1. léxico ----------
    tokens, erros_lexicos = lexico.analisar(codigo)
    if args.tokens or args.so_lexico:
        titulo("TOKENS")
        print(lexico.tabela_tokens(tokens))
    if erros_lexicos:
        titulo("ERROS LÉXICOS")
        for erro in erros_lexicos:
            print(erro)
        print(f"\n{len(erros_lexicos)} erro(s) léxico(s). Processamento interrompido.")
        return 1
    if args.so_lexico:
        print(f"\nLéxico OK: {len(tokens)} tokens (contando o FIM).")
        return 0

    # ---------- 2. parser (sintaxe + AST) ----------
    try:
        ast, derivacao = parser_gambiarra.analisar(tokens)
    except ErroSintatico as erro:
        titulo("ERRO SINTÁTICO")
        print(erro)
        print("\nProcessamento interrompido.")
        return 2
    if args.derivacao:
        titulo("ÁRVORE DE DERIVAÇÃO")
        print(derivacao.para_texto())

    # ---------- 3. semântica ----------
    erros_semanticos = semantico.analisar(ast)
    if args.ast:
        titulo("AST")
        print(ast_para_texto(ast))
    if erros_semanticos:
        titulo("ERROS SEMÂNTICOS")
        for erro in erros_semanticos:
            print(erro)
        print(f"\n{len(erros_semanticos)} erro(s) semântico(s). O código C NÃO foi gerado.")
        return 3

    # ---------- 4. geração de C ----------
    codigo_c = gerador.gerar(ast)
    os.makedirs(args.saida, exist_ok=True)
    nome = os.path.splitext(os.path.basename(args.arquivo))[0]
    caminho_c = os.path.join(args.saida, nome + ".c").replace("\\", "/")
    with open(caminho_c, "w", encoding="utf-8", newline="\n") as arquivo:
        arquivo.write(codigo_c)
    if args.c:
        titulo("CÓDIGO C")
        print(codigo_c, end="")
    print(f"\nOK: sem erros. C gerado em {caminho_c}")

    # ---------- 5. (opcional) gcc + execução ----------
    if args.executar:
        return compilar_e_executar(caminho_c)
    return 0


def compilar_e_executar(caminho_c):
    if shutil.which("gcc") is None:
        print("gcc não encontrado no PATH: instale o gcc para usar --executar.")
        return 5
    executavel = os.path.splitext(caminho_c)[0] + (".exe" if os.name == "nt" else "")
    resultado = subprocess.run(["gcc", "-Wall", "-o", executavel, caminho_c],
                               capture_output=True, text=True)
    if resultado.returncode != 0:
        print("Falha ao compilar o C gerado:")
        print(resultado.stderr)
        return 5
    if resultado.stderr.strip():             # avisos do gcc (-Wall): mostramos, mas seguimos
        print("Avisos do gcc:")
        print(resultado.stderr)
    titulo("EXECUÇÃO")
    sys.stdout.flush()                       # o programa em C escreve direto no terminal
    execucao = subprocess.run([os.path.abspath(executavel)])
    return execucao.returncode


if __name__ == "__main__":
    sys.exit(main())
