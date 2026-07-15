[CmdletBinding()]
param(
    [string]$WorkspaceRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path,
    [switch]$Check
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$ScriptBytes = [System.IO.File]::ReadAllBytes($PSCommandPath)
$HasUtf8Bom = $ScriptBytes.Length -ge 3 -and
        $ScriptBytes[0] -eq 0xEF -and
        $ScriptBytes[1] -eq 0xBB -and
        $ScriptBytes[2] -eq 0xBF
if (-not $HasUtf8Bom) {
    throw 'This script contains non-ASCII TOML descriptions and must be saved as UTF-8 with BOM.'
}

$Utf8NoBom = [System.Text.UTF8Encoding]::new($false)
$BeginMarker = '# BEGIN WORKSPACE CODEX AGENT CONFIG'
$EndMarker = '# END WORKSPACE CODEX AGENT CONFIG'
$RoleRoot = ((Join-Path $WorkspaceRoot '.codex\agents') -replace '\\', '/')

$ProjectRoots = @(
    '.',
    'DragonPow2',
    'DragonPow2\DragonPow2_Tools',
    'DragonPow2\DragonPow2_Trunk',
    'lqs_automation',
    'lqs_automation\build_dragon2'
)

$ManagedBlock = @"
$BeginMarker
[features]
multi_agent = true

[agents]
max_threads = 2
max_depth = 1

[agents.repo_explorer]
description = "只读调查任务书指定的单一工程，自行读取局部上下文，只返回精简证据摘要。"
config_file = "$RoleRoot/repo-explorer.toml"

[agents.repo_worker]
description = "执行任务书指定的单一工程改动，自行读取局部上下文，只向主 Agent 返回精简结果。"
config_file = "$RoleRoot/repo-worker.toml"
$EndMarker
"@.Trim()

function Get-UpdatedContent {
    param([string]$Existing)

    $pattern = '(?s)' + [regex]::Escape($BeginMarker) + '.*?' + [regex]::Escape($EndMarker)
    if ([regex]::IsMatch($Existing, $pattern)) {
        return [regex]::Replace($Existing, $pattern, [System.Text.RegularExpressions.MatchEvaluator]{ param($match) $ManagedBlock }, 1)
    }

    if ([string]::IsNullOrWhiteSpace($Existing)) {
        return "# Project-local Codex configuration.`r`n`r`n$ManagedBlock`r`n"
    }

    return $Existing.TrimEnd() + "`r`n`r`n$ManagedBlock`r`n"
}

$Drift = [System.Collections.Generic.List[string]]::new()

foreach ($relativeRoot in $ProjectRoots) {
    $projectRoot = if ($relativeRoot -eq '.') { $WorkspaceRoot } else { Join-Path $WorkspaceRoot $relativeRoot }
    if (-not (Test-Path -LiteralPath $projectRoot -PathType Container)) {
        throw "Project root not found: $projectRoot"
    }

    $configPath = Join-Path $projectRoot '.codex\config.toml'
    $existing = if (Test-Path -LiteralPath $configPath -PathType Leaf) {
        [System.IO.File]::ReadAllText($configPath, [System.Text.Encoding]::UTF8)
    } else {
        ''
    }
    $updated = Get-UpdatedContent -Existing $existing

    if ($updated -cne $existing) {
        $Drift.Add($configPath)
        if (-not $Check) {
            [System.IO.Directory]::CreateDirectory((Split-Path -Parent $configPath)) | Out-Null
            [System.IO.File]::WriteAllText($configPath, $updated, $Utf8NoBom)
            Write-Host "UPDATED $configPath"
        }
    } elseif (-not $Check) {
        Write-Host "OK $configPath"
    }
}

if ($Check) {
    if ($Drift.Count -gt 0) {
        foreach ($path in $Drift) {
            Write-Host "DRIFT $path"
        }
        exit 1
    }

    Write-Host 'Codex agent governance is in sync.'
}
