# Textos do Google Sala de Aula — (2026/2º) Linguagens Formais e Compiladores (01RCOMP-101_6N)

Copiados do Classroom em 2026-09-23 (sem os menus do site). O enunciado completo do TP1 está em `TP1_Linguagem_Tematica_v6.md`.

---

## TP1 — aviso do professor (data do post e data de entrega não vieram no texto colado)

Chegou a hora do primeiro trabalho prático da disciplina!

Vocês vão criar a própria linguagem de programação temática (inspirada no exemplo BIRL, apresentado em aula) e desenvolver um transpilador que traduz essa linguagem para C ou Python.

O trabalho vale 30 pontos, divididos em:
- 15 pontos: especificação léxica, gramática (GLC em BNF/EBNF), analisador léxico/sintático funcionando e geração de código.
- 15 pontos: apresentação, demonstração ao vivo do transpilador e defesa técnica (com perguntas individuais a cada integrante do grupo).

Entregáveis:
1. Relatório Técnico de Especificação (tabela de tokens + gramática completa).
2. Código-fonte do transpilador.
3. Programa de teste (com condicionais, laços e expressões aritméticas).
4. Apresentação e defesa técnica presencial.

Cronograma sugerido:
Semana 1 — tema definido + especificação léxica
Semana 2 — gramática completa (G = (V,T,P,S)) em BNF/EBNF + início do léxico
Semana 3 — analisador sintático funcionando, com árvore de derivação
Semana 4 — geração de código, programa de teste e entrega final

Todos os detalhes, requisitos técnicos, o modelo de referência BIRL-Lite (gramática, tokens e exemplo completo) e os critérios de avaliação estão no documento anexo. Leiam com atenção antes de começar.

Dúvidas, tragam para a próxima aula ou postem aqui no Classroom.

---

## EI03: Especificação e Implementação de um Analisador Léxico

MARCOS RONALDO MELO CAVALHEIRO • 11 de set. (editado: 11 de set.) • Estudos Independentes
**Data de entrega: 9 de out., 19:20** • Status em 2026-09-23: Atribuído • "Não é possível entregar atividades após a data de entrega"

📅 CRONOGRAMA E PRAZOS
Componente Curricular: GRP00543 — Linguagens Formais e Compiladores
Encaminhamento — Aula 6
Orientação Intermediária — Aula 7
Entrega — Aula 9: até as 19h15
Forma de realização: individual ou em dupla (como parte do Projeto Prático)
Carga horária estimada: 4 horas

🎯 OBJETIVO
Aplicar expressões regulares, autômatos finitos e técnicas de reconhecimento de padrões na especificação, implementação, teste e explicação técnica de um analisador léxico para uma linguagem simplificada.
Esta atividade possui caráter formativo e preparatório para as avaliações teóricas, atividades práticas e projetos desenvolvidos durante o semestre — em especial, atuando como etapa de especificação, prototipação e implementação preparatória para o Projeto Prático do Analisador Léxico da Primeira Etapa (30 pontos).

Consulte estas referências para embasar a resolução da atividade:
• MENEZES, Paulo Blauth. Linguagens Formais e Autômatos, 6ª edição. Porto Alegre: Bookman, 2011. (Capítulo 3: Linguagens Regulares — Seção 3.1: O Papel do Analisador Léxico, Seção 3.4: O Reconhecimento de Tokens e Seção 3.6: Expressões Regulares).
• AHO, Alfred V.; SETHI, Ravi; ULLMAN, Jeffrey D. Compiladores: Princípios, Técnicas e Ferramentas, 2ª edição. São Paulo: Pearson Addison-Wesley, 2007. (Capítulo 3: Análise Léxica).
• PRICE, Ana Maria de Alencar; TOSCANI, Simão Sirineo. Implementação de Linguagens de Programação: Compiladores, 2ª edição. Porto Alegre: Instituto de Informática da UFRGS / Bookman, 2001. (Capítulo 2.2: Tokens).
• Plano de Ensino da disciplina de Linguagens Formais e Compiladores — UNIJUÍ.

📝 ATIVIDADE
O Estudo Independente 03 consiste no desenvolvimento formativo, progressivo e justificado da especificação e da implementação do analisador léxico de seu compilador. Para realizar a atividade, apresente a resolução comentada e estruturada dos seguintes problemas:

Problema 1 — Especificação Formal dos Tokens (Léxico)
Escreva e justifique detalhadamente as expressões regulares (ER) na notação formal (EBNF ou notação aceita pelo JFlex) para as seguintes categorias léxicas da linguagem proposta:
a) Palavras reservadas (palavras-chave com significado fixo);
b) Identificadores (regras estritas para a nomeação de variáveis e funções);
c) Números inteiros (sequências de um ou mais dígitos) e decimais/reais (regras de formatação com no máximo um ponto decimal);
d) Operadores aritméticos, relacionais e lógicos;
e) Símbolos de atribuição, delimitadores e caracteres de pontuação;
f) Espaços em branco, quebras de linha e comentários (tanto comentários de linha única quanto de múltiplas linhas).

Problema 2 — Resolução de Conflitos e Tratamento Léxico
Explique de maneira fundamentada na teoria de compiladores como o seu analisador léxico resolve e implementa as seguintes regras procedimentais de varredura:
a) Prioridade de Reconhecimento: Como garantir que uma palavra-chave como "int" ou "while" seja reconhecida como palavra reservada e não casada erroneamente como um identificador comum;
b) Regra do Maior Casamento (Longest Match): Como garantir que operadores compostos (como ">=" ou ":=") sejam reconhecidos de forma atômica e unitária, sem serem fracionados em múltiplos tokens individuais (como ">" e "=");
c) Controle de Posição: Como a sua implementação mantém o registro ativo das posições de linha e coluna onde cada token ou erro léxico foi encontrado.

Problema 3 — Implementação Prática do Analisador Léxico (Manual ou com JFlex)
Desenvolva o código-fonte funcional do analisador léxico que execute as seguintes operações básicas:
a) Receba um arquivo de entrada em formato de texto simples (contendo o código-fonte a ser analisado);
b) Faça a leitura de caracteres e realize a varredura (scanning), gerando na saída padrão ou em arquivo a sequência estruturada de tokens correspondente (identificando a classe do token e o seu valor/lexema associado);
c) Implemente o tratamento de erros: ao detectar um caractere inválido ou malformado (que não pertença ao alfabeto de entrada ou não case com nenhum padrão de token), o analisador deve reportar um erro léxico informativo, indicando de forma explícita a linha, a coluna e o lexema problemático, e prosseguir com o reconhecimento dos elementos seguintes.

Problema 4 — Casos de Teste e Evidências de Validação
Crie arquivos de teste para validar o comportamento e a robustez do analisador léxico desenvolvido, fornecendo:
a) Um arquivo de código de teste composto estritamente por trechos de código estruturados e válidos segundo a gramática definida (comprovando o correto reconhecimento e classificação de todos os tokens válidos);
b) Um arquivo de teste contendo casos propositais de erros léxicos (por exemplo, caracteres inválidos como "@", identificadores iniciados por dígitos ou constantes numéricas malformadas) para validar se o mecanismo de tratamento de erros léxicos do analisador está reportando a localização e os caracteres problemáticos corretamente.

🤖 DIRETRIZES PARA O USO DE INTELIGÊNCIA ARTIFICIAL
Conforme o plano de ensino, ferramentas de Inteligência Artificial generativa poderão ser utilizadas como recurso de apoio à pesquisa, à geração de exemplos, à organização das ideias e à revisão do material.
Declaração obrigatória: deverá ser incluída, ao final do documento, uma declaração de uso ou de não uso de Inteligência Artificial.
Quando houver uso de IA, informe:
• ferramenta utilizada;
• finalidade do uso;
• etapas da atividade em que foi utilizada;
• procedimentos adotados para verificar as expressões regulares e os autômatos produzidos (testes de reconhecimento realizados);
• fontes utilizadas para validação;
• alterações realizadas pelo estudante.
A Inteligência Artificial:
• não substitui a autoria do estudante;
• não deverá ser utilizada como única fonte de informação;
• não deverá ser apresentada como referência bibliográfica;
• não elimina a necessidade de consultar livros, materiais da disciplina e fontes técnicas confiáveis.
Domínio técnico: o estudante deverá compreender e ser capaz de explicar integralmente qualquer expressão regular, autômato, conversão ou simulação apresentada no trabalho.
Quando nenhuma ferramenta de IA tiver sido utilizada, inclua a seguinte declaração:
"Declaro que não utilizei ferramentas de Inteligência Artificial generativa na elaboração desta atividade."

📦 FORMATO E ORIENTAÇÕES DE ENTREGA
A entrega deverá ser realizada exclusivamente nesta atividade do Google Classroom.
Formatos aceitos:
• Arquivo compactado (.zip) contendo as resoluções comentadas do trabalho escrito (especificações formais dos tokens, justificativas de conflitos e referências), os arquivos de código-fonte (.flex e/ou classes Java), os arquivos de teste de entrada/saída utilizados, e a declaração de uso de IA generativa.
• O documento explicativo descritivo/relatório deverá ser entregue preferencialmente em formato PDF.
O relatório/documentação contido no arquivo compactado deverá apresentar:
• Nome completo do estudante (ou dos integrantes do grupo);
• Identificação do componente curricular e do professor;
• Título da atividade (Estudo Independente 03);
• Resolução comentada e documentada dos 4 problemas da atividade;
• Evidências de testes com a captura de tela ou listagem da saída do analisador para as entradas corretas e incorretas;
• Referências bibliográficas consultadas;
• Declaração de uso ou de não uso de Inteligência Artificial generativa.

Sugestão de nome do arquivo compactado:
EI03_NomeCompleto.zip (ou EI03_NomesIntegrantes.zip se realizado em dupla)

Antes do envio, verifique:
• se o arquivo compactado abre e extrai corretamente;
• se todo o código-fonte, especificações e arquivos de teste foram incluídos;
• se a documentação explicativa está em formato PDF legível;
• se o nome do estudante ou integrantes está claramente identificado;
• se todos os problemas e requisitos técnicos (reconhecimento, prioridades, tratamento de erros) foram resolvidos e documentados;
• se as evidências do correto funcionamento dos testes foram incluídas;
• se as referências foram informadas;
• se a declaração sobre Inteligência Artificial generativa está presente e devidamente preenchida.

📌 CARÁTER FORMATIVO
A entrega do Estudo Independente não atribuirá pontuação específica.
Entretanto, as especificações formais, os padrões de tokens, a modelagem de tratamento de erros e os componentes práticos de código-fonte desenvolvidos nesta atividade integram diretamente o conteúdo da disciplina e constituem as etapas fundamentais de construção do seu Projeto Prático do Analisador Léxico (Unidade 1), avaliado com valor de até 30 pontos na Aula 09. Todo o esforço de especificação, codificação e validação realizado nesta atividade será diretamente herdado, expandido e incorporado na entrega final de avaliação de seu compilador.

---

## EI 02 — Expressões Regulares e Autômatos Finitos: da Especificação ao Reconhecimento de Tokens

MARCOS RONALDO MELO CAVALHEIRO • 21 de ago. (editado: 11 de set.) • Estudos Independentes
**Data de entrega: 11 de set.** • Status em 2026-09-23: Não entregue

📅 CRONOGRAMA E PRAZOS
Componente Curricular: GRP00543 — Linguagens Formais e Compiladores
Professor: Marcos Ronaldo Melo Cavalheiro
Turma: 02RCOMP-101_4N
Encaminhamento — Aula 4
Mobilização — Aula 5
Entrega — Aula 6: até as 19h15
Forma de realização: individual
Carga horária estimada: 4 horas

🎯 OBJETIVO
Representar e reconhecer linguagens regulares por meio de expressões regulares e autômatos finitos, relacionando essas representações à especificação de tokens.

Esta atividade possui caráter formativo e preparatório para as avaliações teóricas, atividades práticas e projetos desenvolvidos durante o semestre — em especial, para a especificação dos tokens que será utilizada no Projeto Prático de Analisador Léxico.

📚 O QUE FAZER?
Resolva os problemas da atividade abaixo, envolvendo expressões regulares, linguagens regulares e autômatos finitos.
Não se limite a apresentar o resultado final. Explique seu raciocínio, justifique cada construção e demonstre compreensão dos conceitos envolvidos.

📚 REFERENCIAL BIBLIOGRÁFICO PARA CONSULTA
Bibliografia básica (Plano de Ensino):
• AHO, Alfred V. et al. Compiladores: princípios, técnicas e ferramentas. São Paulo: Pearson Addison Wesley, 1995/2007. (capítulo de Análise Léxica — expressões regulares e autômatos aplicados a tokens)
• MENEZES, Paulo Blauth. Linguagens formais e autômatos. Porto Alegre: Bookman/Sagra Luzzatto, 2002/2008. (capítulos sobre expressões regulares e autômatos finitos)
• PRICE, Ana Maria de Alencar; TOSCANI, Simão Sirineo. Implementação de linguagens de programação: compiladores. Porto Alegre: Bookman, 2001/2008.
Bibliografia complementar:
• HOPCROFT, John E.; ULLMAN, Jeffrey D.; MOTWANI, Rajeev. Introdução à teoria de autômatos, linguagens e computação. Rio de Janeiro: Campus, 2003.
• SANTOS, Pedro Reis; LANGLOIS, Thibault. Compiladores: da teoria à prática. Rio de Janeiro: LTC, 2018.

📝 ATIVIDADE
Problema 1 — Construção de expressões regulares
Escreva uma expressão regular para cada uma das linguagens a seguir:
a) identificadores que iniciam com letra minúscula e podem conter letras minúsculas e dígitos;
b) números inteiros sem sinal (sequência de um ou mais dígitos);
c) números reais com no máximo um ponto decimal (deve aceitar, por exemplo, 3.14, e rejeitar 3.4.5).

Problema 2 — Identificação da linguagem representada
Dada a expressão regular (a|b)*abb, descreva em português a linguagem que ela representa e apresente 3 exemplos de palavras aceitas e 2 exemplos de palavras rejeitadas.

Problema 3 — Construção de autômatos finitos
a) Construa um AFD que reconheça a linguagem representada pela expressão regular do Problema 2 — (a|b)*abb. Apresente o diagrama de estados e a tabela de transição.
b) Construa um AFN que reconheça palavras sobre o alfabeto {0,1} que terminam em "01". Apresente o diagrama de estados.

Problema 4 — Simulação de reconhecimento
Utilizando o AFD construído no Problema 3a, simule passo a passo o reconhecimento das palavras "aabb" e "abab", indicando a sequência de estados percorrida e se cada palavra é aceita ou rejeitada, justificando.

Problema 5 — Conversão de AFN para AFD (conceitual)
Explique, com suas próprias palavras e um exemplo simples, o que significa converter um AFN em um AFD equivalente e por que essa conversão é sempre possível.

Problema 6 — Comparação entre representações
Compare expressões regulares e autômatos finitos como formas de representar uma linguagem regular. Em que situações cada representação é mais vantajosa? Justifique.

Problema 7 — Aplicação à especificação de tokens
Escolha dois tokens de uma linguagem de programação simples (por exemplo: identificador, número inteiro, número real ou operador relacional) e, para cada um deles:
a) defina o padrão em expressão regular;
b) construa o autômato finito correspondente (diagrama ou tabela de transição).
Explique por que expressões regulares e autômatos finitos são adequados para especificar tokens de uma linguagem.

Para cada problema, apresente a resolução comentada: não basta o resultado — justifique por que a expressão regular ou o autômato representam corretamente a linguagem pedida.

🤖 DIRETRIZES PARA O USO DE INTELIGÊNCIA ARTIFICIAL
(Mesmo texto do EI03, acima.)

📦 FORMATO E ORIENTAÇÕES DE ENTREGA
A entrega deverá ser realizada exclusivamente nesta atividade do Google Classroom.
Formatos aceitos:
• PDF — formato recomendado;
• PNG ou JPG, desde que todo o conteúdo esteja em uma única imagem legível (ou em um conjunto de imagens claramente numeradas);
• arquivo de apresentação convertido em PDF.

O arquivo deverá conter:
• nome completo do estudante;
• identificação do componente curricular;
• título da atividade;
• resolução comentada dos 7 problemas propostos;
• expressões regulares, diagramas e/ou tabelas de transição;
• simulações de reconhecimento;
• referências consultadas;
• declaração de uso ou de não uso de Inteligência Artificial.

Sugestão de nome do arquivo:
EI02_NomeCompleto.pdf

📌 CARÁTER FORMATIVO
A entrega do Estudo Independente não atribuirá pontuação específica.
Entretanto, os conceitos, expressões regulares, autômatos, conversões e exemplos desenvolvidos nesta atividade integram os conhecimentos do componente curricular e poderão ser cobrados na Prova Escrita Individual da Primeira Etapa (Aula 8, 16/09/2026), nas atividades práticas e no Projeto Prático de Analisador Léxico.
