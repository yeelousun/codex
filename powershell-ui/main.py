
"""Launch PowerShell in a selected directory."""

from __future__ import annotations

import os
import shutil
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox


def _find_powershell() -> str | None:
    """Return the path to a PowerShell executable if one is available."""
    for name in ("powershell", "pwsh"):
        path = shutil.which(name)
        if path:
            return path
    return None


def open_powershell() -> None:
    """Prompt for a directory and open PowerShell there."""
    exe = _find_powershell()
    if not exe:
        messagebox.showerror("Error", "PowerShell executable not found.")
        return

    directory = filedialog.askdirectory()
    if not directory:
        return

    cmd = f"Set-Location '{directory}'"
    kwargs: dict[str, object] = {}
    if os.name == "nt":
        # On Windows launch in a new console window
        kwargs["creationflags"] = subprocess.CREATE_NEW_CONSOLE  # type: ignore[attr-defined]

    subprocess.Popen([exe, "-NoExit", "-Command", cmd], **kwargs)



def main() -> None:
    root = tk.Tk()
    root.title("PowerShell Launcher")
    tk.Button(root, text="Open PowerShell", command=open_powershell).pack(
        padx=10, pady=10
    )

    root.mainloop()


if __name__ == "__main__":
    main()