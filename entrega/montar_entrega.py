"""
montar_entrega.py — Gera os documentos de entrega a partir dos modelos HTML.

  entrega/modelos/relatorio_tp1.html  →  entrega/Relatorio_TP1_Gambiarra.pdf
  entrega/modelos/ei03.html           →  entrega/EI03_<nomes>.pdf  +  entrega/EI03_<nomes>.zip

Os modelos têm marcadores que este script troca pelo conteúdo REAL, rodando o
transpilador na hora (assim as evidências nunca ficam velhas):
  {{INTEGRANTES}}                  nomes do grupo (lista abaixo)
  {{INTEGRANTES_EI03}}             nomes de quem entrega o EI03 (individual ou dupla)
  {{DATA}}                         data de hoje
  {{ARQUIVO caminho}}              conteúdo de um arquivo do projeto
  {{TRANSPILADOR arquivo opções}}  saída de: python transpilador.py arquivo opções
  {{LEXICO arquivo}}               saída de: python lexico.py arquivo
  {{SUITE}}                        saída de: python rodar_testes.py

O PDF sai pelo Microsoft Edge em modo headless (já vem no Windows).

Uso (da pasta do projeto):  python entrega/montar_entrega.py
"""

import datetime
import html
import os
import re
import subprocess
import sys
import zipfile

# ------------------------------------------------------------------
# Quem entrega. O EI03 é individual ou em DUPLA: cada dupla troca a
# lista INTEGRANTES_EI03 e roda o script de novo.
# ------------------------------------------------------------------
INTEGRANTES = ["Eduardo Manhabosco", "Rafael", "Felipe", "Gabriel"]   # completar os sobrenomes
INTEGRANTES_EI03 = ["Eduardo Manhabosco"]

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PASTA_ENTREGA = os.path.join(RAIZ, "entrega")
PASTA_MODELOS = os.path.join(PASTA_ENTREGA, "modelos")

EDGE = [r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"]

# Arquivos que vão no zip do EI03 (o léxico roda sozinho com estes três).
ARQUIVOS_EI03 = ["lexico.py", "tokens.py", "erros.py",
                 "testes/06_lexico_todos_tokens.gam", "testes/03_erro_lexico.gam"]


def rodar(argumentos):
    """Roda um comando Python do projeto e devolve o que apareceu na tela."""
    resultado = subprocess.run([sys.executable, *argumentos], cwd=RAIZ, capture_output=True,
                               text=True, encoding="utf-8")
    return (resultado.stdout + resultado.stderr).rstrip()


def ler(caminho):
    with open(os.path.join(RAIZ, caminho), encoding="utf-8-sig") as arquivo:
        return arquivo.read().rstrip()


def preencher(modelo):
    """Troca cada {{MARCADOR ...}} pelo conteúdo (escapado para HTML)."""
    def trocar(casamento):
        comando, _, resto = casamento.group(1).strip().partition(" ")
        if comando == "INTEGRANTES":
            return "<br>".join(html.escape(n) for n in INTEGRANTES)
        if comando == "INTEGRANTES_EI03":
            return "<br>".join(html.escape(n) for n in INTEGRANTES_EI03)
        if comando == "DATA":
            return datetime.date.today().strftime("%d/%m/%Y")
        if comando == "ARQUIVO":
            return html.escape(ler(resto))
        if comando == "TRANSPILADOR":
            return html.escape(rodar(["transpilador.py", *resto.split()]))
        if comando == "LEXICO":
            return html.escape(rodar(["lexico.py", resto]))
        if comando == "SUITE":
            return html.escape(rodar(["rodar_testes.py"]))
        raise ValueError(f"marcador desconhecido: {casamento.group(0)}")
    return re.sub(r"\{\{(.+?)\}\}", trocar, modelo)


def gerar_pdf(nome_modelo, nome_pdf):
    """Preenche o modelo, salva o HTML ao lado do PDF e imprime com o Edge."""
    with open(os.path.join(PASTA_MODELOS, nome_modelo), encoding="utf-8") as arquivo:
        pagina = preencher(arquivo.read())
    caminho_html = os.path.join(PASTA_ENTREGA, os.path.splitext(nome_pdf)[0] + ".html")
    with open(caminho_html, "w", encoding="utf-8") as arquivo:
        arquivo.write(pagina)

    caminho_pdf = os.path.join(PASTA_ENTREGA, nome_pdf)
    edge = next((e for e in EDGE if os.path.exists(e)), None)
    if edge is None:
        print(f"Edge não encontrado: abra {caminho_html} no navegador e imprima em PDF.")
        return None
    subprocess.run([edge, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={caminho_pdf}", "file:///" + caminho_html.replace("\\", "/")],
                   capture_output=True, timeout=120)
    print(f"PDF: {os.path.relpath(caminho_pdf, RAIZ)}")
    return caminho_pdf


def nome_arquivo(nomes):
    """EI03_EduardoManhabosco (ou EI03_Nome1_Nome2 na dupla), como pede o EI03."""
    return "EI03_" + "_".join(n.replace(" ", "") for n in nomes)


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    os.environ["PATH"] = r"C:\MinGW\bin" + os.pathsep + os.environ["PATH"]   # gcc para a suíte

    gerar_pdf("relatorio_tp1.html", "Relatorio_TP1_Gambiarra.pdf")

    base = nome_arquivo(INTEGRANTES_EI03)
    pdf = gerar_pdf("ei03.html", base + ".pdf")

    # Zip do EI03: PDF + código do léxico + testes com a saída de cada um.
    caminho_zip = os.path.join(PASTA_ENTREGA, base + ".zip")
    with zipfile.ZipFile(caminho_zip, "w", zipfile.ZIP_DEFLATED) as zip_:
        if pdf:
            zip_.write(pdf, os.path.basename(pdf))
        for caminho in ARQUIVOS_EI03:
            zip_.write(os.path.join(RAIZ, caminho), "codigo/" + caminho)
            if caminho.startswith("testes/"):     # saída do léxico para este teste
                zip_.writestr("codigo/" + caminho.replace(".gam", ".saida.txt"),
                              rodar(["lexico.py", caminho]) + "\n")
        zip_.writestr("LEIA-ME.txt",
                      "Analisador léxico da linguagem Gambiarra (EI03).\n"
                      "Requer Python 3.10+. Na pasta codigo/:\n"
                      "  python lexico.py testes/06_lexico_todos_tokens.gam   (todos os tokens válidos)\n"
                      "  python lexico.py testes/03_erro_lexico.gam           (erros léxicos)\n"
                      "A saída de cada teste está em testes/*.saida.txt.\n")
    print(f"ZIP: {os.path.relpath(caminho_zip, RAIZ)}")

    # Conferência do zip (o EI03 pede: "o arquivo compactado abre e extrai corretamente").
    with zipfile.ZipFile(caminho_zip) as zip_:
        problema = zip_.testzip()
        print("Zip conferido:", "OK" if problema is None else f"arquivo corrompido: {problema}")
        for nome in zip_.namelist():
            print("   ", nome)


if __name__ == "__main__":
    main()
