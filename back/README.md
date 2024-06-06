# MyBackend

Backtend exemplo de Protótipo de Aplicação Web (Prova de Conceito) de CRUD de usuários e imagens

[Quadro de Atividades do Projeto](http://TBD)

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

Abra o browser: http://localhost:8000/docs

## 4. Overview da aplicação

https://docs.google.com/document/d/1E8QYMgsawNVASWFHHU_ii1VbgwUiLRE4a-kui_ZyN4A/edit?usp=sharing