$ErrorActionPreference = 'Stop'
$destino = Join-Path $PSScriptRoot 'vendor/lemonade'
New-Item -ItemType Directory -Force $destino | Out-Null
$release = Invoke-RestMethod 'https://api.github.com/repos/lemonade-sdk/lemonade/releases/tags/v2026.46.2'
$asset = $release.assets | Where-Object { $_.name -eq 'lemonade-embeddable-2026.46.2-windows-x64.zip' } | Select-Object -First 1
if (-not $asset) { throw 'Pacote Lemonade nao encontrado.' }
$zip = Join-Path $destino 'pacote.zip'
Write-Host 'Baixando Lemonade local...'
Invoke-WebRequest $asset.browser_download_url -OutFile $zip
$unpack = Join-Path $destino 'unpack'
Expand-Archive $zip -DestinationPath $unpack -Force
Copy-Item (Join-Path $unpack 'lemonade-embeddable-2026.46.2-windows-x64/*') $destino -Recurse -Force
if (-not (Test-Path (Join-Path $destino 'resources/server_models.json'))) { throw 'Pacote incompleto.' }
$config = Join-Path $destino 'config.json'
if (-not (Test-Path $config)) {
    @{ config_version = 2; ctx_size = 8192; models_dir = (Join-Path $destino 'models') } | ConvertTo-Json | Set-Content -LiteralPath $config -Encoding UTF8
}
Write-Host 'Pronto. Execute python iniciar_ia_local.py no ambiente Python do projeto. O primeiro uso baixa o modelo.'
