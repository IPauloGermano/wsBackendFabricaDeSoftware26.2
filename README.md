# 📚 Biblioteca - Catálogo & Favoritos

Sistema web desenvolvido em Django para gerenciamento de catálogo de livros e acompanhamento de leituras pessoais. O projeto combina acervo local com integração à API pública da [Open Library](https://openlibrary.org/).

---

## 🚀 Funcionalidades

- **Catálogo Híbrido**:
  - Busca integrada entre acervo local e remoto (Open Library).
  - Importação e persistência automática de livros da Open Library para o banco local.
  - CRUD completo de livros cadastrados (criação, edição, detalhamento e exclusão).
- **Gerenciamento de Favoritos e Leitura**:
  - Adição de livros aos favoritos por usuário autenticado.
  - Registro de progresso (página atual), nota de avaliação (1 a 5 estrelas) e anotações pessoais de leitura.
  - Remoção e edição de favoritos.
- **Autenticação**:
  - Cadastro de novas contas de usuário (`UserCreationForm` customizado).
  - Login e logout de usuários.

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.14+**
- **Django 6.1**
- **SQLite**
- **Python Decouple** (gerenciamento de variáveis de ambiente)
- **Requests** (consumo da API Open Library)
- **Bootstrap 5** (interface responsiva)

---

## 📦 Como Executar o Projeto Localmente

### 1. Clonar o Repositório
```bash
git clone <URL_DO_REPOSITORIO>
cd wsBackendFabricaDeSoftware26.2
```

### 2. Criar e Ativar o Ambiente Virtual
```bash
python3 -m venv .venv
source .venv/bin/activate  # No Linux/macOS
# ou: .venv\Scripts\activate no Windows
```

### 3. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 4. Configurar as Variáveis de Ambiente
Crie o arquivo `.env` na raiz do projeto com base no `.env.example`:
```bash
cp .env.example .env
```

Exemplo de conteúdo do `.env`:
```env
DJANGO_SECRET_KEY=sua-chave-secreta-aqui
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=*
```

### 5. Executar as Migrações
```bash
python manage.py migrate
```

### 6. Executar o Servidor de Desenvolvimento
```bash
python manage.py runserver
```
Acesse a aplicação em `http://127.0.0.1:8000/`.

---

## 🧪 Execução dos Testes Unitários

Para rodar a suíte de testes do projeto:
```bash
python manage.py test
```

---

## 📁 Estrutura do Projeto

```text
├── config/              # Configurações do projeto Django (settings, urls, wsgi, asgi)
├── livros/              # App de catálogo e integração com a Open Library
│   ├── models.py        # Modelo Livro
│   ├── services.py      # Integração com a API Open Library
│   ├── forms.py         # Formulário de livros
│   ├── views.py         # Views de listagem, detalhe e CRUD
│   └── tests.py         # Testes automatizados do app livros
├── favoritos/           # App de favoritos e acompanhamento de leitura
│   ├── models.py        # Modelo Favorito
│   ├── forms.py         # Formulários de favorito e registro de usuário
│   ├── views.py         # Views de favoritos e autenticação
│   └── tests.py         # Testes automatizados do app favoritos
├── templates/           # Templates HTML (base, livros, favoritos, registration)
├── static/              # Arquivos estáticos (CSS, JS, imagens)
├── .env.example         # Exemplo de configuração de variáveis de ambiente
├── requirements.txt     # Lista de dependências Python
└── manage.py            # Utilitário CLI do Django
```
