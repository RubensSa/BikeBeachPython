<#
run_local.ps1
Script simples para execução local no Windows (apresentação acadêmica).

Funcionalidades:
- cria/atualiza ambiente virtual (`.venv` por padrão)
- instala `requirements.txt`
- executa `migrate` e `collectstatic`
- inicia o servidor Django localmente (em foreground)

Uso:
  .\run_local.ps1 [-VenvPath .venv] [-Bind 127.0.0.1] [-Port 8000] [-NoStart]
#>

param(
    [string]$VenvPath = ".venv",
    [string]$Bind = "127.0.0.1",
    [int]$Port = 8000,
    [switch]$NoStart
)

Set-StrictMode -Version Latest

function Fail([string]$msg){ Write-Error $msg; exit 1 }

Write-Host "Preparando ambiente local..." -ForegroundColor Cyan

# localizar executável Python (prefira py)
$pythonCmd = (Get-Command py -ErrorAction SilentlyContinue)?.Source -or (Get-Command python -ErrorAction SilentlyContinue)?.Source
if (-not $pythonCmd) { Fail "Python não encontrado no PATH. Instale Python 3 e tente novamente." }

Write-Host "Usando Python: $pythonCmd"

# criar virtualenv se necessário
if (-not (Test-Path $VenvPath)){
    Write-Host "Criando virtualenv em '$VenvPath'..."
    & $pythonCmd -3 -m venv $VenvPath
    if ($LASTEXITCODE -ne 0) { Fail "Falha ao criar virtualenv." }
} else {
    Write-Host "Virtualenv encontrado em '$VenvPath'"
}

$venvPython = Join-Path $VenvPath "Scripts\python.exe"
$venvPip = Join-Path $VenvPath "Scripts\pip.exe"

if (-not (Test-Path $venvPython)) { Fail "Python da virtualenv não encontrado em $venvPython" }

Write-Host "Atualizando pip..."
& $venvPython -m pip install --upgrade pip setuptools wheel

if (Test-Path "requirements.txt"){
    Write-Host "Instalando dependências de requirements.txt..."
    & $venvPip install -r requirements.txt
} else {
    Write-Warning "Arquivo requirements.txt não encontrado — pulando instalação de dependências." 
}

Write-Host "Executando migrações..."
& $venvPython manage.py migrate --noinput

Write-Host "Coletando arquivos estáticos..."
& $venvPython manage.py collectstatic --noinput

if ($NoStart) { Write-Host "Preparação concluída (servidor não iniciado porque -NoStart foi especificado)."; exit 0 }

Write-Host "Iniciando servidor de desenvolvimento Django em http://$Bind`:$Port/ (ctrl+C para parar)" -ForegroundColor Green
& $venvPython manage.py runserver "$Bind`:$Port"
