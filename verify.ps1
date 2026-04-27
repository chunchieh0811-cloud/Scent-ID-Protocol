Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

Set-Location $PSScriptRoot

Write-Host "== Scent-ID Health Check ==" -ForegroundColor Cyan

$requiredDirs = @(
    "01_Constitution",
    "02_Protocol",
    "03_Application"
)

foreach ($dir in $requiredDirs) {
    if (-not (Test-Path $dir -PathType Container)) {
        throw "Missing required directory: $dir"
    }
    Write-Host "[OK] Directory exists: $dir"
}

if (-not (Test-Path ".env")) {
    Write-Host "[WARN] .env not found (expected for external USB key workflow)."
} else {
    Write-Host "[OK] .env found"
}

Write-Host "Running locked PDF build..." -ForegroundColor Yellow
python "02_Protocol/build_locked_pdf.py"
if ($LASTEXITCODE -ne 0) {
    throw "PDF generation failed."
}

$pdf = "03_Application/ScentID_Master_Archive_LOCKED.pdf"
if (-not (Test-Path $pdf -PathType Leaf)) {
    throw "Output PDF not found: $pdf"
}

Write-Host "[OK] PDF generated: $pdf"
Write-Host "Health check completed." -ForegroundColor Green
