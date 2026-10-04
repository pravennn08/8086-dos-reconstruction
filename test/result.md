# Verification results

## Initial setup

Verified on 2026-10-04 on Windows using the installed VS Code extension tools.

| Check | Result |
| --- | --- |
| TASM 4.1 assembly | PASS: zero errors and zero warnings |
| TLINK 7.1.30.1 COM linking | PASS: 58-byte REBUILD.COM |
| Exact banner output | PASS: the two lines documented in README |
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

Status: **not run**. Target selection and algorithm recovery are pending.
No claim of compatibility with an original binary is made at this stage.
