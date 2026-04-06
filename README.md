# Solitaire Pro

## Descrição do Projeto

O **Solitaire Pro** é uma aplicação desenvolvida em Python com a framework Flet, baseada no clássico jogo de cartas Solitaire. O projeto foi desenvolvido no âmbito da unidade curricular de Computação Móvel, com o objetivo de consolidar a utilização da framework Flet em aplicações interativas com interface gráfica.

A aplicação permite jogar Solitaire com as regras principais do modo clássico, incluindo movimentação de cartas entre colunas, fundações, pilha de compra e descarte. Foram ainda adicionadas funcionalidades obrigatórias e funcionalidades extra para melhorar a experiência de utilização.

---

## Funcionalidades Obrigatórias Implementadas

* Reiniciar o jogo
* Desfazer jogadas (undo)
* Guardar estado do jogo
* Alterar verso das cartas
* Sistema de pontuação
* Cronómetro visível durante toda a partida

---

## Funcionalidades Extra – Objetivo 3

## 1. Tema Dark / Light

Uma das funcionalidades extra implementadas foi a possibilidade de alternar entre dois temas visuais da aplicação: modo claro e modo escuro. Esta funcionalidade foi adicionada com o objetivo de melhorar a experiência de utilização e tornar a interface mais confortável em diferentes condições de iluminação, sobretudo em dispositivos móveis, onde o utilizador pode jogar em ambientes com pouca luz.

A implementação foi feita através de um botão disponível na barra superior da aplicação, identificado com o ícone de tema. Quando o utilizador carrega nesse botão, a cor de fundo principal do jogo altera entre verde tradicional e um tom escuro, mantendo a legibilidade dos elementos visuais principais. Esta mudança é imediata e não interfere com o estado atual do jogo.

A escolha desta funcionalidade prende-se com o facto de muitas aplicações modernas oferecerem modos visuais alternativos, permitindo maior personalização e adaptação às preferências do utilizador. Embora tecnicamente simples, representa uma melhoria relevante ao nível da usabilidade.

Para utilizar esta funcionalidade basta clicar no botão de tema localizado no topo da interface. O estado visual muda automaticamente, podendo ser alternado sempre que necessário durante a partida.

---

## 2. Novo Jogo Aleatório

A segunda funcionalidade extra implementada foi a criação de um botão de novo jogo aleatório. Esta funcionalidade permite iniciar imediatamente uma nova partida com uma distribuição diferente de cartas, sem necessidade de reiniciar toda a aplicação.

A sua inclusão teve como objetivo melhorar a fluidez da experiência de jogo, permitindo ao utilizador testar rapidamente novas combinações de cartas e iniciar várias partidas consecutivas de forma mais prática. Em jogos de cartas como o Solitaire, esta funcionalidade é bastante relevante porque aumenta a rejogabilidade.

A implementação reutiliza a lógica já existente de criação de jogo, limpando o estado atual, reorganizando as cartas e distribuindo novamente o baralho de forma aleatória. O cronómetro é reiniciado, a pontuação volta a zero e todas as pilhas são reconstruídas.

A funcionalidade encontra-se acessível através do botão **Novo Jogo**, presente na barra superior da aplicação.

Sempre que o utilizador carrega neste botão, é gerada imediatamente uma nova configuração de jogo, mantendo a aplicação responsiva e sem necessidade de recarregar a página.

---

## Deploy

A aplicação foi preparada para execução em ambiente web através do Flet, permitindo deploy em serviços como Replit.

Para execução local:

```bash
python main.py
```

A aplicação utiliza:

* host = 0.0.0.0
* port = 8550 (ou 8080 em deploy)

---

## Estrutura do Projeto

* main.py
* solitaire.py
* card.py
* slot.py
* model.py
* images/
* README.md

---

## Autor

João Oliveira
