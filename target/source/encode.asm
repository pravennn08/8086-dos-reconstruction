; Reference training fixture; source is disclosed for reproducibility.
; SPDX-License-Identifier: MIT (see target/LICENSE.md).
; This version transforms the input buffer in place, then formats through
; a lookup table using XLAT. It is not an unknown third-party binary.
.8086
.model tiny
.code
org 100h

MAX_INPUT equ 64

start:
    push cs
    pop ds
    mov dx, offset title_text
    mov ah, 09h
    int 21h
    mov dx, offset prompt_text
    mov ah, 09h
    int 21h
    mov dx, offset input_buffer
    mov ah, 0Ah
    int 21h
    xor cx, cx
    mov cl, byte ptr [input_buffer + 1]
    mov bx, offset input_buffer + 2
    jcxz print_result
transform_next:
    xor byte ptr [bx], 2Ah
    inc bx
    loop transform_next
print_result:
    mov dx, offset result_text
    mov ah, 09h
    int 21h
    xor cx, cx
    mov cl, byte ptr [input_buffer + 1]
    mov si, offset input_buffer + 2
    jcxz finish
print_next:
    mov al, byte ptr [si]
    call print_hex_byte
    inc si
    dec cx
    jz finish
    mov dl, ' '
    mov ah, 02h
    int 21h
    jmp print_next
finish:
    mov dx, offset newline_text
    mov ah, 09h
    int 21h
    mov ax, 4C00h
    int 21h

print_hex_byte proc near
    push ax
    push bx
    push cx
    push dx
    mov bx, offset hex_digits
    push ax
    mov cl, 4
    shr al, cl
    xlat
    mov dl, al
    mov ah, 02h
    int 21h
    pop ax
    and al, 0Fh
    xlat
    mov dl, al
    mov ah, 02h
    int 21h
    pop dx
    pop cx
    pop bx
    pop ax
    ret
print_hex_byte endp

title_text db '8086 DOS Encoder', 13, 10, '$'
prompt_text db 'Enter text (max 64 characters): $'
result_text db 13, 10, 'Encoded: $'
newline_text db 13, 10, '$'
hex_digits db '0123456789ABCDEF'
input_buffer db MAX_INPUT + 1, 0, MAX_INPUT + 1 dup (0)
end start
