# CLAUDE.md — Linguagem temática + transpilador (TP1 de Compiladores)

Resumo de TUDO sobre este projeto. Leia inteiro antes de mexer. O usuário fala português (BR); responda em português, com respostas breves (modo estudo). Criado em 2026-09-23.

- Disciplina: Linguagens Formais e Compiladores (GRP00543) — UNIJUÍ, 2026/2º, turma 01RCOMP-101_6N · Prof. Marcos Ronaldo Melo Cavalheiro
- Pasta: `G:\linguagem do manha` · Python 3.11 (global; ainda sem venv, só biblioteca padrão)
- Git: repositório **PRIVADO** `github.com/eduardomanhabosco/linguagem-do-manha` (branch `main`), criado em 2026-09-24 para trocar de PC. Leva o código, este arquivo, `docs/`, `novo 1.txt`, os materiais da aula e `docs/claude/` (LEIA-ME + cópia da conversa). **Só entra o que é da disciplina** (pedido do usuário). Ter os docs no git é exceção à regra geral do usuário (ver "Decisões").
- Documentos: este arquivo e `docs/` (DEVLOG.md = diário técnico, APRENDIZADOS.md = caderno de termos, MAPA.md = checklist, `enunciados/` = textos do professor, `claude/` = como continuar no PC novo + cópia da conversa)

## Carregados automaticamente ao abrir a sessão
O Claude Code carrega os arquivos abaixo junto com este (imports com `@`; o `\ ` indica o espaço no nome). Todo `.md` novo do projeto entra nesta lista.

Anotações do usuário (resumos, aprendizados, ideias). O arquivo é dele: eu leio e não edito. **Pedidos escritos lá (gerar imagem, montar HTML visual) NÃO devem ser feitos agora**; ele decide depois e pede no chat.
@novo\ 1.txt

Diário técnico, caderno de termos, enunciados e mapa de tarefas:
@docs/DEVLOG.md
@docs/APRENDIZADOS.md
@docs/enunciados/TP1_Linguagem_Tematica_v6.md
@docs/enunciados/classroom.md
@docs/MAPA.md

## Objetivo
Criar uma linguagem de programação temática (inspirada na BIRL) e um transpilador que a traduz para C (ou Python), passando por: código-fonte → léxico → tokens → parser → AST → semântica → código destino. Vale 30 pontos: 15 do produto + 15 da apresentação e defesa (com perguntas individuais). Trabalho em grupo.

## Prazos (conferir no Classroom)
| O quê | Quando | Observação |
|---|---|---|
| EI03: analisador léxico (formativo, sem nota) | **09/10/2026, 19:20** (Aula 9; o texto diz "até 19h15") | **não aceita atraso**; individual ou dupla; vira a base do TP1 |
| TP1 (30 pts) | **provavelmente Aula 9 (09/10)**, a confirmar | o EI03 diz que o projeto de 30 pts é "avaliado na Aula 09"; o enunciado v6 cita a Aula 18 para o "Projeto Integrado de Compilador"; o aviso sugere 4 semanas |
| EI02: ER e autômatos (formativo) | 11/09 (passou; Classroom mostra "Não entregue") | sem nota; ver se ainda aceita entrega |
| Prova escrita individual (Aula 8) | **confirmar** | o texto do EI02 é da turma 4N (prova em 16/09); a sua turma é a 6N. Conteúdo: EI02 e aulas 2 e 3 |

## Estado atual (2026-09-24)
- Só pesquisa, planejamento e estudo. Nenhum código do transpilador ainda.
- `lexico.py`: por enquanto só testes de regex (`=` × `==`); ainda não é o léxico.
- Tema não fechado (ideia mais forte: cassino). Linguagem destino não decidida (recomendado: C).
- Nada testado. **Sem compilador C no PC antigo** (gcc, clang, tcc e cl não encontrados em 23/09); conferir no PC novo e instalar antes da geração de código (MAPA 0.6).
- Fase atual: estudo dos conceitos, um por mensagem (MAPA §1). Vistos: 1 (visão geral) e 2 (GLC). **3 (BNF e EBNF) enviado em 24/09**; perguntar se há dúvidas e seguir para o 4 (derivação).
- **Troca de PC em 2026-09-24:** repo privado no GitHub com tudo o que é da disciplina; commits e push feitos pelo Claude a pedido do usuário e conferidos com um clone de teste. No PC novo: `docs/claude/LEIA-ME.md`.

## Como retomar
1. Abrir o Claude Code **dentro desta pasta** (PowerShell: `cd "<pasta do projeto>"` e depois `claude`). Só assim este arquivo e os imports carregam sozinhos; aberto em outra pasta, nada disso é lido.
2. **PC novo?** Ver `docs/claude/LEIA-ME.md` (instalar, `git clone`, abrir o `claude` dentro da pasta).
3. **Usando dois PCs:** ao começar, `git pull`; ao terminar, commit + `git push` (ver "Fluxo de trabalho").
4. Seguir "Pendências" e o `docs/MAPA.md`.
5. Rodar testes: `python lexico.py` (de dentro da pasta do projeto).

## Estrutura
```
CLAUDE.md               este resumo
.gitignore              ignora __pycache__/
.gitattributes          *.jsonl sem conversão de quebra de linha (para o claude --resume ler a conversa)
novo 1.txt              anotações do usuário (resumos, aprendizados, ideias); só leitura para o Claude
lexico.py               testes de regex; vai virar o analisador léxico
Aula_02_-_Formal_Languages_Aluno.pptx (+ cópia "(1)", mesmo texto)  alfabeto Σ, palavra, ε, Σ*, Σ⁺, concatenação, fecho de Kleene, ∅ × {ε}
aula_03_linguagens_regulares_AlunoV3.pdf   AFD, AFN, AFN-ε, construção de subconjuntos, ER, gramáticas regulares (29 págs.)
docs/DEVLOG.md          diário técnico (também é a base da declaração de uso de IA)
docs/APRENDIZADOS.md    caderno de termos (gatilho "memória")
docs/MAPA.md            checklist de TUDO o que é pedido (com a origem de cada item) + roteiro dos conceitos
docs/enunciados/TP1_Linguagem_Tematica_v6.md   enunciado completo do TP1 (achado no GitHub; ver "Referências")
docs/enunciados/classroom.md                    textos do Classroom: aviso do TP1, EI03 e EI02
docs/claude/            LEIA-ME.md (como continuar no PC novo) e conversa-2026-09-23.jsonl (cópia da conversa de 23–24/09)
```

## O que o trabalho exige
Checklist completo em `docs/MAPA.md` (carregado acima): cada exigência do enunciado v6, do aviso e do EI03 vira um item, com a origem. **Seguir à risca: nada do que é pedido pode ficar de fora.** Nota (30): produto 15 (léxico 2 · gramática 2,5 · léxico + parser + AST 3 · semântica 2 · geração 3 · testes 2,5) + apresentação e defesa 15.

## Decisões (e por quê)
- **Léxico e parser à mão, em Python** (parser por descida recursiva), sem PLY/Flex: na defesa o professor pede explicações e mudanças ao vivo, e código próprio é mais fácil de explicar. O enunciado permite ferramentas, mas escolhemos não usar.
- **Sorte/aposta só dentro da linguagem, nunca no transpilador:** sortear ou apagar partes do código quebra a exigência de preservar o comportamento e a comparação com a saída esperada dos testes. Se houver um comando de aposta, o C gerado usa `rand()` com `srand(semente fixa)`.
- **Emojis, se usados, só na tela do editor** (extensões Prettify Symbols Mode ou vsc-conceal). Motivos: digitar emoji ao vivo é lento, alguns emojis são vários caracteres Unicode (❤️ = U+2764 + U+FE0F) e o terminal do Windows pode mostrar `?`. O léxico só vê texto. **Não testado.**
- **Maior casamento pela ordem das regras:** à mão, as regras são testadas em ordem e fica a primeira que casa, então os operadores longos (`==`, `>=`, `<=`, `!=`) vêm antes dos curtos.
- **Palavra reservada × identificador (planejado):** casar como identificador e depois consultar a tabela de palavras reservadas (é a resposta do EI03, problema 2a).
- **Repositório privado com os docs (2026-09-24):** para trocar de PC, um `git clone` leva código, docs, anotações, materiais e a conversa. Por ser privado, não há exposição pública. Isso abre exceção à regra geral do usuário (`CLAUDE.md`, `docs/` e APRENDIZADOS fora do GitHub), pensada para repositórios públicos. **Só entra o que é da disciplina:** a config geral do Claude e outros projetos ficaram de fora (pedido do usuário). **Antes de abrir o repo ao grupo ou deixá-lo público:** tirar do histórico `CLAUDE.md`, `docs/`, `novo 1.txt` e os materiais da aula (ou criar um repo novo só com o código). Descartadas: repo só com código + .zip à parte; só .zip.
- **Descartadas:** transpilador que sorteia/apaga código; emoji obrigatório na sintaxe.

## Em aberto
- Tema. Ideia mais forte: cassino (ex.: `ABRE_MESA`/`FECHA_MESA`, `FICHA`, `GIRA_ROLETA`, `SE_DER`/`SE_NAO_DER`, `MOSTRA_CARTA`).
- Linguagem destino: C (referência do enunciado; recomendado) ou Python (precisa justificar e avisar o professor no Marco 1).
- As 3 decisões próprias de sintaxe.
- Integrantes do grupo.

## Aprendizados e cuidados
- **Notação de ER:** nos slides do professor, `+` é **união** (`(a + b)*`), mas `digit+` aparece como "um ou mais". No Python e no JFlex, união é `|` e `+` é "um ou mais". No relatório, dizer qual notação usamos.
- **`2abc` e `3.4.5`:** sem uma regra própria, o léxico quebra em `NUM(2) ID(abc)` e `NUM(3.4) ...` em vez de dar erro. O EI03 pede erro nesses casos.
- **Lex/Flex** fazem o maior casamento sozinhos (a ordem só desempata). **Rexical e léxico à mão com `re`** dependem da ordem. A alternância `|` do `re` também fica com a primeira opção que serve: `re.match(r"=|==", "==")` devolve `=`.
- **Token = par [tipo, lexema].** O exemplo "Caipires" de um blog tinha erro de digitação (`['(', ')']` no lugar de `['(', '(']`).
- **Blog do Sérgio Miranda ("Caipires") × TP1:** cobre léxico, parser/AST e compilador. Runtime, interpretador e máquina virtual não entram no TP. **Faltam no blog:** semântica, tratamento de erros, especificação formal (Σ, tokens/ER, G = (V,T,P,S)), precedência, recursão à esquerda, maior casamento e geração de C. **Erro no blog:** a lista das classes de Chomsky traz "recursiva" no lugar de "sensível ao contexto".
- **Erro sintático × semântico, o teste dos tokens:** troque cada nome e número pelo tipo do token (`x` → `id`, `5` → `num`). Se o erro continua visível, é sintático; se sumiu, é semântico. `CE_QUER_VER (x);` e `CE_QUER_VER (y);` viram a mesma sequência de tokens, então o parser não tem como saber se `y` foi declarada. Teoria: "declarar antes de usar" não é livre de contexto (linguagem {wcw}); o Aho trata disso no cap. 4 (seção 4.3.5 da 2ª ed., pela memória do Claude — **conferir no livro antes de citar**).
- **EBNF:** `{ }` = zero ou mais, `[ ]` = opcional, `( | )` = agrupar. Não descreve nenhuma linguagem a mais que a BNF, só abrevia. `"("` com aspas é token; `(` sem aspas é da notação. Cada pedaço vira código: `<Nome>` → chamar função, `{ }` → `while`, `[ ]` → `if`.
- **Regra "pega-tudo" (`.`):** no Rexical, `. { [text, text] }` transforma QUALQUER caractere em token, então um `@` seria aceito. No nosso léxico, cada símbolo tem regra e nome próprios (`ABRE_PAREN`, `MAIS`...) e o "qualquer outro caractere" vira **erro léxico** (linha, coluna e lexema), e a leitura continua (EI03, P3c).

## Referências e links
- **Enunciado completo:** `docs/enunciados/TP1_Linguagem_Tematica_v6.md`, copiado do repositório público de outro grupo da turma ([ChristianGCa/transpilador-starwars](https://github.com/ChristianGCa/transpilador-starwars), arquivo adicionado em 18/09/2026). **Comparar com o PDF anexo do Classroom** (pode haver versão mais nova).
- **Outros exemplos (só referência, não copiar):** transpilador-starwars (Python → C, mesma disciplina), [BagualScript](https://github.com/lucasarenhardt/BagualScript) (Flex/Bison), [WakeUp-Lang](https://github.com/GetulioVictor/WakeUp-Lang) (→ Python), [WizardScript](https://github.com/LuahnKaye/trab-compiladores) (→ C++), [golscript](https://github.com/gabrielcamargo01/golscript), [transpylar](https://github.com/andermoreira/transpylar).
- **BIRL:** https://birl-language.github.io/ · https://github.com/birl-language/birl-server
- **Teoria:** [freeCodeCamp PT](https://www.freecodecamp.org/portuguese/news/escrevi-uma-linguagem-de-programacao-e-voce-tambem-pode/) · [Compiladores para Humanos](https://johnidm.gitbooks.io/compiladores-para-humanos/content/) · [LabCompl (UFES)](https://www.inf.ufes.br/~tavares/labcomp2000/intro2.html) · [Wikiversidade: Análise Léxica](https://pt.wikiversity.org/wiki/Introdu%C3%A7%C3%A3o_%C3%A0_Teoria_dos_Compiladores/An%C3%A1lise_L%C3%A9xica) · [blog Sérgio Miranda](http://sergiohenriquemiranda.com.br/blog/como-funcionam-as-linguagens-de-programacao) · [Crafting Interpreters, cap. 6](https://craftinginterpreters.com/parsing-expressions.html) · [Ruslan Spivak, parte 7](https://ruslanspivak.com/lsbasi-part7/)
- **Emojis no editor:** [Prettify Symbols Mode](https://marketplace.visualstudio.com/items?itemName=siegebell.prettify-symbols-mode) · [vsc-conceal](https://github.com/rocq-community/vsc-conceal)
- **Livros da disciplina:** Menezes (2011) cap. 3 · Aho, Sethi e Ullman (2007) cap. 3 · Price e Toscani (2001) cap. 2.2.

## Ideias (apresentação e futuro)
- **Metáfora do léxico (do usuário):** um separador de moedas, ou uma "cascata": os caracteres rolam e cada pedaço cai no buraco do seu tipo de token. `==` × `=`: se o buraco do `=` vier antes, o `==` "cai no buraco errado" e vira dois tokens. Serve para slide e para a arguição.
- **Página visual (HTML) com imagens** resumindo o `novo 1.txt`: pedida lá, **adiada pelo usuário em 2026-09-23**. Não fazer até ele pedir de novo no chat.
- Demonstração de token × lexema com emojis como apelido (dois lexemas, mesmo token), se a ideia dos emojis for usada.

## Pendências
Tudo está no `docs/MAPA.md`; marcar `[x]` lá quando o item ficar pronto e testado. Ordem agora: dúvidas do conceito 3 → conceitos 4 a 13 (MAPA §1) → itens 0.x (confirmar prazos e grupo, instalar gcc no PC em uso) → Marco 1.

## Riscos / cuidados
- **Originalidade e plágio:** o repositório do outro grupo é público e da mesma turma. Usar só como referência de formato; o professor faz perguntas individuais e pede mudanças ao vivo.
- **Declaração de IA obrigatória** (TP1, EI02, EI03): ferramenta, finalidade, etapas, como verificamos, fontes e o que o aluno alterou. O DEVLOG registra isso ao longo do projeto.
- **Todos precisam dominar tudo:** a arguição é individual, e trecho que ninguém souber explicar conta como não demonstrado.

## Fluxo de trabalho (IMPORTANTE)
- **O usuário roda os comandos** (python, git) e traz a saída; **eu edito/crio os arquivos direto no disco** (copiar código do terminal traz 2 espaços de margem e quebra a indentação do Python).
- **Modo estudo** (regra geral do usuário, escrita aqui para valer em qualquer PC): passos pequenos; o usuário roda os comandos; respostas **breves** em PT-BR simples (termo novo = 2–3 linhas + exemplo); documentar tudo. Gatilho **"memória"** (ex.: "memória: o que é token") → nova entrada em `docs/APRENDIZADOS.md` no formato `## termo  (data)` / `**O que é:**` / `**Explicação:**`, confirmando em uma linha. Desligar só se ele disser "desativa modo estudo".
- **Decisões já tomadas:** se ele perguntar algo já decidido (às vezes como teste, como a "pegadinha" do Flex), abrir a resposta pela decisão registrada em "Decisões", sem perguntar de novo se mantém.
- **Escopo:** trabalhar só neste projeto; não mexer nem vasculhar outros projetos do PC sem pedido explícito.
- **Modo aula** (pedido em 2026-09-23): o usuário pergunta sobre tudo o que vamos usar, intercalado com código. Explicar no estilo do blog (texto corrido + um exemplo que acompanha; exemplo: a BIRL-Lite do enunciado), **um conceito por mensagem**, na ordem do MAPA §1, terminando com "dúvidas?" e o nome do próximo. Léxico já foi visto (pular).
- **À risca:** nada do que o enunciado, o aviso ou o EI03 pedem pode faltar. Antes de dar uma parte por pronta, conferir os itens do MAPA com a origem.
- **Antes de todo commit:** pente fino no que vai ao GitHub. **Padrão de commit** ([iuricode/padroes-de-commits](https://github.com/iuricode/padroes-de-commits)): `:emoji: tipo: Descrição`, título curto (~4 palavras), detalhes no corpo, um commit por assunto. Tipos: `feat` :sparkles: · `fix` :bug: · `docs` :books: · `refactor` :recycle: · `perf` :zap: · `build` :package: · `chore` :wrench: · `style` :lipstick: · `cleanup` :broom: · `remove` :wastebasket: · `test` :test_tube: · primeiro commit `:tada: init`.
- **Anotar TUDO o que for programado** (pedido do usuário em 2026-09-23): registrar no DEVLOG o que foi feito, por quê, como testamos (comando + saída), os erros e as correções, e a linha da tabela de uso de IA. Esse material vira o relatório, o README, o roteiro da apresentação e a declaração de IA. O estado resumido fica neste arquivo. **Checkpoint de documentação a cada 9 trocas de mensagens** (pedido do usuário em 2026-09-23): atualizar DEVLOG, APRENDIZADOS, MAPA e este arquivo, e avisar numa linha; também ao encerrar/pausar e quando ele pedir. Último checkpoint: 2026-09-24 (troca de PC; conceitos 2 e 3).
- **Git (repo privado):** commits no padrão acima, com a linha `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>` no fim quando o Claude ajudou (reforça a transparência no uso de IA que o professor exige). **Só entra o que é da disciplina** (pedido do usuário em 24/09); `__pycache__/` fica fora. Em geral o usuário roda `git add/commit/push`; na troca de PC (24/09) ele pediu que o Claude fizesse.

## Histórico
- 2026-09-23: primeira conversa. Busca na web (enunciado completo achado no GitHub, exemplos, teoria), ideias de tema (cassino, emojis), dúvidas de léxico (token/lexema, Rexical, Lex, maior casamento), montagem desta documentação e dos imports. Detalhes no DEVLOG.
- 2026-09-24: conceitos 2 (GLC) e 3 (BNF/EBNF); dúvida sintático × semântico; "pegadinha" do Flex; troca de PC com repo privado (só o que é da disciplina). A conversa, até o pedido de commit, está em `docs/claude/conversa-2026-09-23.jsonl`.
