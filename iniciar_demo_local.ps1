$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
$python = Join-Path $PSScriptRoot '.venv/Scripts/python.exe'
if (-not (Test-Path $python)) { throw 'Prepare .venv seguindo documentacao/af/EXECUCAO.md.' }
$java = Get-Command java -ErrorAction SilentlyContinue
if (-not $java) { throw 'Configure Java 17 no PATH antes de continuar.' }
& $python preparar_af.py
Get-Content .env.af | ForEach-Object {
    if ($_ -match '^([^#=]+)=(.*)$') { [Environment]::SetEnvironmentVariable($matches[1], $matches[2], 'Process') }
}
$env:AF_AI_HOST = '127.0.0.1'
$env:ML_DATA_DIR = Join-Path $PSScriptRoot 'runtime/ml-demo'
$env:ML_AUTO_TRAIN = 'false'
$env:OPENBLAS_NUM_THREADS = '1'
& .\mvnw.cmd package -DskipTests
if ($LASTEXITCODE -ne 0) { throw 'Falha ao compilar Java.' }
Push-Location ml
try { & $python training.py } finally { Pop-Location }
if ($LASTEXITCODE -ne 0) { throw 'Falha ao preparar modelo sintetico.' }
New-Item -ItemType Directory -Force runtime | Out-Null
$children = @()
try {
    $children += Start-Process -FilePath $python -ArgumentList 'iniciar_ia_local.py' -WorkingDirectory $PSScriptRoot -WindowStyle Hidden -RedirectStandardOutput 'runtime/ia-out.log' -RedirectStandardError 'runtime/ia-err.log' -PassThru
    $children += Start-Process -FilePath $python -ArgumentList '-m','uvicorn','app:app','--host','127.0.0.1','--port','8011' -WorkingDirectory (Join-Path $PSScriptRoot 'ml') -WindowStyle Hidden -RedirectStandardOutput 'runtime/ml-out.log' -RedirectStandardError 'runtime/ml-err.log' -PassThru
    $children += Start-Process -FilePath $java.Source -ArgumentList '-jar','target/educacao-gamificada-0.0.1-SNAPSHOT.jar','--spring.profiles.active=af','--server.address=127.0.0.1','--spring.rabbitmq.listener.simple.auto-startup=false' -WorkingDirectory $PSScriptRoot -WindowStyle Hidden -RedirectStandardOutput 'runtime/core-out.log' -RedirectStandardError 'runtime/core-err.log' -PassThru
    Write-Host 'Demo local: http://localhost:8085/af.html. Aguarde os servicos iniciarem.'
    Write-Host 'Core/H2 + ML + RAG/RAGAS locais. Sem RabbitMQ: demonstre treinamento pela evidencia da CI.'
    Write-Host 'Consulte AF_ADMIN_PASSWORD no .env.af local. Nao mostre a senha na gravacao.'
    Read-Host 'Pressione Enter somente quando quiser ENCERRAR a demonstracao'
} finally {
    foreach ($child in $children) {
        if (-not $child.HasExited) { & taskkill /PID $child.Id /T /F | Out-Null }
    }
}
