[CmdletBinding()]
param(
    [string]$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path,
    [string[]]$Project,
    [switch]$IncludeRoot,
    [switch]$Check
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$Utf8NoBom = [System.Text.UTF8Encoding]::new($false)
$GovernanceDir = Join-Path $Root 'governance\agent-docs'

$Targets = @(
    [pscustomobject]@{
        RelativePath = 'AGENTS.md'
        Template = 'common.md'
        Marker = 'DRAGONPOW2 COMMON AGENT RULES'
        Title = 'DragonPow2 Shared Agent Instructions'
    },
    [pscustomobject]@{
        RelativePath = 'CLAUDE.md'
        Template = 'common.md'
        Marker = 'DRAGONPOW2 COMMON CLAUDE RULES'
        Title = 'DragonPow2 Shared Claude Instructions'
    },
    [pscustomobject]@{
        RelativePath = 'client\AGENTS.md'
        Template = 'client.md'
        Marker = 'DRAGONPOW2 CLIENT AGENT RULES'
        Title = 'DragonPow2 Client Agent Instructions'
    },
    [pscustomobject]@{
        RelativePath = 'client\CLAUDE.md'
        Template = 'client.md'
        Marker = 'DRAGONPOW2 CLIENT CLAUDE RULES'
        Title = 'DragonPow2 Client Claude Instructions'
    },
    [pscustomobject]@{
        RelativePath = 'server\AGENTS.md'
        Template = 'server.md'
        Marker = 'DRAGONPOW2 SERVER AGENT RULES'
        Title = 'DragonPow2 Server Agent Instructions'
    },
    [pscustomobject]@{
        RelativePath = 'server\CLAUDE.md'
        Template = 'server.md'
        Marker = 'DRAGONPOW2 SERVER CLAUDE RULES'
        Title = 'DragonPow2 Server Claude Instructions'
    }
)

function Read-Utf8Text {
    param([string]$Path)
    return [System.IO.File]::ReadAllText($Path, [System.Text.Encoding]::UTF8)
}

function Write-Utf8Text {
    param(
        [string]$Path,
        [string]$Content
    )
    [System.IO.Directory]::CreateDirectory((Split-Path -Parent $Path)) | Out-Null
    [System.IO.File]::WriteAllText($Path, $Content, $Utf8NoBom)
}

function Get-TemplateText {
    param([string]$TemplateName)
    $path = Join-Path $GovernanceDir $TemplateName
    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) {
        throw "Missing agent doc template: $path"
    }
    return (Read-Utf8Text $path).Trim()
}

function New-ManagedBlock {
    param(
        [string]$Marker,
        [string]$TemplateText
    )

    return "<!-- BEGIN $Marker -->`r`n$TemplateText`r`n<!-- END $Marker -->"
}

function Set-ManagedBlock {
    param(
        [string]$ExistingContent,
        [string]$Title,
        [string]$Marker,
        [string]$TemplateText
    )

    $block = New-ManagedBlock -Marker $Marker -TemplateText $TemplateText
    $begin = [regex]::Escape("<!-- BEGIN $Marker -->")
    $end = [regex]::Escape("<!-- END $Marker -->")
    $pattern = "(?s)$begin.*?$end"

    if ([regex]::IsMatch($ExistingContent, $pattern)) {
        return [regex]::Replace($ExistingContent, $pattern, [System.Text.RegularExpressions.MatchEvaluator]{ param($m) $block }, 1)
    }

    if ([string]::IsNullOrWhiteSpace($ExistingContent)) {
        return "# $Title`r`n`r`n$block`r`n"
    }

    $titlePattern = '^(# .+?)(\r?\n)'
    $match = [regex]::Match($ExistingContent, $titlePattern)
    if ($match.Success) {
        $prefix = $ExistingContent.Substring(0, $match.Length)
        $suffix = $ExistingContent.Substring($match.Length).TrimStart()
        return "$prefix`r`n$block`r`n`r`n$suffix"
    }

    return "$block`r`n`r`n$ExistingContent"
}

function Resolve-TargetRoots {
    $roots = [System.Collections.Generic.List[string]]::new()
    $resolvedRoot = (Resolve-Path -LiteralPath $Root).Path

    if ($IncludeRoot) {
        $roots.Add($resolvedRoot)
    }

    if ($Project -and $Project.Count -gt 0) {
        foreach ($projectName in $Project) {
            $projectPath = if ([System.IO.Path]::IsPathRooted($projectName)) {
                $projectName
            } else {
                Join-Path $resolvedRoot $projectName
            }

            if (-not (Test-Path -LiteralPath $projectPath -PathType Container)) {
                throw "Project path not found: $projectPath"
            }
            $roots.Add((Resolve-Path -LiteralPath $projectPath).Path)
        }
    } else {
        $skipNames = @('governance', 'scripts', '.agents', '.codex', '.git', '.svn', '_codex_tmp', 'Rider', 'Tools')
        foreach ($dir in Get-ChildItem -LiteralPath $resolvedRoot -Directory) {
            if ($skipNames -contains $dir.Name) {
                continue
            }

            $hasAgentDoc = (Test-Path -LiteralPath (Join-Path $dir.FullName 'AGENTS.md') -PathType Leaf) -or
                    (Test-Path -LiteralPath (Join-Path $dir.FullName 'CLAUDE.md') -PathType Leaf)
            $hasKnownLayer = (Test-Path -LiteralPath (Join-Path $dir.FullName 'client') -PathType Container) -or
                    (Test-Path -LiteralPath (Join-Path $dir.FullName 'server') -PathType Container)

            if ($hasAgentDoc -or $hasKnownLayer) {
                $roots.Add($dir.FullName)
            }
        }
    }

    return $roots | Sort-Object -Unique
}

function Test-TargetApplies {
    param(
        [string]$ProjectRoot,
        [string]$RelativePath
    )

    $parentRelative = Split-Path -Parent $RelativePath
    if ([string]::IsNullOrEmpty($parentRelative)) {
        return $true
    }

    return Test-Path -LiteralPath (Join-Path $ProjectRoot $parentRelative) -PathType Container
}

$changes = [System.Collections.Generic.List[string]]::new()

foreach ($projectRoot in Resolve-TargetRoots) {
    foreach ($target in $Targets) {
        if (-not (Test-TargetApplies -ProjectRoot $projectRoot -RelativePath $target.RelativePath)) {
            continue
        }

        $targetPath = Join-Path $projectRoot $target.RelativePath
        $existing = if (Test-Path -LiteralPath $targetPath -PathType Leaf) {
            Read-Utf8Text $targetPath
        } else {
            ''
        }

        $template = Get-TemplateText $target.Template
        $updated = Set-ManagedBlock -ExistingContent $existing -Title $target.Title -Marker $target.Marker -TemplateText $template

        if ($updated -ne $existing) {
            $changes.Add($targetPath)
            if (-not $Check) {
                Write-Utf8Text -Path $targetPath -Content $updated
                Write-Host "UPDATED $targetPath"
            }
        } elseif (-not $Check) {
            Write-Host "OK $targetPath"
        }
    }
}

if ($Check) {
    if ($changes.Count -gt 0) {
        foreach ($path in $changes) {
            Write-Host "DRIFT $path"
        }
        exit 1
    }

    Write-Host 'Agent docs are in sync.'
}
