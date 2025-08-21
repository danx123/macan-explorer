# file: core/error_handler.py

import traceback
import logging
import os 

class ErrorHandler:
    def __init__(self, log_path="logs/error_log.txt"):
        self.log_path = log_path
        
        # Pastikan direktori log ada
        log_dir = os.path.dirname(self.log_path)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True) 

        # --- PERBAIKAN PENTING: logging.basicConfig() DIHAPUS DARI SINI ---
        # Ini akan dikonfigurasi secara global di main.py.
        # Di sini, kita hanya mendapatkan logger spesifik untuk kelas ini.
        self.logger = logging.getLogger(__name__) 
        # Level untuk logger ini diatur di setup_logging() di main.py
        # ----------------------------------------------------------------

    def handle(self, error, context=""):
        error_type = type(error).__name__
        error_msg = str(error)
        trace = traceback.format_exc()

        full_log = f"[⚠️] Shrine Error in {context}\nType: {error_type}\nMessage: {error_msg}\nTrace:\n{trace}\n"

        # Gunakan logger spesifik yang sudah didapatkan
        self.logger.error(full_log) 

        # Optional: tampilkan di konsol untuk pengembangan
        print(full_log)

        return full_log