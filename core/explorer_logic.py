# file: core/explorer_logic.py

import os
import shutil
import subprocess
from PyQt6.QtWidgets import QMessageBox

class ExplorerLogic:
    def __init__(self, window):
        self.window = window  # refer ke MainWindow untuk akses path & UI

    # 📄 Copy Ritual
    def copy_files(self, source_files, dest_folder):
        total = len(source_files)
        self.window.overlay.show_overlay(self.window.rect().center())
        self.window.progress.start(total)

        for i, file in enumerate(source_files):
            try:
                dest = os.path.join(dest_folder, os.path.basename(file))
                shutil.copy2(file, dest)
            except Exception as e:
                self.window.status.showMessage(f"❌ Gagal salin: {file}")
                QMessageBox.warning(self.window, "Copy Error", str(e))
            self.window.progress.update(i + 1)
            self.window.overlay.update_progress(i + 1, total)

        self.window.overlay.hide_overlay()
        self.window.status.showMessage("✅ Ritual salin selesai")

    # 📥 Paste Ritual (Mocked Clipboard Logic)
    def paste_files(self, clipboard_files, current_folder):
        self.copy_files(clipboard_files, current_folder)

    # 🔒 Seal Ritual (Delete)
    def seal_file(self, file_path):
        try:
            os.remove(file_path)
            self.window.status.showMessage(f"🔒 File disegel: {file_path}")
        except PermissionError:
            QMessageBox.warning(self.window, "Seal Error", f"File sedang digunakan: {file_path}")
        except Exception as e:
            QMessageBox.critical(self.window, "Seal Failed", str(e))

    # 🧿 Invoke Ritual (Open)
    def invoke_file(self, file_path):
        try:
            subprocess.Popen([file_path], shell=True)
            self.window.status.showMessage(f"🧿 Invoke: {file_path}")
        except Exception as e:
            QMessageBox.critical(self.window, "Invoke Failed", str(e))