; Guided analysis of target/ENCODE.COM, not a build input.
; Source is disclosed; names below are descriptive labels assigned for clarity.
; SHA-256: 2028290647ca744d2aea1ee810f812f5e9b91cbb8512f2c10ab7e108b28fa1af
; Decoded by GNU objdump in i8086/Intel mode, origin 0100h.
; See traces/target-disassembly.txt for the raw code-region decode.
;
; Address  Bytes         Instruction                 Interpretation
; 0110h    BA CC 01      mov dx,01CCh                 Input buffer at DS:01CCh
; 0113h    B4 0A         mov ah,0Ah                   DOS buffered line input
; 0115h    CD 21         int 21h
; 0117h    33 C9         xor cx,cx                    Clear full loop counter
; 0119h    8A 0E CD 01   mov cl,byte ptr ds:[01CDh]   Returned character count
; 011Dh    BB CE 01      mov bx,01CEh                 First input character
; 0120h    E3 06         jcxz print_result            Skip XOR loop if empty
;
; transform_next:
; 0122h    80 37 2A      xor byte ptr [bx],2Ah        Transform one byte in place
; 0125h    43            inc bx                       Advance to next character
; 0126h    E2 FA         loop transform_next          Decrement CX and repeat
;
; print_result starts at 0128h; hex routine starts at 0157h.
; The hex table is at 01BCh; XLAT instructions are at 0163h and 016Dh.
; Termination: 0152h B8 00 4C (mov ax,4C00h), 0155h CD 21 (int 21h).
; Code ends at 0178h. Starting at 0179h, bytes represent data, not instructions.
;
; Illustrative transition, derived from instruction semantics:
; 41h XOR 2Ah = 6Bh ('A' becomes encoded byte 6Bh).
; A live register/memory transition has not yet been captured with a debugger.
