<#
.\deploy\deploy.ps1 - Deploy wrapper for Windows (uses WSL when available)

Usage:
  .\deploy\deploy.ps1 -Remote user@host -RemoteDir /srv/bikebeach -Branch main

This script will try to invoke the existing `deploy/deploy.sh` inside WSL.
If WSL is not available it prints instructions to run the bash deploy script manually
or to run an equivalent deploy in PowerShell/Win32 tools.
#>

param(
    [Parameter(Mandatory=$true)] [string]$Remote,
    [string]$RemoteDir = "/srv/bikebeach",
    [string]$Branch = "main"
)

function Convert-WindowsPathToWsl([string]$path){
    # Convert C:\Users\... to /mnt/c/Users/...
    $p = $path -replace "\\","/"
    if ($p -match '^([A-Za-z]):/(.*)'){
        $drive = $matches[1].ToLower()
        $rest = $matches[2]
        return "/mnt/$drive/$rest"
    }
    return $p
}

$wsl = (Get-Command wsl -ErrorAction SilentlyContinue)
if ($null -ne $wsl){
    Write-Host "WSL detected — invoking deploy/deploy.sh inside WSL..."
    $cwd = (Get-Location).Path
    $wslPath = Convert-WindowsPathToWsl $cwd
    $scriptPath = "$wslPath/deploy/deploy.sh"
    $cmd = "bash -lc 'cd "$wslPath" && ./deploy/deploy.sh $Remote $RemoteDir $Branch'"
    & wsl $cmd
    exit $LASTEXITCODE
} else {
    Write-Warning "WSL not found on this system."
    Write-Host "You can either:"
    Write-Host "  1) Install WSL and run this script again (recommended), or"
    Write-Host "  2) Run the bash deploy script from a Linux host or WSL: ./deploy/deploy.sh $Remote $RemoteDir $Branch"
    Write-Host "  3) I can generate a native PowerShell deploy script if you want (reply 'PS')."
    exit 2
}
