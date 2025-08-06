# PowerShell UI

A tiny Tkinter helper that launches a PowerShell session in a directory you choose.

## Features

- Pick a local directory using a file dialog.
- Open PowerShell in that directory and keep the shell open for further commands.


## Usage

```bash
python main.py
```

On Windows the app looks for `powershell`. On other systems it attempts to use `pwsh`.
