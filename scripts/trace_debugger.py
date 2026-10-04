"""Capture checked 8086 instruction traces using DOSBox-X's bundled DOS DEBUG."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent
FIXTURE_SHA256 = '2028290647ca744d2aea1ee810f812f5e9b91cbb8512f2c10ab7e108b28fa1af'
REGISTER_LINE = re.compile(
    r'AX=([0-9A-F]{4}) BX=([0-9A-F]{4}) CX=([0-9A-F]{4}) DX=([0-9A-F]{4}) '
    r'SP=([0-9A-F]{4}) BP=([0-9A-F]{4}) SI=([0-9A-F]{4}) DI=([0-9A-F]{4})\n'
    r'DS=([0-9A-F]{4}) ES=([0-9A-F]{4}) SS=([0-9A-F]{4}) CS=([0-9A-F]{4}) '
    r'IP=([0-9A-F]{4}) ([^\n]+)\n([^\n]+)'
)
REGISTER_NAMES = ('AX', 'BX', 'CX', 'DX', 'SP', 'BP', 'SI', 'DI', 'DS', 'ES', 'SS', 'CS', 'IP')


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def snapshots(text: str) -> list[dict]:
    result = []
    for match in REGISTER_LINE.finditer(text):
        item = dict(zip(REGISTER_NAMES, match.groups()[:13]))
        item['flags'] = match.group(14)
        item['instruction'] = match.group(15)
        result.append(item)
    return result


def dumps(text: str) -> list[str]:
    result = []
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.lower() != '-d 1cc 1d1':
            continue
        values = []
        for row in lines[index + 1:]:
            if not re.match(r'^[0-9A-F]{4}:[0-9A-F]{4} ', row):
                break
            # DEBUG's 16-byte rows put the ASCII rendering after column 60.
            values.extend(re.findall(r'\b[0-9A-F]{2}\b', row[11:60]))
        require(len(values) == 6, 'Expected six captured input-buffer bytes.')
        result.append(' '.join(values))
    return result


def commands(empty: bool) -> str:
    seed = '41 00 0d 00 00 00' if empty else '41 03 41 42 43 0d'
    lines = [f'e 1cc {seed}', 'r ip', '117']
    if not empty:
        lines += ['g 122', 'r', 'd 1cc 1d1', 't', 'r', 'd 1cc 1d1']
    lines += ['g 128', 'r', 'd 1cc 1d1', 'g', 'q']
    return '\r\n'.join(lines) + '\r\n'


def capture(dosbox: Path, reference: Path, empty: bool, timeout: float) -> bytes:
    work = ROOT / '.local/debug-trace' / ('empty' if empty else 'abc')
    work.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(reference, work / 'ENCODE.COM')
    (work / 'TRACE.IN').write_bytes(commands(empty).encode('ascii'))
    raw_path = work / 'TRACE.TXT'
    if raw_path.exists():
        raw_path.unlink()
    config = f'''[sdl]
fullscreen=false
[cpu]
core=normal
cycles=fixed 3000
[autoexec]
mount c "{work}"
c:
debug ENCODE.COM < TRACE.IN > TRACE.TXT
exit
'''
    config_path = work / 'trace.conf'
    config_path.write_bytes(config.replace('\n', '\r\n').encode('ascii'))
    startup = None
    if sys.platform == 'win32':
        startup = subprocess.STARTUPINFO()
        startup.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startup.wShowWindow = subprocess.SW_HIDE
    completed = subprocess.run(
        [str(dosbox), '-noconsole', '-conf', str(config_path)],
        cwd=work,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        timeout=timeout,
        startupinfo=startup,
    )
    require(completed.returncode == 0, f'DOSBox-X exited with {completed.returncode}.')
    return raw_path.read_bytes()


def validate(raw: bytes, empty: bool) -> dict:
    text = raw.decode('ascii').replace('\r\n', '\n')
    states = snapshots(text)
    memory = dumps(text)
    require(states, 'DEBUG did not capture any register state.')
    require('Program terminated normally (0000)' in text, 'Target did not exit normally.')
    require('error' not in text.lower(), 'DEBUG reported an error.')
    require('-e 1cc ' in text and 'IP 0100  :117' in text, 'Controlled input setup was not recorded.')
    for state in states:
        require(state['DS'] == state['CS'], 'COM data/code segments differ.')
    at = lambda ip: next((state for state in states if state['IP'] == ip), None)
    finish = at('0128')
    require(finish is not None, 'Missing loop-exit breakpoint.')
    require(finish['CX'] == '0000', 'Loop did not consume the input count.')
    if empty:
        require(finish['BX'] == '01CE', 'Empty-input branch advanced the buffer pointer.')
        require(memory == ['41 00 0D 00 00 00'], 'Empty input buffer was changed.')
        require('Encoded: \n' in text, 'Expected an empty encoded result.')
        return {'name': 'empty', 'passed': True, 'loop_exit': finish, 'buffer': memory[0]}
    before, after = at('0122'), at('0125')
    require(before is not None and after is not None, 'Missing before/after XOR snapshots.')
    require(before['BX'] == after['BX'] == '01CE', 'XOR step changed the data pointer.')
    require(before['CX'] == after['CX'] == '0003', 'XOR step changed the loop count.')
    require('80372A' in before['instruction'], 'Stopped on an unexpected instruction.')
    require('DS:01CE=41' in before['instruction'], 'XOR operand was not the original A byte.')
    require(memory == ['41 03 41 42 43 0D', '41 03 6B 42 43 0D', '41 03 6B 68 69 0D'],
            'Captured memory does not show the expected live transitions.')
    require(finish['BX'] == '01D1', 'Completed loop pointer is incorrect.')
    require('Encoded: 6B 68 69\n' in text, 'Formatted output is incorrect.')
    return {'name': 'ABC', 'passed': True, 'before_xor': before, 'after_xor': after,
            'loop_exit': finish, 'buffers': memory}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dosbox', type=Path, required=True)
    parser.add_argument('--timeout', type=float, default=20)
    args = parser.parse_args()
    require(args.timeout > 0, 'Timeout must be positive.')
    dosbox = args.dosbox.resolve(strict=True)
    reference = ROOT / 'target/ENCODE.COM'
    digest = hashlib.sha256(reference.read_bytes()).hexdigest()
    require(digest == FIXTURE_SHA256,
            'This trace is specific to training fixture v1. Review the new binary and addresses first.')
    metadata = json.loads((ROOT / 'target/metadata.json').read_text(encoding='utf-8'))
    require(metadata['sha256'] == digest, 'Target metadata does not match the executable.')
    captures = []
    for empty in (False, True):
        raw = capture(dosbox, reference, empty, args.timeout)
        checked = validate(raw, empty)
        checked['raw_sha256'] = hashlib.sha256(raw).hexdigest()
        captures.append((raw, checked))
        print(f"PASS: real DOS DEBUG trace, {checked['name']}", flush=True)
    directory = ROOT / 'analysis/traces'
    directory.mkdir(parents=True, exist_ok=True)
    for raw, checked in captures:
        filename = 'debugger-abc.txt' if checked['name'] == 'ABC' else 'debugger-empty.txt'
        (directory / filename).write_bytes(raw)
        checked['raw_file'] = filename
    report = {
        'captured_at_utc': datetime.now(timezone.utc).isoformat(),
        'reference_sha256': digest,
        'backend': 'DOSBox-X bundled DOS DEBUG; real executable loaded and stepped',
        'input_setup': 'DEBUG seeds DS:01CC and sets IP=0117, immediately after the DOS input call. '
                       'The keyboard-read call and startup printing are skipped in this controlled trace.',
        'scope': 'Runtime XOR, loop count, empty-input branch, formatting, and normal exit. '
                 'Interactive keyboard entry is captured separately in turbo-session.json and screenshots.',
        'cases': [checked for raw, checked in captures],
    }
    (directory / 'debugger-results.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    markdown = f'''# Executed DOS debugger traces

**2/2 cases passed** using the real reference executable in DOSBox-X's bundled DOS DEBUG.

Reference SHA-256: `{digest}`

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
'''
    (directory / 'debugger-results.md').write_text(markdown, encoding='utf-8')
    print('Saved checked transcripts and evidence in analysis/traces/.')
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (OSError, ValueError, KeyError, subprocess.SubprocessError) as error:
        raise SystemExit(f'Debugger trace failed: {error}')
