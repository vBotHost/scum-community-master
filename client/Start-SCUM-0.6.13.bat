@echo off
rem Start the SCUM 0.6.13 client with the community master server list.
rem Put this file in the 0.6.13 client folder (the one holding SCUM_Launcher.exe) and start the game
rem with it. It goes through the EasyAntiCheat launcher, as the game requires.
rem
rem -NotInstalled keeps this client's settings and saves in SCUM\Saved inside this folder, so they
rem never mix with another SCUM version installed on the same PC.
setlocal
set "MASTER=51.68.190.110"
set "CFG=%~dp0SCUM\Saved\Config\WindowsNoEditor"
set "INI=%CFG%\ServerSettings.ini"
if not exist "%CFG%" mkdir "%CFG%"
rem Write the master address on every start: drop the old section lines, then add them fresh.
if exist "%INI%" (
    findstr /v /b /i /c:"[SCUM.MasterServer]" /c:"Endpoint=" /c:"BanListEndpoint=" "%INI%" > "%INI%.tmp"
    move /y "%INI%.tmp" "%INI%" >nul
)
>>"%INI%" echo [SCUM.MasterServer]
>>"%INI%" echo Endpoint=%MASTER%:31337
>>"%INI%" echo BanListEndpoint=%MASTER%:31330
cd /d "%~dp0"
start "" SCUM_Launcher.exe -NotInstalled %*
