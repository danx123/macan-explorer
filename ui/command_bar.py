# file: ui/command_bar.py

from PyQt6.QtWidgets import (
    QToolBar, QLineEdit, QPushButton, QWidget,
    QSizePolicy, QMenu, QToolButton
)
from PyQt6.QtGui import QAction, QIcon, QActionGroup
from PyQt6.QtCore import pyqtSignal, Qt, QSize
import os

class CommandBar(QToolBar):
    # Sinyal untuk navigasi dan address bar
    back_requested = pyqtSignal()
    forward_requested = pyqtSignal()
    up_requested = pyqtSignal()
    refresh_requested = pyqtSignal()
    address_submitted = pyqtSignal(str)

    # Definisi sinyal khusus lainnya
    search_requested = pyqtSignal(str)
    new_folder_requested = pyqtSignal()
    new_file_requested = pyqtSignal()
    delete_item_requested = pyqtSignal()
    rename_item_requested = pyqtSignal()
    ask_ai_requested = pyqtSignal(str)
    view_mode_changed = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setIconSize(QSize(22, 22))
        self.setMovable(False)

        def get_icon_path(icon_name):
            base_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.abspath(os.path.join(base_dir, '..'))
            if not icon_name.endswith('.svg'):
                icon_name += '.svg'
            return os.path.join(project_root, 'assets', 'icons', icon_name)

        # --- Aksi Navigasi ---
        self.action_back = QAction(QIcon(get_icon_path("back")), "Back", self)
        self.action_forward = QAction(QIcon(get_icon_path("forward")), "Forward", self)
        self.action_up = QAction(QIcon(get_icon_path("up")), "Up", self)
        self.action_refresh = QAction(QIcon(get_icon_path("refresh")), "Refresh", self)
        
        self.action_back.setEnabled(False)
        self.action_forward.setEnabled(False)
        
        self.action_back.triggered.connect(self.back_requested.emit)
        self.action_forward.triggered.connect(self.forward_requested.emit)
        self.action_up.triggered.connect(self.up_requested.emit)
        self.action_refresh.triggered.connect(self.refresh_requested.emit)

        self.addAction(self.action_back)
        self.addAction(self.action_forward)
        self.addAction(self.action_up)
        self.addAction(self.action_refresh)
        self.addSeparator()

        # --- Address Bar ---
        self.address_bar = QLineEdit(self)
        self.address_bar.setPlaceholderText("Enter path...")
        self.address_bar.returnPressed.connect(self._on_address_submit)
        self.addWidget(self.address_bar)

        # Spacer untuk mendorong item berikut ke kanan
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.addWidget(spacer)
        
        # --- Search Bar ---
        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText("Search...")
        self.search_input.setFixedWidth(200)
        self.search_input.returnPressed.connect(self._on_search_clicked)
        self.addWidget(self.search_input)

        self.search_button = QPushButton(QIcon(get_icon_path("search")), "", self)
        self.search_button.setToolTip("Search")
        self.search_button.clicked.connect(self._on_search_clicked)
        self.addWidget(self.search_button)
        self.addSeparator()

        # --- Aksi View Mode ---
        self.action_view_details = QAction(QIcon(get_icon_path("view_details")), "Details View", self)
        self.action_view_details.setCheckable(True)
        self.action_view_details.setChecked(True)
        
        self.action_view_list = QAction(QIcon(get_icon_path("view_list")), "List View", self)
        self.action_view_list.setCheckable(True)
        
        self.action_view_icons = QAction(QIcon(get_icon_path("view_icons")), "Icons View", self)
        self.action_view_icons.setCheckable(True)

        self.view_mode_group = QActionGroup(self)
        self.view_mode_group.setExclusive(True)
        self.view_mode_group.addAction(self.action_view_details)
        self.view_mode_group.addAction(self.action_view_list)
        self.view_mode_group.addAction(self.action_view_icons)
        self.view_mode_group.triggered.connect(self._on_view_mode_changed)

        self.addAction(self.action_view_details)
        self.addAction(self.action_view_list)
        self.addAction(self.action_view_icons)
        self.addSeparator()

        # --- Tombol "Organize" dengan Menu ---
        self.organize_button = QToolButton(self)
        self.organize_button.setText("Organize")
        self.organize_button.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        self.organize_button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.organize_button.setIcon(QIcon(get_icon_path("folder-closed")))
        
        organize_menu = QMenu(self)
        self.action_new_folder = QAction(QIcon(get_icon_path("folder-closed")), "New Folder", self)
        self.action_new_file = QAction(QIcon(get_icon_path("new_file")), "New File", self)
        self.action_rename = QAction(QIcon(get_icon_path("rename")), "Rename", self)
        self.action_delete = QAction(QIcon(get_icon_path("delete")), "Delete", self)
        
        self.action_new_folder.triggered.connect(self.new_folder_requested.emit)
        self.action_new_file.triggered.connect(self.new_file_requested.emit)
        self.action_rename.triggered.connect(self.rename_item_requested.emit)
        self.action_delete.triggered.connect(self.delete_item_requested.emit)

        organize_menu.addAction(self.action_new_folder)
        organize_menu.addAction(self.action_new_file)
        organize_menu.addSeparator()
        organize_menu.addAction(self.action_rename)
        organize_menu.addAction(self.action_delete)
        
        self.organize_button.setMenu(organize_menu)
        self.addWidget(self.organize_button)

        # --- Tombol "More" dengan Menu ---
        self.more_button = QToolButton(self)
        self.more_button.setIcon(QIcon(get_icon_path("more-horizontal"))) # Asumsikan ada ikon 'more'
        self.more_button.setToolTip("More options")
        self.more_button.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)

        more_menu = QMenu(self)
        self.action_open_new_window = QAction(QIcon(get_icon_path("new_window")), "Open New Window", self)
        self.action_about = QAction(QIcon(get_icon_path("about")), "About Macan Explorer", self)
        
        more_menu.addAction(self.action_open_new_window)
        more_menu.addAction(self.action_about)
        
        self.more_button.setMenu(more_menu)
        self.addWidget(self.more_button)

    def _on_address_submit(self):
        path = self.address_bar.text()
        if path:
            self.address_submitted.emit(path)

    def set_address_path(self, path):
        self.address_bar.setText(path)
        self.address_bar.setCursorPosition(0)

    def set_navigation_enabled(self, can_go_back, can_go_forward):
        self.action_back.setEnabled(can_go_back)
        self.action_forward.setEnabled(can_go_forward)

    def _on_view_mode_changed(self, action):
        if action == self.action_view_details:
            self.view_mode_changed.emit("details")
        elif action == self.action_view_list:
            self.view_mode_changed.emit("list")
        elif action == self.action_view_icons:
            self.view_mode_changed.emit("icons")

    def _on_search_clicked(self):
        query = self.search_input.text()
        if query:
            self.search_requested.emit(query)