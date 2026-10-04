# Local tool configuration

The GUI Turbo Assembler workflow needs TASM, TLINK, and a DOS runtime. The
Windows launcher in `scripts/dev.ps1` additionally needs MS-DOS Player.
Python 3 is required for inspection and execution comparison.

## Tool discovery

TASM/TLINK are resolved in this order:

1. The `-TasmDirectory` argument or `TASM_DIR` environment variable.
2. The ignored `tools/tasm/` directory in this repository.
3. The ignored `.local/tasm/` cache, extracted when needed from the installed
   `xsro.masm-tasm` extension's `resources/TASM.jsdos` bundle.

MS-DOS Player uses the `-MsdosPlayer` argument or `MSDOS_PLAYER` environment
variable, then the installed `xsro.vscode-dosbox` extension's native runner.
DOSBox-X uses `-DosboxX` or `DOSBOX_X`, then the same extension's native emulator.
Extension discovery searches `%USERPROFILE%\.vscode\extensions`.

The launcher does not search the system PATH for TASM or DOS emulators.
`python.exe` and optional `objdump.exe` are resolved through PATH.

## Explicit paths

Use your actual installed tool paths in place of these examples:

```powershell
$env:TASM_DIR = 'C:\DOS\TASM'
$env:MSDOS_PLAYER = 'C:\DOS\MSDOS\msdos.exe'
$env:DOSBOX_X = 'C:\DOS\DOSBox-X\dosbox-x.exe'
powershell.exe -NoProfile -ExecutionPolicy RemoteSigned -File .\scripts\dev.ps1 -Action check
```

Keep TASM/TLINK runtime files together with the executables. For a local
installation, put those files in `tools/tasm/`. This directory and the
extension-derived cache are excluded from Git.

## Inspection and debugging

`-Action inspect` collects the reference hash, size, and printable strings.
If GNU objdump is available, it also writes the code-region disassembly.
An explicit objdump path can be supplied directly to the Python inspector:

```powershell
python.exe .\scripts\inspect_target.py --objdump 'C:\MinGW\bin\objdump.exe' --code-end 0x179
```

`0179h` is the recorded training fixture's code end, not a general boundary
for DOS COM programs. Without objdump, the metadata inspection still works;
Turbo Debugger can be used to inspect instructions interactively.

`-Action debug-target` opens the reference in Turbo Debugger (`TD.EXE`)
inside DOSBox-X. `-Action debug` builds and opens the reconstruction. Both
use assembler startup (`-l`) and ignore old saved program state (`-ji`).
TD's working files stay in the ignored `.local/TD/` directory. The expected
no-symbol-table notice can be dismissed to inspect the COM's instructions.

`-Action trace` requires only Python 3 and DOSBox-X with its bundled DOS
DEBUG command. It checks two controlled instruction traces and writes the
captured evidence to `analysis/traces/`. This action does not require TASM
or MS-DOS Player. It is pinned to the training fixture's hash and addresses.
Interactive Turbo Debugger keyboard entry and single stepping have been
captured separately; follow `demo/README.md` to repeat the session.

## Troubleshooting

Run `-Action check` first and use explicit paths when discovery fails.
The project's VS Code tasks invoke the launcher directly; they do not depend
on the extension's separate Run Assembly command.

If MS-DOS Player fails on a long host path, try a shorter local checkout and
short tool paths. Run the DOS-only `build.bat` inside a DOS runtime with TASM
and TLINK on its DOS PATH when using that workflow.

Use tool copies you are entitled to use. Third-party binaries are not
included in the repository and retain their original license terms.
