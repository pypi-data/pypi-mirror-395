# NetShare Firewall Diagnostic Script
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "NetShare Firewall Diagnostic" -ForegroundColor Cyan
Write-Host "============================================`n" -ForegroundColor Cyan

# Check network profile
Write-Host "[1] Network Profile Check:" -ForegroundColor Yellow
Get-NetConnectionProfile | Select-Object Name, NetworkCategory, InterfaceAlias | Format-Table -AutoSize

# Check Python firewall rules
Write-Host "`n[2] Python Firewall Rules:" -ForegroundColor Yellow
$pythonRules = Get-NetFirewallRule | Where-Object { $_.DisplayName -like '*Python*' }
if ($pythonRules) {
    foreach ($rule in $pythonRules) {
        $appFilter = $rule | Get-NetFirewallApplicationFilter
        $portFilter = $rule | Get-NetFirewallPortFilter

        Write-Host "`nRule: $($rule.DisplayName)" -ForegroundColor Green
        Write-Host "  Enabled: $($rule.Enabled)"
        Write-Host "  Direction: $($rule.Direction)"
        Write-Host "  Action: $($rule.Action)"
        Write-Host "  Profile: $($rule.Profile)"
        Write-Host "  Program: $($appFilter.Program)"
        Write-Host "  Protocol: $($portFilter.Protocol)"
        Write-Host "  Local Port: $($portFilter.LocalPort)"
    }
} else {
    Write-Host "  No Python firewall rules found!" -ForegroundColor Red
}

# Check if Windows Firewall is enabled
Write-Host "`n[3] Windows Firewall Status:" -ForegroundColor Yellow
Get-NetFirewallProfile | Select-Object Name, Enabled | Format-Table -AutoSize

# Check for blocking rules
Write-Host "`n[4] Checking for BLOCK rules on Python:" -ForegroundColor Yellow
$blockRules = Get-NetFirewallRule | Where-Object { $_.DisplayName -like '*Python*' -and $_.Action -eq 'Block' }
if ($blockRules) {
    Write-Host "  WARNING: Found blocking rules!" -ForegroundColor Red
    $blockRules | Select-Object DisplayName, Enabled, Direction | Format-Table -AutoSize
} else {
    Write-Host "  No blocking rules found for Python." -ForegroundColor Green
}

Write-Host "`n============================================" -ForegroundColor Cyan
Write-Host "Diagnostic Complete" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
