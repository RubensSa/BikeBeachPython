# Bike Beach

Aplicação Django para gerenciamento de aluguel de bicicletas — projeto acadêmico para Programação Web I.

Pré-requisitos
- Python 3.10+
- virtualenv (recomendado)

Instalação e execução
```bash
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
 
Deploy em produção (resumo)
--------------------------------
Opções recomendadas para colocar a aplicação em produção.

1) Gunicorn + Nginx (Linux)
- Gere um `requirements.txt` atualizado: `pip freeze > requirements.txt`.
- Configure variáveis de ambiente (não usar `SECRET_KEY` no código):
	- `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=False`, `DJANGO_ALLOWED_HOSTS=seu_dominio,IP`
- Instale dependências e Gunicorn: `pip install -r requirements.txt gunicorn`
- Rode migrações e colete estáticos:
```bash
python manage.py migrate
python manage.py collectstatic --noinput
```
- Crie um serviço systemd (ex.: `/etc/systemd/system/bikebeach.service`) que execute:
```bash
gunicorn bikebeach.wsgi:application --bind 127.0.0.1:8000 --workers 3
```
- Configure Nginx como proxy reverso (SSL recomendado via Let's Encrypt) e proxy para `127.0.0.1:8000`.

2) Docker (alternativa portátil)
- Exemplo rápido de `Dockerfile`:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN python manage.py collectstatic --noinput
CMD ["gunicorn", "bikebeach.wsgi:application", "--bind", "0.0.0.0:8000"]
```
- `docker build -t bikebeach .` e `docker run -p 8000:8000 -e DJANGO_DEBUG=False -e DJANGO_SECRET_KEY=... bikebeach`

Boas práticas
- Sempre `DEBUG = False` em produção.
- Use `ALLOWED_HOSTS` restrito (não `['*']`).
- Use um banco de dados apropriado (Postgres é recomendado), e mantenha credenciais em variáveis de ambiente.
- Habilite HTTPS no proxy (Nginx) com Certbot/Let's Encrypt.

Quer que eu gere um `Dockerfile`, `docker-compose.yml` ou um arquivo `systemd` de exemplo aqui no repositório?

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN python manage.py collectstatic --noinput
CMD ["gunicorn", "bikebeach.wsgi:application", "--bind", "0.0.0.0:8000"]
```
- `docker build -t bikebeach .` e `docker run -p 8000:8000 -e DJANGO_DEBUG=False -e DJANGO_SECRET_KEY=... bikebeach`

Boas práticas
- Sempre `DEBUG = False` em produção.
- Use `ALLOWED_HOSTS` restrito (não `['*']`).
- Use um banco de dados apropriado (Postgres é recomendado), e mantenha credenciais em variáveis de ambiente.
- Habilite HTTPS no proxy (Nginx) com Certbot/Let's Encrypt.

Quer que eu gere um `Dockerfile`, `docker-compose.yml` ou um arquivo `systemd` de exemplo aqui no repositório? 

>>>>>>> f53f60b (Save local changes before rebase)
