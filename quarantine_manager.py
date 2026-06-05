import os
import shutil


def quarantine_file(file_path, results):

    quarantine_folder = "quarantine"

    os.makedirs(quarantine_folder, exist_ok=True)

    try:

        filename = os.path.basename(file_path)

        destination = os.path.join(
            quarantine_folder,
            filename + ".quarantined"
        )

        shutil.move(file_path, destination)

        results.insert(
            "end",
            f"[QUARANTINED] {filename}\n"
        )

    except Exception as e:

        results.insert(
            "end",
            f"[ERROR] Could not quarantine file: {e}\n"
        )