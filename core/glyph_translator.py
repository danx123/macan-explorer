# file: core/glyph_translator.py

import os
import json
from core.error_handler import ErrorHandler  # 🛡️ Penjaga Ritual Glyph

class GlyphTranslator:
    def __init__(self, mapping_path="config/glyph_map.json"):
        self.mapping_path = mapping_path
        
        # --- PERBAIKAN: Pastikan direktori 'config' ada ---
        config_dir = os.path.dirname(self.mapping_path)
        if not os.path.exists(config_dir):
            os.makedirs(config_dir, exist_ok=True)
        # ------------------------------------------------

        self.errors = ErrorHandler()  # ✒️ Error Guardian (Ini seharusnya aman sekarang)
        self.load_map()

    def load_map(self):
        try:
            if os.path.exists(self.mapping_path):
                with open(self.mapping_path, "r", encoding="utf-8") as f:
                    self.glyph_map = json.load(f)
            else:
                # Jika file tidak ditemukan, buat dengan default map dan tulis ke file
                self.glyph_map = {
                    ".txt": "📜",
                    ".png": "🖼️",
                    ".mp3": "🎧",
                    ".py": "🐍",
                    ".json": "🧬",
                    ".pdf": "📘",
                    ".exe": "⚙️",
                    ".zip": "🧳",
                    ".rar": "📦", 
                    ".doc": "📄", ".docx": "📄", 
                    ".xls": "📊", ".xlsx": "📊",
                    ".jpg": "🖼️", ".jpeg": "🖼️", ".gif": "🖼️", ".bmp": "🖼️",
                    ".svg": "🎨",
                    ".html": "🌐", ".css": "💅", ".js": "📜",
                    ".java": "☕", ".c": "📄", ".cpp": "📄", ".h": "📄", ".hpp": "📄",
                    ".md": "📝",
                    ".apk": "🤖"
                }
                # Tulis default map ke file agar ada untuk selanjutnya
                with open(self.mapping_path, "w", encoding="utf-8") as f:
                    json.dump(self.glyph_map, f, indent=4)
                
                # Kita tidak perlu raise FileNotFoundError lagi jika kita langsung menyediakan default
                # raise FileNotFoundError("Glyph map config not found.") 
        except Exception as e:
            # Jika ada error lain saat memuat/membuat map (misal: JSON malformed),
            # kita tetap log errornya (karena self.errors sekarang sudah terinisialisasi)
            # dan gunakan default map yang paling sederhana sebagai fallback terakhir.
            self.errors.handle(e, context="GlyphTranslator:load_map")
            self.glyph_map = {
                ".txt": "📜", ".png": "🖼️", ".mp3": "🎧", ".py": "🐍",
                ".json": "🧬", ".pdf": "📘", ".exe": "⚙️", ".zip": "🧳"
            } 

    def get_glyph(self, filename):
        ext = os.path.splitext(filename)[1].lower()
        return self.glyph_map.get(ext, "🗃️")

    def label_with_glyph(self, filename):
        glyph = self.get_glyph(filename)
        return f"{glyph} {filename}"