# Prerequisites
1. Python:
    - Minimum version: 3.13
    - Installation: https://www.python.org/
2. Poetry
    - Minimum version: 2.0.0
    - Installation: https://python-poetry.org/docs/

# Build
Set up environment:
```
poetry install
poetry env activate
```

If you are building for the first time:
```
python3 manage.py migrate
python3 manage.py seeding
```
Currently, it is expected that you have SECRET_KEY environment variable. If you don't have it, a randomly generated key will be used. The corresponding warning will be printed and you will be able to set the generated key to the SECRET_KEY environment variable manually

# Run
With activated environment:
```
python3 manage.py runserver
```

## Troubleshootuing
- `python3 manage.py runserver` failed with error `You don't have permission to access that port` on Windows 10
In my case, the problem was related to the fact that I was using VPN, Hyper-V, and VirtualBox. Run this command in powershell to check if any VPN adapters are in the Up state:
```
Get-NetAdapter | Select-Object Name, InterfaceDescription, Status
```
If you see any of these, you need to disable them. You may need to restart your computer
