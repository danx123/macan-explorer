# file: ui/progress_overlay.py

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar
from PyQt6.QtCore import Qt

class ProgressOverlay(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(400, 120)
        self.setStyleSheet("""
            QWidget {
                background-color: rgba(32, 32, 32, 200);
                border-radius: 12px;
                border: 2px solid #fbc02d;
            }
            QLabel {
                color: #fbc02d;
                font-size: 14px;
                padding: 6px;
            }
            QProgressBar {
                background-color: #3a3a3a;
                border: none;
                height: 10px;
            }
            QProgressBar::chunk {
                background-color: #fbc02d;
            }
        """)

        # 🌿 Komponen
        self.label = QLabel("⛩️ Menyusun berkas dengan ritus...")
        self.progress = QProgressBar()
        self.progress.setRange(0, 100)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.progress)
        self.setLayout(layout)

    def update_progress(self, value, max_value):
        self.progress.setMaximum(max_value)
        self.progress.setValue(value)
        self.label.setText(f"📦 Progres: {value}/{max_value}")

    def show_overlay(self, center_point):
        self.move(center_point.x() - self.width() // 2, center_point.y() - self.height() // 2)
        self.show()

    def hide_overlay(self):
        self.hide()