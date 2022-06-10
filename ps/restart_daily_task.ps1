# restart_daily_task.ps1
# ======================
# Version:
#   v1.0 (6/10/2022)
#
# Author:
#   Heath Vernet (hvernet93@gmail.com)
#
# Arguments:
#   None
#
# Description:
#   Creates a task scheduler task to force reboot at specified time.
#
# Usage:
#   Copy to flash drive and execute script in PowerShell.
#   Once executed you can remove your flash drive and insert your YubiKey.
#
# Notes:
#   Modify $taskTrigger arguments to change time and frequency.


# Define temp path variable
$scriptCopy = $env:temp + "\" + (Split-Path $PSCommandPath -Leaf)

# Copy file to temp and execute in same PowerShell process
if (!(Test-Path $scriptCopy)) {
    Copy-Item $PSCommandPath -Destination $env:temp
    & $scriptCopy
}
else {
    # Define variables for elevation check
    $identity = [System.Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object System.Security.Principal.WindowsPrincipal($identity)

    # Elevation check
    if (!$principal.IsInRole([System.Security.Principal.WindowsBuiltInRole]::Administrator)) {
        Write-Host "PowerShell not ran as Administrator" -ForegroundColor Red
        Write-Host "Please elevate"

        # Run elevate
        elevate

        # ReRun PowerShell as Administrator
        $powershell = [System.Diagnostics.Process]::GetCurrentProcess()
        $ps = New-Object System.Diagnostics.ProcessStartInfo $powershell.Path
        $ps.Arguments = "-file " + $script:MyInvocation.MyCommand.Path
        $ps.Verb = "runas"
        [System.Diagnostics.Process]::Start($ps) | Out-Null
    }
    else {
        Write-Host "PowerShell ran as Administrator" -ForegroundColor Green
        Write-Host "Creating daily reboot task"

        # Define task variables
        $taskName = "Daily Restart"
        $taskDescription = "Restarts computer daily at 5:30 AM"

        $taskPrincipal = New-ScheduledTaskPrincipal `
            -UserID "NT AUTHORITY\SYSTEM" `
            -LogonType ServiceAccount `
            -RunLevel Highest

        $taskAction = New-ScheduledTaskAction `
            -Execute "powershell.exe" `
            -Argument "Restart-Computer -Force"

        $taskTrigger = New-ScheduledTaskTrigger -Daily -At 5:30AM

        # Create task
        if (Get-ScheduledTask -TaskName $taskName -ErrorAction Ignore) {
            Write-Host "Task already exists" -ForegroundColor Green
        }
        else {
            Register-ScheduledTask `
                -TaskName $taskName `
                -Description $taskDescription `
                -Principal $taskPrincipal `
                -Action $taskAction `
                -Trigger $taskTrigger
            Write-Host "Task created successfully" -ForegroundColor Green
        }

        # Remove script from $env:temp
        Remove-Item -Path $PSCommandPath

        # Pause
        Read-Host -Prompt "Press Enter to exit"
        exit
    }
}