@echo off
rem sync_from_github.bat - copy dk3s_cad and the nanocad-lisp skill from GitHub into THIS folder, byte-exact.
rem Requires Git for Windows. Double-click from the target folder (e.g. G:\My Drive\AutoCAD).
setlocal
cd /d "%~dp0"
set "REPO=https://github.com/ldovg777-art/46clod.git"
set "BRANCH=claude/nanocat-lisp-drawings-mtztge"
set "TMPDIR=%TEMP%\dk3s_sync_%RANDOM%"
echo Cloning %REPO% (%BRANCH%) ...
git clone -q --depth 1 --filter=blob:none --sparse -b %BRANCH% "%REPO%" "%TMPDIR%" 2>nul
if errorlevel 1 (
  echo Branch %BRANCH% not found, trying main ...
  git clone -q --depth 1 --filter=blob:none --sparse -b main "%REPO%" "%TMPDIR%" || (echo git clone failed & pause & exit /b 1)
)
pushd "%TMPDIR%"
git sparse-checkout set dk3s_cad .claude/skills/nanocad-lisp || (popd & echo sparse-checkout failed & pause & exit /b 1)
popd
robocopy "%TMPDIR%\dk3s_cad" "%~dp0dk3s_cad" /E /NFL /NDL /NJH /NJS >nul
robocopy "%TMPDIR%\.claude\skills\nanocad-lisp" "%~dp0.claude\skills\nanocad-lisp" /E /NFL /NDL /NJH /NJS >nul
rmdir /s /q "%TMPDIR%"
echo.
echo Done. Updated: %~dp0dk3s_cad  and  %~dp0.claude\skills\nanocad-lisp
echo Next: open dk3s_cad\dk3s_drawing.dxf in nanoCAD, or APPLOAD dk3s_cad\dk3s_drawing.lsp and run DK3S.
pause
