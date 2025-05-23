@echo off
echo Building Docker image: astro-annotator...
docker build -f docker\Dockerfile -t astro-annotator .
if %ERRORLEVEL% neq 0 (
    echo Build failed!
    exit /b %ERRORLEVEL%
)
echo Build completed successfully.
