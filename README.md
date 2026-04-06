# Solitaire Pro

## Descrição
O **Solitaire Pro** é uma aplicação desenvolvida em **Python** com a framework **Flet**, baseada no jogo clássico Solitaire.  
A aplicação permite jogar através de interface gráfica, com suporte para ações como mover cartas entre colunas, enviar cartas para as fundações, reiniciar o jogo, desfazer jogadas e personalizar o visual das cartas.

Além das funcionalidades base do tutorial, foram também implementadas funcionalidades extra obrigatórias e duas funcionalidades adicionais escolhidas para melhorar a experiência de utilização.

---

## Funcionalidades implementadas

### Funcionalidades base
- Jogo de Solitaire funcional
- Tableau, stock, waste e foundations
- Drag and drop de cartas
- Regras de movimento entre colunas e fundações
- Deteção de vitória

### Funcionalidades extra obrigatórias
- Reiniciar jogo
- Desfazer jogadas
- Guardar estado do jogo
- Escolher a traseira das cartas entre 4 opções
- Sistema de pontuação
- Cronómetro visível durante toda a partida

### Funcionalidades adicionais (Objetivo 3)
- Tema **dark/light**
- Botão de **novo jogo aleatório**

---

## Funcionalidade extra 1: Tema dark/light
Foi adicionada a possibilidade de alternar entre um tema visual mais claro, com o tabuleiro verde tradicional, e um tema mais escuro.  
Esta funcionalidade foi escolhida por ser útil em diferentes contextos de utilização. Num ambiente com pouca luz, o tema escuro torna a interface mais confortável para o utilizador, reduzindo o impacto visual e melhorando a legibilidade. Já o tema clássico mantém uma aparência semelhante ao jogo tradicional, tornando a experiência mais familiar.

A alternância é feita através de um botão disponível na barra superior da aplicação. Assim, o utilizador pode mudar rapidamente o aspeto visual da interface sem interromper a partida.  
Esta melhoria contribui para a personalização da aplicação e para uma melhor experiência de utilização, especialmente em dispositivos móveis, onde a adaptação visual é importante.

---

## Funcionalidade extra 2: Novo jogo aleatório
Foi adicionada uma opção de **novo jogo aleatório**, que permite começar imediatamente uma nova partida com uma distribuição diferente das cartas.  
Esta funcionalidade difere da opção de reiniciar, pois o reinício mantém a lógica da mesma sessão, enquanto o novo jogo cria uma nova configuração aleatória desde o início.

A principal vantagem desta funcionalidade é aumentar a rejogabilidade. O utilizador pode iniciar rapidamente uma nova partida sem precisar de fechar ou recarregar a aplicação.  
Esta opção também melhora a usabilidade, porque oferece uma forma simples e direta de continuar a jogar, tornando a interação mais fluida. Em contexto académico, esta funcionalidade demonstra também a capacidade de controlar o estado interno da aplicação e gerar novas sessões de jogo de forma organizada.

---

## Guardar estado
A aplicação inclui uma funcionalidade de guardar estado, utilizando armazenamento local disponível no navegador.  
São guardados elementos relevantes como a pontuação, o tempo decorrido e o verso atualmente selecionado para as cartas. Isto permite preservar informação entre execuções da aplicação.

---

## Estrutura do projeto

- `main.py` — ponto de entrada da aplicação
- `solitaire.py` — lógica principal do jogo
- `card.py` — definição e comportamento das cartas
- `slot.py` — definição dos espaços/pilhas
- `model.py` — classes auxiliares (`Suite` e `Rank`)
- `images/` — imagens das cartas e recursos visuais

---

## Como executar localmente

1. Garantir que o Python está instalado.
2. Instalar a framework Flet:
   ```bash
   pip install flet
