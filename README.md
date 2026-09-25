# Gambiarra → C

Transpilador da linguagem temática **Gambiarra** para **C**. Trabalho Prático 1 de Linguagens Formais e Compiladores (UNIJUÍ, 2026/2).

```
código .gam → léxico → tokens → parser → AST → semântica → código C → gcc
```

## Pré-requisitos
- **Python 3.10 ou mais novo** (só a biblioteca padrão). No Windows, marque "Add python.exe to PATH" na instalação.
- **gcc** (só para `--executar` e para `rodar_testes.py`). No Windows: MinGW, MSYS2 ou WinLibs.

## Como usar
```
python transpilador.py testes/01_valido_basico.gam              # gera gerados/01_valido_basico.c
python transpilador.py testes/01_valido_basico.gam --executar   # gera, compila com gcc e roda
python transpilador.py prog.gam --tokens --derivacao --ast --c  # mostra cada etapa
python transpilador.py prog.gam --so-lexico                     # só o léxico (EI03)
python rodar_testes.py                                          # roda a suíte de testes
```
| Opção | O que faz |
|---|---|
| `--tokens` | lista os tokens (linha:coluna, tipo, lexema) |
| `--so-lexico` | para depois do léxico |
| `--derivacao` | mostra a árvore de derivação |
| `--ast` | mostra a AST |
| `--c` | mostra o C gerado |
| `--executar` | compila o C com `gcc -Wall` e roda |
| `--saida PASTA` | onde salvar o `.c` (padrão: `gerados/`) |

Código de saída: 0 ok · 1 erro léxico · 2 erro sintático · 3 erro semântico · 4 arquivo não encontrado · 5 falha no gcc.

## Exemplo
```
gambiarra {
    remendo fita = 10;
    remendo cola = 2.5;
    fita = fita + 5;
    mostra("fita: ", fita, " cola: ", cola);
}
```
vira
```c
#include <stdio.h>

int main(void) {
    int v_fita = 10;
    float v_cola = 2.5f;
    v_fita = v_fita + 5;
    printf("%s%d%s%g\n", "fita: ", v_fita, " cola: ", v_cola);
    return 0;
}
```
e imprime `fita: 15 cola: 2.5`.

## A linguagem em uma tela
| Gambiarra | Faz |
|---|---|
| `gambiarra { ... }` | o programa |
| `remendo x = 10;` | declara (o tipo vem do valor: `10` inteiro, `2.5` real, `firme` lógico) |
| `x = x + 1;` | atribui |
| `mostra("x = ", x);` | mostra vários itens e pula linha |
| `pega(x);` | lê um inteiro ou real do teclado |
| `se (x > 0) { } senao { }` | decisão |
| `enquanto (x < 10) { }` | repetição |
| `+ - * / %` · `== != > >= < <=` · `&& \|\| !` | operadores (precedência do C) |
| `// linha` · `/* bloco */` | comentários |

Especificação completa (Σ, tokens, gramática, regras semânticas): `docs/ESPECIFICACAO.md`.

## Organização do código (uma estação por arquivo)
| Arquivo | Estação |
|---|---|
| `tokens.py` | tipos de token e palavras reservadas |
| `erros.py` | `ErroLexico`, `ErroSintatico`, `ErroSemantico` |
| `lexico.py` | 1. léxico: texto → tokens (reporta erros e continua) |
| `ast_nos.py` | os nós da AST e o desenho da árvore |
| `parser.py` | 2. parser por descida recursiva: tokens → AST (para no 1º erro) |
| `semantico.py` | 3. tabela de símbolos, escopo e tipos (lista todos os erros) |
| `gerador.py` | 4. AST → C |
| `transpilador.py` | liga as estações (linha de comando) |
| `rodar_testes.py` | suíte de testes |

## Testes
`testes/NN_nome.gam`; a saída esperada fica em `NN_nome.esperado.txt` e a entrada do teclado (para o `pega`) em `NN_nome.entrada.txt`. Se a 1ª linha for `// opcoes: ...`, o teste roda com essas opções; senão, com `--executar`.

| Teste | Mostra |
|---|---|
| 01_valido_basico | declaração, atribuição e saída |
| 02_valido_completo | se/senao, enquanto, pega, precedência `2 + 3 * 4` e `(2 + 3) * 4`, associatividade `10 - 3 - 2` |
| 03_erro_lexico | `@`, `2abc`, `3.4.5`, `preço`, `&`, texto e comentário sem fechar (todos na mesma rodada) |
| 04_erro_sintatico / 04b | `;` esquecido / declaração sem expressão depois do `=` |
| 05_erro_semantico | as regras R1, R2, R5, R7, R9, R10 e R11 |
| 06_lexico_todos_tokens | todos os tipos de token (só o léxico) |
| 07_valido_escopo | escopo por bloco e sombreamento |
| 08_valido_exemplo_enunciado | o exemplo do enunciado, na Gambiarra |

`python rodar_testes.py --mostrar` mostra a saída de cada teste; `--gravar` grava a saída atual como esperada (só depois de conferir à mão).

**Acentos no terminal do Windows:** o transpilador imprime em UTF-8. Se aparecer `Ã©` no lugar de `é`, rode `chcp 65001` antes.
