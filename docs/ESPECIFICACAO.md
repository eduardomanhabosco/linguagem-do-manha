# Especificação da linguagem Gambiarra (base do relatório técnico)

Rascunho do relatório do TP1 [v6 §9]: tema, 3 decisões próprias, alfabeto Σ, tabela de tokens/ER, G = (V, T, P, S), EBNF e regras semânticas. **Tem que ficar igual ao código** (`lexico.py`, `parser.py`, `semantico.py`); se um mudar, o outro muda junto.

## 0. Tema e objetivo
**Gambiarra**: uma linguagem com o vocabulário do "conserto improvisado" (`remendo`, `firme`, `quebrado`), que é traduzida para **C** pelo nosso transpilador em Python (léxico e parser feitos à mão, por descida recursiva). O vocabulário veio de um integrante do grupo; a especificação e a implementação são deste repositório.

```
gambiarra {
    remendo fita = 10;
    remendo cola = 2.5;
    se (fita > 5 && cola < 3.0) {
        mostra("fita: ", fita, " cola: ", cola);
    } senao {
        mostra("quebrou");
    }
}
```

| Gambiarra | Significado | C gerado |
|---|---|---|
| `gambiarra { ... }` | início e fim do programa | `int main(void) { ... return 0; }` |
| `remendo x = valor;` | declara variável; o tipo vem do valor | `int` / `float` / `int` (lógico) |
| `x = valor;` | atribuição | `v_x = ...;` |
| `mostra(a, b, ...);` | saída; pula linha no fim | `printf("...\n", ...);` |
| `pega(x);` | entrada (inteiro ou real) | `scanf("%d"/"%f", &v_x);` |
| `se (c) { } senao { }` | decisão com alternativa | `if (c) { } else { }` |
| `enquanto (c) { }` | repetição | `while (c) { }` |
| `firme` / `quebrado` | verdadeiro / falso | `1` / `0` |

## 1. As três decisões próprias (regra de originalidade)
1. **Declaração sem tipo escrito (tipo deduzido do valor).** Na BIRL-Lite o tipo vem antes do nome (`MONSTRO x = 3;`) e o valor é opcional. Na Gambiarra escreve-se `remendo x = 3;`: o valor é **obrigatório** e o tipo da variável é o tipo dele (`3` → inteiro, `2.5` → real, `firme` → lógico). A tipagem continua **estática**: o tipo é fixado na declaração e conferido na semântica (R7, R12). *Por quê:* menos palavras para decorar, nenhuma variável fica sem valor (não existe "lixo" de variável não inicializada no C) e a semântica ganha uma regra própria (R12).
2. **Blocos com `{ }` no lugar de uma palavra de fechamento.** A BIRL-Lite fecha programa, if e while com a mesma palavra (`BIRL`). Na Gambiarra todo bloco (programa, `se`, `senao`, `enquanto`) é delimitado por chaves, **obrigatórias**. *Por quê:* dá para ver onde cada bloco começa e termina, e, com as chaves obrigatórias, não existe o "else pendurado" (cada `senao` fica colado ao `}` do seu `se`).
3. **Saída com vários itens e quebra de linha automática.** A BIRL-Lite mostra um item por comando e exige `\n` no texto. Na Gambiarra, `mostra("total: ", x, " de ", y);` mistura textos e expressões separados por vírgula, e cada `mostra` termina a linha sozinho. *Por quê:* evita esquecer o `\n` e o gerador monta um único `printf`, escolhendo o formato de cada item pelo tipo (`%d`, `%g`, `firme`/`quebrado`).

Outras diferenças da BIRL-Lite: tipo lógico (`firme`/`quebrado`), operadores lógicos `&& || !`, resto `%`, menos unário e comentários `//` e `/* */`.

## 2. Alfabeto Σ
Σ = letras `a–z` `A–Z` (sem acento) ∪ dígitos `0–9` ∪ `{ _ " . , ; ( ) { } + - * / % = ! < > & | \ }` ∪ `{ espaço, tab, quebra de linha }`.
Dentro de um **texto** ou de um **comentário** vale qualquer caractere (inclusive acento). Fora deles, qualquer símbolo fora de Σ (ex.: `@`, `#`, `ç`) é **erro léxico**.
Um programa é uma palavra de Σ*; o léxico reconhece, dentro dela, as palavras de cada linguagem regular da tabela abaixo (Menezes, 2011, cap. 3).

## 3. Tabela de tokens
Notação das ER: a do Python/JFlex (`|` = união, `*` = zero ou mais, `+` = um ou mais, `[ ]` = classe). **Atenção:** nos slides da Aula 3, `+` é união.

| Categoria | Token | ER / padrão | Exemplo | Descrição |
|---|---|---|---|---|
| reservada | GAMBIARRA | `gambiarra` | `gambiarra` | início do programa |
| reservada | REMENDO | `remendo` | `remendo` | declaração |
| reservada | MOSTRA | `mostra` | `mostra` | saída |
| reservada | PEGA | `pega` | `pega` | entrada |
| reservada | SE / SENAO | `se` / `senao` | `se` | decisão |
| reservada | ENQUANTO | `enquanto` | `enquanto` | repetição |
| reservada | FIRME / QUEBRADO | `firme` / `quebrado` | `firme` | literais lógicos |
| identificador | ID | `[a-zA-Z_][a-zA-Z0-9_]*` | `fita_2` | nome de variável (diferencia maiúsculas) |
| número | NUM_INT | `[0-9]+` | `42` | inteiro |
| número | NUM_REAL | `[0-9]+\.[0-9]+` | `10.5` | real (exatamente um ponto, dígitos dos dois lados) |
| texto | TEXTO | `"([^"\\\n] \| \\[nt"\\])*"` | `"oi\n"` | só no `mostra`; escapes `\n \t \" \\` |
| aritmético | MAIS MENOS VEZES DIVIDE RESTO | `+ - * / %` | `*` | contas |
| atribuição | ATRIB | `=` | `=` | guardar valor |
| relacional | IGUAL_IGUAL DIFERENTE MAIOR MAIOR_IGUAL MENOR MENOR_IGUAL | `== != > >= < <=` | `>=` | comparações |
| lógico | E_LOGICO OU_LOGICO NAO_LOGICO | `&& \|\| !` | `&&` | e, ou, não |
| delimitador | ABRE_PAREN FECHA_PAREN ABRE_CHAVE FECHA_CHAVE PONTO_VIRGULA VIRGULA | `( ) { } ; ,` | `{` | agrupamento e separação |
| ignorado | — | `[ \t\r\n]+` | | espaços e quebras de linha |
| ignorado | — | `//[^\n]*` | `// nota` | comentário de linha |
| ignorado | — | `/\*` (qualquer coisa, o mínimo possível) `\*/` | `/* ... */` | comentário de bloco |

**Como o léxico resolve os conflitos** (EI03 P2):
- **Palavra reservada × identificador (P2a):** `se` casa com a ER de ID; em seguida o léxico consulta a tabela `PALAVRAS_RESERVADAS` e, se o lexema está lá, o token vira `SE`.
- **Maior casamento (P2b):** as regras são testadas em ordem e fica a primeira que casa; por isso `== != >= <= && ||` vêm antes de `= ! > < `. Sem isso, `==` viraria dois `=` (a alternância do `re` fica com a primeira opção que serve: `re.match("=|==", "==")` devolve `=`). Pelo mesmo motivo, NUM_REAL vem antes de NUM_INT.
- **Fim do número:** NUM_INT e NUM_REAL exigem que o número termine ali (`(?![\w.])`); sem isso, `2abc` viraria `NUM(2) ID(abc)` e `3.4.5` viraria `NUM(3.4) ...`.
- **Posição (P2c):** o léxico guarda linha e coluna; a cada lexema, soma o tamanho à coluna e, se houver quebra de linha, soma à linha e reinicia a coluna.

**Erros léxicos** (reporta linha, coluna e lexema e **continua**): caractere fora de Σ (`@`, `&` sozinho), número malformado (`2abc`, `3.4.5`, `5.`, `.5`), identificador com acento (`preço`), texto sem fechar aspas, escape inválido (`\q`) e comentário de bloco sem fechar. Se houver erro léxico, o parser não roda.

## 4. Gramática G = (V, T, P, S)
**V** = { Programa, Bloco, Instrucao, Declaracao, Atribuicao, Leitura, Escrita, Item, Condicional, Repeticao, Expressao, ExprE, ExprRel, OpRel, ExprAdit, Termo, Unario, Fator }

**T** = { gambiarra, remendo, mostra, pega, se, senao, enquanto, firme, quebrado, id, num_int, num_real, texto, `+ - * / % = == != > >= < <= && || ! ( ) { } ; ,` }

**S** = Programa

**P** (EBNF: `{ }` zero ou mais, `[ ]` opcional, `( | )` agrupamento, `"x"` terminal):
```
<Programa>    ::= "gambiarra" <Bloco>
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
<Expressao>   ::= <ExprE> { "||" <ExprE> }
<ExprE>       ::= <ExprRel> { "&&" <ExprRel> }
<ExprRel>     ::= <ExprAdit> [ <OpRel> <ExprAdit> ]
<OpRel>       ::= "==" | "!=" | ">" | ">=" | "<" | "<="
<ExprAdit>    ::= <Termo> { ( "+" | "-" ) <Termo> }
<Termo>       ::= <Unario> { ( "*" | "/" | "%" ) <Unario> }
<Unario>      ::= ( "!" | "-" ) <Unario> | <Fator>
<Fator>       ::= num_int | num_real | "firme" | "quebrado" | id | "(" <Expressao> ")"
```

**Precedência** (um andar por nível; o mais fraco fica perto da raiz):

| Andar | Operadores | Associatividade |
|---|---|---|
| 1 (mais fraco) | `\|\|` | esquerda |
| 2 | `&&` | esquerda |
| 3 | `== != > >= < <=` | nenhuma (`a < b < c` é erro sintático) |
| 4 | `+ -` | esquerda (`10 - 3 - 2 = 5`) |
| 5 | `* / %` | esquerda |
| 6 | `!` e `-` unários | direita (`- -5 = 5`) |
| 7 (mais forte) | número, variável, `firme`, `quebrado`, `( )` | — |

Mesma ordem do C, por isso o C gerado se comporta igual. Sem recursão à esquerda: `A → A op B` foi escrito como `A → B { op B }` (um `while` no parser). A gramática é LL(1): as alternativas de `<Instrucao>` começam com tokens diferentes (remendo, id, pega, mostra, se, enquanto), e em `<Item>` o `texto` não está em PRIMEIROS(`<Expressao>`). Não existe "senão se": escreve-se `senao { se (...) { } }`.

**Árvore de derivação de `2 + 3 * 4`** (saída de `--derivacao`, recortada):
```
<ExprAdit>
├─ <Termo>
│  └─ <Unario> └─ <Fator> └─ num_int (2)
├─ +
└─ <Termo>
   ├─ <Unario> └─ <Fator> └─ num_int (3)
   ├─ *
   └─ <Unario> └─ <Fator> └─ num_int (4)
```
O `*` fica dentro de um `<Termo>`, mais fundo que o `+`, então é calculado primeiro: `2 + (3 * 4) = 14`. Na AST: `Binario(+, 2, Binario(*, 3, 4))`.

**Erros sintáticos:** o parser para no primeiro e mostra linha, coluna, o token encontrado e o esperado. Um `;` esquecido é apontado no fim da linha em que ele falta.

## 5. Regras semânticas adotadas
Tipos: **inteiro**, **real** e **lógico**. A semântica percorre a AST com uma **tabela de símbolos** (nome → tipo), organizada como uma pilha de escopos, e **lista todos os erros**. Com qualquer erro, o C não é gerado.

| Regra | Descrição | Exemplo de erro |
|---|---|---|
| R1 | variável só pode ser usada depois de declarada | `mostra(pontos);` sem `remendo pontos` |
| R2 | não pode declarar duas vezes no mesmo escopo | `remendo x = 1; remendo x = 2;` |
| R3 | escopo por bloco: `se`, `senao` e `enquanto` têm o seu | usar fora do `se` uma variável declarada dentro dele |
| R4 | sombreamento permitido (bloco interno pode redeclarar um nome de fora) | — (é válido) |
| R5 | `+ - * /` só com números; int op int = int; com real dá real. `%` só com inteiros | `peso % 2` com `peso` real |
| R6 | `> >= < <=` só com números; `== !=` entre números ou entre lógicos; `&& \|\| !` só com lógicos; `-` unário só com números | `vidas && firme` |
| R7 | atribuição: real ← inteiro vale; inteiro ← real não; número ↔ lógico não | `vidas = 2.5;` com `vidas` inteiro |
| R8 | `/` entre inteiros é divisão inteira (`7 / 2 = 3`), como no C | — |
| R9 | na declaração, o valor é conferido antes de o nome existir | `remendo x = x + 1;` sem outro `x` antes |
| R10 | a condição de `se`/`enquanto` tem que ser lógica | `se (vidas) { }` |
| R11 | `pega` só lê variável inteira ou real, já declarada | `pega(ligado);` com `ligado` lógico |
| R12 | a variável fica com o tipo do valor inicial, e ele não muda | (é o que faz a R7 funcionar) |

## 6. Geração de C
Só roda se léxico, sintaxe e semântica passaram. Percorre a AST (não troca texto). inteiro → `int`, real → `float`, lógico → `int` (0/1). Variáveis com prefixo `v_`; no sombreamento, a de dentro vira `v_x_2` (no C, `int v_x = v_x + 1;` leria o `x` novo, ainda sem valor, e a R9 diz que é o de fora). Toda operação ganha parênteses. `mostra` vira um `printf` com `%d` (inteiro), `%g` (real), `%s` (texto e lógico, que aparece como `firme`/`quebrado`) e `\n` no fim; `pega` vira `scanf` com `%d` ou `%f`.
