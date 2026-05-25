# Bike Beach

Aplicação Django para gerenciamento de aluguel de bicicletas — projeto acadêmico para Programação Web I.

Pré-requisitos
- Python 3.10+
- virtualenv (recomendado)

Instalação e execução
```bash
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
.venv\Scripts\activate      # Windows PowerShell
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser  # opcional
python manage.py runserver
```

Funcionalidades
- Cadastro, login e logout (sistema nativo do Django)
- Perfil de usuário
- CRUD de bicicletas (apenas dono pode editar/excluir)
- Alugar e devolver bicicletas; disponibilidade controlada
- Busca por nome/modelo via GET
- Mensagens de feedback com Django Messages

Estrutura
- app `accounts`: autenticação, registro, perfil
- app `rentals`: modelos `Bicicleta` e `Aluguel`, views e templates

Banco de dados
- SQLite (arquivo `db.sqlite3`)
