# file: core/stealth_manager.py

import os
import json
from core.error_handler import ErrorHandler  # 🛡️ Shrine Guardian

class StealthManager:
    def __init__(self, stealth_map_path="config/stealth_map.json"):
        self.stealth_map_path = stealth_map_path
        self.errors = ErrorHandler()  # ✒️ Ritual log jika terjadi anomaly
        self.load_stealth_map()

    def load_stealth_map(self):
        try:
            if os.path.exists(self.stealth_map_path):
                with open(self.stealth_map_path, "r", encoding="utf-8") as f:
                    self.stealth_map = json.load(f)
            else:
                raise FileNotFoundError(f"No stealth map found at {self.stealth_map_path}")
        except Exception as e:
            self.errors.handle(e, context="StealthManager:load_stealth_map")
            self.stealth_map = {
                ".bak": True,
                ".log": False,
                ".tmp": True
            }

    def is_stealth(self, path):
        try:
            ext = os.path.splitext(path)[1].lower()
            return self.stealth_map.get(ext, False)
        except Exception as e:
            self.errors.handle(e, context=f"StealthManager:is_stealth({path})")
            return False

    def cloak(self, file_list):
        try:
            return [f for f in file_list if not self.is_stealth(f)]
        except Exception as e:
            self.errors.handle(e, context="StealthManager:cloak")
            return file_list  # fallback: tampilkan semua jika gagal