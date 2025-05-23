@echo off
echo Running astro-annotator container...

docker run --rm -v "%cd%":/data -w /data astro-annotator

if %ERRORLEVEL% neq 0 (
    echo Error: The container execution failed.
    exit /b %ERRORLEVEL%
)

echo Annotation process completed.
