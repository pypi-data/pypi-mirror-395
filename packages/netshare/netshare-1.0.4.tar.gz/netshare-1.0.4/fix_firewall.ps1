# NetShare Firewall Fix Script
# This script creates firewall rules for Python that apply to Private network profile only (for security)

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "NetShare Firewall Fix" -ForegroundColor Cyan
Write-Host "============================================`n" -ForegroundColor Cyan

# Check if running as Administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "ERROR: This script must be run as Administrator!" -ForegroundColor Red
    Write-Host "Right-click PowerShell and select 'Run as Administrator', then run this script again." -ForegroundColor Yellow
    Read-Host -Prompt "Press Enter to exit"
    exit 1
}

Write-Host "[1] Creating firewall rules for Python..." -ForegroundColor Yellow

# Python installations detected from diagnostic
$pythonPaths = @(
    "C:\users\hp\appdata\roaming\uv\python\cpython-3.12.11-windows-x86_64-none\python.exe",
    "C:\python313\python.exe"
)

$ruleCount = 0

foreach ($pythonPath in $pythonPaths) {
    if (Test-Path $pythonPath) {
        $pythonVersion = Split-Path (Split-Path $pythonPath -Parent) -Leaf

        # Remove existing rules for this Python to avoid conflicts
        Write-Host "  Removing old rules for $pythonVersion..." -ForegroundColor Gray
        Get-NetFirewallRule | Where-Object { $_.DisplayName -like "*NetShare*$pythonVersion*" } | Remove-NetFirewallRule -ErrorAction SilentlyContinue

        # Create TCP rule for Private profile only
        Write-Host "  Creating TCP rule for $pythonVersion (Private Profile)..." -ForegroundColor Green
        New-NetFirewallRule `
            -DisplayName "NetShare Python - $pythonVersion (TCP)" `
            -Description "Allow NetShare file sharing on Private network (home/trusted networks only)" `
            -Direction Inbound `
            -Protocol TCP `
            -LocalPort Any `
            -Program $pythonPath `
            -Action Allow `
            -Profile Private `
            -Enabled True `
            -ErrorAction SilentlyContinue | Out-Null

        # Create UDP rule for Private profile only
        Write-Host "  Creating UDP rule for $pythonVersion (Private Profile)..." -ForegroundColor Green
        New-NetFirewallRule `
            -DisplayName "NetShare Python - $pythonVersion (UDP)" `
            -Description "Allow NetShare file sharing on Private network (home/trusted networks only)" `
            -Direction Inbound `
            -Protocol UDP `
            -LocalPort Any `
            -Program $pythonPath `
            -Action Allow `
            -Profile Private `
            -Enabled True `
            -ErrorAction SilentlyContinue | Out-Null

        $ruleCount += 2
        Write-Host "  Created 2 rules for $pythonVersion" -ForegroundColor Green
    } else {
        Write-Host "  Skipping $pythonPath (not found)" -ForegroundColor Gray
    }
}

Write-Host "`n[2] Verifying new rules..." -ForegroundColor Yellow
$newRules = Get-NetFirewallRule | Where-Object { $_.DisplayName -like "*NetShare Python*" }
if ($newRules) {
    Write-Host "  Successfully created $($newRules.Count) firewall rules!" -ForegroundColor Green
    $newRules | Select-Object DisplayName, Enabled, Direction, Action, Profile | Format-Table -AutoSize
} else {
    Write-Host "  WARNING: No rules were created!" -ForegroundColor Red
}

Write-Host "`n============================================" -ForegroundColor Cyan
Write-Host "Firewall Fix Complete!" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "`nYou can now test the connection from your mobile device." -ForegroundColor Yellow
Write-Host "Try accessing: http://192.168.0.96:8080`n" -ForegroundColor Yellow

Read-Host -Prompt "Press Enter to exit"
