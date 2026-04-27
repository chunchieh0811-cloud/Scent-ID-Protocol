# Security Baseline

This repository enforces a practical baseline for stable operations.

## Enabled in Repository

- `verify` workflow on push/pull request to `main`
- Release workflow on `v*` tags
- Local health check script: `verify.ps1`
- Secret leakage prevention via `.gitignore`

## Branch Protection Target (`main`)

- Require pull request before merge
- Require 1 approval
- Dismiss stale approvals on new commits
- Require conversation resolution before merge
- Require status check: `verify`
- Require branch to be up to date before merge
- Disallow force push
- Disallow branch deletion
- Enforce for admins
- Require linear history

## Apply Branch Protection

Prerequisites:

- GitHub CLI authenticated with admin repo permissions

Command:

```powershell
.\scripts\apply_branch_protection.ps1
```
