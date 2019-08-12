# Desafio SmarttBot

## Instalação

 - Requisitos: Docker, docker-compose
 - De dentro da pasta do repositório, executar os seguintes comandos:
    - `docker image build --tag desafio-smarttbot:latest docker/`
    - `docker-compose up -d --build`
    - `docker exec -it bots flask db upgrade`
    - `docker exec -it bots python setup/setup_db.py` (inicialização do banco de dados)

## Descrição do desafio

O desafio consistem em construir uma aplicação web para consumir a API pública de dados da Poloniex e distribuir o dados dos criptoativos para robôs de negociação. A estratégia utilizada pelos robôs é baseada no cruzamento de médias móveis e simula ordens de compra e venda de acordo com o comportamento das linhas.

Cada robô tem seus parâmetros de configuração e deve calcular uma média curta e uma longa com base nesses parâmetros. A ordem de compra é enviada quando a média curta cruza a média longa de baixo para cima e a ordem de venda é enviada quando a média curta cruza a longa de cima para baixo. A aplicação deve mostrar o resultado das operações para cada robô, listando quais foram as ordems e quanto aquele robô teria de lucro/prejuízo até o momento.

## Considerações

Para os robôs, considerei que eles são cadastrados em um formulário e, além das configurações referentes às médias móveis e ao período utilizados na estratégia, cada robô possui um risco e um retorno pré-definidos para suas operações. A partir desse risco e retorno é possível encontrar o preço alvo e o preço de stop loss do criptoativo negociado pelo robô. No caso da compra, o ```preço alvo = preço de entrada + retorno esperado```, e o preço de ```stop loss = preço de entrada - risco```. A venda funciona da mesma maneira, porém no sentido contrário. Outra configuração feita foi a quantidade operada. Como são criptoativos, o formulário considera quantidades fracionadas.

A motivação da entrada das operações segue a estratégia de cruzamento das médias móveis, porém uma vez dentro da operação, a operação só é fechada atingindo o preço alvo ou o stop loss. Esse comportamento foi adotado, para evitar repetidas operações de compra e venda quando as médias ficam "dançando" uma em cima da outra. Dessa maneira, uma nova operação só é realizada após o fechamento da anterior.

## App

A aplicação web possui duas seções principais: Cotações e Bots. Os links para essas seções são encontrados na barra de navegação superior, conforme imagem abaixo. A tela abaixo apresenta a grade de cotações dos criptoativos com as informações das últimas 24 horas para cada ativo disponibilizado na Poloniex. Essa tela não possui funcionalidades e somente apresenta as cotações atuais que são atualizadas a cada atualização da página.

![Grade de cotações](https://raw.githubusercontent.com/ricardoerikson/desafio-smarttbot/master/img/cotacoes.png)

A página seguinte (que pode ser acessada pelo link 'Bots' da barra de navegação) apresenta os robôs cadastrados e o seu estado atual. Os robôs ativos e que estão operando são os que possuem o status 'On'. Novos robôs são cadastrados pelo formulário que aparece ao clicar no botão ```Novo Bot``` que aparece logo acima da tabela. Essa tela também apresenta para cada robô listado, a possibilidade de editar os parâmetros do robô (assim como ativá-lo ou desativá-lo) e o link para a visualização das operações realizadas por cada robô. Uma vez ativado, o robô começa a monitorar o ativo cadastrado para ele com a finalidade de realizar as operações.

![Bots](https://raw.githubusercontent.com/ricardoerikson/desafio-smarttbot/master/img/bots.png)

Ao clicar no link ```Novo Bot``` ou ```Editar``` da tela anterior, é aberto um formulário que permite o cadastramento de um robô ou a edição de um robô já existente. Nesse formulário, é possível fazer o cadastramento e a edição dos parâmetros de cada robô.

![Form](https://raw.githubusercontent.com/ricardoerikson/desafio-smarttbot/master/img/edit.png)

Na tela a seguir (acessada pelo botão ```Visualizar``` na tela onde são listados os robôs), é possível visualizar as operações realizadas pelo robô identificado na página. Essa página mostra informações referentes à cada operação pelo robô, como horário de início da operação, horário de fechamento, par de moedas negociado, quantidade operada, preços de entrada e saída, direção da operação e resultado. Caso uma operação ainda não tenha sido fechada, ela aparece com status Aberta na cor amarela na coluna de horário de saída. Além disso, o preço de saída mostra o preço atual do criptoativo e não a saída real. Por conta disso, esse preço também fica na cor amarela. A coluna 'Resultado' mostra o resultado financeiro das operações já fechadas e da operação aberta, caso exista alguma.

![Trades](https://raw.githubusercontent.com/ricardoerikson/desafio-smarttbot/master/img/trades.png)

## Ferramentas e tecnologias utilizadas

 - Git
 - Github
 - Python 3.5
 - Bootstrap 4
 - Flask
 - SQLAlchemy
 - MySQL 5.7
 - Docker

### Versionamento de código

Para o gerenciamento de versões de código foi utilizado o Git com repositório no Github. Algumas configurações foram realizadas com a ajuda de bibliotecas de desenvolvimento do npm (`commitizen` e `cz-conventional-changelog`). Essas configurações visam justamente manter a padronização e organização das mensagens de commits a fim de auxiliar no versionamento da aplicação seguindo as convenções de [versionamento semântico](https://semver.org/). O pacote de desenvolvimento `semantic-release` faz a leitura das mensagens dos commits e faz o versionamento automático com base no lançamento de novas features e breaking changes. Além disso, essas ferramentas possuem integração com ferramentas de CI/CD como TravisCI, CircleCI e Gitlab CI/CD permitindo a atualização automatizada de changelog e criação de novas tags.

### Programação para Web

O backend da aplicação foi desenvolvido inteiramente na linguagem Python e o frontend foi desenvolvido em HTML utilizando componentes do Bootstrap4. O framework web utilizado foi o Flask juntamente com suas diversas bibliotecas relacionadas ao desenvolvimento web. Esse framework facilita a construção de rotas dinâmicas nas URLs e simplifica o desenvolvimento de aplicações Restful. O roteamento dinâmico das URLs foi todo realizado por meio das funcionalidades do Flask. A definição dos métodos HTTP para cada rota e criação de formulários também foram realizados, tratando inclusive de aspectos de segurança, como a proteção contra ataques CSRF.

Na aplicação web também foi realizado um agendamento da execução dos robôs para seguir a estratégia de cruzamento das médias móveis. Embora eu acredite que não seja a melhor solução, o arranjo de curto prazo encontrado foi executar a estratégia dos robôs a cada 10s para buscar oportunidades de compra e venda. Na parte de melhorias sugeridas eu comento o que penso sobre esse assunto da execução das estratégias dos robôs.

### Programação para Banco de Dados

Os modelos de dados da aplicação foram desenvolvidos utilizando o SQLAlchemy, que é um framework de mapeamento objeto-relacional desenvolvido em Python, que abstrai a manipulação de dados feita com SQL. Com esses modelos é possível fazer a criação da base e toda a manipulação dos dados sem escrever SQL. Embora o banco de dados utilizado nesse projeto tenha sido o MySQL 5.7, o recurso de mapeamento objeto relacional do SQLAlchemy, possibilita a utilização de outras bases de dados mantendo o mesmo modelo, realizando somente configurações mínimas para o projeto continuar funcionando.

### Docker

O docker permitiu a criação de uma aplicação multi-container que separou o projeto em 3 partes:

A primeira parte é uma aplicação que realiza as requisições à API pública da Poloniex. Essa primeira parte também foi desenvolvida com Flask e o roteamento dinâmico facilitou a customização e passagem de parâmetros para realizar requisições à Poloniex. Toda a implementação dessas requisições foi encapsulada no container e exposta por meio de uma API web de onde outras apalicações podem fazer requisições. Com isso a aplicação ganhou em modularidade. A API da Poloniex pode ser completamente substituída por outra (a do Google, por exemplo) e ainda assim, as outras partes da aplicação continuarão funcionando.

A segunda parte da aplicação também foi pensada em modularidade e é um container para o banco de dados. O container foi construído em cima de uma imagem do MySQL 5.7 e foi mapeado para a porta 3306, onde outras aplicações podem ter acesso a ele. Com o banco rodando em um container e com o mapeamento feito no SQLAlchemy, é possível trocar a base de dados por um outro banco realizando mudanças mínimas na aplicação.

A terceira parte da aplicação foi colocada em um terceiro container e onde está a lógica da aplicação propriamente dita. É lá onde os robôs são cadastrados e são executados para monitorar as médias móveis do ativo relacionado a ele.

Com essa configuração, 2 containers podem ser substituídos com impacto minimizado na estrutura do sistema como um todo.

## Desafios e dificuldades

Uma das principais dificuldades do projeto foi encontrar uma imagens do Docker compatível com as bibliotecas que seriam utilizadas no projeto. Não achando, a solução foi construir a própria imagem. Porém, duas das bibliotecas (pandas e numpy) que me economizariam tempo na parte de agregação de candles se tornaram um problema com o Docker. As imagem linux que tentei utilizar inicialmente não ofereciam um suporte amplo para a instalação do pandas e numpy. Dessa maneira, a compilação dessas bibliotecas no build da imagem demorava horas. Após muita procura, encontrei uma imagem compatível que diminuiu sgnificativamente o tempo de instalação das bibliotecas e dependências no build da imagem. Assim, o projeto seguiu.

Um desafio foi a falta de tempo para a criação de soluções mais elaboradas e fazer ajustes para entregar algo funcional. Por ser um sistema que a execução real depende de movimentações externas no mercado de criptomoedas, testar a execução das estratégias dos robôs se tornou algo bem complicado. Muitas vezes foi necessário manualmente enviar operações com valores manipulados diante de situações que se espera algo (o fechamento de uma operação, por exemplo) e esperar para ver como o sistema reagiria.

## Melhorias

Uma das melhorias que eu faria, conforme o crescimento do projeto, é separar o código por responsabilidades de cada feature. Isso melhora a organização do código, reduz acoplamento e aumenta coesão. Em um projeto grande, esse tipo de organização é essencial para a manter um crescimento saudável e sustentável do projeto.

Outra melhoria para esse projeto seria utilizar um sistema de cache para as requisições à API da Poloniex. Com o aumento do número de robôs, inúmeras requisições seriam realizadas, aumentando consideravelmente o tráfego de dados. Utilizando um sistema de cache, reduziria consideravelmente a quantidade de dados recuperados nas requisições. Ao solicitar os 10 candles de 5 minutos mais recentes de uma API, eu sei que somente o candle mais recente pode variar dentro dessa janela de 5 minutos. Os 9 candles mais antigos não se modificam. Portanto, não há a necessidade de requisitar sempre os 10 candles. Eu poderia, por exemplo, salvar os 9 candles mais antigos em um banco de dados não relacional com um tempo de expiração de 5 minutos e solicitar somente o candle mais recente da API. Assim, eu faria somente uma requisição completa (10 candles) a cada 5 minutos. Entre uma requisição completa e outra, recuperaria somente o candle mais recente. Embora seja possível pensar em soluções mais elaboradas, somente essa pequena mudançã, reduziria o tráfego de dados consideravelmente.

Outra melhoria que não foi possível implemementar é utilizar CI/CD. Cheguei a fazer uma configuração inicial no TravisCI, mas pela necessidade de partir direto para codificar as funcionalidades, o CI/CD acabou ficando para depois. Cheguei a desenvolver alguns testes unitários par executar localmente durante o desenvolvimento, porém seria interessante desenvolver mais testes unitários e de integração e executar de maneira automática em ferramentas de integração contínua. Isso possibilitaria também ter relatórios de cobertura dos teste e estabelecimento de métricas para aumentar a qualidade do código.