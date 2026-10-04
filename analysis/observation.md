# Recorded behavioral observations

These observations come from executing the reference ENCODE.COM through
MS-DOS Player with redirected input. Each input ends in CRLF. Full captured
bytes and matching reconstruction runs are in ../test/encoder-results.json.
Source is disclosed: this is a guided lab.

| Experiment | Input | Observed encoded result | Evidence |
| --- | --- | --- | --- |
| O-001 | Empty line | Empty result; process returns 0 | E-001 |
| O-002 | ABC | 6B 68 69 | E-002 |
| O-003 | AAAA | 6B 6B 6B 6B | E-003 |
| O-004 | One space | 0A | E-006 |
| O-005 | Dollar/punctuation | User dollar sign is encoded as 0E | E-008 |
| O-006 | 64 A characters | 64 encoded bytes, each 6B | E-010 |
| O-007 | 65 / 128 A characters | 64 encoded bytes; excess is ignored | E-012/E-013 |
| O-008 | Printable ASCII in two chunks | Every printable byte encoded correctly | E-014/E-015 |

Input is echoed by DOS. This backend captures extra carriage returns around
the Enter key; tests compare raw bytes without hiding those differences.
Output has uppercase hexadecimal, one space between bytes, CRLF termination,
and no trailing separator.

Behavior alone suggests an independent per-byte transformation. The compiled
instruction at 0122h confirms XOR with the constant 2Ah for this fixture.
Keyboard-editing and live memory/register observations still require a
separate GUI debugger session.
