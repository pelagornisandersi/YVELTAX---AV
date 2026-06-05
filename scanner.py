import sys
import os
import hashlib
from virustotal import check_hash_virustotal

def resource_path(relative_path):

    try:
        base_path = sys._MEIPASS

    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)



suspicious_extensions = [
    ".exe",
    ".bat",
    ".vbs",
    ".ps1",
    ".scr"
]


def calculate_hash(file_path):

    sha256 = hashlib.sha256()

    try:

        with open(file_path, "rb") as file:

            while chunk := file.read(4096):
                sha256.update(chunk)

        return sha256.hexdigest()

    except:
        return None


def load_signatures():

    signatures = set()

    try:

        with open(signature_path, "r") as file:

            for line in file:
                signatures.add(line.strip())

    except:
        pass

    return signatures

def scan_folder(
    selected_folder,
    results,
    progress,
    stats_label,
    app,
    quarantine_file
):

    if not selected_folder:
        results.insert("end", "[!] No folder selected\n")
        return

    results.delete("1.0", "end")

    results.insert("end", "\n[+] Starting Scan...\n\n")

    signatures = load_signatures()

    total_files = 0

    for root, dirs, files in os.walk(selected_folder):
        total_files += len(files)

    file_count = 0
    threat_count = 0

    for root, dirs, files in os.walk(selected_folder):

        for file in files:

            file_path = os.path.join(root, file)

            file_count += 1

            file_hash = calculate_hash(file_path)
            vt_result = check_hash_virustotal(file_hash)

            _, extension = os.path.splitext(file)

            if file_hash in signatures:

                threat_count += 1

                results.insert(
                    "end",
                    f"[MALWARE DETECTED] {file_path}\n"
                )

                quarantine_file(file_path, results)

            elif extension.lower() in suspicious_extensions:

                results.insert(
                    "end",
                    f"[WARNING] Suspicious File: {file_path}\n"
                )

            else:

                if vt_result:

                    malicious, suspicious = vt_result

                    if malicious > 0:

                        results.insert(
                            "end",
                            f"[VT DETECTED: {malicious}] {file_path}\n"
                        )

                    else:

                        results.insert(
                            "end",
                            f"[SAFE] {file_path}\n"
                        )

                else:

                    results.insert(
                        "end",
                        f"[SAFE] {file_path}\n"
                    )

            progress["value"] = (
                file_count / total_files
            ) * 100

            stats_label.config(
                text=f"Files Scanned: {file_count} | Threats Found: {threat_count}"
            )

            results.see("end")

            app.update_idletasks()

    progress["value"] = 100

    results.insert(
        "end",
        f"\n[+] Scan Complete. {file_count} files scanned.\n"
    )