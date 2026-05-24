$ErrorActionPreference = "Continue"

Write-Host "Starting Synthara locally..." -ForegroundColor Magenta
Write-Host ""

# Start backend
$backendJob = Start-Job -ScriptBlock {
    Set-Location D:\synthara\backend
    python app.py
}
Write-Host "  Backend starting on http://localhost:8000" -ForegroundColor Cyan

# Start frontend
$frontendJob = Start-Job -ScriptBlock {
    Set-Location D:\synthara\frontend
    npm run dev
}
Write-Host "  Frontend starting on http://localhost:5173" -ForegroundColor Cyan

Write-Host ""
Write-Host "Open http://localhost:5173 in your browser" -ForegroundColor Green
Write-Host ""
Write-Host "Press Ctrl+C to stop both servers" -ForegroundColor Yellow

# Wait for both
Wait-Job $backendJob, $frontendJob
