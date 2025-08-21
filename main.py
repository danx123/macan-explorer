# file: main.py

import sys
import logging
import os
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow

# Fungsi untuk mengonfigurasi logging secara global
def setup_logging():
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True) # Pastikan direktori log ada

    shrine_log_file = os.path.join(log_dir, "shrine_ritual_log.txt")
    error_log_file = os.path.join(log_dir, "error_log.txt") # Dari error_handler.py

    # Buat handler untuk shrine_ritual_log.txt
    shrine_file_handler = logging.FileHandler(shrine_log_file, mode='a')
    shrine_file_handler.setLevel(logging.INFO) # Atur level untuk handler ini

    # Buat handler untuk error_log.txt
    error_file_handler = logging.FileHandler(error_log_file, mode='a')
    error_file_handler.setLevel(logging.ERROR) # Atur level untuk handler ini

    # Buat stream handler untuk konsol
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO) # Atur level untuk handler konsol

    # Konfigurasi root logger hanya sekali
    if not logging.getLogger().handlers: # Pastikan belum ada handler yang terpasang
        logging.basicConfig(
            level=logging.INFO, # Level default untuk root logger
            format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
            handlers=[
                shrine_file_handler,
                error_file_handler,
                console_handler
            ]
        )
        # Opsional: Atur level untuk logger spesifik jika perlu (misal: 'core.error_handler' ke ERROR)
        logging.getLogger('core.error_handler').setLevel(logging.ERROR)
        logging.getLogger('core.logger').setLevel(logging.INFO)


def load_theme(app):
    """🌑 Load QSS theme (no error shield)."""
    try:
        with open("style/theme.qss", "r", encoding="utf-8") as f:
            qss = f.read()
            app.setStyleSheet(qss)
    except Exception as e:
        print(f"⚠️ Theme load failed: {e}")

def main():
    app = QApplication(sys.argv)
    load_theme(app)
    setup_logging() # Panggil setup_logging di sini!

    # 🔮 Inisialisasi Shrine Window
    window = MainWindow()
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()