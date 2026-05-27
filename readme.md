# 📰 Agregador de Notícias API

API REST para agregação automática de notícias de múltiplas fontes, desenvolvida com Django REST Framework.

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Django](https://img.shields.io/badge/Django-5.2-green)
![DRF](https://img.shields.io/badge/DRF-3.17-red)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue)

## 🚀 Funcionalidades

- Coleta automática de notícias via RSS e NewsAPI
- Autenticação com JWT (registro, login, refresh token)
- Filtro de artigos por fonte e categoria
- Busca por palavra-chave
- Preferências personalizadas por usuário
- Documentação interativa com Swagger

## 🛠️ Tecnologias

- **Python 3.10** + **Django 5.2**
- **Django REST Framework** — endpoints REST
- **SimpleJWT** — autenticação com tokens JWT
- **Celery + Redis** — coleta automática em background
- **PostgreSQL** — banco de dados
- **drf-spectacular** — documentação Swagger
- **feedparser** — leitura de feeds RSS

## ⚙️ Como rodar localmente

### Pré-requisitos
- Python 3.10+
- PostgreSQL 15
- Redis

### Instalação

```bash
# Clone o repositório
git clone https://github.com/CaaCPaaP/agregador-noticias.git
cd agregador-noticias

# Crie e ative o virtualenv
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Instale as dependências
pip install -r requirements.txt

# Configure as variáveis de ambiente
cp .env.example .env
# Edite o .env com suas configurações
```

### Banco de dados

```bash
# Crie o banco no PostgreSQL
psql -U postgres -c "CREATE DATABASE agregador_noticias;"

# Aplique as migrations
python manage.py migrate

# Crie um superusuário
python manage.py createsuperuser
```

### Rodando o servidor

```bash
python manage.py runserver
```

## 📋 Endpoints principais

| Método | Endpoint | Descrição | Auth |
|--------|----------|-----------|------|
| POST | `/api/auth/register/` | Cadastro de usuário | ❌ |
| POST | `/api/auth/login/` | Login e geração de token | ❌ |
| POST | `/api/auth/refresh/` | Refresh do token | ❌ |
| GET | `/api/articles/` | Listar artigos | ❌ |
| GET | `/api/articles/?search=python` | Buscar artigos | ❌ |
| GET | `/api/articles/?category=1` | Filtrar por categoria | ❌ |
| GET | `/api/categories/` | Listar categorias | ❌ |
| GET | `/api/sources/` | Listar fontes | ❌ |
| GET | `/api/user/preferences/` | Ver preferências | ✅ |
| PUT | `/api/user/preferences/` | Atualizar preferências | ✅ |

## 📖 Documentação

Com o servidor rodando, acesse:

```
http://127.0.0.1:8000/api/docs/
```

## 🧪 Testes

```bash
python manage.py test
```