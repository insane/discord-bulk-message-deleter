@echo off
title Discord Purge Tool

:choice_prompt
cls
echo Please choose an option:
echo [1] - cl deletion
echo [2] - silent deletion
echo [3] - reverse silent deletion
echo.

set /p choice="Enter your choice (1, 2, or 3): "

if "%choice%"=="1" (
    cls
    py -3.7 modules/cl.py
    goto end
) else if "%choice%"=="2" (
    cls
    py -3.7 modules/silent.py
    goto end
) else if "%choice%"=="3" (
    cls
    py -3.7 modules/rsilent.py
    goto end
) else (
    echo Invalid choice. Please enter 1, 2, or 3.
    timeout /t 2 > nul
    goto choice_prompt
)

:end
