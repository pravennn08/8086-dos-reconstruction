[CmdletBinding()]
param(
    [ValidateSet('check', 'build', 'run', 'verify', 'debug')]
    [string]$Action = 'check',
    [string]$TasmDirectory = $env:TASM_DIR,
    [string]$MsdosPlayer = $env:MSDOS_PLAYER,
    [string]$DosboxX = $env:DOSBOX_X
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
$buildDirectory = Join-Path $projectRoot 'build'
$localDirectory = Join-Path $projectRoot '.local'

function Find-ExtensionFile {
    param([string]$Prefix, [string]$RelativePath)
    $extensionRoot = Join-Path $env:USERPROFILE '.vscode\extensions'
    if (Test-Path -LiteralPath $extensionRoot) {
        $extensions = Get-ChildItem -LiteralPath $extensionRoot -Directory |
            Where-Object { $_.Name -like ($Prefix + '-*') } |
            Sort-Object LastWriteTime -Descending
        foreach ($extension in $extensions) {
            $candidate = Join-Path $extension.FullName $RelativePath
            if (Test-Path -LiteralPath $candidate -PathType Leaf) {
                return $candidate
            }
        }
    }
    return $null
}

function Invoke-DosTool {
    param([string]$Executable, [string[]]$ToolArguments)
    & $MsdosPlayer $Executable @ToolArguments
    if ($LASTEXITCODE -ne 0) {
        throw ('{0} exited with code {1}.' -f (Split-Path $Executable -Leaf), $LASTEXITCODE)
    }
}

try {
    if (-not $MsdosPlayer) {
        $MsdosPlayer = Find-ExtensionFile 'xsro.vscode-dosbox' 'emu\msdos_player\win32-x64\msdos.exe'
    }
    if (-not $MsdosPlayer -or -not (Test-Path -LiteralPath $MsdosPlayer -PathType Leaf)) {
        throw 'MS-DOS Player was not found. Install xsro.vscode-dosbox or set MSDOS_PLAYER to msdos.exe.'
    }

    if (-not $TasmDirectory) {
        $manualTools = Join-Path $projectRoot 'tools\tasm'
        if (Test-Path -LiteralPath (Join-Path $manualTools 'TASM.EXE')) {
            $TasmDirectory = $manualTools
        } else {
            $TasmDirectory = Join-Path $localDirectory 'tasm'
            if (-not (Test-Path -LiteralPath (Join-Path $TasmDirectory 'TASM.EXE')) -or
                -not (Test-Path -LiteralPath (Join-Path $TasmDirectory 'TLINK.EXE'))) {
                $bundle = Find-ExtensionFile 'xsro.masm-tasm' 'resources\TASM.jsdos'
                if (-not $bundle) {
                    throw 'TASM was not found. Install xsro.masm-tasm or set TASM_DIR to your TASM/TLINK directory.'
                }
                New-Item -ItemType Directory -Path $TasmDirectory -Force | Out-Null
                Add-Type -AssemblyName System.IO.Compression.FileSystem
                $archive = [System.IO.Compression.ZipFile]::OpenRead($bundle)
                try {
                    foreach ($entry in $archive.Entries) {
                        if ($entry.FullName.StartsWith('tasm/') -and $entry.Name) {
                            $destination = Join-Path $TasmDirectory $entry.Name
                            [System.IO.Compression.ZipFileExtensions]::ExtractToFile($entry, $destination, $true)
                        }
                    }
                } finally {
                    $archive.Dispose()
                }
                Write-Host 'Prepared local TASM cache from the installed extension.'
            }
        }
    }

    $TasmDirectory = (Resolve-Path -LiteralPath $TasmDirectory).Path
    $MsdosPlayer = (Resolve-Path -LiteralPath $MsdosPlayer).Path
    $assembler = Join-Path $TasmDirectory 'TASM.EXE'
    $linker = Join-Path $TasmDirectory 'TLINK.EXE'
    foreach ($tool in @($assembler, $linker)) {
        if (-not (Test-Path -LiteralPath $tool -PathType Leaf)) {
            throw ('Required tool is missing: ' + $tool)
        }
    }
    if (-not $DosboxX) {
        $DosboxX = Find-ExtensionFile 'xsro.vscode-dosbox' 'emu\dosbox_x\win32-x64\dosbox-x.exe'
    }

    if ($Action -eq 'check') {
        Write-Host ('TASM: ' + $assembler)
        Write-Host ('TLINK: ' + $linker)
        Write-Host ('DOS runner: ' + $MsdosPlayer)
        if ($DosboxX -and (Test-Path -LiteralPath $DosboxX -PathType Leaf)) {
            Write-Host ('DOSBox-X (interactive): ' + $DosboxX)
        } else {
            Write-Host 'DOSBox-X was not found; set DOSBOX_X before using interactive debugging.'
        }
        Write-Host 'Build/run tools located. Use -Action verify to compile and execute the smoke program.'
        exit 0
    }

    New-Item -ItemType Directory -Path $buildDirectory -Force | Out-Null
    # Clear only these known generated files; never recursively remove directories.
    foreach ($name in @('REBUILD.COM', 'REBUILD.OBJ', 'REBUILD.LST', 'BUILD.OK', 'SMOKE.TXT')) {
        $generatedFile = Join-Path $buildDirectory $name
        if (Test-Path -LiteralPath $generatedFile) {
            Remove-Item -LiteralPath $generatedFile -Force
        }
    }
    Copy-Item -LiteralPath (Join-Path $projectRoot 'src\rebuild.asm') -Destination (Join-Path $buildDirectory 'REBUILD.ASM')
    Push-Location $buildDirectory
    try {
        Invoke-DosTool $assembler @('/m2', '/l', 'REBUILD.ASM')
        Invoke-DosTool $linker @('/t', 'REBUILD.OBJ')
        $program = Join-Path $buildDirectory 'REBUILD.COM'
        if (-not (Test-Path -LiteralPath $program -PathType Leaf)) {
            throw 'The linker did not create REBUILD.COM.'
        }
        $size = (Get-Item -LiteralPath $program).Length
        if ($size -le 0 -or $size -gt 65278) {
            throw ('Unexpected COM image size: ' + $size)
        }
        Set-Content -LiteralPath (Join-Path $buildDirectory 'BUILD.OK') -Value 'Build successful.' -Encoding ASCII
        Write-Host ('Built build\REBUILD.COM ({0} bytes).' -f $size)

        if ($Action -eq 'run') {
            Invoke-DosTool $program @()
        } elseif ($Action -eq 'verify') {
            $output = @(& $MsdosPlayer $program)
            if ($LASTEXITCODE -ne 0) {
                throw ('Smoke program returned code ' + $LASTEXITCODE)
            }
            $actual = ($output -join "`n").Trim()
            $expected = "8086 DOS Reconstruction`nToolchain ready."
            if ($actual -ne $expected) {
                throw ('Smoke output did not match. Actual output: ' + $actual)
            }
            Set-Content -LiteralPath (Join-Path $buildDirectory 'SMOKE.TXT') -Value $actual -Encoding ASCII
            Write-Host $actual
            Write-Host 'PASS: TASM assembly, TLINK COM linking, exact banner output, and DOS exit code zero.'
        }
    } finally {
        Pop-Location
    }

    if ($Action -eq 'debug') {
        if (-not $DosboxX -or -not (Test-Path -LiteralPath $DosboxX -PathType Leaf)) {
            throw 'Interactive debugger unavailable. Install xsro.vscode-dosbox or set DOSBOX_X.'
        }
        New-Item -ItemType Directory -Path $localDirectory -Force | Out-Null
        $configPath = Join-Path $localDirectory 'debug.conf'
        $configText = @"
[sdl]
fullscreen=false
[cpu]
cycles=auto
[autoexec]
mount c "$projectRoot"
mount t "$TasmDirectory"
path t:\;z:\
c:
cd build
DEBUGBOX REBUILD.COM
"@
        Set-Content -LiteralPath $configPath -Value $configText -Encoding ASCII
        # This action explicitly opens an interactive debugger for the user.
        Start-Process -FilePath $DosboxX -ArgumentList @('-console', '-conf', ('"{0}"' -f $configPath)) -WorkingDirectory $projectRoot -WindowStyle Normal | Out-Null
        Write-Host 'Opened DOSBox-X. Debugger availability depends on the installed DOSBox-X build.'
    }
} catch {
    Write-Error $_ -ErrorAction Continue
    exit 1
}
