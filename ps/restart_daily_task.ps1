#requires -RunAsAdministrator

# define task variables
$name = "Daily Restart"
$description = "Restarts computer daily at 5:30 AM EST"

$principal = New-ScheduledTaskPrincipal `
    -UserID "NT AUTHORITY\SYSTEM" `
    -LogonType ServiceAccount `
    -RunLevel Highest

$action = New-ScheduledTaskAction `
    -Execute 'powershell.exe' `
    -Argument 'Restart-Computer -Force'

$trigger = New-ScheduledTaskTrigger -Daily -At 5:30AM

# create task
if (Get-ScheduledTask -TaskName $name -ErrorAction Ignore) {
    Write-Host "Task already exists" -ForegroundColor Green
}
else {
    Register-ScheduledTask `
        -TaskName $name `
        -Description $description `
        -Principal $principal `
        -Action $action `
        -Trigger $trigger
    Write-Host "Task created successfully" -ForegroundColor Green
}

Read-Host -Prompt "Press Enter to exit"
exit