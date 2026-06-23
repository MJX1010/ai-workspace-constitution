#Requires -Version 5.1
<#
.SYNOPSIS
  Install the AI Workspace Constitution on Windows.

.EXAMPLE
  $env:WORKSPACE_ROOT = "D:\projects\agents"
  .\scripts\install.ps1

.EXAMPLE
  .\scripts\install.ps1 --workspace-root D:\projects\agents --dry-run

.EXAMPLE
  .\scripts\install.ps1 --workspace-root D:\projects\agents --user-home D:\tmp\home --dry-run
#>
[CmdletBinding()]
param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Forwarded
)

$ErrorActionPreference = 'Stop'

$ScriptDir = Split-Path -Parent $PSCommandPath
$RepoDir   = (Resolve-Path (Join-Path $ScriptDir '..')).Path

# ── Find a usable Python 3.8+ ────────────────────────────────────────
function Find-Python {
    $candidates = @('python', 'python3', 'py')
    foreach ($cand in $candidates) {
        $cmd = Get-Command $cand -ErrorAction SilentlyContinue
        if (-not $cmd) { continue }
        # 'py' launcher: prefer py -3
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
if (-not $py) {
    Write-Error @"
Python 3.8+ not found.

Install via:
  winget install Python.Python.3.12
  -- OR --
  Download from https://python.org/downloads/
  -- OR --
  Microsoft Store: search "Python 3.12"

After installing, reopen your terminal so PATH is refreshed.
"@
    exit 2
}

$pyExe = $py.Exe
$pyArgsPrefix = if ($py.Launcher) { @('-3') } else { @() }

# ── Bootstrap PyYAML on first run ────────────────────────────────────
$null = & $pyExe @pyArgsPrefix -c 'import yaml' 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "[constitution] PyYAML not found; installing via pip --user (one-time)..."
    & $pyExe @pyArgsPrefix -m pip install --user --quiet --disable-pip-version-check pyyaml
    if ($LASTEXITCODE -ne 0) {
        Write-Error @"
Failed to install PyYAML. Try manually:
  $pyExe -m pip install --user pyyaml

If your environment blocks pip, see docs\migration.md for offline options.
"@
        exit 3
    }
}

# ── Dispatch to Python entrypoint ────────────────────────────────────
Set-Location $RepoDir
& $pyExe @pyArgsPrefix -m scripts.lib.install @Forwarded
exit $LASTEXITCODE
