# Guided encoder algorithm

Target: ENCODE.COM, identified in target/provenance.md and metadata.json.
This is a guided exercise with disclosed source. The annotations below were
checked against objdump's decode of the compiled binary.

## Evidence

| Behavior | Binary evidence | Execution evidence |
| --- | --- | --- |
| Buffered DOS input | 0113h: MOV AH,0Ah; 0115h: INT 21h; DS:DX points to 01CCh | E-001, E-010, E-012, E-013 |
| Input length | 0119h reads byte at DS:01CDh into CL | E-001 and boundary cases |
| Empty input bypass | 0120h: JCXZ 0128h | E-001 |
| In-place XOR 2Ah | 0122h: bytes 80 37 2A, XOR BYTE PTR [BX],2Ah | E-002: ABC -> 6B 68 69 |
| Visit each input byte | 0125h INC BX; 0126h LOOP 0122h | E-003 and maximum-length cases |
| Hex formatting | 015Bh loads table at 01BCh; XLAT at 0163h/016Dh | Printable ASCII coverage E-014/E-015 |
| Successful termination | 0152h MOV AX,4C00h; INT 21h | All recorded exit codes zero |

Code occupies 0100h through 0178h in the current fixture. The title, prompts,
hex table, and input buffer begin at 0179h. Raw linear disassembly of data
can produce misleading instructions, including opcodes from newer CPUs.

## Specification

```text
print title and input prompt
read one DOS-edited line, accepting at most 64 characters
print a newline and "Encoded: "
for each accepted byte:
    encoded = byte XOR 0x2A
    print its high and low hexadecimal digits in uppercase
    print a space only if another byte follows
print CRLF
exit with code 0
```

The input buffer's maximum byte is 65 because DOS reserves one slot for CR.
The count excludes CR; transformation starts two bytes after the buffer base.
Dollar signs in user input are handled as data. Only fixed prompts use the
DOS dollar-terminated display-string service.

## Reconstruction decisions

The reference changes the input buffer and uses XLAT with a hexadecimal
lookup table. The reconstruction reads the unchanged buffer, XORs AL with
2Ah, and converts each nibble using arithmetic. Both guard against a zero
length before entering the loop and preserve the outer loop count in the
hex-print routine.

Matching captured outputs establish agreement for the tested cases. Interactive
editing, Ctrl-C, other code pages, and high-bit input remain unverified.
Runtime register/memory trace claims are deferred until a debugger session.
