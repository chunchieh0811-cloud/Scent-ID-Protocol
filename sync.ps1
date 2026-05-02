Set-Location "D:\Scent-ID-v38.0"

Write-Host "🚀 Scent-ID Auto Sync Start" -ForegroundColor Cyan

git add .

$status = git status --porcelain

if ($status) {

    git commit -m "auto sync $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" --no-verify

    git pull origin main --rebase

    git push origin main

    Write-Host "✅ Sync Complete" -ForegroundColor Green

} else {

    Write-Host "🟡 No changes" -ForegroundColor Yellow

}