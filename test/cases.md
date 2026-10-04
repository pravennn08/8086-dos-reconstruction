# Verification cases

## Setup regression

`scripts/dev.ps1 -Action smoke` builds src/smoke.asm and checks the original
two-line banner and DOS exit code zero. This is also DOS: Verify setup.

## Guided encoder comparison

`scripts/dev.ps1 -Action verify` builds the reconstruction and runs both
executables with the same input. Reference identity must match metadata.json.

Each case checks identical stdout bytes, zero exit codes, empty stderr,
and an independently calculated expected encoded result.

- E-001: empty input; zero-count loop guard.
- E-002/E-003: ABC and repeated characters.
- E-004..E-009: upper/lowercase, spaces, dollar signs, punctuation, and digits.
- E-010/E-011: exactly 64 characters, including varied data.
- E-012/E-013: 65 and 128 characters; verify the 64-character limit.
- E-014/E-015: all printable ASCII characters split into accepted-size inputs.
- E-016..E-031: deterministic generated inputs, seed 8086.

Executed outcomes: [encoder-results.md](encoder-results.md).
Raw byte evidence: [encoder-results.json](encoder-results.json).

Interactive editing keys, Ctrl-C, code-page changes, and arbitrary binary
input are outside this set. GUI execution is not automated by these tests.
