$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
$pythonPath = Join-Path $PSScriptRoot '.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $pythonPath)) {
    python -m venv .venv
    if ($LASTEXITCODE -ne 0) { throw 'Virtual environment creation failed.' }
    & $pythonPath -m pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) { throw 'Dependency installation failed.' }
}
$env:DEBUG = 'true'
$env:DEMO_MODE = 'true'
& $pythonPath manage.py migrate --noinput
if ($LASTEXITCODE -ne 0) { throw 'Migration failed.' }
& $pythonPath manage.py seed_demo
if ($LASTEXITCODE -ne 0) { throw 'Demo initialization failed.' }
& $pythonPath manage.py runserver 127.0.0.1:8000
