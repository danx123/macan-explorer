# file: core/config_manager.py

import json
import os

class ConfigManager:
    """
    Manajer untuk menyimpan dan memuat konfigurasi aplikasi.
    """
    def __init__(self, config_file="macan_explorer_config.json"):
        # Tentukan path file konfigurasi, relatif terhadap root proyek
        # Asumsikan config_manager.py berada di core/, dan config.json di root
        self.config_file_name = config_file
        self.project_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
        self.config_path = os.path.join(self.project_root, self.config_file_name)
        self.config_data = {}
        self._load_config()

    def _load_config(self):
        """Memuat data konfigurasi dari file JSON."""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    self.config_data = json.load(f)
            except json.JSONDecodeError as e:
                print(f"Error loading config file {self.config_path}: {e}. Initializing with empty config.")
                self.config_data = {} # Handle empty or corrupt file
            except Exception as e:
                print(f"Unexpected error loading config file {self.config_path}: {e}. Initializing with empty config.")
                self.config_data = {}
        else:
            self.config_data = {} # File doesn't exist yet

    def _save_config(self):
        """Menyimpan data konfigurasi ke file JSON."""
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config_data, f, indent=4)
        except Exception as e:
            print(f"Error saving config file {self.config_path}: {e}")

    def get(self, key, default=None):
        """Mendapatkan nilai konfigurasi berdasarkan kunci."""
        return self.config_data.get(key, default)

    def set(self, key, value):
        """Mengatur nilai konfigurasi untuk kunci tertentu dan menyimpannya."""
        self.config_data[key] = value
        self._save_config()

    def add_to_list(self, key, item):
        """Menambahkan item ke daftar dalam konfigurasi jika belum ada."""
        current_list = self.get(key, [])
        if item not in current_list:
            current_list.append(item)
            self.set(key, current_list)
            return True
        return False

    def remove_from_list(self, key, item):
        """Menghapus item dari daftar dalam konfigurasi jika ada."""
        current_list = self.get(key, [])
        if item in current_list:
            current_list.remove(item)
            self.set(key, current_list)
            return True
        return False