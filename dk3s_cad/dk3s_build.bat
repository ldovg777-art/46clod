@echo off
rem dk3s_build.bat - build DK-3S drawing in nanoCAD without GUI (see README.md)
cd /d "%~dp0"
set NCAD=
for /d %%D in ("%ProgramFiles%\Nanosoft\*") do if exist "%%D\nCad.exe" set "NCAD=%%D\nCad.exe"
if "%NCAD%"=="" (
  echo nCad.exe not found under "%ProgramFiles%\Nanosoft". Set NCAD manually, e.g.:
  echo   set "NCAD=C:\Program Files\Nanosoft\nanoCAD x64 25.0\nCad.exe"
  exit /b 1
)
echo Using %NCAD%
"%NCAD%" -invisible -s "%~dp0dk3s_build.scr"
if exist dk3s_drawing.dwg (echo OK: dk3s_drawing.dwg created) else (echo WARNING: dk3s_drawing.dwg not created - run DK3S interactively, see README.md)
