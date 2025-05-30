# Physics Question Management System - One-click Start Script
Write-Host "===== Physics Question Management System One-click Start =====" -ForegroundColor Cyan

# Set environment variables
$env:PATH = "$PWD\local_python;$PWD\local_python\Scripts;$env:PATH"
$env:PYTHONPATH = $PWD
$env:PYTHONNOUSERSITE = 1

# Check if dependencies are installed
Write-Host "Checking dependencies..." -ForegroundColor Yellow
$pythonPath = "$PWD\local_python\python.exe"
if (-not (Test-Path $pythonPath)) {
    Write-Host "Error: Local Python environment not found, please run setup.bat first" -ForegroundColor Red
    exit 1
}

# Start backend service (in new window)
Write-Host "Starting backend service (new window)..." -ForegroundColor Green
$backendScript = @"
cd '$PWD'
`$env:PATH = '$PWD\local_python;$PWD\local_python\Scripts;' + `$env:PATH
`$env:PYTHONPATH = '$PWD'
`$env:PYTHONNOUSERSITE = 1
Write-Host 'Backend service running at http://localhost:8000' -ForegroundColor Green
& '$PWD\local_python\Scripts\uvicorn.exe' main:app --host 0.0.0.0 --port 8000
"@
Start-Process powershell -ArgumentList "-NoExit", "-Command", $backendScript

# Wait for backend to start
Write-Host "Waiting for backend service to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 3

# Check if backend started successfully
$maxRetries = 10
$retryCount = 0
$backendReady = $false

while ($retryCount -lt $maxRetries) {
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:8000/docs" -Method Head -ErrorAction Stop
        if ($response.StatusCode -eq 200) {
            Write-Host "Backend service started successfully!" -ForegroundColor Green
            $backendReady = $true
            break
        }
    }
    catch {
        $retryCount++
        Write-Host "Waiting for backend service to start... ($retryCount/$maxRetries)" -ForegroundColor Yellow
        Start-Sleep -Seconds 1
    }
}

if (-not $backendReady) {
    Write-Host "Backend service failed to start, please check error messages" -ForegroundColor Red
    exit 1
}

# Start frontend GUI
Write-Host "Starting frontend GUI..." -ForegroundColor Green
& "$PWD\local_python\python.exe" "$PWD\gui.py"

Write-Host "Program exited" -ForegroundColor Yellow 