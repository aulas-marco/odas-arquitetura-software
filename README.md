# ODAs de Arquitetura de Software

Objetos Digitais de Aprendizagem (ODAs) da disciplina Arquitetura de Backend, do curso de Arquitetura de Software Distribuído do IEC/PUC Minas. Cada ODA tem 25 minutos, quatro etapas (Objetivo, Conceitos, Laboratório e Verificação) e rastreabilidade para o [material oficial da disciplina](https://marco-mendes.github.io/arquitetura-software/).

Portal publicado: <https://aulas-marco.github.io/odas-arquitetura-software/>

## Para alunos

1. Conclua o [Módulo 0](https://aulas-marco.github.io/odas-arquitetura-software/modulo-0/), que instala o Git, o VS Code e o Python e clona este repositório.
2. No início de cada aula, atualize o repositório com `git pull`.
3. Abra a ODA da aula pelo portal e execute os programas da pasta `codigo/` indicados no Laboratório.

## Estrutura

| Caminho | Conteúdo |
| --- | --- |
| `codigo/` | Programas Python executados nos Laboratórios, sem dependências externas |
| `odas/<oda>/oda.yml` | Conteúdo de cada ODA, organizado em quatro abas de blocos |
| `catalogo/odas.yml` | Catálogo das ODAs, com módulo, tempo, fontes no material oficial e commit de referência do código |
| `docs/` | Página mestre, Módulo 0 e página de rastreabilidade, publicadas com MkDocs Material |
| `motor/` | Aplicação em JavaScript, sem dependências, que monta cada ODA a partir dos dados |
| `scripts/gerar_odas.py` | Valida cada `oda.yml` e gera `site/<oda>/index.html` |

O motor, o gerador e o hook do catálogo foram adaptados do roteiro de autoria de ODAs em <https://arkhibr.github.io/oda-arquitetura-software/> (repositório `arkhibr/oda-arquitetura-software`, commit `30565bf`). A adaptação reduz as abas de sete para quatro e admite ODAs a partir de 15 minutos.

## Trabalhar localmente

    python3 -m venv .venv
    .venv/bin/pip install -r requirements.txt
    npm ci
    .venv/bin/mkdocs build --strict
    .venv/bin/python scripts/gerar_odas.py --destino site
    python3 scripts/servidor_estatico.py 8000 site

## Portões de qualidade

    .venv/bin/python -m unittest discover -s tests -v
    node --test "tests/js/*.test.mjs"
    npx playwright test

Os testes em Python conferem que cada trecho de código exibido numa ODA é idêntico ao arquivo do repositório e que cada saída de terminal simulado é a saída real do programa.
