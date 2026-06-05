import threading
import ttkbootstrap as tb
from tkinter import filedialog

from scanner import scan_folder
from quarantine_manager import quarantine_file


selected_folder = ""


def create_gui():

    global selected_folder

    app = tb.Window(themename="darkly")

    app.title("YVELTAX Security")
    app.geometry("900x550")
    app.resizable(False, False)

    def choose_folder():

        global selected_folder

        folder = filedialog.askdirectory()

        if folder:

            selected_folder = folder

            results.insert(
                "end",
                f"[+] Selected Folder: {folder}\n"
            )

    def run_scan_thread():

        scan_thread = threading.Thread(
            target=scan_folder,
            args=(
                selected_folder,
                results,
                progress,
                stats_label,
                app,
                quarantine_file
            )
        )

        scan_thread.start()

    title = tb.Label(
        app,
        text="YVELTAX Security",
        font=("Segoe UI", 24, "bold"),
        bootstyle="info"
    )
    title.pack(pady=20)

    folder_button = tb.Button(
        app,
        text="Select Folder",
        bootstyle="primary",
        command=choose_folder,
        width=20
    )
    folder_button.pack(pady=10)

    scan_button = tb.Button(
        app,
        text="Start Scan",
        bootstyle="success",
        command=run_scan_thread,
        width=20
    )
    scan_button.pack(pady=10)

    progress = tb.Progressbar(
        app,
        length=400,
        bootstyle="info-striped",
        maximum=100
    )
    progress.pack(pady=20)

    stats_label = tb.Label(
        app,
        text="Files Scanned: 0 | Threats Found: 0",
        font=("Segoe UI", 10)
    )
    stats_label.pack(pady=5)

    results = tb.Text(
        app,
        height=15,
        width=90,
        font=("Consolas", 10)
    )
    results.pack(pady=10)

    app.mainloop()