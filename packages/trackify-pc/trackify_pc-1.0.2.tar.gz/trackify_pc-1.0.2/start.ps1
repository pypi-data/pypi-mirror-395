# Trackify Startup Script
# Starts all three components in separate windows

Write-Host "Starting Trackify..." -ForegroundColor Green
Write-Host ""

# Start Backend
Write-Host "1. Starting Backend API..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot'; .venv\Scripts\python.exe run_backend.py"
Start-Sleep -Seconds 2

# Start Tracker
Write-Host "2. Starting Activity Tracker..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot'; .venv\Scripts\python.exe tracker\main.py"
Start-Sleep -Seconds 1

# Start Frontend
Write-Host "3. Starting Frontend..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot\frontend'; npm run dev"
Start-Sleep -Seconds 2

Write-Host ""
Write-Host "All components started!" -ForegroundColor Green
Write-Host "Backend:  http://localhost:8000" -ForegroundColor Yellow
Write-Host "Frontend: http://localhost:5173" -ForegroundColor Yellow
Write-Host ""
Write-Host "Press any key to exit (components will keep running)..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
