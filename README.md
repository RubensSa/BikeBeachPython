# Bike Beach

Aplicação Django para gerenciamento de aluguel de bicicletas — projeto acadêmico.

Pré-requisitos
- Python 3.10+ (ou `py` launcher)

Instalação e execução (modo local — para apresentação acadêmica)
```powershell
python -m venv .venv
. .venv\Scripts\Activate.ps1   # Windows PowerShell
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput  # opcional, se usar arquivos estáticos
# Bike Beach

Aplicação Django para gerenciamento de aluguel de bicicletas — projeto acadêmico.

Pré-requisitos
- Python 3.10+ (ou `py` launcher)

Instalação e execução (modo local — para apresentação acadêmica)
```powershell
python -m venv .venv
. .venv\Scripts\Activate.ps1   # Windows PowerShell
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput  # opcional, se usar arquivos estáticos
python manage.py runserver
```

Parar o servidor
- Para interromper o servidor de desenvolvimento no Windows, volte ao terminal onde o servidor está rodando e pressione CTRL + C.

Banco de dados
- SQLite (arquivo `db.sqlite3`)

Script disponível
- `deploy\\deploy_windows.ps1`: script PowerShell para Windows que cria o ambiente virtual, instala dependências, aplica migrações, coleta estáticos e inicia o servidor localmente.

Observação
- O repositório foi simplificado para execução local apenas (sem configurações de deploy remoto).

