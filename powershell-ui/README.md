# PowerShell UI

A simple cross-platform Tkinter application that opens a PowerShell session and allows interactive command execution.

## Features

- Choose a local directory and send `Set-Location` to PowerShell.
- Open a PowerShell subprocess and interact with it through a GUI.
- Send arbitrary commands and see the output streamed in the window.

## Usage

```bash
python main.py
```

On Windows the app looks for `powershell`. On other systems it attempts to use `pwsh`.
