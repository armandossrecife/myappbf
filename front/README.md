# MyFrontend

Frontend exemplo de Protótipo de Aplicação Web (Prova de Conceito) de CRUD de usuários e imagens

[Quadro de Atividades do Projeto Frontend](https://github.com/users/armandossrecife/projects/2)

# A. Ambiente de Desenvolvimento

Existe uma estrutura base que vamos seguir para a construção de nossas aplicações em [Flask](https://flask.palletsprojects.com): 

## 1. Virtual Environment

Vamos usar o esquema de [virtual environment](https://docs.python.org/3/library/venv.html)

```bash
python3 -m venv venv
```

Mais detalhes em [python venv](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment)

### 1.1 Para ativar o venv (Linux e MacOS)

```bash
source venv/bin/activate
```

### 1.2 Para desativar o venv 

```bash
deactivate
```

## 2. Uma vez criado e ativado o venv precisamos instalar os módulos, pacotes e bibliotecas usadas pela aplicação

```bash
pip3 install -r requirements.txt
```

## 3. É preciso configurar as variáveis de ambiente da aplicação

```bash
export MY_SECRET_KEY=?????????
```

## 4. Para executar a aplicação principal

```bash
flask --app main run --host=0.0.0.0 --port=5000
```

ou 

```bash
.\exec.sh
```

Abra o browser: http://localhost:5000/login

## Flask frontend review

https://docs.google.com/document/d/18dNSvBeZ-Ji6WL9jrgi468BCAzoJJKyjhowf5yxAlg0/edit?usp=sharing

## AdminLTE review

https://docs.google.com/document/d/1mgGSvdUIWNY7x4scjPTaJktxT_j2794COigfYlWTSME/edit?usp=sharing

# B. Descrição da estrutura da aplicação 

Segue uma breve descrição dos diretórios e arquivos:

**front/app**: O diretório (pacote) raiz da sua aplicação frontend.

**front/app/routes**: diretório contendo a implementação das rotas da aplicação frontend.

**front/static**: diretório que contem os arquivos e recursos estáticos da aplicação frontend.

**front/templates**: O diretório que contém os templates HTML usados para renderizar as páginas da aplicação frontend. Os templates estão organizados em subdiretórios, como auth/ e usuarios/, correspondendo as rotas das quais eles pertencem.

**front/main.py**: O ponto de entrada da aplicação Flask, onde você cria a instância do aplicativo frontend e registra os blueprints (routes).

**front/exec.sh**: Script para inicializar a aplicação frontend.

**front/README.md**: Um arquivo de documentação contendo informações sobre o projeto.

**front/requirements.txt**: Um arquivo que lista as dependências do projeto.
