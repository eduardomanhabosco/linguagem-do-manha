# DEVLOG — Linguagem temática + transpilador (TP1)

Diário técnico. Fonte para: relatório, **declaração de uso de IA**, README e apresentação.
Formato de cada entrada: **Data · Problema/decisão · O que tentamos · Resultado · Aprendizado**.

## 2026-09-23 · Pesquisa inicial e ideias
- **Pedido:** achar na web material sobre o trabalho (linguagem temática + transpilador), de preferência em PT-BR.
- **Achado principal:** o enunciado completo (v6) estava no repositório público de outro grupo da mesma turma (`ChristianGCa/transpilador-starwars`, arquivo adicionado em 18/09/2026). Copiado para `docs/enunciados/`. Ele traz o que o aviso do Classroom não diz: C como destino de referência, análise semântica obrigatória, 5 testes mínimos, 3 decisões próprias e declaração de IA.
- **Outros exemplos:** BagualScript (Flex/Bison), WakeUp-Lang (→ Python), WizardScript (→ C++), golscript, transpylar; a BIRL original traduz para C e compila com gcc.
- **Teoria:** freeCodeCamp PT, Compiladores para Humanos, LabCompl (UFES), Wikiversidade, Crafting Interpreters (cap. 6), Ruslan Spivak (parte 7).
- **Tema:** cassino é a ideia mais forte. Transpilador que sorteia/apaga código foi **descartado** (quebra "preservar o comportamento" e os testes com saída esperada). Alternativa: comando de aposta com `srand(semente fixa)`.
- **Emojis:** digitar ao vivo é lento, há emojis com vários code points e o console do Windows pode quebrar. Ideia: mostrar emoji só no editor (Prettify Symbols Mode / vsc-conceal). **Não testado.**
- **Dúvidas de léxico estudadas:** exemplo "Caipires" com erros (`['(', ')']` → `['(', '(']`; o léxico não muda maiúsculas); token = [tipo, lexema]; Rexical (macro × rule, `text`, regra `.` → `[text, text]`); maior casamento (`=` × `==`).
- **Correção feita pela IA:** primeiro ela disse que a ordem das regras decide `=` × `==` em qualquer léxico. No Lex/Flex o maior casamento é automático (a ordem só desempata); a ordem importa no léxico feito à mão e no Rexical.
- **Decisão:** léxico e parser à mão em Python (descida recursiva), sem PLY/Flex, porque é mais fácil de explicar e alterar na defesa.
- **Material na pasta:** slides da Aula 02 (duas cópias com o mesmo texto) e PDF da Aula 03 (29 págs.). Os slides usam `+` para união nas ER.
- **Prazos vistos no Classroom:** EI03 até 09/10, 19:20 (sem atraso); o TP1 provavelmente é no mesmo dia (a confirmar).
- **Aprendizado:** ler o enunciado completo antes de começar. O aviso do Classroom omitia metade dos requisitos.

## 2026-09-23 · Documentação que carrega sozinha
- **Pedido do usuário:** anotar tudo o que for programado (vai para o relatório, a apresentação e a declaração de IA); carregar o `novo 1.txt` (anotações dele) e todos os `.md` ao abrir a sessão; não gerar agora as imagens pedidas no `novo 1.txt`.
- **O que fizemos:** imports com `@` no `CLAUDE.md`, recurso do Claude Code que carrega os arquivos ao abrir. Um pedido escrito ("leia X") não garante nada: o Claude só lê se decidir abrir o arquivo.
- **Problema:** o espaço no nome `novo 1.txt`. A documentação não fala de espaço. No programa instalado (`claude.exe`), o leitor de imports usa a regex `(?:^|\s)@((?:[^\s\\]|\\ )+)` e troca `\ ` por espaço, então `@novo\ 1.txt` funciona.
- **Teste:** reproduzimos o leitor (mesma regex + biblioteca `marked` 18) e rodamos no `CLAUDE.md`. Resultado: 5 de 5 arquivos achados, nenhum import acidental, ~63 KB (~18 mil tokens) carregados por sessão. Teste negativo: `@novo 1.txt` sem a barra tenta importar "novo" e falha.
- **Cuidado:** só funciona com o Claude Code aberto dentro de `G:\linguagem do manha`. Os arquivos são lidos só ao abrir a sessão.
- **Lendo o `novo 1.txt`:** a regra pega-tudo do Rexical (`. { [text, text] }`) não serve para o nosso léxico, porque aceitaria `@` como token. No nosso, ela vira erro léxico.
- **Ideia do usuário para a apresentação:** o léxico como separador de moedas (cada buraco é um tipo de token; `==` × `=` = "cair no buraco errado").
- **Aprendizado:** quando a documentação não responde, o próprio programa pode responder (achar o trecho que faz o trabalho e testar uma cópia dele).

## 2026-09-23 · Blog "Caipires" comparado com o enunciado
- **Pergunta do usuário:** o que o blog do Sérgio Miranda explica é o que o trabalho exige?
- **Resultado:** léxico, parser/AST e compilador, sim. Runtime, interpretador e máquina virtual, não (são extras). Faltam no blog: semântica, erros, especificação formal, precedência, recursão à esquerda, maior casamento e geração de C. O blog usa ferramentas (Rexical e Racc); nós faremos à mão (descida recursiva).
- **Erros achados no blog:** classes de Chomsky ("recursiva" no lugar de "sensível ao contexto"); `['(', ')']`; "programa teste" × "programa de teste".

## 2026-09-23 · Mapa de tarefas e jeito de trabalhar
- **Pedido:** um mapa de tudo o que precisamos fazer.
- **Feito:** `docs/MAPA.md`, checklist montado linha por linha do enunciado v6, do aviso e do EI03, com a origem de cada item ([v6 §N], [aviso], [EI03 Pn]), pontos e datas sugeridas (contando com 09/10). Carrega sozinho pelo `CLAUDE.md`. As seções "O que o trabalho exige" e "Pendências" do `CLAUDE.md` passaram a apontar para ele, para não haver duas listas.
- **Achados:** não há compilador C no PC (procurados gcc, clang, tcc e cl) → item 0.6. Os documentos do outro grupo (README, RELATORIO, ROTEIRO) não citam datas. O texto do EI02 é da turma 4N (a do usuário é a 6N) → confirmar a data da prova.
- **Regras novas do usuário:** seguir o enunciado à risca (nada pode faltar); checkpoint de documentação a cada 9 trocas de mensagens; modo aula: conceitos um por mensagem, no estilo do blog, com o usuário perguntando; léxico já visto.
- **Roteiro dos conceitos:** 13 (MAPA §1), com a BIRL-Lite do enunciado como exemplo. Conceito 1 (visão geral: as estações do transpilador) enviado.
- **Tropeço:** o script Python que editou o `CLAUDE.md` gravou quebras de linha do Windows (CRLF), e o diff mostrou o arquivo inteiro como mudado. Voltamos para LF e conferimos que só mudaram as linhas pretendidas.

## 2026-09-24 · Conceitos 2 e 3, dúvida sintático × semântico, troca de PC
- **Pegadinha do usuário:** perguntou se o trabalho permite Flex, já sabendo que decidimos não usar. A IA respondeu certo (permite: "Lex/Yacc ou equivalentes", v6 §4), mas citou a decisão só no fim e ainda perguntou "mantemos?". **Aprendizado:** abrir pela decisão registrada e não reabrir o que já foi decidido.
- **Conceito 2 (GLC):** G = (V, T, P, S) com uma mini gramática da BIRL-Lite; derivação de exemplo; recursão (a variável "no meio" conta parênteses, o aⁿbⁿ do slide 12 da Aula 3); por que "livre de contexto"; dois níveis (léxico = Tipo 3 sobre caracteres, parser = Tipo 2 sobre tokens).
- **Dúvida do usuário:** a semântica (checar se `y` foi declarada) e o parser (contar parênteses) pareciam a mesma coisa. **Resposta:** o teste dos tokens. Trocando os nomes pelos tipos, `CE_QUER_VER (x);` e `CE_QUER_VER (y);` viram a mesma sequência, então o parser não distingue e o erro é semântico. Já `((2))` × `((2)` muda os tokens, então o erro é sintático. Analogia: parêntese faltando é erro de forma; "Ele sentou" sem apresentar quem é "ele" é erro de sentido (tabela de símbolos = lista de personagens). Teoria: "declarar antes de usar" não é livre de contexto ({wcw}); o número da seção do Aho (4.3.5) não foi confirmado online.
- **Conceito 3 (BNF/EBNF):** os símbolos, a mini gramática em BNF, os atalhos da EBNF, leitura linha a linha da gramática da BIRL-Lite, a pegadinha `"("` × `(`, e como a EBNF vira código de descida recursiva.
- **Troca de PC:** o usuário pediu para commitar tudo e manter a conversa. O G: é um HD interno (SATA), então não dá para levar o disco. Git 2.45 configurado; sem `gh`. **Decisão (usuário):** repo **privado** com os docs, exceção à regra "docs fora do git". Pente fino: nada sensível nos arquivos do projeto (grep de nomes, senhas, e-mails e tokens: 0 ocorrências); a cópia da conversa contém o e-mail da UNIJUÍ (saída de um comando), aceitável por ser privado.
- **Correção do usuário (escopo):** entendi o "leva tudo" como incluindo outros projetos do PC e comecei a levantá-los. Ele interrompeu: "não commita nada que não seja em relação a isso da matéria". Por isso o `docs/claude/` ficou só com o LEIA-ME e a cópia desta conversa (a config geral do Claude ficou de fora), e as regras que valem para este trabalho (modo estudo, padrão de commit, decisões já tomadas, escopo) foram escritas no `CLAUDE.md` do projeto. **Aprendizado:** "tudo" = tudo do projeto atual.
- **Conversa:** `docs/claude/conversa-2026-09-23.jsonl`, copiada antes do pedido de commit. A documentação oficial confirma que `claude --resume <caminho do .jsonl>` retoma uma conversa a partir do arquivo.
- **Commits** (feitos pelo Claude, a pedido do usuário): `:tada: init`, `:books: docs` (enunciados e materiais), `:books: docs` (documentação e anotações) e `:wrench: chore` (conversa com o Claude), todos com `Co-Authored-By` do Claude.
- **Commit extra:** `.gitattributes` com `*.jsonl -text`. No Windows, o Git trocaria as quebras de linha (LF → CRLF) da cópia da conversa ao baixar, o que podia atrapalhar o `claude --resume`.
- **Push:** OK, 5 commits (`bd4a16b` a `6cbdb0d`), mais um último com este registro. **Teste:** clone numa pasta temporária: mesmo commit do GitHub, os 15 arquivos iguais aos originais, slides e PDF idênticos byte a byte, `.jsonl` idêntico (909 linhas JSON válidas) e os imports do `CLAUDE.md` carregando.

## 2026-09-24 · Conceitos 3 a 8 (de volta ao PC antigo)
- **Retomada:** o usuário voltou ao PC antigo. `git fetch` mostrou o GitHub igual ao local, então não havia nada a baixar. O conceito 3 foi reenviado, porque tinha ido logo antes da troca.
- **Dúvidas no conceito 3:** (1) `"("` × `(`: com aspas é token e aparece no programa; sem aspas só agrupa na notação. Exemplo: sem o agrupamento, a regra do `<Escrita>` aceitaria `CE_QUER_VER ("oi"` sem fechar. (2) OpRel = operador relacional (compara e dá verdadeiro/falso) × aritmético (faz conta) × lógico (E/OU/NÃO, junta comparações). A `<ExprLogica>` da BIRL-Lite só aceita uma comparação; o EI03 pede os lógicos no léxico → **recomendação:** pôr na gramática também.
- **Conceito 4 (derivação):** ⇒, ⇒*, forma sentencial, sentença; derivação mais à esquerda × mais à direita = mesma árvore; árvores de `2 + 3 * 4` e `(2 + 3) * 4`.
- **Conceito 5 (ambiguidade e precedência):** `E → E + E | E * E` dá duas árvores (14 × 20); os "andares" Expressao/Termo/Fator, com os parênteses como "elevador"; tabela de andares incluindo os lógicos; o "else pendurado" e como um fechamento explícito o evita.
- **Conceito 6 (associatividade e recursão à esquerda):** `10 - 3 - 2`; a árvore pende para o lado da recursão; recursão à esquerda → `RecursionError` na descida recursiva; `{ }` = `while` que acumula à esquerda; a transformação do livro `A → β A'`, `A' → α A' | ε`; recursão à esquerda indireta.
- **Conceito 7 (descida recursiva):** parser de exemplo (~90 linhas, subconjunto da BIRL-Lite) mostrado **no chat, não salvo em arquivo**; LL(1), conjunto PRIMEIROS, fatoração à esquerda; como o `BIRL` pode fechar três coisas. Dica de projeto: cada comando começa com a sua própria palavra-chave.
- **Conceito 8 (erros sintáticos):** onde o erro é detectado (no `consome` e nos pontos de escolha); mensagem = linha, coluna, encontrado e esperado; tokens passam a levar linha e coluna; classe `ErroSintatico`; o `;` esquecido (apontar a linha do token anterior); o léxico continua e o parser para.
- **Achado "à risca":** o aviso do Classroom diz "analisador sintático funcionando, **com árvore de derivação**", e o v6 pede AST. Para cobrir os dois, entrou no MAPA uma opção que imprime a árvore de derivação (as chamadas do parser, indentadas), além da AST.

## 2026-09-25 · Conceitos 9 a 13, resumo visual e decisões do grupo
- **Conceitos 9 a 13:** AST (dataclasses com a linha em cada nó); semântica (tabela de símbolos, escopo por bloco com uma pilha de tabelas, sombreamento a decidir); tipos (de baixo para cima, promoção, pelo menos um "❌", divisão inteira do C); geração de C (mapa AST → C, parênteses sempre, prefixo `v_`, `printf("%s")` para texto, `float` para o `scanf` usar `%f`); compilador × transpilador × interpretador (o Cfront gerava C). Terminada a fase de estudo.
- **Resumo visual** (pedido do usuário): `docs/resumo-conceitos.html` + versão online privada (https://claude.ai/artifact/25wcNyj8hd6nGu1x7vgBuZ). Segue a estrutura do `novo 1.txt`, com as anotações dele, os 2 prints do "else pendurado" (ALGOL 68 e C/C++), o vídeo de Pratt parsing (com aviso: não é a técnica que usamos), um desenho do "separador de moedas" do léxico e uma pergunta de arguição por conceito. Corrigida uma anotação: a regra `. → [text, text]` não será usada.
- **Seção D no MAPA:** as decisões que o grupo precisa tomar estavam espalhadas pelos conceitos; foram reunidas em D1 a D6 (53 itens, 26 com recomendação), incluindo o rascunho das regras semânticas R1 a R11.
- **Commit e push** feitos pelo Claude a pedido do usuário.

## 2026-09-25 · Decisões fechadas e primeira versão do código (ainda não testada)
- **Pasta nova:** `C:\Users\manha\Downloads\compilador\linguagem-do-manha`. Neste PC há gcc 4.9.2 (`C:\MinGW\bin`); o **Python não funciona** (o `python` abre a Microsoft Store e a pasta do 3.12 está sem `python.exe`). O usuário vai instalar.
- **Decisões (MAPA §D, todas em 25/09, em 7 rodadas de perguntas):** tema **Gambiarra**, com as palavras do repositório de um colega do grupo (`Gabeez11/gambiarra-transpiler`). Por pedido do usuário, foram copiadas **só as palavras**; nada da lógica, porque ele não confia que o código de lá siga as regras. Destino C; tipos inteiro, real e lógico (o lógico veio de `firme`/`quebrado`); `remendo` sem tipo escrito, com o tipo deduzido do valor; `%` só entre inteiros; sem aposta; extensão `.gam`; comentários `//` e `/* */`; `!` com a precedência do C; menos unário; `mostra` com vários itens; sombreamento permitido; `7/2 = 3`; condição só lógica; semântica lista todos os erros; lógico impresso como `firme`/`quebrado`; `%g`; `mostra` sempre pula linha; `pega` só numérico; um arquivo por estação; testes com saída esperada.
- **Código escrito:** `tokens.py`, `erros.py`, `lexico.py` (tabela de regras testadas em ordem, regras de erro que continuam a leitura), `ast_nos.py`, `parser.py` (descida recursiva, AST + árvore de derivação), `semantico.py` (pilha de escopos, R1 a R12), `gerador.py`, `transpilador.py`, `rodar_testes.py`, 9 testes em `testes/`, `README.md` e `docs/ESPECIFICACAO.md` (base do relatório). O `lexico.py` antigo foi para `estudo/regex_igual.py`.
- **Achado no desenho:** com sombreamento, `remendo x = x + 1;` dentro de um bloco lê o `x` de fora (R9). Em C, `int v_x = v_x + 1;` leria o `x` novo, ainda sem valor. Por isso a semântica dá um nome novo à variável de dentro (`v_x_2`).
- **Testado até agora:** só o C. Escrevemos à mão o C que o gerador deve produzir para os testes 02 e 07 e passamos no `gcc -Wall`: **zero avisos**, e com a entrada 4 a saída bateu com a esperada (`a = 14, b = 20, c = 5`, `media = 8.5`, `soma = 10`, `x de dentro: 11`). **O Python ainda não rodou nenhuma vez.**
- **Python instalado pelo Claude**, a pedido do usuário: `winget install Python.Python.3.12 --scope user` (3.12.10).
- **Primeira execução (`rodar_testes.py --mostrar`):** 8 de 9 saídas certas de primeira. O 06 acusou "escape inválido": o heredoc do bash que criou o arquivo transformou `\\` em `\`, então o erro era do arquivo, e o léxico acusou certo. Corrigido o arquivo, conferidas as saídas à mão (contra os comentários "Saída esperada" e as regras), gravados os gabaritos: **9 de 9 OK**. `--ast`, `--c` e `--derivacao` também conferidos (a AST do teste 08 ficou igual à do enunciado).
- **Dúvida do usuário:** "o código não teria que ser em C?". Não: C é a linguagem **destino** (o que o transpilador gera); a linguagem em que ele é escrito é livre (v6 §4 cita até ANTLR/JFlex/Yacc). A justificativa do v6 §1 vale só para trocar o **destino**.

## 2026-09-25 · Entregáveis: relatório, EI03, roteiro
- **Integrantes:** Eduardo (Manhabosco), Rafael, Felipe e Gabriel (sobrenomes a completar em `entrega/montar_entrega.py`).
- **Bug achado:** um `.gam` salvo pelo PowerShell (ou pelo Bloco de Notas) começa com BOM (U+FEFF), e o léxico acusava "caractere que não pertence à linguagem" na linha 1, coluna 1. **Correção:** ler com `encoding="utf-8-sig"` (transpilador, lexico e rodar_testes). Teste novo: `09_valido_com_bom.gam`. Seria um tropeço na demo ao vivo se o arquivo fosse criado na hora.
- **Cosmético:** a última folha da árvore de derivação (token FIM, sem lexema) saía vazia; agora mostra `FIM (fim do arquivo)`.
- **Casos-limite testados à mão** (não viraram teste): programa vazio; variável de dentro do `se` usada fora (R3); `1 < 2 < 3` (erro sintático); bloco sem fechar; conteúdo depois do `}` final; texto dentro de expressão; `- -3`; `7.0 / 2`; lógicos com `== !=`; `se` dentro de `enquanto` com `%`. Todos com o comportamento esperado.
- **Suíte:** 10 de 10.
- **Entregáveis:** `entrega/montar_entrega.py` gera, a partir de `entrega/modelos/*.html`, o `Relatorio_TP1_Gambiarra.pdf` e o `EI03_EduardoManhabosco.pdf` + `.zip` (PDF, léxico, 2 testes e a saída de cada um). As evidências vêm da execução real na hora de gerar, então basta rodar o script de novo se o código mudar. PDF feito pelo Edge headless (`--print-to-pdf`). O zip foi conferido (`testzip`) e o HTML revisado por print.
- **EI03 é individual ou em dupla:** o grupo tem 4 pessoas, então cada dupla (ou pessoa) gera o seu, trocando `INTEGRANTES_EI03` no script. O gerado agora está no nome do Eduardo.
- **Campos em amarelo `[PREENCHER]`** nos PDFs: livros efetivamente consultados e alterações feitas pelo grupo. A IA não pode inventar isso.
- **Roteiro:** `docs/ROTEIRO_APRESENTACAO.md`. Gabriel: abertura/tema/decisões; Eduardo: léxico; Rafael: gramática/parser; Felipe: semântica/geração/testes. Traz os comandos da demo, receitas para pedidos ao vivo e perguntas prováveis.
- **MAPA:** 161 itens `[x]`. Abertos: itens 0.x (confirmar datas e EI03 em Python), mostrar o marco ao professor, todos dominarem o código, teste numa pasta limpa, apresentação.

## Uso de IA (para a declaração obrigatória)
| Data | Ferramenta | Finalidade | Etapa | Como verificamos | O que o aluno fez/alterou |
|---|---|---|---|---|---|
| 2026-09-23 | Claude Code (Claude Opus 5.5, Anthropic) | busca de material na web; explicação de conceitos (token, lexema, maior casamento, Lex/Rexical) | pesquisa / antes do Marco 1 | (preencher) | (preencher) |
| 2026-09-23 | Claude Code (Claude Opus 5.5, Anthropic) | organização da documentação do projeto (CLAUDE.md, DEVLOG, APRENDIZADOS) | planejamento | (preencher) | (preencher) |
| 2026-09-23 | Claude Code (Claude Opus 5.5, Anthropic) | mapa de tarefas a partir do enunciado; explicação dos conceitos (modo aula) | planejamento / estudo | (preencher) | (preencher) |
| 2026-09-24 | Claude Code (Claude Opus 5.5, Anthropic) | explicação de GLC e BNF/EBNF; preparo do repositório privado para trocar de PC | estudo / organização | (preencher) | (preencher) |
| 2026-09-24 | Claude Code (Claude Opus 5.5, Anthropic) | explicação dos conceitos 4 a 8 (derivação, ambiguidade, associatividade, descida recursiva, erros sintáticos), com código de exemplo | estudo | (preencher) | (preencher) |
| 2026-09-25 | Claude Code (Claude Opus 5.5, Anthropic) | explicação dos conceitos 9 a 13; resumo visual a partir das anotações do aluno; lista de decisões do grupo | estudo / organização | (preencher) | (preencher) |
| 2026-09-25 | Claude Code (Claude Opus 5.5, Anthropic) | perguntas para fechar as decisões (o aluno escolheu cada uma); primeira versão do código do transpilador, testes, README e especificação | implementação (Marcos 2 a 5) | C gerado conferido no gcc; o Python ainda não rodou (preencher após os testes) | (preencher) |
