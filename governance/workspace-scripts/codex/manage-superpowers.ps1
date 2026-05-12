param(
    [switch]$ListOnly,
    [string[]]$SetEnabled
)

$ErrorActionPreference = 'Stop'

$userProfile = $env:USERPROFILE
$superpowersSourceRoot = Join-Path $userProfile '.codex\superpowers\skills'
$superpowersVisibleRoot = Join-Path $userProfile '.agents\skills\superpowers'
$agentsMdPath = Join-Path $userProfile '.codex\AGENTS.md'

$managedBlockStart = '<!-- BEGIN MANAGED SUPERPOWERS -->'
$managedBlockEnd = '<!-- END MANAGED SUPERPOWERS -->'

function Get-AvailableSkills {
    if (-not (Test-Path $superpowersSourceRoot)) {
        throw "Superpowers source not found: $superpowersSourceRoot"
    }

    return Get-ChildItem -Path $superpowersSourceRoot -Directory |
        Sort-Object Name |
        ForEach-Object {
            [PSCustomObject]@{
                Name = $_.Name
                SourcePath = $_.FullName
            }
        }
}

function Get-EnabledSkillNames {
    if (-not (Test-Path $superpowersVisibleRoot)) {
        return @()
    }

    return Get-ChildItem -Path $superpowersVisibleRoot -Directory |
        Select-Object -ExpandProperty Name |
        Sort-Object
}

function New-ManagedBlock {
    param(
        [string[]]$EnabledSkills
    )

    $lines = @(
        $managedBlockStart
        '## Superpowers Whitelist'
        ''
    )

    if ($EnabledSkills.Count -gt 0) {
        $lines += 'Only the following superpowers skills are enabled:'
        $lines += ''
        foreach ($skill in $EnabledSkills) {
            $lines += "- ``$skill``"
        }
        $lines += ''
        $lines += 'Do not use any other skill from the installed `superpowers` library unless the user explicitly changes this whitelist.'
    }
    else {
        $lines += 'No superpowers skills are enabled.'
        $lines += ''
        $lines += 'Do not use any skill from the installed `superpowers` library unless the user explicitly enables it.'
    }

    $lines += ''
    $lines += '## Superpowers Activation Policy'
    $lines += ''
    $lines += 'Keep superpowers as an available workflow library, not as a global mandatory startup routine.'
    $lines += ''
    $lines += '- Do not load `using-superpowers` at session startup.'
    $lines += '- Do not invoke a superpowers skill solely because a new conversation started or because the user sent a greeting.'
    $lines += '- Invoke enabled superpowers only when the user explicitly names one or the current task matches the skill purpose.'
    $lines += '- Treat `verification-before-completion` as the only always-on completion guard before claiming code work is done.'
    $lines += '- Treat `systematic-debugging` as task-triggered for bugs, failing tests, errors, and unexpected behavior.'
    $lines += '- Treat `receiving-code-review` as task-triggered when the user provides review feedback.'
    $lines += '- Treat planning, TDD, review, subagent, branch-finishing, and skill-writing superpowers as task-triggered workflows.'
    $lines += $managedBlockEnd

    return ($lines -join [Environment]::NewLine)
}

function Update-AgentsFile {
    param(
        [string[]]$EnabledSkills
    )

    $managedBlock = New-ManagedBlock -EnabledSkills $EnabledSkills
    $header = @(
        '# Personal Codex Rules'
        ''
        'This file applies to your home-level Codex environment.'
        ''
    ) -join [Environment]::NewLine

    if (-not (Test-Path $agentsMdPath)) {
        $content = $header + $managedBlock + [Environment]::NewLine
        [System.IO.File]::WriteAllText($agentsMdPath, $content, [System.Text.UTF8Encoding]::new($false))
        return
    }

    $existing = Get-Content -Raw -Path $agentsMdPath

    if ($existing.Contains($managedBlockStart) -and $existing.Contains($managedBlockEnd)) {
        $pattern = "(?s)$([regex]::Escape($managedBlockStart)).*?$([regex]::Escape($managedBlockEnd))"
        $updated = [regex]::Replace($existing, $pattern, [System.Text.RegularExpressions.MatchEvaluator]{ param($m) $managedBlock })
    }
    else {
        $normalized = $existing.TrimEnd()
        if ($normalized.Length -gt 0) {
            $updated = $normalized + [Environment]::NewLine + [Environment]::NewLine + $managedBlock + [Environment]::NewLine
        }
        else {
            $updated = $header + $managedBlock + [Environment]::NewLine
        }
    }

    [System.IO.File]::WriteAllText($agentsMdPath, $updated, [System.Text.UTF8Encoding]::new($false))
}

function Sync-VisibleSkills {
    param(
        [string[]]$EnabledSkills
    )

    New-Item -ItemType Directory -Force -Path $superpowersVisibleRoot | Out-Null

    $current = @{}
    foreach ($entry in Get-ChildItem -Path $superpowersVisibleRoot -Directory -ErrorAction SilentlyContinue) {
        $current[$entry.Name] = $entry.FullName
    }

    foreach ($name in @($current.Keys)) {
        if ($EnabledSkills -notcontains $name) {
            Remove-Item -LiteralPath $current[$name] -Recurse -Force
        }
    }

    foreach ($name in $EnabledSkills) {
        $visiblePath = Join-Path $superpowersVisibleRoot $name
        if (-not (Test-Path $visiblePath)) {
            $sourcePath = Join-Path $superpowersSourceRoot $name
            if (-not (Test-Path $sourcePath)) {
                throw "Missing source skill: $sourcePath"
            }
            cmd /c mklink /J "$visiblePath" "$sourcePath" | Out-Null
        }
    }
}

function Write-StateSummary {
    param(
        [object[]]$Skills,
        [int]$CursorIndex = -1
    )

    Clear-Host
    Write-Host 'Superpowers skill manager'
    Write-Host ''
    Write-Host 'Use Up/Down to move, Space to toggle, S to save, Q to quit.'
    Write-Host ''

    for ($i = 0; $i -lt $Skills.Count; $i++) {
        $prefix = if ($i -eq $CursorIndex) { '>' } else { ' ' }
        $mark = if ($Skills[$i].Enabled) { '[x]' } else { '[ ]' }
        Write-Host ("{0} {1} {2}" -f $prefix, $mark, $Skills[$i].Name)
    }

    Write-Host ''
    $enabled = $Skills | Where-Object Enabled | Select-Object -ExpandProperty Name
    if ($enabled.Count -gt 0) {
        Write-Host ('Enabled: ' + ($enabled -join ', '))
    }
    else {
        Write-Host 'Enabled: (none)'
    }
}

function Show-ListOnly {
    $available = Get-AvailableSkills
    $enabled = Get-EnabledSkillNames

    foreach ($skill in $available) {
        $mark = if ($enabled -contains $skill.Name) { '[x]' } else { '[ ]' }
        Write-Output ("{0} {1}" -f $mark, $skill.Name)
    }
}

function Set-EnabledSkills {
    param(
        [string[]]$RequestedSkills
    )

    $availableNames = Get-AvailableSkills | Select-Object -ExpandProperty Name
    $selected = @($RequestedSkills | Where-Object { $_ } | Sort-Object -Unique)
    $invalid = @($selected | Where-Object { $availableNames -notcontains $_ })

    if ($invalid.Count -gt 0) {
        throw ('Unknown skill(s): ' + ($invalid -join ', '))
    }

    Sync-VisibleSkills -EnabledSkills $selected
    Update-AgentsFile -EnabledSkills $selected

    if ($selected.Count -gt 0) {
        Write-Output ('Saved enabled skills: ' + ($selected -join ', '))
    }
    else {
        Write-Output 'Saved enabled skills: (none)'
    }
}

if ($ListOnly) {
    Show-ListOnly
    exit 0
}

if ($null -ne $SetEnabled) {
    Set-EnabledSkills -RequestedSkills @($SetEnabled + $args)
    exit 0
}

$availableSkills = Get-AvailableSkills
$enabledNames = Get-EnabledSkillNames

$skills = foreach ($skill in $availableSkills) {
    [PSCustomObject]@{
        Name = $skill.Name
        Enabled = ($enabledNames -contains $skill.Name)
    }
}

$cursor = 0
Write-StateSummary -Skills $skills -CursorIndex $cursor

while ($true) {
    $key = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown')

    switch ($key.VirtualKeyCode) {
        38 {
            if ($cursor -gt 0) {
                $cursor--
            }
        }
        40 {
            if ($cursor -lt ($skills.Count - 1)) {
                $cursor++
            }
        }
        32 {
            $skills[$cursor].Enabled = -not $skills[$cursor].Enabled
        }
        default {
            $char = [char]$key.Character
            if ($char -in @('s', 'S')) {
                $selected = $skills |
                    Where-Object Enabled |
                    Select-Object -ExpandProperty Name |
                    Sort-Object
                Set-EnabledSkills -RequestedSkills $selected
                Write-StateSummary -Skills $skills -CursorIndex $cursor
                Write-Host ''
                Write-Host 'Saved. Restart Codex to refresh skill discovery.'
                exit 0
            }
            if ($char -in @('q', 'Q')) {
                Write-Host ''
                Write-Host 'Cancelled.'
                exit 0
            }
        }
    }

    Write-StateSummary -Skills $skills -CursorIndex $cursor
}
