# ODAs de Arquitetura de Software

Objetos Digitais de Aprendizagem (ODAs) da disciplina Arquitetura de Backend, do curso de Arquitetura de Software Distribuído do IEC/PUC Minas. Cada ODA dura 25 minutos, está dividida em quatro etapas e aponta para as seções correspondentes do [material oficial da disciplina](https://marco-mendes.github.io/arquitetura-software/).

Portal publicado: <https://aulas-marco.github.io/odas-arquitetura-software/>

## Para alunos

1. Concluir o [Módulo 0](https://aulas-marco.github.io/odas-arquitetura-software/modulo-0/), que prepara o ambiente e clona este repositório.
2. Atualizar o repositório com `git pull` no início de cada aula.
3. Abrir a ODA da aula pelo portal e executar os programas da pasta `codigo/` indicados no Laboratório.

## Estrutura

| Caminho | Conteúdo |
| --- | --- |
| `codigo/` | Programas Python executados nos Laboratórios, sem dependências externas |
| `odas/<oda>/oda.yml` | Conteúdo de cada ODA, organizado em quatro abas de blocos |
| `catalogo/odas.yml` | Catálogo das ODAs, com módulo, tempo, fontes no material oficial e commit de referência do código |
| `docs/` | Página mestre, Módulo 0 e página de rastreabilidade, publicadas com MkDocs Material |
| `motor/` | Aplicação em JavaScript, sem dependências, que monta cada ODA a partir dos dados |
| `scripts/gerar_odas.py` | Valida cada `oda.yml` e gera `site/<oda>/index.html` |

O motor, o gerador e o hook do catálogo foram adaptados do roteiro de autoria de ODAs publicado em <https://arkhibr.github.io/oda-arquitetura-software/>, no commit `30565bf` do repositório `arkhibr/oda-arquitetura-software`. A adaptação reduz as abas de sete para quatro, admite ODAs a partir de 15 minutos e desenha os rótulos dos diagramas Mermaid como texto SVG, o que permite rótulos com mais de uma linha.

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

Os testes em Python conferem que cada trecho de código exibido numa ODA é idêntico ao arquivo do repositório, e que cada saída de terminal simulado é igual à saída real do programa.
