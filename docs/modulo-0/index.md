# Preparação do ambiente (Módulo 0)

Este módulo instala as ferramentas usadas nos laboratórios das ODAs e copia este repositório para o computador do aluno. A preparação leva cerca de 20 minutos e deve ser concluída antes do primeiro encontro ao vivo.

| Ferramenta | Para que serve nas ODAs |
| --- | --- |
| Git | Programa de controle de versões. Nas ODAs, o Git copia o repositório para o computador, operação chamada clonar, e o atualiza a cada aula. |
| VS Code (Visual Studio Code) | Editor de código gratuito da Microsoft. Nas ODAs, o VS Code abre os arquivos citados nas abas e oferece um terminal integrado. |
| Python 3.11 ou mais recente | Interpretador da linguagem Python. Nas ODAs, o Python executa os programas prontos do Laboratório. |

Os comandos deste módulo são digitados num terminal, que é o programa em que se escrevem comandos de texto. A tabela abaixo indica o terminal de cada sistema operacional.

| Sistema | Terminal | Onde encontrar |
| --- | --- | --- |
| Windows | PowerShell | Menu Iniciar |
| macOS | Terminal | Aplicativos › Utilitários |
| Linux | Terminal da distribuição | Menu de aplicativos |

## 1. Instalar o Git

=== "Windows"

    No PowerShell, instale o Git pelo `winget`, o gerenciador de pacotes do Windows 10 e 11:

    ```powershell
    winget install --id Git.Git -e --source winget
    ```

    Se o `winget` não for reconhecido, o instalador pode ser baixado em [git-scm.com/download/win](https://git-scm.com/download/win) e executado com as opções padrão. Depois da instalação, o PowerShell precisa ser fechado e aberto de novo.

=== "macOS"

    No Terminal, o comando abaixo instala as ferramentas de linha de comando da Apple, que incluem o Git, depois de uma confirmação numa janela do sistema.

    ```bash
    xcode-select --install
    ```

    A mensagem de que as ferramentas já estão instaladas indica que o Git já está disponível.

=== "Linux"

    Em distribuições baseadas em Debian ou Ubuntu:

    ```bash
    sudo apt update
    sudo apt install -y git
    ```

    Em Fedora, use `sudo dnf install -y git`.

O comando abaixo confere a instalação e deve exibir uma linha como `git version 2.47.0`, em qualquer versão.

```bash
git --version
```

## 2. Instalar o VS Code

=== "Windows"

    ```powershell
    winget install --id Microsoft.VisualStudioCode -e --source winget
    ```

    O instalador também pode ser baixado em [code.visualstudio.com](https://code.visualstudio.com/), com a opção "Adicionar ao PATH" marcada durante a instalação.

=== "macOS"

    Baixe o VS Code em [code.visualstudio.com](https://code.visualstudio.com/) e arraste o aplicativo baixado para a pasta Aplicativos. O comando `code` fica disponível no Terminal depois do comando `Shell Command: Install 'code' command in PATH`, acionado no VS Code pelo atalho Cmd+Shift+P.

=== "Linux"

    Baixe o pacote `.deb` (Debian e Ubuntu) ou `.rpm` (Fedora) em [code.visualstudio.com](https://code.visualstudio.com/) e instale com o gerenciador de pacotes. Em Debian e Ubuntu:

    ```bash
    sudo apt install ./code_*.deb
    ```

A extensão Python, publicada pela Microsoft, destaca a sintaxe dos arquivos `.py` no VS Code. Ela é instalada pelo painel Extensões, aberto com Ctrl+Shift+X (Cmd+Shift+X no macOS), com uma busca por `Python`.

## 3. Instalar o Python

=== "Windows"

    ```powershell
    winget install --id Python.Python.3.13 -e --source winget
    ```

    O instalador também pode ser baixado em [python.org/downloads](https://www.python.org/downloads/), com a opção "Add python.exe to PATH" marcada na primeira tela. No Windows, o comando do interpretador é `py`.

    ```powershell
    py --version
    ```

=== "macOS"

    O instalador da versão estável mais recente está em [python.org/downloads](https://www.python.org/downloads/). No macOS, o comando do interpretador é `python3`.

    ```bash
    python3 --version
    ```

=== "Linux"

    A maioria das distribuições Linux já traz o Python 3 instalado. Quando o comando de versão falha, o pacote `python3` precisa ser instalado pelo gerenciador da distribuição.

    ```bash
    python3 --version
    sudo apt install -y python3
    ```

A versão exibida deve ser 3.11 ou mais recente, e uma versão anterior precisa ser substituída pelo mesmo procedimento de instalação.

## 4. Clonar o repositório

Clonar é copiar o repositório do GitHub para o computador com todo o histórico de versões. Abra o terminal numa pasta de trabalho de sua escolha e execute os comandos abaixo.

```bash
git clone https://github.com/aulas-marco/odas-arquitetura-software
cd odas-arquitetura-software
```

O Git cria a pasta `odas-arquitetura-software`, e o comando `cd` entra nela. O comando abaixo abre essa pasta no VS Code, e o menu Arquivo › Abrir Pasta tem o mesmo efeito.

```bash
code .
```

No VS Code, o terminal integrado abre pelo menu Terminal › Novo Terminal, já posicionado na pasta do repositório, e os comandos dos Laboratórios são executados nele.

## 5. Conferir o ambiente

O programa verificador, executado na raiz do repositório, confere a versão do Python e a presença do Git e das pastas das ODAs.

=== "Windows"

    ```powershell
    py codigo/modulo-0/verificar_ambiente.py
    ```

=== "macOS e Linux"

    ```bash
    python3 codigo/modulo-0/verificar_ambiente.py
    ```

A saída esperada termina com a linha `Ambiente pronto.`, como no exemplo abaixo.

```text
  [OK] Python 3.13.1 (mínimo 3.11)
  [OK] Git encontrado no PATH
  [OK] Repositório clonado, com as pastas codigo/oda-01 e codigo/oda-02

Ambiente pronto.
```

O número da versão do Python pode ser diferente na máquina do aluno. Um item marcado como `FALTA` indica a etapa deste módulo que precisa ser refeita. Um `[AVISO]` sobre o comando `code` permite seguir com os laboratórios, porque o VS Code também abre pelo menu do sistema.

## 6. Atualizar antes de cada aula

O repositório recebe ODAs novas ao longo da disciplina, e a cópia local precisa ser atualizada no início de cada aula com o comando abaixo, executado dentro da pasta do repositório.

```bash
git pull
```

## Problemas comuns

| Sintoma | Causa provável | Correção |
| --- | --- | --- |
| `git`, `code` ou `py` "não é reconhecido como comando" | O terminal foi aberto antes da instalação do programa | Fechar todas as janelas do terminal e do VS Code e abri-las de novo |
| `python3` abre a Microsoft Store no Windows | O Windows associa o nome `python3` a um atalho da loja | Usar o comando `py` |
| `fatal: destination path 'odas-arquitetura-software' already exists` | O repositório já foi clonado nessa pasta | Entrar na pasta com `cd odas-arquitetura-software` e executar `git pull` |
| `git pull` recusa a atualização por causa de alterações locais | Algum arquivo do repositório foi alterado | Desfazer as alterações com `git restore .` e repetir o `git pull` |
