import shutil
import subprocess
import threading
import queue
import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox


class PowerShellUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("PowerShell UI")

        # Queue for thread-safe communication
        self.output_queue: queue.Queue[str] = queue.Queue()
        self.ps_process: subprocess.Popen | None = None

        # UI Elements
        toolbar = tk.Frame(root)
        toolbar.pack(fill=tk.X)

        self.start_button = tk.Button(toolbar, text="Start PowerShell", command=self.start_ps)
        self.start_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.dir_button = tk.Button(toolbar, text="Select Directory", command=self.select_directory, state=tk.DISABLED)
        self.dir_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.command_entry = tk.Entry(root)
        self.command_entry.pack(fill=tk.X, padx=5, pady=5)
        self.command_entry.bind("<Return>", self.send_command)

        self.send_button = tk.Button(root, text="Send", command=self.send_command, state=tk.DISABLED)
        self.send_button.pack(padx=5, pady=5)

        self.output = scrolledtext.ScrolledText(root, state=tk.DISABLED, height=20)
        self.output.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Periodically poll queue for output updates
        self.root.after(100, self.poll_queue)

        # Clean up on close
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def start_ps(self) -> None:
        if self.ps_process:
            return
        exe = self._find_powershell()
        if not exe:
            messagebox.showerror("Error", "PowerShell executable not found.")
            return
        self.ps_process = subprocess.Popen(
            [exe, "-NoLogo"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True,
        )
        threading.Thread(target=self._read_output, daemon=True).start()
        self.dir_button.config(state=tk.NORMAL)
        self.send_button.config(state=tk.NORMAL)

    def _find_powershell(self) -> str | None:
        # Try common executable names
        for name in ("powershell", "pwsh"):
            path = shutil.which(name)
            if path:
                return path
        return None

    def select_directory(self) -> None:
        if not self.ps_process:
            return
        directory = filedialog.askdirectory()
        if directory:
            self._send(f'Set-Location "{directory}"')

    def send_command(self, event=None) -> None:
        if not self.ps_process:
            return
        cmd = self.command_entry.get()
        self.command_entry.delete(0, tk.END)
        if cmd:
            self._send(cmd)

    def _send(self, cmd: str) -> None:
        assert self.ps_process and self.ps_process.stdin
        self.ps_process.stdin.write(cmd + "\n")
        self.ps_process.stdin.flush()

    def _read_output(self) -> None:
        assert self.ps_process and self.ps_process.stdout
        for line in self.ps_process.stdout:
            self.output_queue.put(line)

    def poll_queue(self) -> None:
        while not self.output_queue.empty():
            line = self.output_queue.get_nowait()
            self.output.config(state=tk.NORMAL)
            self.output.insert(tk.END, line)
            self.output.see(tk.END)
            self.output.config(state=tk.DISABLED)
        self.root.after(100, self.poll_queue)

    def on_close(self) -> None:
        if self.ps_process:
            try:
                self.ps_process.terminate()
            except Exception:
                pass
        self.root.destroy()


def main() -> None:
    root = tk.Tk()
    app = PowerShellUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
