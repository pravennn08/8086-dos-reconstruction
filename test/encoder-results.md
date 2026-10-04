# Guided encoder verification

**31/31 cases passed.**

Both DOS executables were actually run. Output bytes, exit codes, and stderr were compared.
The encoded result was also checked against a separate Python specification.

Reference SHA-256: `2028290647ca744d2aea1ee810f812f5e9b91cbb8512f2c10ab7e108b28fa1af`

Reconstruction SHA-256: `d4c456d5f44bda039543da51d33303b66f69d0693082d1de542a081f0d28dcc4`

| ID | Case | Input length | Accepted length | Result |
| --- | --- | ---: | ---: | --- |
| E-001 | empty | 0 | 0 | PASS |
| E-002 | ABC | 3 | 3 | PASS |
| E-003 | repeated | 4 | 4 | PASS |
| E-004 | uppercase | 5 | 5 | PASS |
| E-005 | lowercase | 5 | 5 | PASS |
| E-006 | single-space | 1 | 1 | PASS |
| E-007 | spaces | 5 | 5 | PASS |
| E-008 | punctuation-dollar | 5 | 5 | PASS |
| E-009 | digits | 10 | 10 | PASS |
| E-010 | maximum-64 | 64 | 64 | PASS |
| E-011 | maximum-mixed | 64 | 64 | PASS |
| E-012 | over-limit-65 | 65 | 64 | PASS |
| E-013 | over-limit-128 | 128 | 64 | PASS |
| E-014 | printable-ASCII-1 | 64 | 64 | PASS |
| E-015 | printable-ASCII-2 | 31 | 31 | PASS |
| E-016 | seeded-01 | 1 | 1 | PASS |
| E-017 | seeded-02 | 33 | 33 | PASS |
| E-018 | seeded-03 | 44 | 44 | PASS |
| E-019 | seeded-04 | 53 | 53 | PASS |
| E-020 | seeded-05 | 34 | 34 | PASS |
| E-021 | seeded-06 | 2 | 2 | PASS |
| E-022 | seeded-07 | 56 | 56 | PASS |
| E-023 | seeded-08 | 14 | 14 | PASS |
| E-024 | seeded-09 | 12 | 12 | PASS |
| E-025 | seeded-10 | 48 | 48 | PASS |
| E-026 | seeded-11 | 4 | 4 | PASS |
| E-027 | seeded-12 | 12 | 12 | PASS |
| E-028 | seeded-13 | 1 | 1 | PASS |
| E-029 | seeded-14 | 25 | 25 | PASS |
| E-030 | seeded-15 | 33 | 33 | PASS |
| E-031 | seeded-16 | 51 | 51 | PASS |

Raw inputs and captured outputs: [encoder-results.json](encoder-results.json).

The original and reconstruction have different machine code. This comparison establishes
agreement for the recorded cases, not equivalence for every DOS environment or input.

GUI Turbo Assembler execution has not been automated by this test. Console editing keys,
Ctrl-C handling, other code pages, and high-bit/binary input are outside this test set.
