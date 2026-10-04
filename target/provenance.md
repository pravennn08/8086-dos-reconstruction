# Target provenance

Status: **not selected**. The starter `build/REBUILD.COM` is a toolchain smoke
program and must not be presented as an independently recovered target.

| Field | Value |
| --- | --- |
| Original filename | Pending |
| Source/download URL | Pending |
| Author/project | Pending |
| Version | Pending |
| Distribution terms | Pending |
| File size in bytes | Pending |
| SHA-256 | Pending |
| Acquisition date | Pending |
| Emulator/version/config | Pending |
| Prior access to original source | Record honestly |

After acquiring the target, calculate its identity from the project root:

```powershell
Get-Item .\target\original.com | Select-Object Name, Length
Get-FileHash .\target\original.com -Algorithm SHA256
```

Store the selected executable locally as `target/original.com`. Target
executables are ignored by default. Record a reproducible acquisition path
and distribution terms before deciding whether to include one in Git.
