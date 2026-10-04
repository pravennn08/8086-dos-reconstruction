.8086
.model tiny
.code
    org    100h

    MAX_INPUT equ 64
    XOR_KEY equ 2Ah

start:
    push   cs
    pop    ds
    mov    dx, offset title_text
    mov    ah, 09h
    int    21h
    mov    dx, offset prompt_text
    mov    ah, 09h
    int    21h
    ; Buffer capacity includes space for the terminating carriage return.
    mov    dx, offset input_buffer
    mov    ah, 0Ah
    int    21h
    mov    dx, offset result_text
    mov    ah, 09h
    int    21h
    xor    cx, cx
    mov    cl, byte ptr [input_buffer + 1]
    mov    si, offset input_buffer + 2
    jcxz   finish
encode_next:
    mov    al, byte ptr [si]
    xor    al, XOR_KEY
    call   print_hex_byte
    inc    si
    dec    cx
    jz     finish
    mov    dl, ' '
    mov    ah, 02h
    int    21h
    jmp    encode_next
finish:
    mov    dx, offset newline_text
    mov    ah, 09h
    int    21h
    mov    ax, 4C00h
    int    21h

    ; AL = byte to print. Preserve caller registers, especially the loop count.
    print_hex_byte proc near
        push ax
        push bx
        push cx
        push dx
        mov  bl, al
        ; Original 8086 supports shifts by one or CL, not immediate four.
        shr  al, 1
        shr  al, 1
        shr  al, 1
        shr  al, 1
        call print_nibble
        mov  al, bl
        and  al, 0Fh
        call print_nibble
        pop  dx
        pop  cx
        pop  bx
        pop  ax
        ret
    print_hex_byte endp

    ; AL = 0..15. Convert to an ASCII hexadecimal digit arithmetically.
    print_nibble proc near
        cmp al, 9
        jbe decimal_digit
        add al, 7
decimal_digit:
        add al, '0'
        mov dl, al
        mov ah, 02h
        int 21h
        ret
    print_nibble endp

    title_text db '8086 DOS Encoder', 13, 10, '$'
    prompt_text db 'Enter text (max 64 characters): $'
    result_text db 13, 10, 'Encoded: $'
    newline_text db 13, 10, '$'
    input_buffer db MAX_INPUT + 1, 0, MAX_INPUT + 1 dup (0)
    end start
