# MyFrontend

Frontend exemplo de Protótipo de Aplicação Web (Prova de Conceito) de CRUD de usuários e imagens

[Quadro de Atividades do Projeto](http://TBD)

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
export FLASK_APP=run.py && export FLASK_ENV=development
```
```bash
export MY_SECRET_KEY=?????????
```

## 4. Para executar a aplicação principal

```bash
flask --app main run --host=0.0.0.0 --port=5000
```

Abra o browser: http://localhost:5000/login
