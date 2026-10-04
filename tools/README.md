# Local toolchain

The Windows launcher discovers TASM/TLINK from the installed `xsro.masm-tasm`
extension and MS-DOS Player/DOSBox-X from `xsro.vscode-dosbox`. No download is
performed. These tools are third-party dependencies and are not committed.

Alternatively, place your available TASM files in ignored `tools/tasm/`,
including `TASM.EXE`, `TLINK.EXE`, and their required runtime files, or set:

```powershell
$env:TASM_DIR = 'C:\path\to\tasm'
$env:MSDOS_PLAYER = 'C:\path\to\msdos.exe'
$env:DOSBOX_X = 'C:\path\to\dosbox-x.exe'
.\scripts\dev.ps1 -Action check
```

The same locations can be passed using `-TasmDirectory`, `-MsdosPlayer`, and
`-DosboxX`. Set these only in your local shell, not in committed settings.

The PowerShell tasks are Windows-specific. `build.bat` can be used inside a
DOS emulator on other hosts, with the project mounted as C: and TASM on PATH.

If the legacy console runner fails before the assembler banner in a deeply
nested working directory, move the checkout to a shorter path or use the
DOSBox-X workflow. DOSBox mounts give the program a short DOS-visible path.
