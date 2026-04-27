param(
    [Parameter(Mandatory = $false)]
    [string]$Owner = "chunchieh0811-cloud",

    [Parameter(Mandatory = $false)]
    [string]$Repo = "Scent-ID-Protocol",

    [Parameter(Mandatory = $false)]
    [string]$Branch = "main"
)

$ErrorActionPreference = "Stop"

if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
    throw "GitHub CLI (gh) is required. Install gh first."
}

$payload = @{
    required_status_checks = @{
        strict   = $true
        contexts = @("verify")
    }
    enforce_admins = $true
    required_pull_request_reviews = @{
        dismiss_stale_reviews           = $true
        require_code_owner_reviews      = $false
        required_approving_review_count = 1
    }
    restrictions = $null
    required_linear_history = $true
    allow_force_pushes = $false
    allow_deletions = $false
    block_creations = $false
    required_conversation_resolution = $true
    lock_branch = $false
    allow_fork_syncing = $true
} | ConvertTo-Json -Depth 10 -Compress

$endpoint = "repos/$Owner/$Repo/branches/$Branch/protection"
$tempFile = Join-Path $env:TEMP "branch-protection.json"
$payload | Out-File -FilePath $tempFile -Encoding utf8

gh api --method PUT `
    -H "Accept: application/vnd.github+json" `
    $endpoint `
    --input $tempFile

Write-Host "Branch protection applied to ${Owner}/${Repo}:${Branch}"
