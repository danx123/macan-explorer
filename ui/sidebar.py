# file: ui/sidebar.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QListWidget, QPushButton, QFileDialog,
    QTreeView, QLabel
)
from PyQt6.QtGui import QFileSystemModel
from PyQt6.QtCore import QDir

import os

class Sidebar(QWidget):
    def __init__(self, open_folder_callback, parent=None):
        super().__init__(parent)
        self.setObjectName("Sidebar")
        self.open_folder_callback = open_folder_callback
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)

        # --- BAGIAN MY COMPUTER / DRIVES ---
        self.system_drives_label = QLabel("My Computer")
        self.system_drives_label.setStyleSheet("font-weight: bold; margin-top: 10px; margin-bottom: 5px;")
        layout.addWidget(self.system_drives_label)

        self.file_system_model = QFileSystemModel()
        self.file_system_model.setRootPath("") 
        self.file_system_model.setFilter(QDir.Filter.AllDirs | QDir.Filter.NoDotAndDotDot | QDir.Filter.Drives)

        self.system_tree_view = QTreeView(self)
        self.system_tree_view.setModel(self.file_system_model)
        self.system_tree_view.setRootIndex(self.file_system_model.index(""))
        
        self.system_tree_view.hideColumn(1) 
        self.system_tree_view.hideColumn(2)
        self.system_tree_view.hideColumn(3)
        self.system_tree_view.setHeaderHidden(True)
        self.system_tree_view.setIndentation(10)
        
        # >>> PERBAIKAN: Ubah dari activated ke clicked untuk single-click <<<
        self.system_tree_view.clicked.connect(self._on_system_drive_activated)
        layout.addWidget(self.system_tree_view)
        
        # --- BAGIAN ADDED FOLDERS ---
        self.add_folder_button = QPushButton("➕ Add Folder")
        self.add_folder_button.clicked.connect(self.select_folder)
        layout.addWidget(self.add_folder_button)

        self.added_folders_label = QLabel("Added Folders")
        self.added_folders_label.setStyleSheet("font-weight: bold; margin-top: 10px; margin-bottom: 5px;")
        layout.addWidget(self.added_folders_label)

        self.folder_list_widget = QListWidget(self)
        # >>> PERBAIKAN: Ubah dari itemDoubleClicked ke itemClicked untuk single-click <<<
        self.folder_list_widget.itemClicked.connect(self._on_folder_clicked)
        self.folder_list_widget.setObjectName("FolderList")
        layout.addWidget(self.folder_list_widget)

        layout.addStretch()

    def _on_system_drive_activated(self, index):
        path = self.file_system_model.filePath(index)
        if os.path.isdir(path):
            self.open_folder_callback(path)

    def select_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder to Add")
        if folder_path and folder_path not in [self.folder_list_widget.item(i).text() for i in range(self.folder_list_widget.count())]:
            self.folder_list_widget.addItem(folder_path)

    def _on_folder_clicked(self, item):
        folder_path = item.text()
        self.open_folder_callback(folder_path)