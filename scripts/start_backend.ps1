$ErrorActionPreference = "Stop"

$python = "C:\Users\vamsi\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
if (-not (Test-Path -LiteralPath $python)) {
    $python = "python"
}

Set-Location -LiteralPath (Join-Path $PSScriptRoot "..")
& $python -m uvicorn backend.main:app --host 127.0.0.1 --port 8010
