# file: ui/main_window.py

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QSplitter,
    QStatusBar, QLabel, QMessageBox
)
from PyQt6.QtCore import Qt
from ui.sidebar import Sidebar
from ui.tab_manager import TabManager
from ui.command_bar import CommandBar
from core.error_handler import ErrorHandler
from core.logger import ShrineLogger
import os
import sys
from PyQt6.QtGui import QIcon

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Macan Explorer")
        self.setMinimumSize(1000, 600)   

        if hasattr(sys, "_MEIPASS"): 
            icon_path = os.path.join(sys._MEIPASS, "icon.ico")
        else:
            icon_path = "icon.ico"

        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        self.errors = ErrorHandler() 
        self.logger = ShrineLogger()
        
        self.sidebar = Sidebar(self.open_folder_from_sidebar)
        self.tab_manager = TabManager(self)
        self.toolbar = CommandBar(self)
        
        self.connect_toolbar_actions() 
        self.tab_manager.current_tab_changed.connect(self.connect_active_tab_signals)

        self.status = QStatusBar()
        self.status.addWidget(QLabel("🛕 Shrine ready to explore..."))

        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.setSpacing(10)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(self.sidebar)
        splitter.addWidget(self.tab_manager)
        splitter.setSizes([200, 800]) 
        
        splitter.setHandleWidth(4)
        splitter.setStyleSheet("""
            QSplitter::handle { background-color: #333; }
            QSplitter::handle:hover { background-color: #555; }
        """)
        
        main_layout.addWidget(self.toolbar)
        main_layout.addWidget(splitter)
        
        self.setCentralWidget(central_widget)
        self.setStatusBar(self.status) 

        self.toolbar.setObjectName("CommandBar") 
        self.sidebar.setObjectName("Sidebar")
        self.tab_manager.setObjectName("TabManager")
        self.status.setObjectName("StatusBar")

        # Panggil koneksi awal untuk tab pertama yang dibuat di TabManager
        self.connect_active_tab_signals(self.tab_manager.current_widget())

    def connect_toolbar_actions(self):
        # Aksi Navigasi
        self.toolbar.back_requested.connect(lambda: self.call_active_view_method('go_back'))
        self.toolbar.forward_requested.connect(lambda: self.call_active_view_method('go_forward'))
        self.toolbar.up_requested.connect(lambda: self.call_active_view_method('go_up'))
        self.toolbar.refresh_requested.connect(lambda: self.call_active_view_method('refresh'))
        self.toolbar.address_submitted.connect(self.on_address_bar_submit)
        
        # Aksi View dan File
        self.toolbar.view_mode_changed.connect(self.handle_view_change)
        self.toolbar.search_requested.connect(
            lambda query: self.call_active_view_method('search_files', query)
        )
        self.toolbar.new_folder_requested.connect(
            lambda: self.call_active_view_method('create_new_folder')
        )
        self.toolbar.new_file_requested.connect(
            lambda: self.call_active_view_method('create_new_file')
        )
        self.toolbar.delete_item_requested.connect(
            lambda: self.call_active_view_method('delete_selected_items')
        )
        self.toolbar.rename_item_requested.connect(
            lambda: self.call_active_view_method('rename_selected_item')
        )
        self.toolbar.ask_ai_requested.connect(
            lambda: self.call_active_view_method('ask_ai_about_selection')
        )

        # Aksi Jendela & Lainnya
        self.toolbar.action_open_new_window.triggered.connect(self.open_new_window)
        self.toolbar.action_about.triggered.connect(self.show_about_dialog)

    def connect_active_tab_signals(self, tab_widget):
        if not isinstance(tab_widget, QWidget) or not hasattr(tab_widget, 'path_changed'):
            self.toolbar.set_address_path("")
            self.toolbar.set_navigation_enabled(False, False)
            return

        # Putuskan koneksi lama jika ada untuk menghindari koneksi ganda
        try:
            self.sender().path_changed.disconnect()
            self.sender().navigation_state_changed.disconnect()
        except (TypeError, AttributeError, RuntimeError):
            pass # Abaikan error jika tidak ada koneksi sebelumnya

        # Hubungkan sinyal dari FileView yang aktif
        tab_widget.path_changed.connect(self.toolbar.set_address_path)
        tab_widget.navigation_state_changed.connect(self.toolbar.set_navigation_enabled)

        # Segarkan UI dengan status tab yang baru
        self.toolbar.set_address_path(tab_widget.current_path)
        tab_widget._update_navigation_state()

    def on_address_bar_submit(self, path):
        self.call_active_view_method('set_path', path)

    def call_active_view_method(self, method_name, *args):
        current_tab_widget = self.tab_manager.current_widget()
        if not current_tab_widget:
            return

        method_to_call = getattr(current_tab_widget, method_name, None)
        if method_to_call and callable(method_to_call):
            method_to_call(*args)
        else:
            self.logger.log(f"Method '{method_name}' not found in active tab.", "warning")

    def handle_view_change(self, mode):
        self.call_active_view_method('set_view_mode', mode)

    def open_folder_from_sidebar(self, folder_path):
        if not folder_path: return
        
        tab_label = os.path.basename(folder_path) or os.path.normpath(folder_path)
        self.tab_manager.add_tab(tab_label, folder_path)
        self.logger.ritual("📂", "open", folder_path)
        self.status.showMessage(f"Shrine opened: {folder_path}")

    def open_new_window(self):
        self.new_window = MainWindow()
        self.new_window.show()
        self.logger.ritual("✨", "new_window", "created")

    def show_about_dialog(self):
        QMessageBox.about(self, "About Macan Explorer", "<h3>Macan Explorer 🐅 v1.2</h3><p>Copyright © 2025 Danx Exodus.</p><p>Macan Explorer is a modern file management application designed with developers, creators, and power users in mind. Inspired by the elegance of Windows 11 Explorer and reimagined through the lens of simplicity, speed, and control — Macan Explorer brings a custom, dark-themed interface with powerful features like multi-tab navigation, smart address bar, thumbnail previews, and Shrine-integrated tools. Built as part of the Macan Angkasa ecosystem, it’s more than just a file viewer — it’s a productivity companion crafted to support deep focus, efficient workflow, and visual clarity. Whether you're organizing projects, reviewing media assets, or launching your custom Shrine tools, Macan Explorer is your fast, elegant, and developer-centric gateway into your filesystem.</p>")
        self.logger.ritual("ℹ️", "about", "dialog_shown")