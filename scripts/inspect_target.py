"""Record binary identity, strings, and an optional raw 16-bit disassembly."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess

ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "binary", nargs="?", type=Path, default=ROOT / "target/ENCODE.COM"
    )
    parser.add_argument("--objdump", default="objdump.exe")
    parser.add_argument("--code-end", type=lambda value: int(value, 0))
    args = parser.parse_args()
    data = args.binary.read_bytes()
    if not 0 < len(data) <= 65278:
        raise ValueError(
            "Expected a nonempty conventional DOS COM image smaller than 64 KiB."
        )
    strings = [
        {
            "file_offset": match.start(),
            "dos_offset": hex(0x100 + match.start()),
            "text": match.group().decode("ascii"),
        }
        for match in re.finditer(rb"[\x20-\x7e]{4,}", data)
    ]
    metadata = {
        "name": args.binary.name,
        "size_bytes": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
        "assumed_load_offset": "0x100",
        "first_64_bytes_hex": data[:64].hex(" "),
        "ascii_strings": strings,
    }
    destination = ROOT / "target/metadata.json"
    destination.write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    print(f"{metadata['name']}: {len(data)} bytes; SHA-256 {metadata['sha256']}")
    for entry in strings:
        print(f"  {entry['dos_offset']}: {entry['text']}")
    print(
        "Saved target/metadata.json. The COM format/load origin are assumptions, not signature detection."
    )

    objdump = shutil.which(args.objdump)
    if not objdump:
        print(
            "objdump is unavailable. Use Turbo Debugger for disassembly, or supply --objdump PATH."
        )
        return 0
    command = [
        objdump,
        "-D",
        "-b",
        "binary",
        "-m",
        "i8086",
        "-M",
        "intel",
        "--adjust-vma=0x100",
    ]
    if args.code_end is not None:
        if not 0x100 < args.code_end <= 0x100 + len(data):
            raise ValueError("--code-end must lie inside the loaded COM image.")
        command.append(f"--stop-address={args.code_end}")
    command.append(str(args.binary.resolve().relative_to(ROOT)))
    result = subprocess.run(
        command, cwd=ROOT, capture_output=True, text=True, timeout=10, check=True
    )
    traces = ROOT / "analysis/traces"
    traces.mkdir(parents=True, exist_ok=True)
    (traces / "target-disassembly.txt").write_text(
        "Linear decode of binary bytes. Embedded data can decode as misleading instructions.\n"
        + result.stdout,
        encoding="utf-8",
    )
    print("Saved analysis/traces/target-disassembly.txt.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, subprocess.SubprocessError) as error:
        raise SystemExit(f"Inspection failed: {error}")
