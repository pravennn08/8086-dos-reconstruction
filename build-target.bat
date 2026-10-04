@echo off
rem Explicitly regenerate the disclosed training target inside a DOS emulator.
if not exist build\nul mkdir build
if exist build\ENCODE.COM del build\ENCODE.COM
if exist build\ENCODE.OBJ del build\ENCODE.OBJ
tasm /m2 /l target\source\encode.asm,build\ENCODE.OBJ,build\ENCODE.LST
if errorlevel 1 goto failed
tlink /t build\ENCODE.OBJ,build\ENCODE.COM
if errorlevel 1 goto failed
if not exist build\ENCODE.COM goto failed
copy build\ENCODE.COM target\ENCODE.COM >nul
echo Updated target\ENCODE.COM. Record its identity before comparing.
goto done
:failed
echo Training target build failed. Existing target was not replaced.
:done
