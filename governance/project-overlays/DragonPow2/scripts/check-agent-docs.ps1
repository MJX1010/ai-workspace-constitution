[CmdletBinding()]
param(
    [string]$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path,
    [string[]]$Project,
    [switch]$IncludeRoot
)

$script = Join-Path $PSScriptRoot 'sync-agent-docs.ps1'
$syncParams = @{
    Root = $Root
    Check = $true
}

if ($IncludeRoot) {
    $syncParams.IncludeRoot = $true
}

if ($Project -and $Project.Count -gt 0) {
    $syncParams.Project = $Project
}

& $script @syncParams
exit $LASTEXITCODE
