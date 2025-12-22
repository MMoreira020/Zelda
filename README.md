# ⚔️ Zelda Python RPG

Uma recriação inspirada no clássico "The Legend of Zelda", desenvolvida inteiramente em Python. Este projeto é um RPG de ação que explora mecânicas de combate, sistema de níveis (XP), gestão de inventário e inteligência artificial de inimigos.

![Preview do Jogo](https://github.com/MMoreira020/Zelda/blob/main/ZELDA.jpg)
*Legenda: Explore o mapa, derrote inimigos e evolua suas habilidades.*

## 🎮 Funcionalidades

* **Sistema de Combate:** Ataques com armas e magias elementares com sistema de partículas.
* **Evolução do Personagem:** Interface de upgrade para melhorar atributos como força, saúde e velocidade.
* **IA de Inimigos:** Diferentes tipos de inimigos com comportamentos de perseguição e ataque.
* **UI Completa:** Barras de vida, energia, exibição de armas/magias e sistema de pontuação (`score.txt`).
* **Ambiente Imersivo:** Sons integrados para ações, magias e música de fundo.

## 🛠️ Tecnologias Utilizadas

* **Python 3.x**
* **Pygame:** Biblioteca principal para renderização de gráficos 2D e física.

## 📁 Estrutura do Projeto

* `player.py` & `entity.py`: Lógica do personagem principal e herança de entidades.
* `enemy.py`: Inteligência artificial e estados dos monstros.
* `level.py`: Gerenciamento de mapas, colisões e instanciamento de objetos.
* `magic.py` & `weapon.py`: Sistemas de ataque e partículas.
* `ui.py` & `upgrade.py`: Menus e interface de usuário.
* `graphics/` & `audio/`: Assets visuais e sonoros do jogo.

## 🚀 Como Jogar

**Pré-requisitos:** Ter o Python e a biblioteca Pygame instalados.

1. **Clone o repositório:**
   ```bash
   git clone [https://github.com/MMoreira020/Zelda.git](https://github.com/MMoreira020/Zelda.git)
   cd Zelda
