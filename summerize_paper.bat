@echo off
REM Safe batch to run the summarizer from the `data\input` folder.
REM It changes to the repository root, sets variables using `set`, and forwards them to Python.

REM Change to this script's directory
cd "%~dp0"

set "INPUT_DIR=C:\Users\username\Desktop\summerize_paper"
set "PROMPT_PATH=C:\Users\username\Desktop\summerize_paper\assets\prompt.md"
set "MODEL_NAME=gemini-2.5-flash"
set "MAX_LOOP=5"
set "FONT_SIZE=30"

set "PYTHONPATH=C:\Users\username\autosum-pdf-exporter-llm\main.py"

set "CHOICE="
set /p CHOICE=Enter 'l' to list models, or press Enter to run summarizer: 

if /I "%CHOICE%"=="l" (
	python "%PYTHONPATH%" --list-models
) else (
	python "%PYTHONPATH%" --input-dir "%INPUT_DIR%" --prompt-path "%PROMPT_PATH%" --model-name "%MODEL_NAME%" --max-loop "%MAX_LOOP%" --font-size "%FONT_SIZE%"
)

pause