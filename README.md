# 8086 DOS Reconstruction

A reverse-engineering lab for recovering the behavior of a small DOS binary
and rebuilding it in 8086 assembly with Borland Turbo Assembler (TASM).

## Current status

**Phase 1: development environment and project scaffold.**

`src/rebuild.asm` is a toolchain smoke program. It prints two lines and exits
successfully. It is not yet a reconstruction of a target. No original binary
has been selected, and no algorithm has been recovered.

The earlier `ABC -> 6B 68 69` XOR encoder example is an illustration, not an
observed result or a requirement for an unknown target.

## Quick start in VS Code (Windows)

The local launcher can use tools already installed by these extensions:

- **MASM/TASM** (`xsro.masm-tasm`): TASM and TLINK bundle.
- **vscode-DOSBox** (`xsro.vscode-dosbox`): MS-DOS Player and DOSBox-X.

The project does not download or redistribute these tools. Extension bundles
are discovered automatically; a local TASM cache is extracted into ignored
`.local/tasm/` on first use. See [tools/README.md](tools/README.md) for overrides.

1. Open **Terminal > Run Task > DOS: Check toolchain**.
2. Press **Ctrl+Shift+B** to assemble and link the starter program.
3. Run **DOS: Run program**, or **DOS: Verify setup** for the smoke check.

Expected program output:

```text
8086 DOS Reconstruction
Toolchain ready.
```

Equivalent commands from a PowerShell terminal at the project root:

```powershell
powershell.exe -NoProfile -ExecutionPolicy RemoteSigned -File .\scripts\dev.ps1 -Action check
powershell.exe -NoProfile -ExecutionPolicy RemoteSigned -File .\scripts\dev.ps1 -Action build
powershell.exe -NoProfile -ExecutionPolicy RemoteSigned -File .\scripts\dev.ps1 -Action run
powershell.exe -NoProfile -ExecutionPolicy RemoteSigned -File .\scripts\dev.ps1 -Action verify
```

Build output is `build/REBUILD.COM`, with an object file and assembly listing.
The launcher rebuilds before running, so an earlier executable cannot mask
an assembly error. Build artifacts and local tools are ignored by Git.

## DOS emulator workflow

With `src/rebuild.asm` open, the MASM/TASM extension's **Run ASM Code** and
**Debug ASM Code** commands use `dosasm.jsonc`. Run builds and executes the
same `.COM` program; debug opens it in Turbo Debugger's instruction view.
Symbols/source stepping are not configured for this initial COM build.

`build.bat` is a DOS batch file. Execute it *inside* DOSBox/DOSBox-X with
TASM and TLINK on the DOS PATH, not directly in a Windows terminal.

For DOSBox-X's built-in debugger, run **DOS: Debug program**. The launcher
creates an ignored local config, mounts the project as C: and the TASM
directory as T:, and uses `DEBUGBOX REBUILD.COM`. A debugger-enabled
DOSBox-X build is required. This interactive debugger path is separate from
the console smoke check.

## Project layout

```text
analysis/   Observations, annotated disassembly, algorithm notes, traces
demo/       Instructions for recording a reproducible demonstration
scripts/    Windows tool discovery, build, run, and verification launcher
src/        TASM reconstruction (currently the smoke program)
target/     Original binary provenance; target selection is pending
test/       Test cases and recorded results
tools/      Local toolchain configuration instructions
```

## Next milestone

Choose a small training `.COM` binary whose implementation is initially
unknown to the analyst. Record its origin, distribution terms, size, and
SHA-256 in `target/provenance.md`. Observe input/output before inspecting its
instructions, then replace the scaffold using evidence from that binary.

Keep hypotheses separate from confirmed findings. Reconstruction compatibility
requires comparisons against the original; a successful setup check only
verifies the development tools.

## References

- [MASM/TASM project configuration](https://github.com/dosasm/masm-tasm)
- [DOSBox-X debugger documentation](https://github.com/joncampbell123/dosbox-x/blob/master/README.debugger)
- [Microsoft MS-DOS programming documentation](https://msarchive.pcjs.org/mspl13/msdos/encyclopedia/section2/)

## License

Project-authored code and documentation use the MIT license in `LICENSE.md`.
Third-party tools and any future target binary retain their own licenses.
