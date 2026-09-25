# MAPA — tudo o que precisamos fazer (TP1 + EI03)

Checklist tirado linha por linha do enunciado v6 (`docs/enunciados/TP1_Linguagem_Tematica_v6.md`), do aviso do Classroom e do EI03 (`docs/enunciados/classroom.md`). **Nada do que é pedido pode ficar de fora.**
- `[x]` feito e testado · `[ ]` a fazer · ⚠ fácil de esquecer · (N pts) peso na nota
- Origem: [v6 §N] seção do enunciado · [aviso] post do Classroom · [EI03 Pn] problema do EI03
- Datas são sugestão, contando com entrega em **09/10** (a confirmar no item 0.1). Prazos e transparência no uso de IA também contam na nota [v6 §12].

## 0. Antes de tudo
- [ ] 0.1 ⚠ Confirmar no Classroom a data de entrega e de apresentação do TP1. Os textos não batem: aviso = 4 semanas; EI03 = "Aula 09" (09/10); v6 §11 = "Aula 18". O outro grupo já tem relatório, testes e roteiro de apresentação no GitHub.
- [ ] 0.2 Confirmar a data da prova escrita da sua turma (6N). O texto do EI02 é da turma 4N (prova em 16/09).
- [ ] 0.3 Baixar o PDF anexo do TP1 e comparar com a v6.
- [ ] 0.4 Fechar o grupo: entrega única, e todos participam do planejamento, especificação, implementação, testes, documentação e apresentação [v6 cabeçalho]. EI03: individual ou dupla.
- [ ] 0.5 Perguntar ao professor se o EI03 pode ser em Python (o texto fala em `.flex`/Java).
- [x] 0.8 Python 3.12.10 instalado (winget, 25/09). Suíte: **9 de 9 OK**. Falta revisar os itens dos Marcos 3 a 5 um a um e marcar `[x]`.
- [x] 0.6 gcc: neste PC já existe (`C:\MinGW\bin\gcc.exe` 4.9.2); C de teste compilou com `-Wall` sem avisos (25/09). Texto original: Instalar um compilador C (gcc). Não havia nenhum no PC antigo (gcc, clang, tcc e cl procurados em 23/09); conferir no PC novo. Sem ele, o C gerado não roda. Faremos juntos (MSYS2 ou WinLibs).
- [ ] 0.7 (opcional) EI02: formativo e sem nota; prazo 11/09 passou e o Classroom mostra "Não entregue". Ver se ainda aceita entrega. O conteúdo (ER, AFD, AFN) cai na prova.
- [x] Enunciado completo achado e guardado · decisão: léxico e parser à mão em Python · documentação montada (23/09).

## 1. Estudo dos conceitos (agora; um por mensagem)
Léxico já visto (token, lexema, maior casamento, reservada × identificador). Exemplo usado: a BIRL-Lite do enunciado.
- [x] 1 Visão geral: do código ao programa rodando (23/09)
- [x] 2 Gramática livre de contexto: G = (V, T, P, S) (24/09; dúvida sintático × semântico respondida com o "teste dos tokens")
- [x] 3 BNF e EBNF (lendo a gramática da BIRL-Lite) (24/09; dúvidas: `"("` × `(`, OpRel × operadores lógicos)
- [x] 4 Derivação e árvore de derivação (24/09)
- [x] 5 Ambiguidade e precedência (Expressao → Termo → Fator) (24/09)
- [x] 6 Associatividade e recursão à esquerda (24/09)
- [x] 7 Parser por descida recursiva (24/09; código de exemplo mostrado no chat, ainda não salvo em arquivo)
- [x] 8 Erros sintáticos (24/09)
- [x] 9 AST (árvore sintática abstrata) (24/09)
- [x] 10 Análise semântica e tabela de símbolos (com escopo) (25/09)
- [x] 11 Tipos e compatibilidade (25/09)
- [x] 12 Geração de código: AST → C (25/09)
- [x] 13 Compilador × transpilador × interpretador (e o gcc) (25/09)
- [x] Resumo visual dos 13 conceitos: `docs/resumo-conceitos.html` (online, privado: https://claude.ai/artifact/25wcNyj8hd6nGu1x7vgBuZ)

## D. Decisões a definir (tudo o que o enunciado deixa para o grupo escolher)
Reunidas aqui em 25/09 (antes estavam espalhadas nos conceitos). Cada uma tem as opções, a recomendação e o conceito que explica. **O que for decidido vai para o relatório.**
- `[ ]` aberta · `[~]` tem recomendação, falta o grupo confirmar · `[x]` decidida

### D1. A linguagem (Marco 1) → relatório: tema, objetivos e as 3 decisões próprias
- [x] Tema: **Gambiarra** (25/09). Vocabulário tirado do repo do colega do grupo (`github.com/Gabeez11/gambiarra-transpiler`): **só as palavras**; a lógica/código de lá não é usada (usuário não confia que siga as regras).
- [x] Palavras (25/09), todas minúsculas:

  | Palavra | Significado | C |
  |---|---|---|
  | `gambiarra { ... }` | início e fim do programa | `int main(void) { ... }` |
  | `remendo` | declara variável (tipo deduzido do valor) | `int` / `float` |
  | `mostra( )` | saída | `printf` |
  | `pega( )` | entrada | `scanf` |
  | `se` / `senao` | if / else | `if` / `else` |
  | `enquanto` | while | `while` |
  | `firme` / `quebrado` | verdadeiro / falso | `1` / `0` |
  | `{ } ( ) ;` | bloco, agrupamento, fim de comando | iguais |
  | `+ - * / %` · `== != > >= < <=` · `&& \|\| !` | operadores | iguais |
  | `//` | comentário de linha | — |
- [x] ⚠ As 3 decisões próprias (25/09), justificativas em `docs/ESPECIFICACAO.md` §1: (1) declaração `remendo` sem tipo escrito, tipo deduzido do valor; (2) blocos com `{ }` no lugar de palavra de fechamento; (3) `mostra(a, b, ...)` com vários itens e quebra de linha automática.
- [x] Linguagem destino: **C** (25/09). gcc 4.9.2 (TDM/MinGW) já instalado neste PC.
- [x] Tipos: **inteiro, real e lógico** (25/09); texto só como literal no `mostra`. O lógico veio de `firme`/`quebrado`.
- [x] Declaração: `remendo x = 10;` — **tipo deduzido do valor inicial**, valor obrigatório, tipo fixo depois (tipagem estática) (25/09).
- [x] `%` entra, **só entre inteiros**, mesmo andar de `*` e `/` (25/09).
- [x] Repetição: só `enquanto` (while).
- [x] Blocos com `{ }` obrigatórios no `se`/`senao`/`enquanto` = fechamento explícito, sem "else pendurado".
- [x] Cada comando começa com a sua própria palavra-chave; o `id` sozinho só na atribuição.
- [x] Operadores lógicos na gramática, como **símbolos** `&& || !` (vocabulário do colega).
- [x] Extensão dos arquivos: `.gam` (25/09).
- [x] Aposta/sorte: **não** (25/09).
- [x] Colega do repo é do grupo (25/09). Nomes dos integrantes: a preencher.
- [ ] (extra) Emojis só na tela do editor? Testar antes.

### D2. Léxico (Marco 2 e EI03) → relatório: alfabeto Σ e tabela de tokens
- [x] Alfabeto Σ: letras sem acento, dígitos, `_`, espaço/tab/quebra de linha e `" . , ; ( ) { } + - * / % = ! < > & |`; dentro de texto e comentário vale qualquer caractere (25/09).
- [x] Identificador: `[a-zA-Z_][a-zA-Z0-9_]*`, sem acento, **diferencia maiúscula de minúscula** (25/09).
- [x] Palavras reservadas em **minúsculas** (vocabulário do colega).
- [x] Real: só `[0-9]+\.[0-9]+` (`10.5`). `.5`, `5.`, `3.4.5` e `2abc` = erro léxico (25/09).
- [x] Texto: aspas duplas, sem quebra de linha; escapes `\n \t \" \\` (iguais aos do C); outro escape = erro léxico; aspas sem fechar = erro léxico (25/09).
- [x] Comentários: `//` (linha) e `/* ... */` (bloco); bloco sem fechar = erro léxico (25/09).
- [x] Nome de cada token definido no código (`MAIS`, `IGUAL_IGUAL`, `ATRIB`...), em vez de `['(', '(']`.
- [x] Notação das ER no relatório: estilo JFlex/Python (`|` = união).
- [x] Erro léxico: reporta (linha, coluna, lexema) e continua; no fim, se houve erro, para antes do parser.
- [x] Reservada × identificador: casa como identificador e consulta a tabela de reservadas.
- [x] Maior casamento: operadores longos antes dos curtos.

### D3. Gramática e parser (Marcos 2 e 4) → relatório: G = (V, T, P, S) e BNF/EBNF
- [x] EBNF no relatório, com V, T, P e S explícitos.
- [x] Condição do `se`/`enquanto`: expressão completa, com `&& || !` (25/09).
- [x] Precedência (do mais fraco ao mais forte): `||` < `&&` < relacionais < `+ -` < `* / %` < unários (`!`, `-`) < fator. **`!` como no C** (25/09).
- [x] Menos unário (`-5`, `-x`) entra (25/09).
- [x] Declaração (`remendo`) em qualquer lugar do bloco (25/09).
- [x] `mostra(a, b, ...)`: vários itens separados por vírgula (texto ou expressão) (25/09).
- [x] Erro sintático: para no primeiro, com linha, coluna, encontrado e esperado; `;` esquecido apontado no token anterior.
- [x] Opções de saída: `--tokens`, `--derivacao`, `--ast` (25/09).

### D4. Semântica (Marco 5) → relatório: "regras semânticas adotadas" [v6 §9]
- [x] R1: variável só pode ser usada depois de declarada.
- [x] R2: não pode declarar duas vezes no mesmo escopo.
- [x] R3: escopo por bloco (`se`, `senao` e `enquanto` têm o seu).
- [x] R4: sombreamento **permitido**, como no C (25/09).
- [x] R5: inteiro op inteiro = inteiro; com um real, dá real (promoção). `%` só entre inteiros. Lógico não entra em conta.
- [x] R6: relacionais só entre números e dão lógico; `==`/`!=` também entre dois lógicos. `&& || !` só com lógicos.
- [x] R7: atribuir: inteiro ← inteiro ✅, real ← inteiro ✅, real ← real ✅, lógico ← lógico ✅; inteiro ← real ❌; número ↔ lógico ❌.
- [x] R8: `7 / 2 = 3` (divisão inteira, como no C) (25/09).
- [x] R9: na declaração, o valor é conferido antes de o nome existir (`remendo x = x + 1;` é erro).
- [x] R10: condição do `se`/`enquanto` tem que ser **lógica** (25/09).
- [x] R11: `pega` só aceita variável inteira ou real já declarada (25/09).
- [x] R12 (nova, vem da declaração sem tipo): a variável fica com o tipo do valor inicial, e ele não muda.
- [x] Erros semânticos: **lista todos** e não gera C (25/09).

### D5. Geração de C (Marco 5)
- [x] inteiro → `int`, real → `float` (`scanf %f`), lógico → `int` 0/1.
- [x] Real na saída com `%g` (`10.5`) (25/09).
- [x] Cada `mostra` pula linha no fim (25/09).
- [x] Lógico impresso como `firme`/`quebrado` (25/09).
- [x] Prefixo `v_` nas variáveis do C.
- [x] Parênteses em toda operação.
- [x] Texto com `printf("%s", ...)`.
- [x] C salvo em `gerados/<nome>.c`; `--executar` chama o gcc e roda (25/09).

### D6. Projeto e entrega
- [x] Um arquivo por estação: `erros.py`, `tokens.py`, `lexico.py`, `ast_nos.py`, `parser.py`, `semantico.py`, `gerador.py`, `transpilador.py`; pastas `testes/`, `gerados/` (25/09).
- [x] Testes: `testes/NN_nome.gam` + `NN_nome.esperado.txt`; `python rodar_testes.py` roda todos, compila o C e compara (25/09).
- [x] O `lexico.py` antigo (regex `=` × `==`) vai para `estudo/regex_igual.py` (25/09).
- [x] Extensão `.gam` (25/09).
- [x] Roteiro da apresentação: `docs/ROTEIRO_APRESENTACAO.md` (25/09).

## 2. Marco 1 — Tema e decisões (sugestão: até 25/09) [v6 §13]
- [x] Tema, e uma linguagem "pequena, coerente e executável" [v6 §1]. **Gambiarra** (25/09). **Todas as escolhas deste marco estão em §D1.**
- [x] Tabela de comandos: palavra da linguagem → significado → equivalente em C
- [x] ⚠ 3 decisões próprias de sintaxe, justificadas (declaração, delimitador de bloco, entrada/saída, condicional ou repetição). Não pode ser a BIRL-Lite com as palavras trocadas [v6 originalidade]
  - Dicas dos conceitos 5 e 7: if/while com **fechamento explícito** evita o "else pendurado"; **cada comando começando com sua própria palavra-chave** (o `id` sozinho só na atribuição) deixa o parser LL(1) simples.
- [x] Linguagem destino: C (referência). Outra linguagem só com justificativa técnica e avisando o professor neste marco [v6 §1]
- [x] Exemplos preliminares: 2 ou 3 programas na linguagem nova [v6 §13]
- [x] Extensão dos arquivos → `.gam`
- [ ] Mostrar o marco ao professor: os marcos servem para revisão, e ele pode pedir mudança de sintaxe antes da implementação [v6 §13]

### Escopo mínimo (conferir no desenho da linguagem) [v6 §1]
- [x] 2+ tipos primitivos, pelo menos 1 numérico (ex.: inteiro e real)
- [x] Declaração de variáveis e atribuição
- [x] `+ - * /` com precedência e parênteses
- [x] Operadores relacionais para expressões lógicas (`== != > >= < <=`)
- [x] Decisão com alternativa (if/else)
- [x] Repetição controlada por expressão lógica (while ou for)
- [x] Entrada e saída de dados
- [x] Início/fim do programa e dos blocos bem marcados
- [x] Operadores lógicos (E, OU, NÃO): o léxico precisa reconhecer [EI03 P1d]; decidir se a gramática também usa (recomendado: sim, com andares de precedência OU < E < NÃO < relacionais; decidir onde fica o NÃO)

## 3. Marco 2 — Especificação: tokens e gramática (até 28/09) — léxico 2 pts · gramática 2,5 pts
### Léxico [v6 §2, EI03 P1]
- [x] Alfabeto Σ, ligado a alfabeto, palavra e linguagem regular (Menezes, 2011)
- [x] Tabela de tokens: categoria · ER/padrão · exemplo de lexema · descrição
- [x] ER justificadas, em notação formal (EBNF ou JFlex), dizendo qual notação usamos (nos slides, `+` = união) [EI03 P1]
- [x] Palavras reservadas [EI03 P1a]
- [x] Identificadores, com regra estrita [EI03 P1b]
- [x] Inteiros e reais (no máximo 1 ponto decimal) [EI03 P1c]
- [x] Textos (strings) entre aspas [v6 §2]
- [x] Operadores aritméticos, relacionais e lógicos [EI03 P1d]
- [x] Atribuição, delimitadores e pontuação [EI03 P1e]
- [x] Espaços, quebras de linha ⚠ e comentários de linha E de bloco [EI03 P1f]
- [x] (opcional) AFD de 1 ou 2 tokens (identificador, número real), ligando o léxico à Aula 3
### Gramática [v6 §3]
- [x] G = (V, T, P, S) com V, T, P e S escritos explicitamente
- [x] Produções em BNF/EBNF para todas as estruturas do escopo mínimo
- [x] Expressões sem ambiguidade, com precedência (Expressao → Termo → Fator) e parênteses
- [x] Sem recursão à esquerda (descida recursiva)
- [x] ⚠ A gramática tem que ser IGUAL à implementada: revisar no fim se o código mudou [v6 §3]
- [x] Árvore de derivação de um exemplo (ex.: `2 + 3 * 4`) para o relatório [aviso: "com árvore de derivação"]

## 4. Marco 3 — Analisador léxico = EI03 (código até 01/10; EI03 até 09/10, 19:20, sem atraso)
- [x] Criar repositório git + `.gitignore` → adiantado em 24/09 (troca de PC): repo PRIVADO com o que é da disciplina, inclusive `CLAUDE.md` e `docs/`; push conferido com um clone.
- [x] Lê o programa de um arquivo de texto [EI03 P3a]
- [x] Gera a sequência de tokens (classe + lexema, com linha e coluna) na tela ou em arquivo [EI03 P3b]
- [x] Palavra reservada × identificador (tabela de reservadas) [EI03 P2a]
- [x] Maior casamento: `==` antes de `=`, `>=` antes de `>` etc. [v6 §2, EI03 P2b]
- [x] Controle de linha e coluna [EI03 P2c]
- [x] Ignora espaços, quebras de linha e comentários [v6 §2]
- [x] ⚠ Erro léxico com linha, coluna e lexema, e CONTINUA lendo [EI03 P3c, v6 §7]
- [x] ⚠ Erro para `@`, identificador começando com dígito (`2abc`), número malformado (`3.4.5`), texto sem fechar aspas e comentário de bloco sem fechar [EI03 P4b]
- [x] Teste válido cobrindo TODOS os tipos de token [EI03 P4a]
- [x] Teste com erros léxicos propositais [EI03 P4b]
- [x] Guardar a saída de cada teste (print ou listagem) para o relatório
### Entrega do EI03: `EI03_NomeCompleto.zip` (ou nomes da dupla)
- [~] PDF: nome completo, disciplina (GRP00543), professor, título "Estudo Independente 03" → pronto em `entrega/`, falta completar os campos [PREENCHER] (livros consultados, alterações do grupo, sobrenomes)
- [x] P1 ER justificadas · P2 conflitos explicados com a teoria · P3 código · P4 testes com evidências (prints ou listagem)
- [x] Referências: Menezes cap. 3 (3.1, 3.4, 3.6), Aho cap. 3, Price e Toscani cap. 2.2, Plano de Ensino
- [~] ⚠ Declaração de IA: ferramenta, finalidade, etapas, como verificamos as ER, fontes usadas para validar, o que o aluno alterou → pronto em `entrega/`, falta completar os campos [PREENCHER] (livros consultados, alterações do grupo, sobrenomes)
- [x] Zip com: PDF + código + arquivos de teste (entrada e saída)
- [x] Conferir: o zip abre, tem tudo, o PDF está legível e com o nome

## 5. Marco 4 — Parser + AST (até 04/10) — léxico + parser + AST: 3 pts [v6 §4]
- [x] Parser por descida recursiva: uma função por regra da gramática
- [x] Monta a AST
- [x] ⚠ Precedência na própria AST: `2 + 3 * 4` → `2 + (3 * 4)`, e `(2 + 3) * 4` respeitado. O gerador não "conserta" nada [v6 precedência]
- [x] Opção para mostrar a AST na tela (demo e relatório)
- [x] ⚠ Erro sintático PARA o processamento e mostra linha, token encontrado e o que era esperado [v6 §4, §7]
  - Tokens com linha e coluna; classes de erro próprias (`ErroLexico`, `ErroSintatico`, `ErroSemantico`); `;` esquecido apontado na linha do token anterior.
- [x] Opção para mostrar a **árvore de derivação** (as chamadas das funções do parser, indentadas). Cobre ao pé da letra o "analisador sintático funcionando, com árvore de derivação" do [aviso]
- [x] Nós da AST guardam a **linha**, para os erros semânticos poderem dizer onde estão
- [ ] Todos sabem dizer qual produção reconhece cada estrutura [v6 §4]

## 6. Marco 5 — Semântica, geração de C, testes e relatório (até 07/10)
### Semântica — 2 pts [v6 §5]
- [x] ⚠ Separada do parser, no código e na explicação
- [x] Tabela de símbolos com nome e tipo
- [x] Erro: variável usada antes de ser declarada
- [x] Erro: variável declarada duas vezes no mesmo escopo
- [x] Erro: tipos incompatíveis em atribuições e operações (escrever as regras: real recebe inteiro? inteiro recebe real? texto em conta?)
- [x] Mensagem clara: nome da variável + regra violada [v6 §7]
- [x] Decidir e documentar os escopos (o critério da nota cita "escopo") [v6 §12]
### Geração de código — 3 pts [v6 §6]
- [x] Só roda se léxico, sintaxe e semântica passarem
- [x] Percorre a AST (troca de texto não vale)
- [x] Tipos e declarações mapeados de forma consistente (ex.: inteiro → `int`, real → `float`/`double`)
- [x] if/else, laço, expressões, entrada (`scanf`) e saída (`printf`) gerados dos nós da AST, com o formato certo (`%d`, `%f`)
- [x] ⚠ O C gerado compila no gcc sem erro e se comporta igual ao programa de entrada
- [x] Roda com qualquer arquivo (`python transpilador.py arquivo`), porque o professor pode pedir teste novo na hora [v6 §11]
- [x] (se houver aposta/sorte) `srand` com semente fixa → não se aplica (sem aposta)
### Suíte de testes — 2,5 pts [v6 §8]
- [x] `01_valido_basico`: declaração, atribuição e saída
- [x] `02_valido_completo`: if/else, laço, entrada/saída ⚠ e precedência (`2 + 3 * 4` ou `(2 + 3) * 4`) [v6 §8, aviso]. Sugestão: também `10 - 3 - 2` (associatividade, dá 5)
- [x] `03_erro_lexico`: símbolo ou lexema inválido
- [x] `04_erro_sintatico`: estrutura que viola a GLC (o parser para no 1º erro, então é um erro por arquivo; pode ter `04a`, `04b`…)
- [x] `05_erro_semantico`: uso sem declarar, redeclaração ou tipos incompatíveis
- [x] Nos inválidos, aparece a mensagem de erro do PRÓPRIO transpilador
- [x] Saída esperada de cada teste + um comando que roda todos
- [x] Os `.c` gerados dos testes válidos, guardados (são entregáveis) [v6 §9]
### Relatório técnico (PDF) [v6 §9, §10, aviso]
- [x] Tema e objetivos
- [x] ⚠ As 3 decisões próprias, justificadas
- [x] Alfabeto Σ + tabela de tokens/ER
- [x] G = (V, T, P, S) + gramática BNF/EBNF completa
- [x] Regras semânticas adotadas (rascunho R1 a R11 em §D4)
- [~] ⚠ Ferramentas de IA usadas e para quê → pronto em `entrega/`, falta completar os campos [PREENCHER] (livros consultados, alterações do grupo, sobrenomes)
### README [v6 §9]
- [x] Pré-requisitos (Python, gcc), como compilar/rodar, exemplo de uso
- [ ] Código organizado; testar do zero numa pasta limpa

## 7. Apresentação e defesa — 15 pts (ensaio 08/10; data real no item 0.1) [v6 §11, §12]
- [ ] Apresentar a linguagem, a proposta e as características (2)
- [ ] Explicar a especificação léxica, a gramática e as decisões de projeto (3)
- [ ] Demo ao vivo: arquivo → tokens → AST → C → gcc → execução (3)
- [ ] Demo dos casos válidos e dos erros léxico, sintático e semântico (2)
- [ ] ⚠ Arguição individual: todos explicam tokens, produções, AST, semântica e geração (3). O que ninguém souber explicar conta como não demonstrado [v6 §10]
- [x] Participação de todos (2): roteiro de quem fala o quê → `docs/ROTEIRO_APRESENTACAO.md` (25/09)
- [ ] Ensaiar pedidos ao vivo: novo teste, explicar uma produção, analisar a AST, corrigir um erro, pequena mudança no código (ex.: novo operador `%`, trocar uma palavra-chave)
- [ ] Testar no computador da sala (Python, gcc, fonte grande no terminal)

## Extras (não obrigatórios)
- [ ] Emojis só na tela do editor (Prettify Symbols Mode / vsc-conceal); testar antes
- [x] Página visual com o resumo do `novo 1.txt` → feita em 25/09 (`docs/resumo-conceitos.html`)
