# MyBackend

Backend exemplo de Protótipo de Aplicação Web (Prova de Conceito) de CRUD de usuários e imagens

[Quadro de Atividades do Projeto Backend](https://github.com/users/armandossrecife/projects/1)

# A. Ambiente de Desenvolvimento

Existe uma estrutura base que vamos seguir para a construção de nossas aplicações em [FastAPI](https://fastapi.tiangolo.com/): 

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

## 3. Para executar a aplicação principal

```bash
uvicorn main:app --reload
```
ou 
```bash
./exec.sh
```

Abra o browser: http://localhost:8000/docs

## 4. Overview da aplicação

https://docs.google.com/document/d/1E8QYMgsawNVASWFHHU_ii1VbgwUiLRE4a-kui_ZyN4A/edit?usp=sharing

FastAPI backend review
https://docs.google.com/document/d/1mBNrYlrtHHlRcOyCSKadlsosLWAQUtsysH0kwCPsZiw/edit?usp=sharing

## 5. Execução dos testes automáticos

```bash
python3 -m pytest
```

# B. Descrição da estrutura da aplicação

Segue uma breve descrição dos diretórios e arquivos:

**back/app**: O diretório (pacote) raiz da sua aplicação.

**back/app/routes**: diretório que contém as rotas aplicação. Os arquivos auth.py, notes.py, profile.py e users.py definem as rotas e a lógica associada a cada uma delas.

**back/app/entidades.py**: módulo que contém as definições das classes de entidade da aplicação. 

**back/app/modelos.py**: módulo que contém as definições das classes de modelo da aplicação. 

**back/app/seguranca.py**: módulo que contém as definições de controle de acesso usando OAuth2PasswordBearer

**back/app/utilidades.py**: módulo que contem funções de hash e tokens da aplicação backend.

**back/app/banco.py**: módulo de acesso ao banco de dados.

**back/testes**: diretório contendo a implementação dos casos de testes automáticos da aplicação.

**back/main.py**: O ponto de entrada da aplicação FastAPI, onde você cria a instância do aplicativo e registra as rotas da aplicação backend.

**back/exec.sh**: Script que inicia a aplicação backend.

**back/README.md**: Um arquivo de documentação contendo informações sobre a aplicação backend.

**back/requirements.txt**: Um arquivo que lista as dependências do projeto.

**back/users.db**: O arquivo de banco de dados SQLite onde os dados dos usuários são armazenados.

**back/images**: Pasta (file system) que armazena os arquivos dos usuários.
