This project is going to be a NAND gate, similar to E003-tdd-nand, but I'm going
to try to develop it in a more disciplined way, so to speak. In particular, it's
going to use Python library code that lives in a different directory in the
repository.

To try to run the Python test script, do something like this:

    python -m venv .venv
    source .venv/bin/activate       # if you're in bash
    .\.venv\Scripts\Activate.ps1    # if you're in PowerShell
    poetry install --no-root
    python test/tests.py
