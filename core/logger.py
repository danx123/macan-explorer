# file: core/logger.py

import logging
import os
from datetime import datetime

class ShrineLogger:
    def __init__(self, log_dir="logs"):
        self.log_dir = log_dir
        self.log_file = os.path.join(log_dir, "shrine_ritual_log.txt")

        # 🪶 Ensure log directory exists (ini tetap perlu karena log_file spesifik)
        os.makedirs(log_dir, exist_ok=True)

        # --- PERBAIKAN: Hapus logging.basicConfig dari sini ---
        # Root logger akan dikonfigurasi di main.py.
        # Di sini, kita hanya mendapatkan logger spesifik untuk kelas ini.
        self.logger = logging.getLogger(__name__) 
        # Anda juga bisa memberi nama spesifik, misalnya: self.logger = logging.getLogger("ShrineLogger")
        # Level logging untuk logger ini akan mewarisi dari konfigurasi root,
        # atau bisa diatur secara spesifik jika dibutuhkan (misal: self.logger.setLevel(logging.INFO))
        # --------------------------------------------------------

    def log(self, message, level="info", tag=None):
        full_message = f"[{tag}] {message}" if tag else message
        if level == "info":
            self.logger.info(full_message)
        elif level == "warning":
            self.logger.warning(full_message)
        elif level == "error":
            self.logger.error(full_message)
        elif level == "critical":
            self.logger.critical(full_message)
        else:
            self.logger.debug(full_message) # Default ke debug untuk level tidak dikenal

    def ritual(self, emoji, ritual_type, target):
        self.log(f"{emoji} Ritual {ritual_type} on {target}", tag="RITUAL")

    def stealth(self, message):
        self.logger.info(f"👻 Stealth mode: {message}")