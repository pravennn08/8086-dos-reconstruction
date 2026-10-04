"""Execute the actual reference and reconstruction with identical DOS input."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import random
import subprocess

ROOT = Path(__file__).resolve().parent.parent


def test_cases() -> list[tuple[str, bytes]]:
    curated = [
        ("empty", b""),
        ("ABC", b"ABC"),
        ("repeated", b"AAAA"),
        ("uppercase", b"HELLO"),
        ("lowercase", b"hello"),
        ("single-space", b" "),
        ("spaces", b" A B "),
        ("punctuation-dollar", b"$!?.*"),
        ("digits", b"0123456789"),
        ("maximum-64", b"A" * 64),
        ("maximum-mixed", b"Ab09 $!?" * 8),
        ("over-limit-65", b"A" * 65),
        ("over-limit-128", b"A" * 128),
        ("printable-ASCII-1", bytes(range(0x20, 0x60))),
        ("printable-ASCII-2", bytes(range(0x60, 0x7F))),
    ]
    rng = random.Random(8086)
    for number in range(16):
        curated.append(
            (
                f"seeded-{number + 1:02d}",
                bytes(rng.randrange(0x20, 0x7F) for _ in range(rng.randrange(65))),
            )
        )
    return curated


def execute(runner: Path, program: Path, data: bytes) -> dict:
    result = subprocess.run(
        [str(runner), str(program)],
        input=data + b"\r\n",
        capture_output=True,
        cwd=ROOT / "build",
        timeout=5,
    )
    return {
        "exit_code": result.returncode,
        "stdout_hex": result.stdout.hex(),
        "stderr_hex": result.stderr.hex(),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runner", required=True, type=Path)
    args = parser.parse_args()
    reference = ROOT / "target/ENCODE.COM"
    candidate = ROOT / "build/REBUILD.COM"
    reference_hash = hashlib.sha256(reference.read_bytes()).hexdigest()
    candidate_hash = hashlib.sha256(candidate.read_bytes()).hexdigest()
    pinned = json.loads((ROOT / "target/metadata.json").read_text(encoding="utf-8"))
    if reference_hash != pinned["sha256"]:
        raise ValueError(
            "Reference hash changed. Inspect the target and review its provenance before comparing."
        )

    results = []
    banner = b"8086 DOS Encoder\r\nEnter text (max 64 characters): "
    for number, (name, data) in enumerate(test_cases(), 1):
        reference_run = execute(args.runner, reference, data)
        candidate_run = execute(args.runner, candidate, data)
        expected_result = (
            b"Encoded: "
            + b" ".join(f"{byte ^ 0x2a:02X}".encode("ascii") for byte in data[:64])
            + b"\r\n"
        )
        reference_stdout = bytes.fromhex(reference_run["stdout_hex"])
        candidate_stdout = bytes.fromhex(candidate_run["stdout_hex"])
        checks = {
            "identical_stdout_bytes": reference_stdout == candidate_stdout,
            "exit_codes_zero": reference_run["exit_code"]
            == candidate_run["exit_code"]
            == 0,
            "stderr_empty": reference_run["stderr_hex"]
            == candidate_run["stderr_hex"]
            == "",
            "reference_matches_spec": reference_stdout.startswith(banner)
            and reference_stdout.endswith(expected_result),
            "reconstruction_matches_spec": candidate_stdout.startswith(banner)
            and candidate_stdout.endswith(expected_result),
        }
        passed = all(checks.values())
        results.append(
            {
                "id": f"E-{number:03d}",
                "name": name,
                "input_hex": data.hex(),
                "accepted_length": min(len(data), 64),
                "expected_result_hex": expected_result.hex(),
                "reference": reference_run,
                "reconstruction": candidate_run,
                "checks": checks,
                "passed": passed,
            }
        )
        print(f"{'PASS' if passed else 'FAIL'} E-{number:03d}: {name}", flush=True)

    trace = {
        "verified_at_utc": datetime.now(timezone.utc).isoformat(),
        "reference_sha256": reference_hash,
        "reconstruction_sha256": candidate_hash,
        "implementation": "Guided fixture with disclosed source; not an independent blind target.",
        "backend": "MS-DOS Player; input supplied as raw bytes followed by CRLF.",
        "results": results,
    }
    (ROOT / "test/encoder-results.json").write_text(
        json.dumps(trace, indent=2) + "\n", encoding="utf-8"
    )
    passing = sum(item["passed"] for item in results)
    lines = [
        "# Guided encoder verification",
        "",
        f"**{passing}/{len(results)} cases passed.**",
        "",
        "Both DOS executables were actually run. Output bytes, exit codes, and stderr were compared.",
        "The encoded result was also checked against a separate Python specification.",
        "",
        f"Reference SHA-256: `{reference_hash}`",
        "",
        f"Reconstruction SHA-256: `{candidate_hash}`",
        "",
        "| ID | Case | Input length | Accepted length | Result |",
        "| --- | --- | ---: | ---: | --- |",
    ]
    for item in results:
        lines.append(
            f"| {item['id']} | {item['name']} | {len(bytes.fromhex(item['input_hex']))} | {item['accepted_length']} | {'PASS' if item['passed'] else 'FAIL'} |"
        )
    lines += [
        "",
        "Raw inputs and captured outputs: [encoder-results.json](encoder-results.json).",
        "",
        "The original and reconstruction have different machine code. This comparison establishes",
        "agreement for the recorded cases, not equivalence for every DOS environment or input.",
        "",
        "GUI Turbo Assembler execution has not been automated by this test. Console editing keys,",
        "Ctrl-C handling, other code pages, and high-bit/binary input are outside this test set.",
        "",
    ]
    (ROOT / "test/encoder-results.md").write_text("\n".join(lines), encoding="utf-8")
    print(
        f"{passing}/{len(results)} passed. Evidence saved in test/encoder-results.json and .md."
    )
    return 0 if passing == len(results) else 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, KeyError, subprocess.SubprocessError) as error:
        raise SystemExit(f"Encoder verification failed: {error}")
