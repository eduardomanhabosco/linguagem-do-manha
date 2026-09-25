# APRENDIZADOS (privado, fora do git)

Caderno de termos do projeto, explicados de forma simples. O gatilho "memória" acrescenta novos.

## Transpilador  (2026-09-23)
**O que é:** compilador "fonte a fonte": traduz de uma linguagem para outra de alto nível.
**Explicação:** a BIRL traduz para C e usa o gcc para compilar. O nosso faz o mesmo: linguagem temática → C.

## As estações do transpilador  (2026-09-23)
**O que é:** o caminho do código até o programa rodando, como uma linha de montagem.
**Explicação:** léxico ("as palavras existem?") → parser ("a ordem está certa?", monta a AST) → semântica ("faz sentido?", tabela de símbolos) → geração ("como fica em C?") → gcc compila e roda. Cada estação tem o seu tipo de erro, e o trabalho exige mostrar os três (léxico, sintático e semântico).

## Token e lexema  (2026-09-23)
**O que é:** o lexema é o pedaço de texto do código; o token é a classificação dele.
**Explicação:** em `saldo = 10;` o lexema `saldo` vira `[ID, "saldo"]` e o `10` vira `[NUM, 10]`. Quando o tipo tem o mesmo nome do símbolo, ele aparece repetido: `['(', '(']`.

## Analisador léxico (lexer / scanner)  (2026-09-23)
**O que é:** a 1ª fase: lê caractere por caractere e devolve a lista de tokens.
**Explicação:** ignora espaços e comentários e acusa erro quando acha algo que não pertence à linguagem (ex.: `@`), dizendo linha e coluna.

## Expressão regular (ER) e a notação do professor  (2026-09-23)
**O que é:** padrão que descreve um conjunto de palavras (ex.: `[0-9]+` = um ou mais dígitos).
**Explicação:** nos slides, `+` pode ser **união** (`(a + b)*` = qualquer palavra com a e b). No Python, união é `|` e `+` é "um ou mais". No relatório, dizer qual notação usamos.

## Maior casamento (longest match)  (2026-09-23)
**O que é:** quando duas regras servem, fica a que pega o pedaço maior.
**Explicação:** `==` deve virar um token só, e não dois `=`. No Flex isso é automático. Feito à mão (testando as regras em ordem), os operadores longos (`==`, `>=`, `<=`, `!=`) vêm antes dos curtos.

## Palavra reservada × identificador  (2026-09-23)
**O que é:** `while` casa com a ER de identificador, mas é uma palavra da linguagem.
**Explicação:** jeito comum: casar como identificador e depois olhar numa tabela de palavras reservadas. Se estiver lá, vira token de palavra reservada.

## Gerador de léxico (Lex, Flex, Rexical, PLY)  (2026-09-23)
**O que é:** ferramenta que recebe regras "ER → ação" e gera o código do léxico.
**Explicação:** Lex/Flex geram C, Rexical gera Ruby e PLY é para Python. Têm macros (apelidos de ER, ex.: `BLANK`) e regras; `yytext`/`text` é o lexema casado. Decidimos não usar: vamos escrever à mão.

## Regra "pega-tudo" (`.`)  (2026-09-23)
**O que é:** a última regra do léxico, que casa com qualquer caractere que sobrou.
**Explicação:** no Rexical, `. { [text, text] }` transforma tudo em token, até um `@`. No nosso léxico, cada símbolo válido tem regra própria (`ABRE_PAREN`, `MAIS`...), e a regra pega-tudo vira **erro léxico** (linha, coluna e lexema). Depois do erro, a leitura continua.

## `=` × `==` no Python  (2026-09-23)
**O que é:** `=` guarda um valor (atribuição); `==` pergunta se é igual (comparação).
**Explicação:** `x = 5` põe 5 em x; `x == 5` devolve `True`. Dentro de uma regex (`r"=|=="`) eles são só texto a procurar.

## Gramática livre de contexto (GLC) e BNF/EBNF  (2026-09-23)
**O que é:** regras que dizem como os tokens podem se combinar. G = (V, T, P, S): variáveis, terminais, produções e símbolo inicial.
**Explicação:** BNF/EBNF é o jeito de escrever as regras: `<Termo> ::= <Fator> { ("*" | "/") <Fator> }`. ER não dá conta de parênteses aninhados; GLC dá.

## Erro sintático × erro semântico (o teste dos tokens)  (2026-09-24)
**O que é:** um jeito rápido de saber qual estação acusa o erro.
**Explicação:** troque cada nome e número pelo tipo do token (`x` → `id`, `5` → `num`). Se o erro continua visível, é sintático (ex.: `((2)`, falta um `)`). Se sumiu, é semântico (ex.: `CE_QUER_VER (y);` com `y` não declarada vira `CE_QUER_VER ( id ) ;`, igual a um programa certo). Analogia: "Ele sentou." está certa na forma, mas só faz sentido se "ele" foi apresentado antes.

## Por que a GLC conta parênteses e a ER não  (2026-09-24)
**O que é:** a diferença entre gramática regular (Tipo 3) e livre de contexto (Tipo 2).
**Explicação:** na gramática regular a variável só fica na ponta (`A → wB`). Na GLC ela pode ficar no meio: `Expressao → ( Expressao )`, e cada `(` que entra obriga um `)` a sair. É o aⁿbⁿ do slide 12 da Aula 3. Um autômato finito tem estados contados e não consegue contar sem limite.

## BNF e EBNF  (2026-09-24)
**O que é:** notações padrão para escrever as regras (P) de uma gramática.
**Explicação:** BNF: `<Nome>` = variável, `::=` = "é definido como", `|` = ou, `"texto"` = terminal fixo, `id`/`num` = classe de token. EBNF acrescenta `{ }` (zero ou mais), `[ ]` (opcional) e `( )` (agrupar). Exemplo: `<Bloco> ::= <Comando> <Bloco> | ε` vira `<Bloco> ::= { <Comando> }`. Não aumenta o poder da BNF, só abrevia.

## `"("` com aspas × `(` sem aspas  (2026-09-24)
**O que é:** na BNF/EBNF, aspas = token que aparece no programa; sem aspas = agrupamento da notação.
**Explicação:** em `"(" ( string | <Expressao> ) ")"` só os parênteses com aspas aparecem em `CE_QUER_VER ("oi");`. Os de fora das aspas só dizem "um texto OU uma expressão", como os parênteses de `2 × (3 + 4)`.

## Operador relacional × lógico  (2026-09-24)
**O que é:** relacional (OpRel) compara dois valores; lógico junta comparações.
**Explicação:** relacionais: `== != > >= < <=` (`saldo >= 10`). Lógicos: E, OU, NÃO (em C: `&&`, `||`, `!`), como em `x > 0 E x < 10`. Os dois dão verdadeiro/falso; os aritméticos (`+ - * /`) dão número.

## Derivação e árvore de derivação  (2026-09-24)
**O que é:** derivação = trocar uma variável de cada vez até sobrar só terminal; a árvore é o desenho disso.
**Explicação:** `⇒` = um passo, `⇒*` = vários. Na árvore, a raiz é o símbolo inicial, os nós são variáveis e as folhas, lidas da esquerda para a direita, formam o programa. A derivação mais à esquerda e a mais à direita dão a mesma árvore: ela guarda a estrutura, não a ordem.

## Ambiguidade e precedência  (2026-09-24)
**O que é:** uma gramática é ambígua quando um programa tem duas árvores; a precedência diz o que é calculado primeiro.
**Explicação:** `E → E + E | E * E` dá duas árvores para `2 + 3 * 4` (14 ou 20). A solução é um "andar" por nível: Expressao (+ −) → Termo (* /) → Fator (número, variável, parênteses). O mais fraco fica perto da raiz, e o que está mais fundo é calculado primeiro.

## Associatividade e recursão à esquerda  (2026-09-24)
**O que é:** associatividade decide a ordem entre operadores do mesmo nível; recursão à esquerda é uma regra que começa por ela mesma.
**Explicação:** `10 - 3 - 2` = `(10 - 3) - 2` = 5 (à esquerda). `E → E - T` daria isso, mas trava a descida recursiva: a função chama a si mesma sem consumir token (laço infinito). Solução: `T { - T }`, um `while` que junta cada termo novo à direita da árvore já montada.

## LL(1) e conjunto PRIMEIROS  (2026-09-24)
**O que é:** LL(1) = lê da esquerda, derivação mais à esquerda, espiando 1 token. PRIMEIROS = os tokens que podem iniciar uma regra.
**Explicação:** o parser escolhe a regra olhando só o próximo token, então as alternativas precisam começar com tokens diferentes (Declaracao com `MONSTRO`, Escrita com `CE_QUER_VER`...). Se duas começarem igual, é preciso reescrever a gramática (fatoração à esquerda).

## Erro sintático  (2026-09-24)
**O que é:** tokens válidos numa ordem que a gramática não gera.
**Explicação:** detectado no `consome` ou num ponto de escolha. A mensagem deve dizer linha, coluna, o token encontrado e o esperado ("esperava ';', mas encontrei 'CE_QUER_VER'"). O parser para no primeiro erro; o léxico, ao contrário, reporta e continua.

## Escopo e pilha de tabelas  (2026-09-25)
**O que é:** escopo é a região do programa em que um nome existe.
**Explicação:** com escopo por bloco (como no C), cada if/while tem a sua tabela: empilha ao entrar e desempilha ao sair. Declarar olha só o topo ("mesmo escopo"); procurar vai do topo para baixo. Declarar dentro do bloco um nome que já existe fora é o "sombreamento".

## Promoção de tipos e tipagem estática  (2026-09-25)
**O que é:** tipagem estática = o tipo é conhecido antes de rodar; promoção = o inteiro "sobe" para real numa conta mista.
**Explicação:** `2 + 3.5` é real. A semântica calcula o tipo de baixo para cima (literal pelo formato, variável pela tabela, operação pela regra). No C, `7 / 2` dá 3 (divisão inteira).

## Parser por descida recursiva  (2026-09-23)
**O que é:** a 2ª fase: confere se os tokens seguem a gramática. Cada regra vira uma função.
**Explicação:** `Expressao` chama `Termo`, que chama `Fator`. Como `*` fica num nível mais baixo, `2 + 3 * 4` vira `2 + (3 * 4)` sozinho: a precedência está na gramática.

## AST (árvore sintática abstrata)  (2026-09-23)
**O que é:** o programa em forma de árvore, sem a pontuação.
**Explicação:** `carga = carga + 2 * 1.5;` vira `Atrib(carga, Soma(carga, Mult(2, 1.5)))`. O gerador de código percorre essa árvore.

## Análise semântica e tabela de símbolos  (2026-09-23)
**O que é:** a 3ª fase: confere o que a gramática não enxerga.
**Explicação:** a tabela guarda nome e tipo de cada variável. Dá erro se usar variável não declarada, declarar duas vezes ou misturar tipos incompatíveis.

## Hierarquia de Chomsky  (2026-09-23)
**O que é:** as 4 classes de linguagens formais, da mais simples à mais geral.
**Explicação:** Tipo 3 regulares (ER e autômato finito → léxico) ⊂ Tipo 2 livres de contexto (GLC → parser) ⊂ Tipo 1 sensíveis ao contexto ⊂ Tipo 0 recursivamente enumeráveis. O blog do Sérgio Miranda erra ao pôr "recursiva" no lugar de "sensível ao contexto".

## Interpretador × compilador × transpilador  (2026-09-23)
**O que é:** três jeitos de fazer um programa rodar.
**Explicação:** o interpretador percorre a AST e executa na hora. O compilador traduz para código de máquina ou bytecode. O transpilador traduz para outra linguagem de alto nível (o nosso: → C, e depois o gcc compila). O nosso gerador de código percorre a AST como um interpretador, só que escreve C em vez de executar.

## Prettify symbols (conceal)  (2026-09-23)
**O que é:** recurso do editor que mostra um símbolo no lugar de um texto, sem mudar o arquivo.
**Explicação:** você digita `GIRA_ROLETA` e vê 🎰. O léxico continua lendo o texto.
