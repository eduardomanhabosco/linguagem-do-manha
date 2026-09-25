"""
rodar_testes.py — Roda a suíte de testes e compara com a saída esperada.

Para cada testes/NN_nome.gam:
  1. roda  python transpilador.py testes/NN_nome.gam <opções>
     - opções: as da 1ª linha do teste, se ela for "// opcoes: ...";
       senão, --executar (gera o C, compila no gcc e roda);
     - entrada do teclado: testes/NN_nome.entrada.txt, se existir (para o 'pega');
  2. compara tudo o que apareceu na tela com testes/NN_nome.esperado.txt.

Uso:
    python rodar_testes.py            roda todos e mostra OK / FALHOU
    python rodar_testes.py 02         roda só os testes cujo nome contém "02"
    python rodar_testes.py --mostrar  mostra também a saída de cada teste
    python rodar_testes.py --gravar   grava a saída atual como esperada
                                      (use só depois de CONFERIR a saída à mão)
"""

import difflib
import glob
import os
import subprocess
import sys

RAIZ = os.path.dirname(os.path.abspath(__file__))
PASTA_TESTES = os.path.join(RAIZ, "testes")


def opcoes_do_teste(caminho):
    with open(caminho, encoding="utf-8-sig") as arquivo:
        primeira = arquivo.readline().strip()
    if primeira.startswith("// opcoes:"):
        return primeira[len("// opcoes:"):].split()
    return ["--executar"]


def rodar(caminho):
    """Roda o transpilador num teste e devolve o que apareceu na tela."""
    base = os.path.splitext(caminho)[0]
    entrada = ""
    if os.path.exists(base + ".entrada.txt"):
        with open(base + ".entrada.txt", encoding="utf-8") as arquivo:
            entrada = arquivo.read()
    relativo = os.path.relpath(caminho, RAIZ).replace("\\", "/")
    resultado = subprocess.run(
        [sys.executable, "transpilador.py", relativo, *opcoes_do_teste(caminho)],
        cwd=RAIZ, input=entrada, capture_output=True, text=True, encoding="utf-8")
    saida = resultado.stdout + resultado.stderr
    # Normaliza: sem espaços no fim das linhas e sem linhas vazias no fim.
    return "\n".join(linha.rstrip() for linha in saida.strip().splitlines()) + "\n"


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    args = sys.argv[1:]
    gravar = "--gravar" in args
    mostrar = "--mostrar" in args
    filtros = [a for a in args if not a.startswith("--")]

    testes = sorted(glob.glob(os.path.join(PASTA_TESTES, "*.gam")))
    if filtros:
        testes = [t for t in testes if any(f in os.path.basename(t) for f in filtros)]

    falhas = 0
    for caminho in testes:
        nome = os.path.basename(caminho)
        esperado_caminho = os.path.splitext(caminho)[0] + ".esperado.txt"
        obtido = rodar(caminho)

        if gravar:
            with open(esperado_caminho, "w", encoding="utf-8", newline="\n") as arquivo:
                arquivo.write(obtido)
            print(f"GRAVADO   {nome}")
        elif not os.path.exists(esperado_caminho):
            print(f"SEM GABARITO  {nome}  (confira a saída e rode com --gravar)")
            falhas += 1
        else:
            with open(esperado_caminho, encoding="utf-8") as arquivo:
                esperado = arquivo.read()
            if obtido == esperado:
                print(f"OK        {nome}")
            else:
                falhas += 1
                print(f"FALHOU    {nome}")
                diferenca = difflib.unified_diff(esperado.splitlines(), obtido.splitlines(),
                                                 "esperado", "obtido", lineterm="")
                print("\n".join("    " + linha for linha in diferenca))

        if mostrar or (not gravar and not os.path.exists(esperado_caminho)):
            print("\n".join("    | " + linha for linha in obtido.splitlines()))

    print(f"\n{len(testes) - falhas} de {len(testes)} testes passaram.")
    return 1 if falhas else 0


if __name__ == "__main__":
    sys.exit(main())
