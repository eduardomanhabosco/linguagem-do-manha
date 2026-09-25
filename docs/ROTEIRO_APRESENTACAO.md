# Roteiro da apresentação e defesa (15 pts)

Critérios [v6 §12.2]: clareza (2) · léxico, gramática e decisões (3) · demo (3) · casos válidos e os 3 tipos de erro (2) · arguição individual (3) · participação de todos (2).
**Todos falam, e todos precisam saber responder sobre TODAS as partes**: a pergunta pode ir para qualquer um, e o que ninguém souber explicar conta como não demonstrado [v6 §10].

## Divisão (~15 min + perguntas)
| Quem | Parte | Arquivos que tem que dominar | Demo |
|---|---|---|---|
| **Gabriel** | Abertura: tema Gambiarra, as palavras (vieram dele), tabela de comandos, as 3 decisões próprias | `docs/ESPECIFICACAO.md` §0–1 | abre `testes/01_valido_basico.gam` e roda com `--executar` |
| **Eduardo** | 1. Léxico: Σ, tabela de tokens/ER, maior casamento, reservada × identificador, linha/coluna, erros que continuam | `lexico.py`, `tokens.py` | `--tokens` no 01; teste 03 (8 erros de uma vez) |
| **Rafael** | 2. Gramática e parser: G = (V,T,P,S), EBNF, precedência em andares, sem recursão à esquerda, LL(1), derivação × AST, erro sintático | `parser.py`, `ast_nos.py` | `exemplos/precedencia.gam --derivacao --ast`; testes 04 e 04b |
| **Felipe** | 3 e 4. Semântica e geração: tabela de símbolos, escopo, R1–R12, AST → C, gcc; fechamento com a suíte | `semantico.py`, `gerador.py`, `transpilador.py` | teste 05 (10 erros); teste 02 com `--c --executar`; `python rodar_testes.py` |

## Sequência da demo (comandos prontos)
Antes: `chcp 65001` (acentos), fonte grande no terminal, estar na pasta `linguagem-do-manha`.
```
python transpilador.py testes/01_valido_basico.gam --executar
python transpilador.py testes/01_valido_basico.gam --tokens --so-lexico
python transpilador.py testes/03_erro_lexico.gam
python transpilador.py exemplos/precedencia.gam --derivacao --ast --c --executar
python transpilador.py testes/04_erro_sintatico.gam
python transpilador.py testes/05_erro_semantico.gam
python transpilador.py testes/02_valido_completo.gam --ast --c --executar      (digitar 4)
python transpilador.py testes/07_valido_escopo.gam --c --executar
python rodar_testes.py
```

## Pedidos ao vivo: receitas
1. **Trocar uma palavra-chave** (ex.: `mostra` → `grita`): `tokens.py`, dicionário `PALAVRAS_RESERVADAS`, troque a chave `"mostra"`. Só isso: a mensagem de erro se ajusta sozinha (`DESCRICAO`). Os testes que usam `mostra` passam a dar erro sintático, porque `mostra` vira identificador; dá para mostrar isso.
2. **Novo teste na hora:** crie `x.gam` e rode `python transpilador.py x.gam --executar`.
3. **Nova regra semântica** (ex.: divisão por zero literal): em `semantico.py`, função `binario`, antes do `if op in ("+", "-", "*", "/")`:
   ```python
   if op in ("/", "%") and isinstance(no.direita, NumeroInt) and no.direita.valor == 0:
       self.erro("divisão por zero (regra R13)", no)
   ```
4. **Novo operador no mesmo andar de `* / %`:** léxico (nova linha em `REGRAS` + novo `TipoToken`), parser (`termo()`: acrescentar o tipo na tupla do `while`), semântica (`binario`: dizer quais tipos aceita), gerador (se o operador existir igual no C, nada muda).
5. **Achar onde uma produção é reconhecida:** cada regra da EBNF é uma função de mesmo nome em `parser.py` (ex.: `<Condicional>` → `condicional()`).

## Perguntas prováveis (resposta curta)
- **Token × lexema?** Lexema é o texto (`fita`); token é a classificação + o lexema (`ID, "fita"`).
- **Como `==` não vira dois `=`?** Maior casamento pela ordem: os de 2 caracteres vêm antes na tabela `REGRAS`.
- **Como `se` não vira identificador?** Casa como ID e consulta `PALAVRAS_RESERVADAS`.
- **Por que `2abc` dá erro?** As ER de número exigem que o número acabe ali `(?![\w.])`; senão sairia `NUM(2) ID(abc)`.
- **O léxico para no 1º erro?** Não: registra e continua. O parser, sim, para.
- **Por que a gramática não é ambígua?** Um andar (variável) por nível de precedência; o `*` fica mais fundo que o `+`.
- **Por que não tem recursão à esquerda, e o que aconteceria?** `E → E + T` faria `expr_adit()` chamar a si mesma sem consumir token (laço infinito / `RecursionError`). Usamos `T { + T }` = `while`.
- **E a associatividade à esquerda?** O `while` junta cada termo novo à esquerda: `10 - 3 - 2 = (10 - 3) - 2 = 5`.
- **LL(1)?** Escolhe a regra espiando 1 token; cada comando começa com um token diferente.
- **Árvore de derivação × AST?** A de derivação tem todas as variáveis e tokens (`;`, `(`); a AST só o que importa para gerar C.
- **Por que `mostra(y)` com `y` não declarada não é erro sintático?** Tem os mesmos tokens de `mostra(x)`; só a tabela de símbolos sabe. É dependente de contexto.
- **Escopo?** Pilha de tabelas: cada bloco empilha; declarar olha o topo; procurar desce a pilha.
- **Por que `v_x_2` no C?** Sombreamento + R9: `remendo x = x + 1;` interno lê o `x` de fora, mas no C `int v_x = v_x + 1;` leria o novo. Nome novo preserva o comportamento.
- **O tipo de `remendo x = 10;`?** Deduzido do valor (R12), fixo depois. Tipagem estática.
- **Por que `float` e não `double`?** `scanf` com `float` usa `%f` (com `double` seria `%lf`).
- **Por que parênteses em toda operação no C?** Garantia de que o C lê igual à nossa AST; a precedência já foi decidida no parser.
- **Isso é substituição de texto?** Não: o gerador percorre a AST e escolhe o formato do `printf` pelo tipo que a semântica calculou.
- **Por que Python, se o destino é C?** O transpilador pode ser escrito em qualquer linguagem; o enunciado só fixa o destino (C). A justificativa do v6 §1 é para trocar o destino.
- **Uso de IA?** Declarado no relatório §11: o que foi feito com IA, como verificamos e o que o grupo decidiu.

## Checklist do dia
- [ ] Python e gcc no computador da sala (ou levar notebook); `python rodar_testes.py` antes de começar.
- [ ] Ensaio completo com cronômetro (sugestão: 08/10).
- [ ] Cada um explica em voz alta uma parte que NÃO é a dele.
