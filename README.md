<div align="center">

# 8086 DOS Reconstruction

[![Assembly (8086)](https://img.shields.io/badge/Assembly-8086-red)](src/rebuild.asm)
[![PowerShell](https://img.shields.io/badge/PowerShell-build_scripts-5391FE)](scripts/dev.ps1)
[![Python](https://img.shields.io/badge/Python-inspection_%26_tests-3776AB)](scripts/inspect_target.py)
[![DOS Batch](https://img.shields.io/badge/Batch-DOS_build_scripts-green)](build.bat)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow)](./LICENSE)

</div>
An 8086 assembly lab for examining a DOS executable, documenting its behavior,
and rebuilding that behavior with Borland Turbo Assembler (TASM).

The current example is a console encoder: enter a line of text and receive
hexadecimal bytes. The project includes a runnable reference, a separate TASM
implementation, disassembly, and **31 passing execution comparisons**.

## What this project solves

When a small legacy executable has no useful documentation, its inputs,
outputs, and machine instructions can reveal what it does. This repository
demonstrates a repeatable process:

1. Identify the executable and record its origin and SHA-256 hash.
2. Run controlled inputs and inspect its 8086 instructions.
3. Document the transformation and DOS input/output behavior.
4. Write a reconstruction and compare both executables on the same inputs.

For this example, each accepted input byte is XORed with `2Ah` and displayed
as two uppercase hexadecimal digits:

| Character | ASCII byte | XOR operation | Output |
| --------- | ---------- | ------------- | ------ |
| A         | `41h`      | `41h XOR 2Ah` | `6B`   |
| B         | `42h`      | `42h XOR 2Ah` | `68`   |
| C         | `43h`      | `43h XOR 2Ah` | `69`   |

This is a reversible teaching example, not secure encryption.

## Current scope

This is a **guided reverse-engineering lab with disclosed source**. The
reference was authored for this project and its source is included. The
analysis uses the executable, but prior access to its implementation is
documented in [target/provenance.md](target/provenance.md).

| Milestone                                                             | Status           |
| --------------------------------------------------------------------- | ---------------- |
| Reference DOS COM executable                                          | Built: 271 bytes |
| TASM reconstruction                                                   | Built: 250 bytes |
| Binary identity, strings, and disassembly                             | Recorded         |
| Execution comparison against the reference and a Python specification | 31/31 passed     |
| Interactive register and memory trace | Captured: keyboard-entered ABC |
| Case study using an initially unfamiliar binary                       | Future work      |

The reference transforms the input buffer in place and uses an `XLAT` lookup
table for hexadecimal digits. The reconstruction transforms each byte while
printing and calculates the digits arithmetically. Their machine code differs;
their output agrees for the recorded tests.

## Run with GUI Turbo Assembler

You need TASM, TLINK, and a DOS runtime, such as the one provided by your GUI
Turbo Assembler setup. The GUI workflow does not require the VS Code extension.

1. Open or reload [src/rebuild.asm](src/rebuild.asm) to load the current encoder.
2. Assemble it with TASM and link a **COM** executable using TLINK's `/t` option.
3. Run the newly built `REBUILD.COM`, type `ABC`, and press Enter.

In a DOS terminal with the current directory set to `src`, the commands are:

```dos
tasm /m2 /l rebuild.asm
tlink /t rebuild.obj
rebuild.com
```

Expected interaction:

```text
8086 DOS Encoder
Enter text (max 64 characters): ABC
Encoded: 6B 68 69
```

The program accepts one line of up to 64 characters and then exits. Empty
input produces `Encoded: ` with no bytes. Output uses a single space between
bytes and no trailing separator. Characters beyond the limit are discarded
by DOS buffered input until Enter.

Run [target/ENCODE.COM](target/ENCODE.COM) in the same DOS runtime to compare
the reference. [src/smoke.asm](src/smoke.asm) preserves the earlier
`Toolchain ready.` setup check.

## Build and verify on Windows

Run these commands from the repository root in PowerShell:

```powershell
# Locate TASM, TLINK, and the DOS runner.
powershell.exe -NoProfile -ExecutionPolicy RemoteSigned -File .\scripts\dev.ps1 -Action check

# Build and run the reconstruction.
powershell.exe -NoProfile -ExecutionPolicy RemoteSigned -File .\scripts\dev.ps1 -Action run

# Inspect the reference and compare both executables.
powershell.exe -NoProfile -ExecutionPolicy RemoteSigned -File .\scripts\dev.ps1 -Action inspect
powershell.exe -NoProfile -ExecutionPolicy RemoteSigned -File .\scripts\dev.ps1 -Action verify
```

The launcher uses Windows PowerShell, TASM/TLINK, and MS-DOS Player. It can
discover tools from installed `xsro.masm-tasm` and `xsro.vscode-dosbox`
extensions or use explicit local paths. Python 3 is required for `inspect`
and `verify`; GNU objdump is optional for disassembly. See
[tools/README.md](tools/README.md) for tool paths and overrides.

In VS Code, **Ctrl+Shift+B** builds the reconstruction. Use **Terminal > Run
Task** for these tasks:

| Task                         | Action                                        |
| ---------------------------- | --------------------------------------------- |
| DOS: Check toolchain         | Locate installed tools                        |
| DOS: Run program             | Build and run the encoder                     |
| DOS: Verify setup            | Build and run the preserved smoke program     |
| DOS: Inspect training target | Collect metadata and available disassembly    |
| DOS: Compare encoder         | Build the reconstruction and run all 31 cases |
| DOS: Build training target   | Explicitly regenerate the disclosed reference |
| DOS: Debug training target | Open the reference in Turbo Debugger |
| DOS: Debug program | Build and debug the reconstruction |
| DOS: Capture debugger trace | Record and check two controlled CPU traces |

These tasks call the project launcher. The extension's separate Run Assembly
command is not required for this workflow.

For a DOS-only build, run `build.bat` from the repository root with TASM and
TLINK on the DOS PATH. It produces `build/REBUILD.COM`.

### Rebuilding the reference

The reference binary is included so normal build/run/verify operations can
compare against it. To regenerate it from the disclosed source, use
`-Action target` or run `build-target.bat` inside DOS. Then run `-Action inspect`
and review the binary identity in [target/provenance.md](target/provenance.md)
before recording new comparisons.

The inspection action uses this fixture's code boundary at `0179h` to avoid
decoding data as instructions. A different target needs its own boundary
analysis.

## Verification and evidence

The automated suite executes both DOS binaries through MS-DOS Player and
compares raw output bytes, exit codes, and stderr. It also checks the encoded
result against a Python specification.

The 31 cases cover empty input, letters, spaces, punctuation, dollar signs,
digits, all printable ASCII characters, 64-character limits, excess input,
and deterministic generated cases. See the
[case descriptions](test/cases.md), [results](test/encoder-results.md), and
[captured input/output bytes](test/encoder-results.json).

GUI keyboard editing, Ctrl-C handling, other code pages, and high-bit or binary
input have not been verified by this suite.

| Evidence                                 | File                                                                             |
| ---------------------------------------- | -------------------------------------------------------------------------------- |
| Origin, license, and source disclosure   | [target/provenance.md](target/provenance.md)                                     |
| Hash, size, and extracted strings        | [target/metadata.json](target/metadata.json)                                     |
| Controlled input/output observations     | [analysis/observation.md](analysis/observation.md)                               |
| Algorithm and implementation differences | [analysis/algorithm.md](analysis/algorithm.md)                                   |
| Annotated instruction excerpt            | [analysis/annotated-disassembly.asm](analysis/annotated-disassembly.asm)         |
| Code-region disassembly                  | [analysis/traces/target-disassembly.txt](analysis/traces/target-disassembly.txt) |
| Demonstration instructions               | [demo/README.md](demo/README.md)                                                 |

## Project layout

```text
analysis/       Observations, algorithm, and disassembly
build/          Generated executables, objects, and listings (ignored)
scripts/        Windows launcher, binary inspection, and comparison
src/            Reconstruction and preserved smoke program
target/         Reference binary, disclosed source, metadata, and license
test/           Cases and captured execution results
tools/          Tool configuration guide
demo/           Demonstration instructions
```

## Live debugger

A live debugger pauses the running DOS program at a breakpoint and lets you
execute one CPU instruction at a time while inspecting registers and memory.
For example, with input `ABC`, stepping over the XOR instruction changes the
first input byte from `41h` (`A`) to `6Bh`. This provides direct evidence of
how the encoder transforms its input.

Use **Terminal > Run Task > DOS: Debug training target**, or run:

```powershell
powershell.exe -NoProfile -ExecutionPolicy RemoteSigned -File .\scripts\dev.ps1 -Action debug-target
```

The task opens the reference in Turbo Debugger's assembly view. Dismiss the
expected **Program has no symbol table** notice. In the CPU code pane,
right-click **Goto**, enter `122h` (relative to `CS`), and press **F2** to set a breakpoint.
Press **F9**, enter `ABC`, and press Enter. At the breakpoint, `BX=01CEh`,
`CX=3`, and the operand display shows `DS:01CE=41`. Press **F7** once, then
select the XOR row again to refresh its operand display: the byte is now
`6Bh` and `IP=0125h`. **Alt+X** exits Turbo Debugger.

The [captured interactive session](analysis/traces/turbo-session.md) contains
real before/after screenshots and registers from keyboard-entered `ABC`.

**DOS: Debug program** opens the reconstruction, whose instruction addresses
and implementation differ from the reference. The breakpoint above applies
to the pinned reference only.

**DOS: Capture debugger trace** (or `-Action trace`) regenerates
[two checked CPU traces](analysis/traces/debugger-results.md). That automated
mode explicitly seeds the input buffer and resumes after the DOS keyboard
call; its input setup differs from the interactive session.

A later independent case study should begin with an unfamiliar executable,
record prior source access, and derive its behavior from the binary.

## Author and license

Created by **Engr. Raven C. Magbanua**.

Project code and documentation are released under the
[MIT License](LICENSE.md). A copy is included with the authored training
fixture in [target/LICENSE.md](target/LICENSE.md). Third-party tools retain
their own licenses and are not redistributed by this repository.
