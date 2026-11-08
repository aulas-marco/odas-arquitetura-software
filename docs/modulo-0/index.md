# Módulo 0 — Preparar o ambiente

Este módulo instala as três ferramentas usadas nos laboratórios das ODAs e copia este repositório para o seu computador. Ele leva cerca de 20 minutos e deve ser concluído antes do primeiro encontro ao vivo.

| Ferramenta | Para que serve nas ODAs |
| --- | --- |
| Git | Programa de controle de versões. Nas ODAs, ele copia o repositório para o seu computador (operação chamada clonar) e o atualiza a cada aula. |
| VS Code (Visual Studio Code) | Editor de código gratuito da Microsoft. Nas ODAs, ele abre os arquivos citados nas abas e oferece um terminal integrado. |
| Python 3.10 ou mais recente | Interpretador da linguagem Python. Nas ODAs, ele executa os programas prontos do Laboratório. |

Os comandos deste módulo são digitados num **terminal**, programa em que se escrevem comandos de texto. No Windows, use o PowerShell, que se abre pelo menu Iniciar. No macOS, use o aplicativo Terminal, em Aplicativos › Utilitários. No Linux, use o terminal da sua distribuição.

## 1. Instalar o Git

=== "Windows"

    No PowerShell, instale o Git pelo `winget`, o gerenciador de pacotes do Windows 10 e 11:

    ```powershell
    winget install --id Git.Git -e --source winget
    ```

    Se o `winget` não for reconhecido, baixe o instalador em [git-scm.com/download/win](https://git-scm.com/download/win) e aceite as opções padrão. Depois da instalação, feche e abra o PowerShell de novo.

=== "macOS"

    No Terminal, o comando abaixo instala as ferramentas de linha de comando da Apple, que incluem o Git. Uma janela pede confirmação.

    ```bash
    xcode-select --install
    ```

    Se aparecer a mensagem de que as ferramentas já estão instaladas, o Git já está disponível.

=== "Linux"

    Em distribuições baseadas em Debian ou Ubuntu:

    ```bash
    sudo apt update
    sudo apt install -y git
    ```

    Em Fedora, use `sudo dnf install -y git`.

Confira a instalação. O terminal deve mostrar uma linha como `git version 2.47.0`, e qualquer versão serve.

```bash
git --version
```

## 2. Instalar o VS Code

=== "Windows"

    ```powershell
    winget install --id Microsoft.VisualStudioCode -e --source winget
    ```

    Se preferir, baixe o instalador em [code.visualstudio.com](https://code.visualstudio.com/) e marque a opção "Adicionar ao PATH" durante a instalação.

=== "macOS"

    Baixe o VS Code em [code.visualstudio.com](https://code.visualstudio.com/), abra o arquivo baixado e arraste o aplicativo para a pasta Aplicativos. Para habilitar o comando `code` no Terminal, abra o VS Code, pressione Cmd+Shift+P, digite `Shell Command: Install 'code' command in PATH` e confirme.

=== "Linux"

    Baixe o pacote `.deb` (Debian e Ubuntu) ou `.rpm` (Fedora) em [code.visualstudio.com](https://code.visualstudio.com/) e instale com o gerenciador de pacotes. Em Debian e Ubuntu:

    ```bash
    sudo apt install ./code_*.deb
    ```

Instale também a extensão Python, da Microsoft, que colore e analisa os arquivos `.py`. No VS Code, abra o painel Extensões com Ctrl+Shift+X (Cmd+Shift+X no macOS), procure por `Python` e instale a extensão publicada pela Microsoft.

## 3. Instalar o Python

=== "Windows"

    ```powershell
    winget install --id Python.Python.3.13 -e --source winget
    ```

    Se preferir o instalador, baixe-o em [python.org/downloads](https://www.python.org/downloads/) e marque a opção "Add python.exe to PATH" na primeira tela. No Windows, o comando do interpretador é `py`.

    ```powershell
    py --version
    ```

=== "macOS"

    Baixe o instalador da versão estável mais recente em [python.org/downloads](https://www.python.org/downloads/) e execute-o. No macOS, o comando do interpretador é `python3`.

    ```bash
    python3 --version
    ```

=== "Linux"

    A maioria das distribuições já traz o Python 3. Confira a versão e, se o comando não existir, instale o pacote `python3` pelo gerenciador da distribuição.

    ```bash
    python3 --version
    sudo apt install -y python3
    ```

A versão mostrada deve ser 3.10 ou mais recente. Se for anterior, instale uma versão nova pelo mesmo caminho.

## 4. Clonar o repositório

Clonar é copiar o repositório do GitHub para o seu computador, com todo o histórico. Escolha uma pasta de trabalho, abra o terminal nela e execute:

```bash
git clone https://github.com/aulas-marco/odas-arquitetura-software
cd odas-arquitetura-software
```

O Git cria a pasta `odas-arquitetura-software`, e o comando `cd` entra nela. Para abri-la no VS Code, use o comando abaixo, ou o menu Arquivo › Abrir Pasta.

```bash
code .
```

No VS Code, abra o terminal integrado pelo menu Terminal › Novo Terminal. Ele já começa na pasta do repositório, e é nele que os comandos dos Laboratórios são executados.

## 5. Conferir o ambiente

Na raiz do repositório, execute o verificador. Ele confere a versão do Python, a presença do Git e as pastas das ODAs.

=== "Windows"

    ```powershell
    py codigo/modulo-0/verificar_ambiente.py
    ```

=== "macOS e Linux"

    ```bash
    python3 codigo/modulo-0/verificar_ambiente.py
    ```

A saída esperada termina com a linha `Ambiente pronto.`:

```text
  [OK] Python 3.13.1 (mínimo 3.10)
  [OK] Git encontrado no PATH
  [OK] Repositório clonado, com as pastas codigo/oda-01 e codigo/oda-02

Ambiente pronto.
```

O número da versão do Python pode ser diferente. Se algum item aparecer como `FALTA`, refaça a etapa correspondente deste módulo. Um `[AVISO]` sobre o comando `code` não impede os laboratórios, porque o VS Code pode ser aberto pelo menu do sistema.

## 6. Atualizar antes de cada aula

O repositório recebe as ODAs novas ao longo da disciplina. No início de cada aula, atualize a sua cópia de dentro da pasta do repositório:

```bash
git pull
```

## Problemas comuns

| Sintoma | Causa provável | Correção |
| --- | --- | --- |
| `git`, `code` ou `py` "não é reconhecido como comando" | O terminal foi aberto antes da instalação e não conhece o novo programa | Feche todas as janelas do terminal e do VS Code e abra de novo |
| `python3` abre a Microsoft Store no Windows | O Windows tem um atalho que aponta para a loja | Use `py` no lugar de `python3` |
| `fatal: destination path 'odas-arquitetura-software' already exists` | O repositório já foi clonado nessa pasta | Entre na pasta com `cd odas-arquitetura-software` e use `git pull` |
| `git pull` recusa a atualização por causa de alterações locais | Algum arquivo do repositório foi alterado | Desfaça as alterações com `git restore .` e repita o `git pull` |
