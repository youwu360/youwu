#$ErrorActionPreference = "Stop"

cd $PSScriptRoot
if (Test-Path items.json)
{
    rm items.json
}

Expand-Archive -Path .\items.json.zip -DestinationPath $PSScriptRoot

if (Test-Path db.sqlite3)
{
    rm db.sqlite3
}
if (Test-Path site_youwu/migrations/*_initial.py)
{
    rm site_youwu/migrations/*_initial.py
}

python.exe manage.py makemigrations
python.exe manage.py migrate
python.exe load_nvshens_data.py
