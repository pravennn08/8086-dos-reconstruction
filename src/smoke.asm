; Phase 1: toolchain smoke program, not a recovered target implementation.
; Assemble with TASM; link with TLINK /t to create a DOS .COM program.

.8086
.model tiny
.code
org 100h

start:
    ; DOS loads the COM image at CS:0100h. Use CS for our data as well.
    push cs
    pop ds

    ; DOS function 09h prints the dollar-terminated banner at DS:DX.
    mov dx, offset banner
    mov ah, 09h
    int 21h

    ; DOS function 4Ch terminates with process return code zero.
    mov ax, 4C00h
    int 21h

banner db '8086 DOS Reconstruction', 13, 10
       db 'Toolchain ready.', 13, 10, '$'

end start
