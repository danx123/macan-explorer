# file: ui/tab_manager.py

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTabWidget
from ui.file_view import FileView
from PyQt6.QtGui import QIcon
from core.glyph_translator import GlyphTranslator
from core.error_handler import ErrorHandler
from core.logger import ShrineLogger
from PyQt6.QtCore import pyqtSignal

class TabManager(QWidget):
    current_tab_changed = pyqtSignal(object)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.currentChanged.connect(self._on_tab_change)

        layout = QVBoxLayout()
        layout.addWidget(self.tabs)
        self.setLayout(layout)

        self.translator = GlyphTranslator()
        self.errors = ErrorHandler()
        self.logger = ShrineLogger()

        self.add_tab("Home Shrine", folder_path=None)

    def _on_tab_change(self, index):
        current_widget = self.tabs.widget(index)
        self.current_tab_changed.emit(current_widget)

    def add_tab(self, label, folder_path=None):
        icon = QIcon("assets/icons/tab-glyph.svg")
        glyph_label = self.translator.label_with_glyph(label)

        try:
            file_view = FileView(folder_path)
            index = self.tabs.addTab(file_view, icon, glyph_label)
            self.tabs.setCurrentIndex(index)

            self.logger.ritual(
                glyph=self.translator.get_glyph(label),
                action="open",
                target=label
            )

        except Exception as e:
            self.errors.handle(e, context=f"TabManager:add_tab({label})")
            self.logger.log(
                f"Failed to open tab for {label}",
                level="error",
                tag="tab-failure"
            )

    def close_tab(self, index):
        widget = self.tabs.widget(index)
        if widget:
            widget.deleteLater()
        self.tabs.removeTab(index)
        self.logger.log(f"Tab index {index} closed", tag="tab-close")

    def current_widget(self):
        return self.tabs.currentWidget()