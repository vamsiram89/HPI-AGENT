$ErrorActionPreference = "Stop"

$python = "C:\Users\vamsi\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
if (-not (Test-Path -LiteralPath $python)) {
    $python = "python"
}

$env:HPI_API_BASE_URL = "http://127.0.0.1:8010"

Set-Location -LiteralPath (Join-Path $PSScriptRoot "..")
& $python -m streamlit run frontend/streamlit_app.py --server.port 8501
