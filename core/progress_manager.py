from PyQt6.QtWidgets import QProgressDialog
from PyQt6.QtCore import Qt, QTimer

class ProgressManager:
    def __init__(self, parent=None):
        self.dialog = QProgressDialog("⛩️ Ritual sedang berjalan...", "Batalkan", 0, 100, parent)
        # --- PERBAIKAN: Mengganti Qt.WindowModal menjadi Qt.WindowModality.WindowModal ---
        self.dialog.setWindowModality(Qt.WindowModality.WindowModal)
        # --------------------------------------------------------------------------------
        self.dialog.setMinimumDuration(0)
        self.dialog.setAutoClose(True)
        self.dialog.setAutoReset(True)
        self.dialog.setFixedSize(400, 100)
        self.dialog.setStyleSheet("""
            QProgressDialog {
                background-color: #1f1f1f;
                color: #ffffff;
                font-size: 14px;
                border: 1px solid #444;
            }
            QProgressBar {
                background-color: #3a3a3a;
                border: none;
                height: 10px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #fbc02d;
            }
        """)

    def start(self, total_steps):
        self.dialog.setMaximum(total_steps)
        self.dialog.setValue(0)
        self.dialog.show()

    def update(self, value):
        self.dialog.setValue(value)
        if value >= self.dialog.maximum():
            self.dialog.setLabelText("✅ Ritual selesai...")
            QTimer.singleShot(500, self.dialog.close)

    def cancelable(self, callback):
        self.dialog.canceled.connect(callback)

    def is_active(self):
        return self.dialog.isVisible()