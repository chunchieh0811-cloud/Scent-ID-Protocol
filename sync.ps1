Set-Location "D:\Scent-ID-v38.0"

Write-Host "🚀 Scent-ID AUTO SYNC START" -ForegroundColor Cyan

git add .

$status = git status --porcelain

if ($status) {
    git commit -m "auto sync $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
}

git pull origin main --rebase

git push origin main

Write-Host "✅ SYNC COMPLETE" -ForegroundColor Green