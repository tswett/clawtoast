This is Clawtoast's Python code.

To run the tests, do something like this:

    python -m venv .venv
    source .venv/bin/activate       # if you're in bash
    .\.venv\Scripts\Activate.ps1    # if you're in PowerShell
    poetry install --no-root
    pytest
