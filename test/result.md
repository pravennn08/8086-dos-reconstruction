# Verification results

## Initial setup

Verified on 2026-10-04 on Windows using the installed VS Code extension tools.

| Check | Result |
| --- | --- |
| TASM 4.1 assembly | PASS: zero errors and zero warnings |
| TLINK 7.1.30.1 COM linking | PASS: 58-byte REBUILD.COM |
| Exact banner output | PASS: the two starter lines preserved in src/smoke.asm |
| DOS process exit code | PASS: 0 |
| Windows PowerShell launcher syntax | PASS |
| VS Code task/settings and dosasm JSON | PASS: parsed successfully |
| Assembly failure handling | PASS: undefined symbol returns launcher exit code 1 |
| Stale build handling | PASS: previous COM image and BUILD.OK removed before failed build |
| Git ignore rules | PASS: build output and locally cached TASM tools excluded |

The failure check used a separate scratch fixture; the project source was
not altered for that check.

SHA-256 of the verified starter executable:

```text
DDC1A7D1981415363D6823A76E78232978E0D6B9C9DB681AB5B4AB8D070414B9
```

Interactive DOSBox-X/Turbo Debugger launch is configured but has not been
verified by this console smoke check.

## Reconstruction compatibility

Status: **31/31 recorded cases passed** against the authored training
reference. This is a guided comparison with disclosed source; an independent
case study against an initially unfamiliar binary is still pending.

## Guided encoder milestone

The encoder target and reconstruction are now implemented. See [executed comparison results](encoder-results.md) and [raw input/output evidence](encoder-results.json). The phase-1 report above applies to the preserved smoke program.


The updated launcher was also checked with invalid assembly in a separate
scratch fixture: failed reconstruction and target builds return exit code 1,
clear stale generated outputs, and preserve unrelated files and the existing
reference binary. Python syntax, VS Code JSON, evidence hashes, and README
file links were checked successfully.

## Live debugger milestone

Keyboard-entered ABC was captured in Turbo Debugger 5.0 inside DOSBox-X
0.83.18. Before/after screenshots show IP 0122h -> 0125h and the memory byte
41h -> 6Bh after a single step. See the
[interactive session](../analysis/traces/turbo-session.md).

The separate [controlled trace report](../analysis/traces/debugger-results.md)
checks ABC and the empty-input branch. Its seeded input and skipped keyboard
call are documented explicitly; it is not presented as GUI keyboard testing.
