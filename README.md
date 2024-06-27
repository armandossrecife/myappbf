# Myappbf

Exemplo de Protótipo de Aplicação Web (Prova de Conceito) de CRUD de usuários e imagens. 

A aplicação é dividida em dois contextos principais: uma aplicação backend (usando FastAPI) e uma aplicação frontend (usando Flask)

[back](https://github.com/armandossrecife/myappbf/tree/main/back) - diretório da aplicação backend

[front](https://github.com/armandossrecife/myappbf/tree/main/front) - diretório da aplicação frontend

# A. Tecnologias e configurações do projeto

## Tecnologias

Aqui estão as principais tecnologias e frameworks utilizados na aplicação:

**FastAPI**: FastAPI é um web framework moderno construir APIs RESTful em Python.

**Flask**: Flask é um framework web em Python utilizado para desenvolvimento de aplicações web. Ele fornece recursos para gerenciamento de rotas, renderização de templates, manipulação de requisições e muito mais. É a base da aplicação e permite a criação de uma aplicação web de forma simples e eficiente.

**SQLite**: SQLite é um banco de dados relacional embutido utilizado para armazenar os dados dos usuários cadastrados na aplicação. É uma opção leve e prática para aplicações de pequeno a médio porte.

**HTML**: [HTML](https://en.wikipedia.org/wiki/HTML) (Hypertext Markup Language) é a linguagem de marcação utilizada para estruturar e organizar o conteúdo das páginas web. É a base para a criação dos templates HTML da aplicação.

**CSS**: [CSS](https://en.wikipedia.org/wiki/CSS) (Cascading Style Sheets) é uma linguagem utilizada para estilizar e formatar as páginas web. É utilizada para definir o layout, cores, fontes e outros aspectos visuais da aplicação.

**PlantUML**: [PlantUML](https://en.wikipedia.org/wiki/PlantUML) é uma ferramenta para criação de diagramas UML de forma textual. Foi utilizado para gerar os diagramas de componentes e camadas da aplicação.

**AdminLTE**: [AdminLTE](https://adminlte.io) é um framework de interface do usuário (UI) e um tema de administração de código aberto amplamente utilizado para criar painéis e painéis de administração modernos, responsivos e atraentes.

Essas são as principais tecnologias e frameworks utilizados na aplicação. Cada uma desempenha um papel importante na construção e funcionamento da aplicação web Flask, desde o framework Flask em si até as linguagens de marcação utilizadas para criar as páginas web.

# B. Principais bibliotecas

## 1. uvicorn

Objetivo: Uma poderosa implementação de servidor ASGI (Asynchronous Server Gateway Interface) para executar estruturas web Python como FastAPI.

Características principais:
- Lida com solicitações e respostas HTTP de maneira eficiente e assíncrona.
- Recarga a quente para atualizações automáticas de código sem reinicialização do servidor.
- Suporta WebSockets para comunicação em tempo real.

Casos de uso: Desenvolvimento e implantação de aplicativos web de alto desempenho desenvolvidos com FastAPI ou outras estruturas ASGI.

## 2. bcrypt

Objetivo: Uma biblioteca segura de hash de senha que implementa o algoritmo bcrypt, um padrão industrial amplamente utilizado para armazenamento de senhas.

Características principais:
- Gera hashes de senha fortes e unilaterais que não podem ser facilmente revertidos.
- Fator de trabalho ajustável para controlar o tempo necessário para gerar um hash, equilibrando segurança com desempenho.
- Verifica as correspondências de senha em relação aos hashes armazenados para autenticação segura.

Casos de uso: Armazenamento seguro de senhas em bancos de dados para autenticação de usuários em aplicações web.

## 3. pydantic

Objetivo: Uma biblioteca de validação e análise de dados para Python. Ajuda a definir modelos de dados e garante que os dados recebidos estejam de acordo com a estrutura especificada.

Características principais:
- Cria modelos de dados com dicas de tipo para representação clara dos dados.
- Valida os dados recebidos em relação aos modelos definidos, gerando exceções para tipos ou valores inválidos.
- Converte dados automaticamente para os tipos definidos durante a análise.

Casos de uso: criação de APIs que impõem formatos de dados específicos para solicitações e respostas. Simplificando a validação e limpeza de dados em aplicativos da web.

## 4. python-jose

Objetivo: Uma biblioteca para implementação de JSON Web Encryption (JWE) e JSON Web Signatures (JWS), tecnologias essenciais para transmissão segura de dados e autenticação usando JSON Web Tokens (JWTs).

Características principais:
- Cria e analisa tokens JWE e JWS usando vários algoritmos de criptografia e métodos de assinatura.
- Verifica a integridade e autenticidade dos tokens assinados.
- Suporta gerenciamento de chaves para uso seguro de chaves de criptografia e assinatura.

Casos de uso: Construindo sistemas de autenticação seguros com JWTs em aplicações web ou APIs.

## 5. cryptography

Objetivo: Uma biblioteca criptográfica abrangente para Python, que fornece uma ampla gama de algoritmos e funcionalidades para criptografia, descriptografia, hash, assinaturas digitais e muito mais.

Características principais:
- Implementa vários algoritmos criptográficos (por exemplo, AES, RSA, Elliptic Curve Cryptography) para manipulação segura de dados.
- Fornece recursos seguros de geração e gerenciamento de chaves.
- Integra-se com outras bibliotecas como python-jose para casos de uso específicos.

Casos de uso: implementação de canais de comunicação seguros, criptografia e descriptografia de dados confidenciais e criação de assinaturas digitais para verificação de integridade de dados.

## 6. httpx

Objetivo: Uma biblioteca cliente HTTP assíncrona para Python, oferecendo desempenho mais rápido para fazer solicitações HTTP em comparação com bibliotecas síncronas tradicionais.

Características principais:
- Lida com solicitações HTTP de forma assíncrona, permitindo operações simultâneas e melhor desempenho.
- Suporta vários métodos HTTP (GET, POST, PUT, etc.) e cabeçalhos de solicitação/resposta.
- Integra-se com estruturas assíncronas como FastAPI para desenvolvimento web eficiente.

Casos de uso: Criação de aplicativos web de alto desempenho que fazem solicitações HTTP frequentes.

## 7. pytest

Objetivo: Uma estrutura de teste Python popular e rica em recursos, amplamente usada para testes unitários, testes de integração e testes ponta a ponta.

Características principais:
- Sintaxe expressiva para escrever casos de teste claros e concisos.
- Dispositivos para gerenciar a configuração e desmontagem dos testes.
- Asserções para verificar os resultados esperados do teste.
- Plugins para estender funcionalidade (por exemplo, para testes assíncronos com pytest-asyncio).

Casos de uso: gravação de testes unitários para funções ou módulos individuais, testes de integração para componentes trabalhando juntos e testes ponta a ponta para funcionalidade completa do aplicativo.

## 8. pytest-asyncio

Objetivo: um plug-in pytest que permite testes assíncronos para aplicativos que usam código assíncrono (por exemplo, com palavras-chave async/await).

Características principais:
- Fornece acessórios e decoradores projetados especificamente para cenários de teste assíncronos.

## 9. requests:

Função: Uma biblioteca HTTP para Python que simplifica o envio e recebimento de requisições HTTP.

Características principais:
- Faz requisições GET, POST, PUT, DELETE e outras com apenas algumas linhas de código.
- Trata automaticamente respostas HTTP, incluindo redirecionamentos e cookies.
- Permite enviar e receber dados em diversos formatos (JSON, XML, etc.).
- Suporta autenticação básica e por cabeçalho.

Casos de uso:
- Consumir APIs RESTful e outros serviços web.
- Fazer scrapings de sites.
- Automatizar tarefas que envolvem requisições HTTP.

## 10. requests-mock:

Função: Uma biblioteca para mockar (simular) respostas HTTP em testes de Python.

Características principais:
- Permite definir respostas HTTP personalizadas para qualquer URL ou método (GET, POST, etc.).
- Suporta simulação de erros, redirecionamentos e diferentes códigos de status.
- Integra-se com a biblioteca requests para facilitar o teste de código que faz requisições HTTP.

Casos de uso:
- Testar o comportamento do seu código em diferentes cenários de resposta HTTP.
- Isolar o código que faz requisições HTTP de outros componentes para testes mais precisos.
- Simular APIs externas para testes quando o acesso real não é possível ou desejável.

## 11. selenium:

Função: Uma biblioteca para automação de testes em navegadores web.

Características principais:
- Controla navegadores como Chrome, Firefox e Edge por meio de comandos programáticos.
- Interage com elementos HTML, como botões, links e campos de texto.
- Preenche formulários, executa JavaScript e captura screenshots.
- Suporta testes de unidade, integração e end-to-end em navegadores.

Casos de uso:
- Testar interfaces web de forma automatizada, identificando e corrigindo bugs.
- Realizar testes de regressão para garantir que novas funcionalidades não quebrem o código existente.
- Automatizar tarefas repetitivas em navegadores, como login em sites ou preenchimento de formulários.

## 12. Werkzeug:

Função: Um conjunto de ferramentas WSGI (Web Server Gateway Interface) para Python, usado para construir servidores web e frameworks web.

Características principais:
- Fornece classes e funções para lidar com requisições HTTP, como roteamento, cabeçalhos e cookies.
- Simplifica o desenvolvimento de frameworks web robustos e escaláveis.
- Inclui ferramentas para manipulação de strings, geração de HTML e tratamento de uploads de arquivos.

Casos de uso:
- Desenvolver frameworks web personalizados e flexíveis.
- Criar servidores web simples para fins de teste ou prototipagem.
- Extender a funcionalidade de frameworks web existentes.
