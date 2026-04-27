param(
    [Parameter(Mandatory = $false)]
    [string]$RemoteUrl = ""
)

$ErrorActionPreference = "Stop"

Set-Location $PSScriptRoot

if (-not (Test-Path ".git")) {
    git init
    git branch -M main
}

if (-not [string]::IsNullOrWhiteSpace($RemoteUrl)) {
    $hasOrigin = git remote | Select-String -SimpleMatch "origin"
    if (-not $hasOrigin) {
        git remote add origin $RemoteUrl
    }
}

git add .
git commit -m "Update Scent-ID Empire Restore artifacts"

$hasOriginAfter = git remote | Select-String -SimpleMatch "origin"
if ($hasOriginAfter) {
    git push -u origin main
} else {
    Write-Host "No origin remote configured. Add one with:"
    Write-Host "  .\\one_click_upload.ps1 -RemoteUrl https://github.com/<user>/<repo>.git"
}
