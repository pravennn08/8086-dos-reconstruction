@echo off
rem Run inside a DOS emulator from the project root with TASM on PATH.
if not exist build\nul mkdir build
if exist build\BUILD.OK del build\BUILD.OK
if exist build\REBUILD.COM del build\REBUILD.COM
if exist build\REBUILD.OBJ del build\REBUILD.OBJ
tasm /m2 /l src\rebuild.asm,build\REBUILD.OBJ,build\REBUILD.LST
if errorlevel 1 goto failed
tlink /t build\REBUILD.OBJ,build\REBUILD.COM
if errorlevel 1 goto failed
if not exist build\REBUILD.COM goto failed
echo Build successful.>build\BUILD.OK
echo Built build\REBUILD.COM
goto done
:failed
echo Build failed. Review assembler or linker diagnostics above.
:done
