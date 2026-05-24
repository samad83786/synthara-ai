$ErrorActionPreference = "Stop"
$repoName = "synthara"
$repoDir = "D:\synthara"

Write-Host "=== Synthara Deploy Script ===" -ForegroundColor Magenta

# 1. Commit to git
Write-Host "[1/4] Committing to git..." -ForegroundColor Cyan
Set-Location $repoDir
git add -A
$commitMsg = "Initial commit: Synthara AI Agent Platform"
git commit -m $commitMsg 2>&1 | Out-Null
Write-Host "  Done" -ForegroundColor Green

# 2. Create GitHub repo
Write-Host "[2/4] Creating GitHub repo..." -ForegroundColor Cyan
$ghUser = $(git config user.name)
$ghToken = $env:GH_TOKEN
if (-not $ghToken) {
    Write-Host "  No GH_TOKEN found. Create a GitHub repo manually:" -ForegroundColor Yellow
    Write-Host "  1. Go to https://github.com/new" -ForegroundColor White
    Write-Host "  2. Repo name: synthara" -ForegroundColor White
    Write-Host "  3. Don't add README/gitignore" -ForegroundColor White
    Write-Host "  4. Run these commands:" -ForegroundColor White
    Write-Host "     git remote add origin https://github.com/$ghUser/synthara.git" -ForegroundColor Gray
    Write-Host "     git push -u origin main" -ForegroundColor Gray
} else {
    Invoke-RestMethod -Uri "https://api.github.com/user/repos" -Method Post `
        -Headers @{Authorization = "token $ghToken"} `
        -Body (@{name = $repoName; private = $false} | ConvertTo-Json) `
        -ContentType "application/json" | Out-Null
    git remote add origin "https://github.com/$ghUser/$repoName.git"
    git push -u origin main
    Write-Host "  Repo created: https://github.com/$ghUser/$repoName" -ForegroundColor Green
}

# 3. Deploy to Railway
Write-Host "[3/4] Deploying to Railway..." -ForegroundColor Cyan
$hasRailway = Get-Command "railway" -ErrorAction SilentlyContinue
if (-not $hasRailway) {
    Write-Host "  Railway CLI not found. Install it:" -ForegroundColor Yellow
    Write-Host "  npm install -g @railway/cli" -ForegroundColor White
    Write-Host "  railway login" -ForegroundColor White
    Write-Host "  railway link" -ForegroundColor White
    Write-Host "  railway up" -ForegroundColor White
} else {
    railway up --service backend --detach
    railway up --service frontend --detach
    Write-Host "  Deployed!" -ForegroundColor Green
}

# 4. Summary
Write-Host "[4/4] Done!" -ForegroundColor Magenta
Write-Host ""
Write-Host "=== Next Steps ===" -ForegroundColor Yellow
Write-Host "1. Set environment variables in Railway dashboard:" -ForegroundColor White
Write-Host "   SYNTHARA_API_TYPE=openai" -ForegroundColor Gray
Write-Host "   SYNTHARA_OPENAI_KEY=your_groq_key" -ForegroundColor Gray
Write-Host "   SYNTHARA_OPENAI_BASE=https://api.groq.com/openai/v1" -ForegroundColor Gray
Write-Host "   SYNTHARA_ORCHESTRATOR_MODEL=mixtral-8x7b-32768" -ForegroundColor Gray
Write-Host "   SYNTHARA_WORKER_MODEL=mixtral-8x7b-32768" -ForegroundColor Gray
Write-Host "   SYNTHARA_WALLET=your_solana_wallet_address" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Get a free Groq API key: https://console.groq.com" -ForegroundColor White
Write-Host "3. Get a Solana wallet: https://phantom.app" -ForegroundColor White
