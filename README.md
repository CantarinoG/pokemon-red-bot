# Pokemon Red Bot

## Índice
1. [Introdução](#introdução)
2. [Instalação](#instalação)
    - [Pré-Requisitos](#pré-requisitos)
    - [Download do Projeto](#download-do-projeto)
    - [Configuração do Ambiente Virtual](#configuração-do-ambiente-virtual)
3. [Uso](#uso)
    - [Preparação do Emulador](#preparação-do-emulador)
    - [Executando o Bot](#executando-o-bot)

## Introdução

Este projeto é um bot automatizado para jogar Pokémon Red, desenvolvido em Python. O bot é capaz de:

- Navegar pelo mapa do jogo de forma autônoma
- Detectar e iniciar batalhas com pokémons selvagens
- Identificar os pokémons em batalha através de reconhecimento de imagem
- Selecionar movimentos de forma inteligente baseado em tipos e dano
- Gerenciar PP dos movimentos
- Exibir informações em tempo real através de uma interface gráfica

O bot utiliza técnicas de processamento de imagem e automação para:

- Capturar a tela do emulador em tempo real
- Detectar elementos visuais usando template matching
- Controlar entradas de teclado de forma programática
- Gerenciar o estado da batalha
- Tomar decisões baseadas na situação atual

A arquitetura do projeto é modular e bem organizada, dividida em diferentes classes com responsabilidades específicas:

- `ScreenCapture`: Responsável por capturar e processar imagens da tela
- `TemplateMatcher`: Realiza a correspondência de templates para reconhecimento visual
- `InputController`: Gerencia as entradas de teclado e foco da janela
- `BattleState`: Mantém o estado da batalha e lógica de decisão
- `GUILogger`: Exibe informações em uma interface gráfica flutuante


## Instalação

Para garantir que todas as dependências do projeto sejam instaladas corretamente e que não haja conflitos com outras bibliotecas do sistema, recomenda-se o uso de um ambiente virtual. Siga os passos abaixo para configurar o ambiente:

**Esse guia de instalação foi feito para sistemas operacionais Linux baseados em Debian. Os comandos podem ter alguma variação em outros sistemas operacionais.**

### Pré-requisitos

* Certifique-se de que você possui o **Python 3.12** ou superior instalado em sua máquina. Você pode verificar a versão do Python instalada executando o seguinte comando no terminal:

```
python --version
```

ou

```
python3 --version
```

* Certifique-se também que você possui o **python3-venv** instalado.

Para instalá-lo **(Linux baseado em Debian)**:

```
sudo apt install python3-venv
```

* Certifique-se também que você possui o **xdotool** instalado.

Para instalá-lo **(Linux baseado em Debian)**:

```
sudo apt install xdotool
```

### Download do Projeto:

Clone o repositório usando o comando:

```
git clone https://github.com/CantarinoG/pokemon-red-bot.git
```

### Configuração do Ambiente Virtual:

* Para criar um ambiente virtual, execute o seguinte comando estando no diretório do projeto:

```
python -m venv env
```

ou

```
python3 -m venv env
```

* Para ativar o ambiente virtual, execute o comando:

```
source env/bin/activate
```

* Para instalar as dependências do projeto, execute o comando:

```
pip install -r requirements.txt
```

## Uso

### Preparação do Emulador:

1. Abra o RetroArch com o core Gambatte (ou outro emulador) e carregue o jogo Pokémon Red/Blue
2. Certifique-se que o nome da janela é "RetroArch Gambatte v0.5.0-netlink"
   - Caso esteja usando outro emulador, altere o valor da variável `window_name` em main.py
3. Configure os controles no RetroArch:
   - Direcional: Setas do teclado
   - Botão A: Tecla X
   - Botão B: Tecla Z
   - Caso queira usar outras teclas, altere os valores nos métodos press_* em main.py

### Executando o Bot:

1. Leve seu personagem para uma área com Pokémon selvagens (como a grama alta)
2. Execute o comando:

```
python src/main.py
```
