# Training target provenance

Status: selected, built, and inspected on 2026-10-04.

| Field | Value |
| --- | --- |
| Filename | ENCODE.COM |
| Origin | Authored for this project as a guided training fixture |
| Source | [source/encode.asm](source/encode.asm), disclosed |
| Version | Training fixture v1 |
| Distribution terms | MIT; see [project license](../LICENSE.md) and [fixture copy](LICENSE.md) |
| Size | 271 bytes |
| SHA-256 | `2028290647ca744d2aea1ee810f812f5e9b91cbb8512f2c10ab7e108b28fa1af` |
| Build | TASM 4.1, TLINK 7.1.30.1, COM linking with /t |
| Execution backend | MS-DOS Player from installed vscode-dosbox extension |
| Prior source access | Yes: author/implementer knows the target source |

The target is a reproducible guided exercise, not an independently recovered
unknown binary. The reconstruction is a different implementation of its
observable behavior. No original symbol names or undocumented third-party
algorithm are claimed to have been discovered.

Regenerate explicitly with `scripts/dev.ps1 -Action target` or DOS
`build-target.bat`. Run `-Action inspect` and review identity after any change.
The comparison suite verifies the executable hash against `metadata.json`.
