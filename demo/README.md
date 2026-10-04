# Live debugger demonstration

1. Run **DOS: Debug training target** from VS Code's Terminal > Run Task,
   or `powershell.exe -NoProfile -ExecutionPolicy RemoteSigned -File
   .\scripts\dev.ps1 -Action debug-target` from the repository root.
2. Dismiss **Program has no symbol table**. The COM fixture intentionally
   has no debugging symbols; its CPU instructions are still visible.
3. In the CPU code pane, right-click **Goto**, enter `122h` (relative to `CS`), and press
   **F2**. View > Breakpoints can confirm the enabled breakpoint.
4. Press **F9**, type `ABC`, and press Enter. The program reads the keyboard
   through its original DOS input call and stops before the first XOR.
5. Observe `IP=0122h`, `BX=01CEh`, `CX=0003h`, and `DS:01CE=41`.
6. Press **F7** once. `IP` advances to `0125h`. Select the XOR row again to
   refresh its memory operand: `DS:01CE=6B`. The counter and pointer are
   unchanged by that single XOR instruction.
7. Use **F9** to continue. The breakpoint will stop again for B and C;
   toggle it off with **F2** at the XOR row to finish without further stops.
8. **Alt+X** exits Turbo Debugger. Close the DOSBox-X window when finished.

The actual captured [interactive trace](../analysis/traces/turbo-session.md)
includes screenshots. Runtime segment values vary; use `CS` and `DS` rather
than copying the session's `0F6Bh` segment value.

Use **DOS: Debug program** to debug the reconstruction after building it.
Its addresses differ; `CS:0122h` is specific to the reference fixture.

## Repeatable automated trace

Run **DOS: Capture debugger trace** or `scripts/dev.ps1 -Action trace`.
The [checked report](../analysis/traces/debugger-results.md) records ABC and
empty-input cases through DOSBox-X's bundled DOS DEBUG. This controlled mode
seeds the input buffer and skips the keyboard-read call. It records actual
runtime registers and memory after executing the target's instructions.

Show the target hash, annotated instructions, interactive before/after images,
controlled trace transcripts, and the 31-case execution comparison report.
Describe the project as a guided reconstruction lab with disclosed source.
