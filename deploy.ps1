$ErrorActionPreference = "Stop"
$repoDir = "D:\synthara"

Write-Host "╔══════════════════════════════════════════╗" -ForegroundColor Magenta
Write-Host "║        Synthara - One-Click Deploy       ║" -ForegroundColor Magenta
Write-Host "╚══════════════════════════════════════════╝" -ForegroundColor Magenta
Write-Host ""

Set-Location $repoDir

# 1. Get GitHub token
$token = $env:GH_TOKEN
if (-not $token) {
    $token = Read-Host "Enter your GitHub Personal Access Token (or press Enter to skip GitHub)"
}

if ($token) {
    Write-Host "[1/4] Creating GitHub repository..." -ForegroundColor Cyan
    $ghUser = "abdul"
    try {
        $body = @{name = "synthara"; private = $false; description = "Create AI agents by describing them in plain English"} | ConvertTo-Json
        Invoke-RestMethod -Uri "https://api.github.com/user/repos" -Method Post `
            -Headers @{Authorization = "token $token"} `
            -Body $body -ContentType "application/json" -UseBasicParsing | Out-Null

        git remote remove origin 2>$null
        git remote add origin "https://$ghUser`:$token@github.com/$ghUser/synthara.git"
        Write-Host "  Pushing to GitHub..." -ForegroundColor Cyan
        git push -u origin main 2>&1 | Out-Null
        Write-Host "  https://github.com/$ghUser/synthara" -ForegroundColor Green
    } catch {
        Write-Host "  GitHub error: $_" -ForegroundColor Yellow
        Write-Host "  Continue with local deploy only..." -ForegroundColor Yellow
    }
}

# 2. Deploy to Railway
Write-Host "[2/4] Deploying to Railway..." -ForegroundColor Cyan
$hasRailway = Get-Command "railway" -ErrorAction SilentlyContinue
if ($hasRailway) {
    railway up --detach 2>&1 | Out-Null
    Write-Host "  Deployed!" -ForegroundColor Green
} else {
    Write-Host "  Railway CLI not found. Install:" -ForegroundColor Yellow
    Write-Host "  npm install -g @railway/cli" -ForegroundColor White
    Write-Host "  railway login" -ForegroundColor White
    Write-Host "  railway link" -ForegroundColor White
    Write-Host "  railway up" -ForegroundColor White
}

# 3. Show summary
Write-Host "[3/4] Done!" -ForegroundColor Green
Write-Host ""
Write-Host "╔══════════════════════════════════════════╗" -ForegroundColor Yellow
Write-Host "║           NEXT STEPS                      ║" -ForegroundColor Yellow
Write-Host "╚══════════════════════════════════════════╝" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Get a FREE Groq API key:" -ForegroundColor White
Write-Host "   https://console.groq.com" -ForegroundColor Cyan
Write-Host ""
Write-Host "2. Get a Solana wallet:" -ForegroundColor White
Write-Host "   https://phantom.app" -ForegroundColor Cyan
Write-Host ""
Write-Host "3. Set Railway env vars:" -ForegroundColor White
Write-Host "   SYNTHARA_API_TYPE=openai" -ForegroundColor Gray
Write-Host "   SYNTHARA_OPENAI_KEY=gsk_your_key" -ForegroundColor Gray
Write-Host "   SYNTHARA_OPENAI_BASE=https://api.groq.com/openai/v1" -ForegroundColor Gray
Write-Host "   SYNTHARA_ORCHESTRATOR_MODEL=mixtral-8x7b-32768" -ForegroundColor Gray
Write-Host "   SYNTHARA_WORKER_MODEL=mixtral-8x7b-32768" -ForegroundColor Gray
Write-Host "   SYNTHARA_WALLET=your_solana_wallet" -ForegroundColor Gray
Write-Host ""
Write-Host "4. Or run locally right now:" -ForegroundColor White
Write-Host "   cd backend; python app.py" -ForegroundColor Cyan
Write-Host "   cd frontend; npm run dev" -ForegroundColor Cyan
Write-Host ""
Write-Host "   Then open http://localhost:5173" -ForegroundColor Cyan
