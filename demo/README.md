# Demonstration

1. Reopen src/rebuild.asm in GUI Turbo Assembler and compile/link as COM.
2. Run it with ABC; show Encoded: 6B 68 69.
3. Show an empty line, a dollar sign, and the 64-character input boundary.
4. Run target/ENCODE.COM with the same inputs and compare results.
5. In Turbo Debugger, break at CS:0122h and inspect DS:01CEh before and after
   the XOR instruction. Record the actual memory bytes and registers.
6. Show the pinned target hash, annotated binary instructions, and the
   31-case execution report.

Call this a guided reconstruction lab with disclosed source. The interactive
debugger step remains for the user to perform; it was not fabricated from
the automated comparison runs.
