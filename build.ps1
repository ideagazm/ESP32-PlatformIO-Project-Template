# ESP32 PlatformIO Project - PowerShell Build Script
param(
    [Parameter(Position = 0)]
    [string]$Command = "help"
)

function Show-Help {
    Write-Host "ESP32 PlatformIO Project - Available Commands:" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Development:" -ForegroundColor Yellow
    Write-Host "  build      - Build the project"
    Write-Host "  upload     - Upload firmware to device"
    Write-Host "  monitor    - Start serial monitor"
    Write-Host "  clean      - Clean build files"
    Write-Host "  deploy     - Full deployment (clean, build, upload, monitor)"
    Write-Host ""
    Write-Host "Advanced:" -ForegroundColor Yellow
    Write-Host "  debug      - Build debug version"
    Write-Host "  ota        - Upload via OTA (Over-The-Air)"
    Write-Host "  uploadfs   - Upload SPIFFS filesystem"
    Write-Host "  devices    - List connected devices"
    Write-Host ""
    Write-Host "Setup:" -ForegroundColor Yellow
    Write-Host "  setup      - Run development environment setup"
    Write-Host "  install    - Install dependencies"
    Write-Host ""
    Write-Host "Usage Examples:" -ForegroundColor Green
    Write-Host "  .\build.ps1 build"
    Write-Host "  .\build.ps1 deploy"
    Write-Host "  .\build.ps1 upload"
}

function Invoke-PioCommand {
    param([string[]]$Arguments)
    
    Write-Host "Running: pio $($Arguments -join ' ')" -ForegroundColor Green
    & pio @Arguments
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Command failed with exit code $LASTEXITCODE" -ForegroundColor Red
        exit $LASTEXITCODE
    }
}

function Invoke-PythonScript {
    param([string]$Script, [string[]]$Arguments)
    
    Write-Host "Running: python $Script $($Arguments -join ' ')" -ForegroundColor Green
    & python $Script @Arguments
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Script failed with exit code $LASTEXITCODE" -ForegroundColor Red
        exit $LASTEXITCODE
    }
}

switch ($Command.ToLower()) {
    "help" { Show-Help }
    "build" { Invoke-PioCommand @("run") }
    "upload" { Invoke-PioCommand @("run", "--target", "upload") }
    "monitor" { Invoke-PioCommand @("device", "monitor") }
    "clean" { Invoke-PioCommand @("run", "--target", "clean") }
    "devices" { Invoke-PioCommand @("device", "list") }
    "uploadfs" { Invoke-PioCommand @("run", "--target", "uploadfs") }
    "debug" { Invoke-PioCommand @("run", "-e", "esp32dev_debug") }
    "ota" { Invoke-PioCommand @("run", "-e", "esp32dev_ota", "--target", "upload") }
    "setup" { Invoke-PythonScript "scripts/setup.py" @() }
    "install" { 
        Write-Host "Installing Python dependencies..." -ForegroundColor Green
        & pip install -r requirements.txt
    }
    "deploy" {
        Write-Host "🚀 Starting full deployment..." -ForegroundColor Cyan
        Invoke-PioCommand @("run", "--target", "clean")
        Invoke-PioCommand @("run")
        Invoke-PioCommand @("run", "--target", "upload")
        Write-Host "✅ Deployment complete! Starting monitor..." -ForegroundColor Green
        Invoke-PioCommand @("device", "monitor")
    }
    "dev" { 
        Invoke-PioCommand @("run")
        Invoke-PioCommand @("run", "--target", "upload")
    }
    "build-all" {
        Invoke-PioCommand @("run", "-e", "esp32dev")
        Invoke-PioCommand @("run", "-e", "esp32dev_debug")
    }
    "check" { Invoke-PioCommand @("check") }
    "update" { Invoke-PioCommand @("lib", "update") }
    "info" { Invoke-PioCommand @("project", "data") }
    default {
        Write-Host "❌ Unknown command: $Command" -ForegroundColor Red
        Write-Host "Use '.\build.ps1 help' to see available commands" -ForegroundColor Yellow
        exit 1
    }
}