@echo off
set ENV=%1
set CONFIG_FILE=%2

echo Deploying %CONFIG_FILE% to %ENV%...

mkdir "%TEMP%\myapp"
copy %CONFIG_FILE% "%TEMP%\myapp\config_%ENV%.json"

echo Deployed to %TEMP%\myapp\config_%ENV%.json
