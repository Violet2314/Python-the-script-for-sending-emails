@echo off
:loop
ping -n 1 www.bilibili.com >nul
if %errorlevel%==0 (
    echo Network is up.
    python "./send.py"
    exit /b
) else (
    echo Network is down, checking again in 1 minute...
    timeout /t 60
    goto loop
)