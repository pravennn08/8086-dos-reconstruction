# Executed DOS debugger traces

**2/2 cases passed** using the real reference executable in DOSBox-X's bundled DOS DEBUG.

Reference SHA-256: `2028290647ca744d2aea1ee810f812f5e9b91cbb8512f2c10ab7e108b28fa1af`

## Controlled setup

The debugger seeds the DOS input buffer at `DS:01CCh`, then sets `IP=0117h`
to resume just after the keyboard-read call. This skips startup printing and
keyboard input. The XOR instructions, loop, formatter, and normal exit are
executed by the DOS CPU emulator. No expected memory values are substituted
for captured post-step values.

| ABC checkpoint | IP | BX | CX | Bytes at DS:01CEh |
| --- | --- | --- | --- | --- |
| Before XOR | 0122h | 01CEh | 0003h | 41 42 43 |
| After one trace step | 0125h | 01CEh | 0003h | 6B 42 43 |
| Completed XOR loop | 0128h | 01D1h | 0000h | 6B 68 69 |

The empty-input case reaches `0128h` with `CX=0`, `BX=01CEh`, and an unchanged
buffer. Both cases produce the expected encoded line and exit normally.

- [ABC raw debugger transcript](debugger-abc.txt)
- [Empty-input raw debugger transcript](debugger-empty.txt)
- [Parsed register and memory evidence](debugger-results.json)
- [Keyboard-entered Turbo Debugger session](turbo-session.md)

Run `scripts/dev.ps1 -Action trace` to regenerate these controlled traces.
Addresses and the required hash are pinned to training fixture v1. Segment
values are runtime allocations and can differ between sessions.
