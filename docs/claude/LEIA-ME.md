# Continuar no PC novo

## Passos
1. Instalar: Git, Python 3.11, VS Code e Claude Code (e entrar na sua conta). O gcc fica para depois (MAPA, item 0.6).
2. Baixar o projeto (PowerShell), trocando a pasta de destino se quiser. O GitHub pede login, porque o repositório é privado:
   `git clone https://github.com/eduardomanhabosco/linguagem-do-manha.git "C:\projetos\linguagem do manha"`
3. Entrar na pasta e abrir o Claude: `cd "C:\projetos\linguagem do manha"` e depois `claude`.
   O `CLAUDE.md` e os arquivos que ele importa carregam sozinhos: é todo o contexto do trabalho.
4. Continuar de onde paramos: dúvidas do conceito 3 e depois o 4 (ver `docs/MAPA.md`, seção 1).

## O que não veio (de propósito)
Neste repositório só entra o que é da disciplina. A config geral do Claude do PC antigo (`~/.claude/CLAUDE.md`, a skill `modo-estudo` e a memória) ficou de fora. As regras que valem para este trabalho estão no `CLAUDE.md` do projeto, seção "Fluxo de trabalho".

## Retomar a conversa antiga (opcional)
`conversa-2026-09-23.jsonl` é a conversa de 23 a 25/09 (o estudo dos 13 conceitos), copiada no último commit. O jeito mais barato é começar uma sessão nova, porque o `CLAUDE.md` já traz o contexto. Para abrir a antiga mesmo assim, copie o arquivo para fora da pasta do projeto (ex.: Documentos) e rode:
`claude --resume "C:\Users\<você>\Documents\conversa-2026-09-23.jsonl"`
É uma conversa grande. Ao retomar, o Claude Code pode oferecer "Resume from summary" (retomar a partir de um resumo), que gasta menos.

## Usando dois PCs
Ao começar: `git pull`. Ao terminar: commit + `git push`.
