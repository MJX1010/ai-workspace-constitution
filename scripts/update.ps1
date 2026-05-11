#Requires -Version 5.1
<#
.SYNOPSIS
  Pull latest constitution, re-render to workspace, and verify.
#>
[CmdletBinding()]
param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Forwarded
)

$ErrorActionPreference = 'Stop'

$ScriptDir = Split-Path -Parent $PSCommandPath
$RepoDir   = (Resolve-Path (Join-Path $ScriptDir '..')).Path

function Find-Python {
    foreach ($cand in @('python', 'python3', 'py')) {
        $cmd = Get-Command $cand -ErrorAction SilentlyContinue
        if (-not $cmd) { continue }
        $exe = $cmd.Source
        $verRaw = if ($cand -eq 'py') {
            & $exe -3 -c 'import sys; print(sys.version_info[0]*100+sys.version_info[1])' 2>$null
        } else {
            & $exe -c 'import sys; print(sys.version_info[0]*100+sys.version_info[1])' 2>$null
        }
        if ($LASTEXITCODE -eq 0 -and [int]$verRaw -ge 308) {
            return @{ Exe = $exe; Launcher = ($cand -eq 'py') }
        }
    }
    return $null
}

$py = Find-Python
if (-not $py) { Write-Error "Python 3.8+ not found."; exit 2 }
$pyExe = $py.Exe
$pyArgsPrefix = if ($py.Launcher) { @('-3') } else { @() }

$null = & $pyExe @pyArgsPrefix -c 'import yaml' 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "[constitution] PyYAML not found; installing via pip --user..."
    & $pyExe @pyArgsPrefix -m pip install --user --quiet --disable-pip-version-check pyyaml
}

Set-Location $RepoDir
& $pyExe @pyArgsPrefix -m scripts.lib.update @Forwarded
exit $LASTEXITCODE
