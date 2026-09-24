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
- [ ] 0.6 ⚠ Instalar um compilador C (gcc). Não havia nenhum no PC antigo (gcc, clang, tcc e cl procurados em 23/09); conferir no PC novo. Sem ele, o C gerado não roda. Faremos juntos (MSYS2 ou WinLibs).
- [ ] 0.7 (opcional) EI02: formativo e sem nota; prazo 11/09 passou e o Classroom mostra "Não entregue". Ver se ainda aceita entrega. O conteúdo (ER, AFD, AFN) cai na prova.
- [x] Enunciado completo achado e guardado · decisão: léxico e parser à mão em Python · documentação montada (23/09).

## 1. Estudo dos conceitos (agora; um por mensagem)
Léxico já visto (token, lexema, maior casamento, reservada × identificador). Exemplo usado: a BIRL-Lite do enunciado.
- [x] 1 Visão geral: do código ao programa rodando (23/09)
- [x] 2 Gramática livre de contexto: G = (V, T, P, S) (24/09; dúvida sintático × semântico respondida com o "teste dos tokens")
- [ ] 3 BNF e EBNF (lendo a gramática da BIRL-Lite): **enviado em 24/09**, antes da troca de PC; perguntar se há dúvidas
- [ ] 4 Derivação e árvore de derivação
- [ ] 5 Ambiguidade e precedência (Expressao → Termo → Fator)
- [ ] 6 Associatividade e recursão à esquerda
- [ ] 7 Parser por descida recursiva
- [ ] 8 Erros sintáticos
- [ ] 9 AST (árvore sintática abstrata)
- [ ] 10 Análise semântica e tabela de símbolos (com escopo)
- [ ] 11 Tipos e compatibilidade
- [ ] 12 Geração de código: AST → C
- [ ] 13 Compilador × transpilador × interpretador (e o gcc)

## 2. Marco 1 — Tema e decisões (sugestão: até 25/09) [v6 §13]
- [ ] Tema, e uma linguagem "pequena, coerente e executável" [v6 §1]. Ideia: cassino.
- [ ] Tabela de comandos: palavra da linguagem → significado → equivalente em C
- [ ] ⚠ 3 decisões próprias de sintaxe, justificadas (declaração, delimitador de bloco, entrada/saída, condicional ou repetição). Não pode ser a BIRL-Lite com as palavras trocadas [v6 originalidade]
- [ ] Linguagem destino: C (referência). Outra linguagem só com justificativa técnica e avisando o professor neste marco [v6 §1]
- [ ] Exemplos preliminares: 2 ou 3 programas na linguagem nova [v6 §13]
- [ ] Extensão dos arquivos (ex.: `.cassino`)
- [ ] Mostrar o marco ao professor: os marcos servem para revisão, e ele pode pedir mudança de sintaxe antes da implementação [v6 §13]

### Escopo mínimo (conferir no desenho da linguagem) [v6 §1]
- [ ] 2+ tipos primitivos, pelo menos 1 numérico (ex.: inteiro e real)
- [ ] Declaração de variáveis e atribuição
- [ ] `+ - * /` com precedência e parênteses
- [ ] Operadores relacionais para expressões lógicas (`== != > >= < <=`)
- [ ] Decisão com alternativa (if/else)
- [ ] Repetição controlada por expressão lógica (while ou for)
- [ ] Entrada e saída de dados
- [ ] Início/fim do programa e dos blocos bem marcados
- [ ] Operadores lógicos (E, OU, NÃO): o léxico precisa reconhecer [EI03 P1d]; decidir se a gramática também usa

## 3. Marco 2 — Especificação: tokens e gramática (até 28/09) — léxico 2 pts · gramática 2,5 pts
### Léxico [v6 §2, EI03 P1]
- [ ] Alfabeto Σ, ligado a alfabeto, palavra e linguagem regular (Menezes, 2011)
- [ ] Tabela de tokens: categoria · ER/padrão · exemplo de lexema · descrição
- [ ] ER justificadas, em notação formal (EBNF ou JFlex), dizendo qual notação usamos (nos slides, `+` = união) [EI03 P1]
- [ ] Palavras reservadas [EI03 P1a]
- [ ] Identificadores, com regra estrita [EI03 P1b]
- [ ] Inteiros e reais (no máximo 1 ponto decimal) [EI03 P1c]
- [ ] Textos (strings) entre aspas [v6 §2]
- [ ] Operadores aritméticos, relacionais e lógicos [EI03 P1d]
- [ ] Atribuição, delimitadores e pontuação [EI03 P1e]
- [ ] Espaços, quebras de linha ⚠ e comentários de linha E de bloco [EI03 P1f]
- [ ] (opcional) AFD de 1 ou 2 tokens (identificador, número real), ligando o léxico à Aula 3
### Gramática [v6 §3]
- [ ] G = (V, T, P, S) com V, T, P e S escritos explicitamente
- [ ] Produções em BNF/EBNF para todas as estruturas do escopo mínimo
- [ ] Expressões sem ambiguidade, com precedência (Expressao → Termo → Fator) e parênteses
- [ ] Sem recursão à esquerda (descida recursiva)
- [ ] ⚠ A gramática tem que ser IGUAL à implementada: revisar no fim se o código mudou [v6 §3]
- [ ] Árvore de derivação de um exemplo (ex.: `2 + 3 * 4`) para o relatório [aviso: "com árvore de derivação"]

## 4. Marco 3 — Analisador léxico = EI03 (código até 01/10; EI03 até 09/10, 19:20, sem atraso)
- [x] Criar repositório git + `.gitignore` → adiantado em 24/09 (troca de PC): repo PRIVADO com o que é da disciplina, inclusive `CLAUDE.md` e `docs/`; push conferido com um clone.
- [ ] Lê o programa de um arquivo de texto [EI03 P3a]
- [ ] Gera a sequência de tokens (classe + lexema, com linha e coluna) na tela ou em arquivo [EI03 P3b]
- [ ] Palavra reservada × identificador (tabela de reservadas) [EI03 P2a]
- [ ] Maior casamento: `==` antes de `=`, `>=` antes de `>` etc. [v6 §2, EI03 P2b]
- [ ] Controle de linha e coluna [EI03 P2c]
- [ ] Ignora espaços, quebras de linha e comentários [v6 §2]
- [ ] ⚠ Erro léxico com linha, coluna e lexema, e CONTINUA lendo [EI03 P3c, v6 §7]
- [ ] ⚠ Erro para `@`, identificador começando com dígito (`2abc`), número malformado (`3.4.5`), texto sem fechar aspas e comentário de bloco sem fechar [EI03 P4b]
- [ ] Teste válido cobrindo TODOS os tipos de token [EI03 P4a]
- [ ] Teste com erros léxicos propositais [EI03 P4b]
- [ ] Guardar a saída de cada teste (print ou listagem) para o relatório
### Entrega do EI03: `EI03_NomeCompleto.zip` (ou nomes da dupla)
- [ ] PDF: nome completo, disciplina (GRP00543), professor, título "Estudo Independente 03"
- [ ] P1 ER justificadas · P2 conflitos explicados com a teoria · P3 código · P4 testes com evidências (prints ou listagem)
- [ ] Referências: Menezes cap. 3 (3.1, 3.4, 3.6), Aho cap. 3, Price e Toscani cap. 2.2, Plano de Ensino
- [ ] ⚠ Declaração de IA: ferramenta, finalidade, etapas, como verificamos as ER, fontes usadas para validar, o que o aluno alterou
- [ ] Zip com: PDF + código + arquivos de teste (entrada e saída)
- [ ] Conferir: o zip abre, tem tudo, o PDF está legível e com o nome

## 5. Marco 4 — Parser + AST (até 04/10) — léxico + parser + AST: 3 pts [v6 §4]
- [ ] Parser por descida recursiva: uma função por regra da gramática
- [ ] Monta a AST
- [ ] ⚠ Precedência na própria AST: `2 + 3 * 4` → `2 + (3 * 4)`, e `(2 + 3) * 4` respeitado. O gerador não "conserta" nada [v6 precedência]
- [ ] Opção para mostrar a AST na tela (demo e relatório)
- [ ] ⚠ Erro sintático PARA o processamento e mostra linha, token encontrado e o que era esperado [v6 §4, §7]
- [ ] Todos sabem dizer qual produção reconhece cada estrutura [v6 §4]

## 6. Marco 5 — Semântica, geração de C, testes e relatório (até 07/10)
### Semântica — 2 pts [v6 §5]
- [ ] ⚠ Separada do parser, no código e na explicação
- [ ] Tabela de símbolos com nome e tipo
- [ ] Erro: variável usada antes de ser declarada
- [ ] Erro: variável declarada duas vezes no mesmo escopo
- [ ] Erro: tipos incompatíveis em atribuições e operações (escrever as regras: real recebe inteiro? inteiro recebe real? texto em conta?)
- [ ] Mensagem clara: nome da variável + regra violada [v6 §7]
- [ ] Decidir e documentar os escopos (o critério da nota cita "escopo") [v6 §12]
### Geração de código — 3 pts [v6 §6]
- [ ] Só roda se léxico, sintaxe e semântica passarem
- [ ] Percorre a AST (troca de texto não vale)
- [ ] Tipos e declarações mapeados de forma consistente (ex.: inteiro → `int`, real → `float`/`double`)
- [ ] if/else, laço, expressões, entrada (`scanf`) e saída (`printf`) gerados dos nós da AST, com o formato certo (`%d`, `%f`)
- [ ] ⚠ O C gerado compila no gcc sem erro e se comporta igual ao programa de entrada
- [ ] Roda com qualquer arquivo (`python transpilador.py arquivo`), porque o professor pode pedir teste novo na hora [v6 §11]
- [ ] (se houver aposta/sorte) `srand` com semente fixa
### Suíte de testes — 2,5 pts [v6 §8]
- [ ] `01_valido_basico`: declaração, atribuição e saída
- [ ] `02_valido_completo`: if/else, laço, entrada/saída ⚠ e precedência (`2 + 3 * 4` ou `(2 + 3) * 4`) [v6 §8, aviso]
- [ ] `03_erro_lexico`: símbolo ou lexema inválido
- [ ] `04_erro_sintatico`: estrutura que viola a GLC
- [ ] `05_erro_semantico`: uso sem declarar, redeclaração ou tipos incompatíveis
- [ ] Nos inválidos, aparece a mensagem de erro do PRÓPRIO transpilador
- [ ] Saída esperada de cada teste + um comando que roda todos
- [ ] Os `.c` gerados dos testes válidos, guardados (são entregáveis) [v6 §9]
### Relatório técnico (PDF) [v6 §9, §10, aviso]
- [ ] Tema e objetivos
- [ ] ⚠ As 3 decisões próprias, justificadas
- [ ] Alfabeto Σ + tabela de tokens/ER
- [ ] G = (V, T, P, S) + gramática BNF/EBNF completa
- [ ] Regras semânticas adotadas
- [ ] ⚠ Ferramentas de IA usadas e para quê
### README [v6 §9]
- [ ] Pré-requisitos (Python, gcc), como compilar/rodar, exemplo de uso
- [ ] Código organizado; testar do zero numa pasta limpa

## 7. Apresentação e defesa — 15 pts (ensaio 08/10; data real no item 0.1) [v6 §11, §12]
- [ ] Apresentar a linguagem, a proposta e as características (2)
- [ ] Explicar a especificação léxica, a gramática e as decisões de projeto (3)
- [ ] Demo ao vivo: arquivo → tokens → AST → C → gcc → execução (3)
- [ ] Demo dos casos válidos e dos erros léxico, sintático e semântico (2)
- [ ] ⚠ Arguição individual: todos explicam tokens, produções, AST, semântica e geração (3). O que ninguém souber explicar conta como não demonstrado [v6 §10]
- [ ] Participação de todos (2): roteiro de quem fala o quê
- [ ] Ensaiar pedidos ao vivo: novo teste, explicar uma produção, analisar a AST, corrigir um erro, pequena mudança no código (ex.: novo operador `%`, trocar uma palavra-chave)
- [ ] Testar no computador da sala (Python, gcc, fonte grande no terminal)

## Extras (não obrigatórios)
- [ ] Emojis só na tela do editor (Prettify Symbols Mode / vsc-conceal); testar antes
- [ ] Página visual com o resumo do `novo 1.txt` (adiada pelo usuário)
