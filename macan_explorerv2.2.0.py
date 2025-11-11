import sys
import os
import json
import shutil
import logging
import traceback
import math
from datetime import datetime
import hashlib
# Pustaka cv2 ditambahkan untuk pembuatan thumbnail
try:
    import cv2
    OPENCV_AVAILABLE = True
except ImportError:
    OPENCV_AVAILABLE = False


from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSplitter,
    QStatusBar, QLabel, QMessageBox, QToolBar, QLineEdit, QPushButton, QMenu,
    QToolButton, QSizePolicy, QListWidget, QListWidgetItem, QTreeView, QListView,
    QInputDialog, QFileDialog, QFrame, QTabWidget, QDialog, QDialogButtonBox,
    QFormLayout, QProgressDialog, QFileSystemModel
)
from PySide6.QtCore import (
    Qt, QSize, Signal, QDir, QUrl, QFileInfo, QSortFilterProxyModel,
    QModelIndex, QPoint, QRect, QEvent, QTimer, QMimeData
)
from PySide6.QtGui import (
    QAction, QIcon, QActionGroup, QDesktopServices, QPixmap,
    QPainter, QMouseEvent, QColor, QKeySequence
)
from PySide6.QtSvg import QSvgRenderer

# --- FFMPEG CHECK DIHAPUS, DIGANTI DENGAN OPENCV CHECK DI GLOBAL SCOPE ---
# FFMPEG_AVAILABLE = False

# --- EMBEDDED SVG ICONS ---
# A simple dictionary to hold SVG data for icons.
# In a real-world app, you might load these from a resource file.
SVG_ICONS = {
    "app_icon": """<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M4 6C4 4.89543 4.89543 4 6 4H18C19.1046 4 20 4.89543 20 6V18C20 19.1046 19.1046 20 18 20H6C4.89543 20 4 19.1046 4 18V6Z" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M12 4V20" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M4 12H20" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>""",
    "back": """<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M19 12H5" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M12 19L5 12L12 5" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>""",
    "forward": """<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M5 12H19" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M12 5L19 12L12 19" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>""",
    "up": """<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M12 19V5" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M5 12L12 5L19 12" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>""",
    "refresh": """<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M23 4V10H17" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M1 20V14H7" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M3.51 9.49C4.82255 7.02334 7.20932 5.5 10 5.5C14.1421 5.5 17.5 8.85786 17.5 13C17.5 17.1421 14.1421 20.5 10 20.5C7.20932 20.5 4.82255 19.0233 3.51 16.51" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>""",
    "search": """<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M11 19C15.4183 19 19 15.4183 19 11C19 6.58172 15.4183 3 11 3C6.58172 3 3 6.58172 3 11C3 15.4183 6.58172 19 11 19Z" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M21 21L16.65 16.65" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>""",
    "view_details": """<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M8 6H21" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M8 12H21" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M8 18H21" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M3 6H3.01" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M3 12H3.01" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M3 18H3.01" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>""",
    "view_list": """<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M3 12H21" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M3 6H21" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M3 18H21" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>""",
    "view_icons": """<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><rect x="4" y="4" width="6" height="6" rx="1" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><rect x="14" y="4" width="6" height="6" rx="1" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><rect x="4" y="14" width="6" height="6" rx="1" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><rect x="14" y="14" width="6" height="6" rx="1" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>""",
    "folder-closed": """<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M22 11V6C22 4.89543 21.1046 4 20 4H12L10 2H4C2.89543 2 2 2.89543 2 4V18C2 19.1046 2.89543 20 4 20H12" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>""",
    "new_file": """<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M14 2H6C5.46957 2 4.96086 2.21071 4.58579 2.58579C4.21071 2.96086 4 3.46957 4 4V20C4 20.5304 4.21071 21.0391 4.58579 21.4142C4.96086 21.7893 5.46957 22 6 22H18C18.5304 22 19.0391 21.7893 19.4142 21.4142C19.7893 21.0391 20 20.5304 20 20V8L14 2Z" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M14 2V8H20" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M12 18V12" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M9 15H15" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>""",
    "rename": """<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M20 16.5L16.5 20L13 16.5" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M16.5 20V4H6.5C5.96957 4 5.46086 4.21071 5.08579 4.58579C4.71071 4.96086 4.5 5.46957 4.5 6V11" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>""",
    "delete": """<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M3 6H5H21" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M8 6V4C8 3.46957 8.21071 2.96086 8.58579 2.58579C8.96086 2.21071 9.46957 2 10 2H14C14.5304 2 15.0391 2.21071 15.4142 2.58579C15.7893 2.96086 16 3.46957 16 4V6M19 6V20C19 20.5304 18.7893 21.0391 18.4142 21.4142C18.0391 21.7893 17.5304 22 17 22H7C6.46957 22 5.96086 21.7893 5.58579 21.4142C5.21071 21.0391 5 20.5304 5 20V6H19Z" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M10 11V17" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M14 11V17" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>""",
    "more-horizontal": """<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><circle cx="12" cy="12" r="1" fill="#e0e0e0"/><circle cx="19" cy="12" r="1" fill="#e0e0e0"/><circle cx="5" cy="12" r="1" fill="#e0e0e0"/></svg>""",
    "new_window": """<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M14 2H6C4.89543 2 4 2.89543 4 4V20C4 21.1046 4.89543 22 6 22H18C19.1046 22 20 21.1046 20 20V8L14 2Z" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M14 2V8H20" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M11 15H17" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M14 12V18" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>""",
    "about": """<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M12 22C17.5228 22 22 17.5228 22 12C22 6.47715 17.5228 2 12 2C6.47715 2 2 6.47715 2 12C2 17.5228 6.47715 22 12 22Z" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M12 16V12" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M12 8H12.01" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>""",
    "add_folder": """<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M20 12H12M12 12H4M12 12V4M12 12V20" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round"/></svg>""",
    "remove_folder": """<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M20 12H4" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round"/></svg>""",
    "tab_glyph": """<svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M4 7V17C4 18.1046 4.89543 19 6 19H18C19.1046 19 20 18.1046 20 17V7" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M2 7H22" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M9 7V5C9 3.89543 9.89543 3 11 3H13C14.1046 3 15 3.89543 15 5V7" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>""",
    "minimize": """<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M5 12H19" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>""",
    "maximize": """<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><rect x="5" y="5" width="14" height="14" rx="2" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>""",
    "restore": """<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M8 16H4V4H16V8" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M8 12H20V20H8V12Z" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>""",
    "close": """<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M18 6L6 18" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M6 6L18 18" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>""",
}
SVG_ICONS["play_overlay"] = """
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
<circle cx="12" cy="12" r="10" fill="#00000088"/>
<path d="M10 8L16 12L10 16V8Z" fill="#ffffff"/>
</svg>
"""
# Video Icon Overlay
def get_overlay_icon(size=24):
        renderer = QSvgRenderer(SVG_ICONS["play_overlay"].encode('utf-8'))
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        renderer.render(painter)
        painter.end()
        return pixmap

def create_icon(key):
    """Creates a QIcon from embedded SVG data."""
    if key not in SVG_ICONS:
        return QIcon()
    renderer = QSvgRenderer(SVG_ICONS[key].encode('utf-8'))
    pixmap = QPixmap(24, 24)
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    renderer.render(painter)
    painter.end()
    return QIcon(pixmap)

# --- THEME QSS ---
THEME_QSS = """
/* General App Styling */
QMainWindow, QWidget {
    background-color: #2e2e2e; /* Dark background */
    color: #e0e0e0; /* Light text */
    font-family: "Segoe UI", "Roboto", "Open Sans", sans-serif;
    font-size: 14px;
}

TitleBar {
    background-color: #2e2e2e;
}

TitleBar #TitleLabel {
    color: #e0e0e0;
    padding-left: 10px;
    font-weight: bold;
}

TitleBar QToolButton {
    background-color: transparent;
    border: none;
    padding: 4px;
    margin: 1px;
    border-radius: 4px;
}
TitleBar QToolButton:hover {
    background-color: #5a5a5a;
}
TitleBar QToolButton#CloseButton:hover {
    background-color: #e74c3c;
}

/* ScrollBars */
QScrollBar:vertical {
    border: none;
    background: #3a3a3a;
    width: 8px;
    margin: 0px 0px 0px 0px;
}
QScrollBar::handle:vertical {
    background: #5a5a5a;
    min-height: 20px;
    border-radius: 4px;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px; /* Hide arrows */
}
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
    background: none;
}
QScrollBar:horizontal {
    border: none;
    background: #3a3a3a;
    height: 8px;
    margin: 0px 0px 0px 0px;
}
QScrollBar::handle:horizontal {
    background: #5a5a5a;
    min-width: 20px;
    border-radius: 4px;
}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0px; /* Hide arrows */
}
QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
    background: none;
}

/* Buttons */
QPushButton {
    background-color: #4a4a4a;
    color: #e0e0e0;
    border: 1px solid #5a5a5a;
    border-radius: 4px;
    padding: 8px 15px;
    min-height: 24px;
    outline: none;
}
QPushButton:hover {
    background-color: #5a5a5a;
    border-color: #6a6a6a;
}
QPushButton:pressed {
    background-color: #3a3a3a;
    border-color: #4a4a4a;
}
QPushButton:flat {
    border: none;
    background-color: transparent;
}
QPushButton:flat:hover {
    background-color: #4a4a4a;
}

/* LineEdit */
QLineEdit {
    background-color: #3a3a3a;
    border: 1px solid #5a5a5a;
    border-radius: 4px;
    padding: 5px 10px;
    color: #e0e0e0;
    selection-background-color: #007acc;
}
QLineEdit:focus {
    border: 1px solid #007acc;
}

/* Labels */
QLabel {
    color: #e0e0e0;
}

/* ListWidget */
QListWidget {
    background-color: #3a3a3a;
    border: 1px solid #4a4a4a;
    border-radius: 4px;
    padding: 5px;
    color: #e0e0e0;
    outline: none;
}
QListWidget::item {
    padding: 6px 8px;
    border-radius: 3px;
}
QListWidget::item:selected {
    background-color: #007acc;
    color: #ffffff;
}
QListWidget::item:hover {
    background-color: #4a4a4a;
}

/* TreeView */
QTreeView {
    background-color: #3a3a3a;
    border: 1px solid #4a4a4a;
    border-radius: 4px;
    color: #e0e0e0;
    selection-background-color: #007acc;
    selection-color: #ffffff;
    outline: none;
    show-decoration-selected: 1;
    alternate-background-color: #3f3f3f;
}
QTreeView::item {
    padding: 5px;
    height: 28px;
}
QTreeView::item:hover {
    background-color: #4a4a4a;
}
QTreeView::item:selected {
    background-color: #007acc;
    color: #ffffff;
}
QHeaderView::section {
    background-color: #4a4a4a;
    color: #e0e0e0;
    padding: 4px;
    border: 1px solid #3a3a3a;
}

/* Menus */
QMenu {
    background-color: #3a3a3a;
    border: 1px solid #5a5a5a;
    border-radius: 4px;
    padding: 5px;
    color: #e0e0e0;
}
QMenu::item {
    padding: 6px 15px;
    border-radius: 3px;
}
QMenu::item:selected {
    background-color: #007acc;
    color: #ffffff;
}
QMenu::separator {
    height: 1px;
    background: #5a5a5a;
    margin: 5px 0px;
}

/* ToolBar (CommandBar) */
QToolBar {
    background-color: #2e2e2e;
    border: none;
    border-radius: 8px;
    padding: 5px;
    margin: 0px;
    spacing: 5px;
}
QToolButton {
    background-color: transparent;
    border: none;
    padding: 6px;
    border-radius: 4px;
    color: #e0e0e0;
    icon-size: 20px;
}
QToolButton:hover {
    background-color: #4a4a4a;
}
QToolButton:pressed {
    background-color: #5a5a5a;
}
QToolButton:checked {
    background-color: #007acc;
}

/* Status Bar */
QStatusBar {
    background-color: #2e2e2e;
    color: #e0e0e0;
    border-top: 1px solid #4a4a4a;
}
QStatusBar::item {
    border: none;
}

/* TabWidget */
QTabWidget::pane {
    border: 1px solid #4a4a4a;
    background-color: #2e2e2e;
    border-radius: 8px;
    padding: 5px;
}
QTabBar::tab {
    background-color: #3a3a3a;
    color: #e0e0e0;
    border: 1px solid #4a4a4a;
    border-bottom: none;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
    padding: 8px 15px;
    margin-right: 2px;
}
QTabBar::tab:selected {
    background-color: #2e2e2e;
    border-color: #4a4a4a;
    border-bottom-color: #2e2e2e;
}
QTabBar::tab:hover:!selected {
    background-color: #4a4a4a;
}
QTabBar::close-button {
    image: url(placeholder.png); /* Will be set in code */
    subcontrol-origin: padding;
    subcontrol-position: center right;
    width: 16px;
    height: 16px;
    padding-left: 5px;
}
QTabBar::close-button:hover {
    background-color: #e74c3c;
    border-radius: 8px;
}

/* Splitter */
QSplitter::handle {
    background-color: #333;
    width: 4px;
}
QSplitter::handle:hover {
    background-color: #555;
}
QSplitter::handle:horizontal {
    margin: 0px 0px;
}

/* QMessageBox and QDialog */
QMessageBox, QDialog {
    background-color: #3a3a3a;
    color: #e0e0e0;
    border: 1px solid #4a4a4a;
    border-radius: 8px;
}
QMessageBox QLabel, QDialog QLabel {
    color: #e0e0e0;
}
QMessageBox QPushButton, QDialog QPushButton {
    background-color: #007acc;
    border: 1px solid #005f99;
    color: #ffffff;
    min-width: 80px;
}
QMessageBox QPushButton:hover, QDialog QPushButton:hover {
    background-color: #008be5;
}
QMessageBox QPushButton:pressed, QDialog QPushButton:pressed {
    background-color: #005f99;
}

/* QFormLayout Styling */
QFormLayout QLabel {
    font-weight: bold;
}
"""


# --- CORE LOGIC & HELPERS ---

def _format_size(size_bytes):
    if size_bytes == 0:
        return "0 B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_name[i]}"

def _get_folder_size(path):
    total_size = 0
    try:
        for dirpath, _, filenames in os.walk(path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                if not os.path.islink(fp):
                    total_size += os.path.getsize(fp)
    except OSError:
        pass
    return total_size

def _get_folder_contents_count(path):
    file_count = 0
    folder_count = 0
    try:
        for _, dirs, files in os.walk(path):
            file_count += len(files)
            folder_count += len(dirs)
            break # We only want the top-level counts for the "Contains" field
    except OSError:
        pass
    return file_count, folder_count

class ErrorHandler:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def handle(self, error, context=""):
        error_type = type(error).__name__
        error_msg = str(error)
        trace = traceback.format_exc()
        full_log = f"[⚠️] Error in {context}\nType: {error_type}\nMessage: {error_msg}\nTrace:\n{trace}\n"
        self.logger.error(full_log)
        print(full_log)
        return full_log

class ShrineLogger:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def log(self, message, level="info", tag=None):
        full_message = f"[{tag}] {message}" if tag else message
        if level == "info":
            self.logger.info(full_message)
        elif level == "warning":
            self.logger.warning(full_message)
        elif level == "error":
            self.logger.error(full_message)
        elif level == "critical":
            self.logger.critical(full_message)
        else:
            self.logger.debug(full_message)

    def ritual(self, emoji, ritual_type, target):
        self.log(f"{emoji} Ritual {ritual_type} on {target}", tag="RITUAL")

class ConfigManager:
    def __init__(self, config_file="macan_explorer_config.json"):
        self.config_path = os.path.join(os.path.expanduser("~"), ".macan_explorer", config_file)
        self.config_data = {}
        self._load_config()

    def _load_config(self):
        base_dir = os.path.dirname(self.config_path)
        if not os.path.exists(base_dir):
            os.makedirs(base_dir)
        
        # Create thumbnail cache directory
        thumbnail_cache_dir = os.path.join(base_dir, "thumbnails")
        if not os.path.exists(thumbnail_cache_dir):
            os.makedirs(thumbnail_cache_dir)
        self.thumbnail_cache_path = thumbnail_cache_dir

        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    self.config_data = json.load(f)
            except (json.JSONDecodeError, Exception) as e:
                print(f"Error loading config file {self.config_path}: {e}. Initializing with empty config.")
                self.config_data = {}
        else:
            self.config_data = {"added_folders": [], "view_mode": "details"}
            self._save_config()

    def _save_config(self):
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config_data, f, indent=4)
        except Exception as e:
            print(f"Error saving config file {self.config_path}: {e}")

    def get(self, key, default=None):
        return self.config_data.get(key, default)

    def set(self, key, value):
        self.config_data[key] = value
        self._save_config()

    def add_to_list(self, key, item):
        current_list = self.get(key, [])
        if item not in current_list:
            current_list.append(item)
            self.set(key, current_list)
            return True
        return False

    def remove_from_list(self, key, item):
        current_list = self.get(key, [])
        if item in current_list:
            current_list.remove(item)
            self.set(key, current_list)
            return True
        return False

# --- UI COMPONENTS ---

class ThumbnailIconProvider(QFileSystemModel):
    def __init__(self, config_manager):
        super().__init__()
        self.config_manager = config_manager
        self.icon_cache = {}
        self.logger = ShrineLogger()
        self.VIDEO_EXTENSIONS = ['mp4', 'mkv', 'avi', 'mov', 'webm', 'flv', 'wmv', 'mpg', 'mpeg']
        self.IMAGE_EXTENSIONS = ['png', 'jpg', 'jpeg', 'bmp', 'gif', 'webp']

    def _get_cached_thumbnail_path(self, video_path):
        filename = hashlib.md5(video_path.encode('utf-8')).hexdigest() + ".jpg"
        return os.path.join(self.config_manager.thumbnail_cache_path, filename)       

    # --- MODIFIKASI START: Fungsi pembuatan thumbnail diubah menggunakan OpenCV ---
    def _generate_video_thumbnail_cv(self, video_path, thumbnail_path):
        """
        Membuat thumbnail dari file video menggunakan OpenCV.
        """
        try:
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                self.logger.log(f"Gagal membuka file video: {os.path.basename(video_path)}", level="warning", tag="OpenCV")
                return False

            # Coba ambil frame dari detik ke-2
            cap.set(cv2.CAP_PROP_POS_MSEC, 2000)
            success, frame = cap.read()
            
            # Jika gagal, coba ambil frame pertama
            if not success:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                success, frame = cap.read()

            if success:
                # Ubah ukuran frame ke lebar 96, dengan aspek rasio tetap
                h, w, _ = frame.shape
                if w > 0:
                    target_w = 96
                    ratio = target_w / w
                    target_h = int(h * ratio)
                    resized_frame = cv2.resize(frame, (target_w, target_h), interpolation=cv2.INTER_AREA)
                    cv2.imwrite(thumbnail_path, resized_frame, [cv2.IMWRITE_JPEG_QUALITY, 90])
                else:
                    success = False # Tidak dapat mengubah ukuran frame dengan lebar nol
            
            cap.release()
            
            if not success:
                 self.logger.log(f"Gagal membaca frame yang valid dari {os.path.basename(video_path)}", level="warning", tag="OpenCV")

            return success and os.path.exists(thumbnail_path)
        except Exception as e:
            self.logger.log(f"Error saat membuat thumbnail untuk {os.path.basename(video_path)} dengan OpenCV: {e}", level="warning", tag="OpenCV")
            if 'cap' in locals() and cap.isOpened():
                cap.release()
            return False       
    # --- MODIFIKASI END ---
    
    def data(self, index, role):
        if role == Qt.ItemDataRole.DecorationRole and index.column() == 0:
            file_path = self.filePath(index)
            
            if file_path in self.icon_cache:
                return self.icon_cache[file_path]

            file_info = QFileInfo(file_path)
            
            if file_info.isDir():
                return super().data(index, role)

            suffix = file_info.suffix().lower()

            # Image handler
            if suffix in self.IMAGE_EXTENSIONS:
                pixmap = QPixmap(file_path)
                if not pixmap.isNull():
                    icon = QIcon(pixmap.scaled(96, 96, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
                    self.icon_cache[file_path] = icon
                    return icon
            
            # --- MODIFIKASI START: Video handler diubah untuk menggunakan OpenCV ---
            if OPENCV_AVAILABLE and suffix in self.VIDEO_EXTENSIONS:
                thumbnail_path = self._get_cached_thumbnail_path(file_path)
                
                # Periksa cache thumbnail yang valid terlebih dahulu
                try:
                    if os.path.exists(thumbnail_path) and os.path.getmtime(thumbnail_path) > os.path.getmtime(file_path):
                        pixmap = QPixmap(thumbnail_path)
                        if not pixmap.isNull():
                            overlay = get_overlay_icon(24)
                            painter = QPainter(pixmap)
                            painter.drawPixmap(pixmap.width() - overlay.width(), pixmap.height() - overlay.height(), overlay)
                            painter.end()
                            icon = QIcon(pixmap)
                            self.icon_cache[file_path] = icon
                            return icon
                except FileNotFoundError:
                    # File sumber mungkin telah dihapus selama pemeriksaan
                    pass

                # Jika tidak ada cache yang valid, buat yang baru
                if self._generate_video_thumbnail_cv(file_path, thumbnail_path):
                    pixmap = QPixmap(thumbnail_path)
                    if not pixmap.isNull():
                        overlay = get_overlay_icon(24)
                        painter = QPainter(pixmap)
                        painter.drawPixmap(pixmap.width() - overlay.width(), pixmap.height() - overlay.height(), overlay)
                        painter.end()
                        icon = QIcon(pixmap)
                        self.icon_cache[file_path] = icon
                        return icon
            # --- MODIFIKASI END ---
        
        # Fallback ke ikon sistem default
        return super().data(index, role)          
    
class SortFilterProxyModel(QSortFilterProxyModel):
    def lessThan(self, left, right):
        source_model = self.sourceModel()
        if self.sortColumn() == 0:
            left_info = QFileInfo(source_model.filePath(left))
            right_info = QFileInfo(source_model.filePath(right))
            
            is_left_dir = left_info.isDir()
            is_right_dir = right_info.isDir()

            if is_left_dir != is_right_dir:
                return is_left_dir if self.sortOrder() == Qt.SortOrder.AscendingOrder else not is_left_dir

            return left_info.fileName().lower() < right_info.fileName().lower()
        return super().lessThan(left, right)

class CommandBar(QToolBar):
    back_requested = Signal()
    forward_requested = Signal()
    up_requested = Signal()
    refresh_requested = Signal()
    address_submitted = Signal(str)
    search_requested = Signal(str)
    new_folder_requested = Signal()
    new_file_requested = Signal()
    delete_item_requested = Signal()
    rename_item_requested = Signal()
    view_mode_changed = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setIconSize(QSize(22, 22))
        self.setMovable(False)
        self.setObjectName("CommandBar")

        # Navigation
        self.action_back = QAction(create_icon("back"), "Back", self)
        self.action_forward = QAction(create_icon("forward"), "Forward", self)
        self.action_up = QAction(create_icon("up"), "Up", self)
        self.action_refresh = QAction(create_icon("refresh"), "Refresh", self)
        
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

        # Address Bar
        self.address_bar = QLineEdit(self)
        self.address_bar.setPlaceholderText("Enter path...")
        self.address_bar.returnPressed.connect(self._on_address_submit)
        self.addWidget(self.address_bar)

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.addWidget(spacer)
        
        # Search Bar
        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText("Search...")
        self.search_input.setFixedWidth(200)
        self.search_input.returnPressed.connect(self._on_search_clicked)
        self.addWidget(self.search_input)

        self.search_button = QToolButton(self)
        self.search_button.setIcon(create_icon("search"))
        self.search_button.setToolTip("Search")
        self.search_button.clicked.connect(self._on_search_clicked)
        self.addWidget(self.search_button)
        self.addSeparator()

        # View Mode
        self.action_view_details = QAction(create_icon("view_details"), "Details View", self)
        self.action_view_details.setCheckable(True)
        self.action_view_details.setChecked(True)
        
        self.action_view_list = QAction(create_icon("view_list"), "List View", self)
        self.action_view_list.setCheckable(True)
        
        self.action_view_icons = QAction(create_icon("view_icons"), "Icons View", self)
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

        # Organize Menu
        self.organize_button = QToolButton(self)
        self.organize_button.setText("Organize")
        self.organize_button.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        self.organize_button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.organize_button.setIcon(create_icon("folder-closed"))
        
        organize_menu = QMenu(self)
        self.action_new_folder = QAction(create_icon("folder-closed"), "New Folder", self)
        self.action_new_file = QAction(create_icon("new_file"), "New File", self)
        self.action_rename = QAction(create_icon("rename"), "Rename", self)
        self.action_delete = QAction(create_icon("delete"), "Delete", self)
        
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

        # More Menu
        self.more_button = QToolButton(self)
        self.more_button.setIcon(create_icon("more-horizontal"))
        self.more_button.setToolTip("More options")
        self.more_button.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)

        more_menu = QMenu(self)
        self.action_open_new_window = QAction(create_icon("new_window"), "Open New Window", self)
        self.action_about = QAction(create_icon("about"), "About Macan Explorer", self)
        
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

    # --- FIX START: VIEW PERSISTENCE ---
    def set_view_mode(self, mode):
        """Checks the correct view mode button based on the mode string."""
        if mode == "details":
            self.action_view_details.setChecked(True)
        elif mode == "list":
            self.action_view_list.setChecked(True)
        elif mode == "icons":
            self.action_view_icons.setChecked(True)
    # --- FIX END: VIEW PERSISTENCE ---
    
    def _on_search_clicked(self):
        query = self.search_input.text()
        if query:
            self.search_requested.emit(query)

class FileView(QWidget):
    path_changed = Signal(str)
    navigation_state_changed = Signal(bool, bool)
    status_message_requested = Signal(str) # For copy/paste status updates

    def __init__(self, config_manager, folder_path=None, parent=None):
        super().__init__(parent)
        self._history = []
        self._history_index = -1
        self.config_manager = config_manager
        
        initial_path = folder_path if folder_path and os.path.exists(folder_path) else QDir.homePath()
        self.current_path = ""

        # Model
        self.model = ThumbnailIconProvider(config_manager)
        self.model.setRootPath(QDir.rootPath())
        self.model.setOption(QFileSystemModel.Option.DontWatchForChanges, False)
        self.model.setFilter(QDir.Filter.AllEntries | QDir.Filter.NoDotAndDotDot | QDir.Filter.Hidden)

        # Proxy Model
        self.proxy_model = SortFilterProxyModel(self)
        self.proxy_model.setSourceModel(self.model)

        # Views
        self.tree_view = QTreeView(self)
        self.list_view = QListView(self)

        self.tree_view.setModel(self.proxy_model)
        self.list_view.setModel(self.proxy_model)
        
        # TreeView Settings
        self.tree_view.setSortingEnabled(True)
        self.tree_view.sortByColumn(0, Qt.SortOrder.AscendingOrder)
        self.tree_view.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tree_view.customContextMenuRequested.connect(self._on_context_menu)
        self.tree_view.doubleClicked.connect(self._on_double_click)
        self.tree_view.setAlternatingRowColors(True)
        self.tree_view.setSelectionMode(QTreeView.SelectionMode.ExtendedSelection)
        self.tree_view.header().setStretchLastSection(True)

        # ListView Settings
        self.list_view.setViewMode(QListView.ViewMode.IconMode)
        self.list_view.setResizeMode(QListView.ResizeMode.Adjust)
        self.list_view.setMovement(QListView.Movement.Static)
        self.list_view.setWordWrap(True)
        self.list_view.setIconSize(QSize(96, 96))
        self.list_view.setGridSize(QSize(120, 120))
        self.list_view.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.list_view.customContextMenuRequested.connect(self._on_context_menu)
        self.list_view.doubleClicked.connect(self._on_double_click)
        self.list_view.setSelectionMode(QListView.SelectionMode.ExtendedSelection)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.tree_view)
        layout.addWidget(self.list_view)
        self.setLayout(layout)

        # --- FIX START: VIEW PERSISTENCE ---
        # The view mode is now set by MainWindow when the tab becomes active.
        # This initial call ensures it's set correctly on first load.
        initial_view_mode = self.config_manager.get('view_mode', 'details')
        self.set_view_mode(initial_view_mode)
        # --- FIX END: VIEW PERSISTENCE ---

        self.set_path(initial_path, initial_load=True)

        # --- FIX START: COPY/PASTE SHORTCUTS ---
        # Add actions with standard shortcuts to the widget
        copy_action = QAction("Copy", self)
        copy_action.setShortcut(QKeySequence.StandardKey.Copy)
        copy_action.triggered.connect(self.copy_selected_items)
        self.addAction(copy_action)

        paste_action = QAction("Paste", self)
        paste_action.setShortcut(QKeySequence.StandardKey.Paste)
        paste_action.triggered.connect(self.paste_items)
        self.addAction(paste_action)

        delete_action = QAction("Delete", self)
        delete_action.setShortcut(QKeySequence.StandardKey.Delete)
        delete_action.triggered.connect(self.delete_selected_items)
        self.addAction(delete_action)
        # --- FIX END: COPY/PASTE SHORTCUTS ---

    @property
    def active_view(self):
        return self.tree_view if self.tree_view.isVisible() else self.list_view

    def set_path(self, path, add_to_history=True, initial_load=False):
        path = os.path.normpath(path)
        if not os.path.exists(path) or not os.path.isdir(path):
            QMessageBox.warning(self, "Invalid Path", f"Folder '{path}' not found.")
            if initial_load:
                 path = QDir.homePath()
            else:
                return        
        
        self.current_path = path
        
        source_index = self.model.index(path)
        proxy_index = self.proxy_model.mapFromSource(source_index)
        
        self.tree_view.setRootIndex(proxy_index)
        self.list_view.setRootIndex(proxy_index)

        self.path_changed.emit(self.current_path)

        if add_to_history:
            if self._history_index < len(self._history) - 1:
                self._history = self._history[:self._history_index + 1]
            if not self._history or self._history[-1] != path:
                self._history.append(path)
                self._history_index += 1

        self._update_navigation_state()
        current_sort_col = self.tree_view.header().sortIndicatorSection()
        current_sort_order = self.tree_view.header().sortIndicatorOrder()
        self.tree_view.sortByColumn(current_sort_col, current_sort_order)

    def _update_navigation_state(self):
        can_go_back = self._history_index > 0
        can_go_forward = self._history_index < len(self._history) - 1
        self.navigation_state_changed.emit(can_go_back, can_go_forward)

    def go_back(self):
        if self._history_index > 0:
            self._history_index -= 1
            self.set_path(self._history[self._history_index], add_to_history=False)

    def go_forward(self):
        if self._history_index < len(self._history) - 1:
            self._history_index += 1
            self.set_path(self._history[self._history_index], add_to_history=False)
            
    def go_up(self):
        parent_path = os.path.dirname(self.current_path)
        if parent_path != self.current_path:
            self.set_path(parent_path)

    def refresh(self):
        """Refreshes the view of the current path."""
        self.set_path(self.current_path, add_to_history=False)
        
    def set_view_mode(self, mode):
        column_count = self.proxy_model.columnCount()
        if mode == "details":
            self.tree_view.show()
            self.list_view.hide()
            self.tree_view.setHeaderHidden(False)
            for i in range(column_count):
                self.tree_view.setColumnHidden(i, False)
        elif mode == "list":
            self.tree_view.show()
            self.list_view.hide()
            self.tree_view.setHeaderHidden(True)
            for i in range(1, column_count):
                self.tree_view.setColumnHidden(i, True)
        elif mode == "icons":
            self.tree_view.hide()
            self.list_view.show()

    def _on_double_click(self, index):
        source_index = self.proxy_model.mapToSource(index)
        if source_index.column() != 0:
            source_index = source_index.sibling(source_index.row(), 0)

        path = self.model.filePath(source_index)
        if self.model.isDir(source_index):
            self.set_path(path)
        else:
            if os.path.exists(path):
                QDesktopServices.openUrl(QUrl.fromLocalFile(path))
            else:
                QMessageBox.warning(self, "File Not Found", f"File '{path}' was not found.")

    def _on_context_menu(self, position):
        view = self.active_view
        proxy_index = view.indexAt(position)
        
        menu = QMenu(self)
        
        if proxy_index.isValid():
            source_index = self.proxy_model.mapToSource(proxy_index)
            path = self.model.filePath(source_index)

            menu.addAction("Open").triggered.connect(lambda: self._on_double_click(proxy_index))
            menu.addSeparator()
            # --- FIX START: COPY/PASTE ACTIONS ---
            menu.addAction("Copy").triggered.connect(self.copy_selected_items)
            # --- FIX END: COPY/PASTE ACTIONS ---
            menu.addAction("Rename").triggered.connect(self.rename_selected_item)
            menu.addAction("Delete").triggered.connect(self.delete_selected_items)
            menu.addSeparator()
            menu.addAction("Copy Path").triggered.connect(lambda: self._copy_path(path))
            menu.addSeparator()
            menu.addAction("Properties").triggered.connect(lambda: self.show_properties(proxy_index))
            menu.addSeparator()

        # --- FIX START: PASTE ACTION ---
        paste_action = menu.addAction("Paste")
        paste_action.triggered.connect(self.paste_items)
        # Disable paste if clipboard doesn't contain file URLs
        if not QApplication.clipboard().mimeData().hasUrls():
            paste_action.setEnabled(False)
        menu.addSeparator()
        # --- FIX END: PASTE ACTION ---

        menu.addAction("New Folder").triggered.connect(self.create_new_folder)
        menu.addAction("New File").triggered.connect(self.create_new_file)
        
        menu.exec(view.viewport().mapToGlobal(position))

    def _copy_path(self, path):
        QApplication.clipboard().setText(path)

    def _get_selected_proxy_indexes(self):
        return self.active_view.selectionModel().selectedIndexes()

    def search_files(self, query):
        results = []
        search_path = self.current_path
        query_lower = query.lower()
        
        try:
            for root, dirs, files in os.walk(search_path):
                for name in dirs:
                    if query_lower in name.lower():
                        results.append(os.path.join(root, name))
                for name in files:
                    if query_lower in name.lower():
                        results.append(os.path.join(root, name))
        except Exception as e:
            QMessageBox.critical(self, "Search Error", f"An error occurred during search: {e}")
            return
            
        if results:
            dialog = SearchResultsDialog(results, query, self)
            dialog.result_selected.connect(self.set_path)
            dialog.exec()
        else:
            QMessageBox.information(self, "Search Results", f"No results found for '{query}'.")

    # --- FIX START: COPY/PASTE METHODS ---
    def copy_selected_items(self):
        """Copies the selected items' paths to the system clipboard."""
        selected_proxy_indexes = self._get_selected_proxy_indexes()
        if not selected_proxy_indexes:
            return

        source_indexes = [self.proxy_model.mapToSource(idx) for idx in selected_proxy_indexes]
        paths = list(set([self.model.filePath(idx.sibling(idx.row(), 0)) for idx in source_indexes]))

        if not paths:
            return

        urls = [QUrl.fromLocalFile(path) for path in paths]
        mime_data = QMimeData()
        mime_data.setUrls(urls)
        QApplication.clipboard().setMimeData(mime_data)
        self.status_message_requested.emit(f"Copied {len(paths)} item(s).")

    def paste_items(self):
        """Pastes items from the clipboard into the current directory."""
        clipboard = QApplication.clipboard()
        mime_data = clipboard.mimeData()

        if not mime_data.hasUrls():
            self.status_message_requested.emit("Nothing to paste.")
            return

        dest_dir = self.current_path
        urls = mime_data.urls()
        total_items = len(urls)

        progress_dialog = OperationProgressDialog(f"Pasting {total_items} items", self)
        progress_dialog.setRange(0, total_items)
        progress_dialog.show()

        for i, url in enumerate(urls):
            QApplication.processEvents()
            if progress_dialog.wasCanceled():
                self.status_message_requested.emit("Paste operation canceled.")
                break

            if url.isLocalFile():
                src_path = url.toLocalFile()
                base_name = os.path.basename(src_path)
                progress_dialog.setLabelText(f"Pasting: {base_name}")
                dest_path = os.path.join(dest_dir, base_name)

                if os.path.normpath(src_path) == os.path.normpath(dest_dir):
                    continue

                if os.path.isdir(src_path) and os.path.normpath(dest_path).startswith(os.path.normpath(src_path)):
                    QMessageBox.warning(self, "Paste Error", f"Cannot copy '{base_name}' into a subdirectory of itself.")
                    continue

                if os.path.exists(dest_path):
                    base, ext = os.path.splitext(base_name)
                    copy_num = 1
                    while os.path.exists(dest_path):
                        dest_path = os.path.join(dest_dir, f"{base} - copy ({copy_num}){ext}")
                        copy_num += 1
                
                try:
                    if os.path.isdir(src_path):
                        shutil.copytree(src_path, dest_path)
                    else:
                        shutil.copy2(src_path, dest_path)
                except Exception as e:
                    QMessageBox.critical(self, "Paste Error", f"Failed to paste '{base_name}':\n{e}")
                    progress_dialog.cancel()
                    break
            
            progress_dialog.setValue(i + 1)
        
        else: # Only runs if the loop completes without a 'break'
            self.status_message_requested.emit("Paste operation complete.")

        progress_dialog.setValue(total_items)
        QTimer.singleShot(150, self.refresh)
    # --- FIX END: COPY/PASTE METHODS ---

    def create_new_folder(self):
        folder_name, ok = QInputDialog.getText(self, "Create New Folder", "Enter new folder name:")
        if ok and folder_name:
            try:
                os.makedirs(os.path.join(self.current_path, folder_name))
                self.refresh()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to create folder: {e}")

    def create_new_file(self):
        file_name, ok = QInputDialog.getText(self, "Create New File", "Enter new file name:")
        if ok and file_name:
            try:
                with open(os.path.join(self.current_path, file_name), 'w') as f:
                    f.write("")
                self.refresh()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to create file: {e}")

    def delete_selected_items(self):
        selected_proxy_indexes = self._get_selected_proxy_indexes()
        if not selected_proxy_indexes: return

        source_indexes = [self.proxy_model.mapToSource(idx) for idx in selected_proxy_indexes]
        paths_to_delete = list(set([self.model.filePath(idx.sibling(idx.row(), 0)) for idx in source_indexes]))
        total_items = len(paths_to_delete)

        reply = QMessageBox.question(self, 'Confirm Deletion',
                                     f"Are you sure you want to permanently delete {total_items} selected item(s)?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, 
                                     QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            progress_dialog = OperationProgressDialog(f"Deleting {total_items} items", self)
            progress_dialog.setRange(0, total_items)
            progress_dialog.show()

            for i, path in enumerate(paths_to_delete):
                QApplication.processEvents()
                if progress_dialog.wasCanceled():
                    self.status_message_requested.emit("Delete operation canceled.")
                    break
                
                base_name = os.path.basename(path)
                progress_dialog.setLabelText(f"Deleting: {base_name}")

                try:
                    if os.path.isdir(path):
                        shutil.rmtree(path)
                    else:
                        os.remove(path)
                except Exception as e:
                    QMessageBox.critical(self, "Deletion Error", f"Failed to delete '{base_name}': {e}")
                    progress_dialog.cancel()
                    break

                progress_dialog.setValue(i + 1)
            
            else: # Only runs if the loop completes without a 'break'
                self.status_message_requested.emit("Delete operation complete.")
            
            progress_dialog.setValue(total_items)
            QTimer.singleShot(150, self.refresh)
            
    def rename_selected_item(self):
        selected_proxy_indexes = self._get_selected_proxy_indexes()
        if not selected_proxy_indexes: return
        
        proxy_index = selected_proxy_indexes[0]
        source_index = self.proxy_model.mapToSource(proxy_index)
        source_index_col0 = source_index.sibling(source_index.row(), 0)
        old_path = self.model.filePath(source_index_col0)
        old_name = os.path.basename(old_path)
        
        new_name, ok = QInputDialog.getText(self, "Rename", "Enter new name:", QLineEdit.EchoMode.Normal, old_name)
        if ok and new_name and new_name != old_name:
            new_path = os.path.join(os.path.dirname(old_path), new_name)
            try:
                os.rename(old_path, new_path)
                self.refresh()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to rename '{old_name}': {e}")

    def show_properties(self, proxy_index):
        if not proxy_index.isValid(): return

        source_index = self.proxy_model.mapToSource(proxy_index)
        source_index_col0 = source_index.sibling(source_index.row(), 0)
        path = self.model.filePath(source_index_col0)
        
        try:
            icon = self.model.fileIcon(source_index_col0)
            dialog = PropertiesDialog(path, icon, self)
            if dialog.exec(): # Accepted
                if dialog.name_changed:
                    self.refresh()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not retrieve properties: {e}")

class Sidebar(QWidget):
    def __init__(self, open_folder_callback, config_manager, parent=None):
        super().__init__(parent)
        self.setObjectName("Sidebar")
        self.open_folder_callback = open_folder_callback
        self.config_manager = config_manager
        self.init_ui()
        self.load_folders()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)

        # Drives
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
        self.system_tree_view.clicked.connect(self._on_system_drive_activated)
        layout.addWidget(self.system_tree_view)
        
        # Added Folders
        self.added_folders_label = QLabel("Favorite Folders")
        self.added_folders_label.setStyleSheet("font-weight: bold; margin-top: 10px; margin-bottom: 5px;")
        layout.addWidget(self.added_folders_label)

        button_layout = QHBoxLayout()
        self.add_folder_button = QToolButton()
        self.add_folder_button.setIcon(create_icon("add_folder"))
        self.add_folder_button.setToolTip("Add folder to favorites")
        self.add_folder_button.clicked.connect(self.select_folder)
        button_layout.addWidget(self.add_folder_button)

        self.remove_folder_button = QToolButton()
        self.remove_folder_button.setIcon(create_icon("remove_folder"))
        self.remove_folder_button.setToolTip("Remove selected folder from favorites")
        self.remove_folder_button.clicked.connect(self.remove_folder)
        button_layout.addWidget(self.remove_folder_button)
        button_layout.addStretch()
        layout.addLayout(button_layout)


        self.folder_list_widget = QListWidget(self)
        self.folder_list_widget.itemClicked.connect(self._on_folder_clicked)
        self.folder_list_widget.setObjectName("FolderList")
        layout.addWidget(self.folder_list_widget)

        layout.addStretch()

    def load_folders(self):
        self.folder_list_widget.clear()
        folders = self.config_manager.get("added_folders", [])
        for folder in folders:
            self.folder_list_widget.addItem(folder)

    def _on_system_drive_activated(self, index):
        path = self.file_system_model.filePath(index)
        if os.path.isdir(path):
            self.open_folder_callback(path)

    def select_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder to Add")
        if folder_path:
            if self.config_manager.add_to_list("added_folders", folder_path):
                self.load_folders()

    def remove_folder(self):
        current_item = self.folder_list_widget.currentItem()
        if not current_item:
            QMessageBox.warning(self, "Remove Folder", "Please select a folder to remove.")
            return

        folder_path = current_item.text()
        reply = QMessageBox.question(self, 'Confirm Removal',
                                     f"Are you sure you want to remove '{os.path.basename(folder_path)}' from favorites?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            if self.config_manager.remove_from_list("added_folders", folder_path):
                self.load_folders()

    def _on_folder_clicked(self, item):
        self.open_folder_callback(item.text())


class TabManager(QWidget):
    current_tab_changed = Signal(object)

    def __init__(self, config_manager, parent=None):
        super().__init__(parent)
        self.config_manager = config_manager
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.currentChanged.connect(self._on_tab_change)
        
        # Set close icon for tabs using QSS trick
        close_icon_path = "close_icon_temp.png"
        create_icon("close").pixmap(QSize(16, 16)).save(close_icon_path)
        self.tabs.setStyleSheet(f"QTabBar::close-button {{ image: url({close_icon_path}); }} QTabBar::close-button:hover {{ background-color: #e74c3c; border-radius: 8px; }}")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.tabs)
        self.setLayout(layout)

        self.logger = ShrineLogger()
        self.add_tab("Home", folder_path=None)
        
        # Clean up temp icon file
        if os.path.exists(close_icon_path):
            # This is a bit of a hack. Ideally, use QRC resources.
            # For a single file script, this is a workaround.
            # It might not delete immediately if in use, but will eventually.
            QTimer.singleShot(1000, lambda: os.remove(close_icon_path))


    def _on_tab_change(self, index):
        self.current_tab_changed.emit(self.tabs.widget(index))

    def add_tab(self, label, folder_path=None):
        icon = create_icon("tab_glyph")
        try:
            file_view = FileView(self.config_manager, folder_path)
            index = self.tabs.addTab(file_view, icon, label)
            self.tabs.setCurrentIndex(index)
            self.tabs.setTabToolTip(index, folder_path or QDir.homePath())
            self.logger.ritual("📂", "open_tab", label)
        except Exception as e:
            ErrorHandler().handle(e, context=f"TabManager:add_tab({label})")

    def close_tab(self, index):
        if self.tabs.count() > 1:
            widget = self.tabs.widget(index)
            if widget:
                widget.deleteLater()
            self.tabs.removeTab(index)
            self.logger.log(f"Tab index {index} closed", tag="tab-close")
        else:
            QApplication.instance().quit()


    def current_widget(self):
        return self.tabs.currentWidget()
        
    def update_current_tab_label(self, path):
        index = self.tabs.currentIndex()
        if index != -1:
            label = os.path.basename(path) or os.path.normpath(path)
            self.tabs.setTabText(index, label)
            self.tabs.setTabToolTip(index, path)

class TitleBar(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent_window = parent
        self.setObjectName("TitleBar")
        self.pressing = False
        self.start_pos = None

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.icon_label = QLabel()
        self.icon_label.setPixmap(create_icon("app_icon").pixmap(QSize(20, 20)))
        layout.addWidget(self.icon_label)
        
        self.title_label = QLabel(parent.windowTitle())
        self.title_label.setObjectName("TitleLabel")
        layout.addWidget(self.title_label)

        layout.addStretch()

        self.minimize_button = QToolButton(self)
        self.minimize_button.setIcon(create_icon("minimize"))
        self.minimize_button.clicked.connect(self.parent_window.showMinimized)
        layout.addWidget(self.minimize_button)

        self.maximize_button = QToolButton(self)
        self.maximize_button.setIcon(create_icon("maximize"))
        self.maximize_button.clicked.connect(self.toggle_maximize)
        layout.addWidget(self.maximize_button)

        self.close_button = QToolButton(self)
        self.close_button.setObjectName("CloseButton")
        self.close_button.setIcon(create_icon("close"))
        self.close_button.clicked.connect(self.parent_window.close)
        layout.addWidget(self.close_button)

        self.setLayout(layout)
        self.setFixedHeight(32)

    def toggle_maximize(self):
        if self.parent_window.isMaximized():
            self.parent_window.showNormal()
            self.maximize_button.setIcon(create_icon("maximize"))
        else:
            self.parent_window.showMaximized()
            self.maximize_button.setIcon(create_icon("restore"))
            
    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.pressing = True
            self.start_pos = event.globalPosition().toPoint() - self.parent_window.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.pressing:
            self.parent_window.move(event.globalPosition().toPoint() - self.start_pos)
            event.accept()

    def mouseReleaseEvent(self, event: QMouseEvent):
        self.pressing = False
        self.start_pos = None

    def mouseDoubleClickEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.toggle_maximize()
        super().mouseDoubleClickEvent(event)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.WindowTitleChange:
            self.title_label.setText(self.parent_window.windowTitle())
        return super().eventFilter(obj, event)

class SearchResultsDialog(QDialog):
    result_selected = Signal(str)

    def __init__(self, results, query, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Search Results for '{query}'")
        self.setMinimumSize(600, 400)

        layout = QVBoxLayout(self)
        
        info_label = QLabel(f"Found {len(results)} item(s):")
        layout.addWidget(info_label)

        self.list_widget = QListWidget()
        self.list_widget.addItems(results)
        self.list_widget.itemDoubleClicked.connect(self._on_item_double_clicked)
        layout.addWidget(self.list_widget)
        
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        
    # --- FIX START: SEARCH RESULT ACTION ---
    def _on_item_double_clicked(self, item):
        """
        Handles double-clicking a search result.
        - If it's a file, opens it with the default system application.
        - If it's a directory, navigates the main view to that directory.
        """
        full_path = item.text()
        if os.path.isdir(full_path):
            # If it's a directory, just navigate to it
            self.result_selected.emit(full_path)
        else:
            # If it's a file, open it with the default application
            QDesktopServices.openUrl(QUrl.fromLocalFile(full_path))
            # And navigate the main view to its containing folder for context
            self.result_selected.emit(os.path.dirname(full_path))
        self.accept()
    # --- FIX END: SEARCH RESULT ACTION ---

class PropertiesDialog(QDialog):
    def __init__(self, path, icon, parent=None):
        super().__init__(parent)
        self.path = path
        self.icon = icon
        self.file_info = QFileInfo(path)
        self.original_name = self.file_info.fileName()
        self.name_changed = False
        
        self.setWindowTitle(f"Properties: {self.original_name}")
        self.setMinimumWidth(450)
        
        self._init_ui()
        self._populate_data()

    def _init_ui(self):
        main_layout = QVBoxLayout(self)
        
        # Top section: Icon and Name
        top_layout = QHBoxLayout()
        icon_label = QLabel()
        icon_label.setPixmap(self.icon.pixmap(QSize(48, 48)))
        self.name_edit = QLineEdit(self.original_name)
        
        top_layout.addWidget(icon_label)
        top_layout.addWidget(self.name_edit)
        main_layout.addLayout(top_layout)
        
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        main_layout.addWidget(line)
        
        # Details section
        self.form_layout = QFormLayout()
        self.form_layout.setSpacing(10)
        self.form_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.addLayout(self.form_layout)
        
        main_layout.addStretch()
        
        # Buttons
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        main_layout.addWidget(button_box)

    def _populate_data(self):
        # Type
        if self.file_info.isDir():
            type_desc = "File Folder"
        else:
            type_desc = f"{self.file_info.suffix().upper()} File" if self.file_info.suffix() else "File"
        self.form_layout.addRow("Type:", QLabel(type_desc))
        
        # Location
        location = os.path.dirname(self.file_info.absoluteFilePath())
        location_label = QLabel(location)
        location_label.setWordWrap(True)
        self.form_layout.addRow("Location:", location_label)
        
        # Size
        if self.file_info.isDir():
            size_bytes = _get_folder_size(self.path)
        else:
            size_bytes = self.file_info.size()
        size_formatted = f"{_format_size(size_bytes)} ({size_bytes:,} bytes)"
        self.form_layout.addRow("Size:", QLabel(size_formatted))
        
        # Contains (for folders)
        if self.file_info.isDir():
            num_files, num_folders = _get_folder_contents_count(self.path)
            contains_str = f"{num_files} files, {num_folders} folders"
            self.form_layout.addRow("Contains:", QLabel(contains_str))
            
        # Dates
        try:
            stat_info = os.stat(self.path)
            created_date = datetime.fromtimestamp(stat_info.st_ctime).strftime("%d %B %Y, %H:%M:%S")
            modified_date = datetime.fromtimestamp(stat_info.st_mtime).strftime("%d %B %Y, %H:%M:%S")
            accessed_date = datetime.fromtimestamp(stat_info.st_atime).strftime("%d %B %Y, %H:%M:%S")
            
            self.form_layout.addRow("Created:", QLabel(created_date))
            self.form_layout.addRow("Modified:", QLabel(modified_date))
            self.form_layout.addRow("Accessed:", QLabel(accessed_date))
        except Exception:
             # Fallback for dates if os.stat fails
             self.form_layout.addRow("Modified:", QLabel(self.file_info.lastModified().toString("dd MMMM yyyy, hh:mm:ss")))

    def accept(self):
        new_name = self.name_edit.text()
        if new_name and new_name != self.original_name:
            new_path = os.path.join(os.path.dirname(self.path), new_name)
            if os.path.exists(new_path):
                QMessageBox.critical(self, "Error", f"An item named '{new_name}' already exists in this location.")
                return
            try:
                os.rename(self.path, new_path)
                self.name_changed = True
            except Exception as e:
                QMessageBox.critical(self, "Rename Error", f"Failed to rename to '{new_name}':\n{e}")
                return
        super().accept()

class OperationProgressDialog(QProgressDialog):
    """A custom progress dialog for file operations."""
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setWindowModality(Qt.WindowModality.WindowModal)
        self.setMinimumDuration(0)  # Show immediately
        self.setCancelButtonText("Cancel")
        self.setValue(0)
        self.setAutoClose(True)  # DIPERBAIKI: Otomatis tutup saat selesai
        self.setAutoReset(True)  # DIPERBAIKI: Otomatis reset setelah ditutup

        # Apply dark theme styles directly to ensure consistency
        self.setStyleSheet("""
            QProgressDialog {
                background-color: #3a3a3a;
                color: #e0e0e0;
                border: 1px solid #4a4a4a;
                border-radius: 8px;
            }
            QProgressDialog QLabel {
                color: #e0e0e0;
                padding: 5px;
            }
            QProgressBar {
                background-color: #2e2e2e;
                border: 1px solid #5a5a5a;
                border-radius: 4px;
                text-align: center;
                color: #e0e0e0;
            }
            QProgressBar::chunk {
                background-color: #007acc;
                border-radius: 4px;
            }
            QPushButton {
                background-color: #4a4a4a;
                border: 1px solid #5a5a5a;
                color: #ffffff;
                min-width: 80px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #5a5a5a;
            }
        """)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Macan Explorer")
        self.setMinimumSize(1000, 600)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setWindowIcon(create_icon("app_icon"))

        # Central frame to apply border
        self.central_frame = QFrame(self)
        self.central_frame.setObjectName("CentralFrame")
        self.central_frame.setStyleSheet("#CentralFrame { border: 1px solid #5a5a5a; }")
        super().setCentralWidget(self.central_frame)
        
        self.main_layout = QVBoxLayout(self.central_frame)
        self.main_layout.setContentsMargins(1, 1, 1, 1) # Match border width
        self.main_layout.setSpacing(0)

        # Custom Title Bar
        self.title_bar = TitleBar(self)
        self.installEventFilter(self.title_bar)
        self.main_layout.addWidget(self.title_bar)

        # Core Components
        self.errors = ErrorHandler()
        self.logger = ShrineLogger()
        self.config_manager = ConfigManager()

        # UI Components
        self.sidebar = Sidebar(self.open_folder_from_sidebar, self.config_manager)
        self.tab_manager = TabManager(self.config_manager, self)
        self.toolbar = CommandBar(self)
        
        self.status = QStatusBar()
        self.status.addWidget(QLabel("🛕 Shrine ready to explore..."))

        # Layout
        container = QWidget()
        content_layout = QVBoxLayout(container)
        content_layout.setContentsMargins(5, 5, 5, 5)
        content_layout.setSpacing(5)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(self.sidebar)
        splitter.addWidget(self.tab_manager)
        splitter.setSizes([200, 800])
        splitter.setHandleWidth(4)

        content_layout.addWidget(self.toolbar)
        content_layout.addWidget(splitter)
        
        self.main_layout.addWidget(container)
        self.setStatusBar(self.status)

        self.connect_signals()
        self.connect_active_tab_signals(self.tab_manager.current_widget())
        
        # Track window state for resizing
        self._is_maximized = False
        self._old_pos = None
        self._old_size = None

    def connect_signals(self):
        # Toolbar -> Main Window/Active Tab
        self.toolbar.back_requested.connect(lambda: self.call_active_view_method('go_back'))
        self.toolbar.forward_requested.connect(lambda: self.call_active_view_method('go_forward'))
        self.toolbar.up_requested.connect(lambda: self.call_active_view_method('go_up'))
        self.toolbar.refresh_requested.connect(lambda: self.call_active_view_method('refresh'))
        self.toolbar.address_submitted.connect(self.on_address_bar_submit)
        self.toolbar.view_mode_changed.connect(self.handle_view_change)
        self.toolbar.search_requested.connect(lambda query: self.call_active_view_method('search_files', query))
        self.toolbar.new_folder_requested.connect(lambda: self.call_active_view_method('create_new_folder'))
        self.toolbar.new_file_requested.connect(lambda: self.call_active_view_method('create_new_file'))
        self.toolbar.delete_item_requested.connect(lambda: self.call_active_view_method('delete_selected_items'))
        self.toolbar.rename_item_requested.connect(lambda: self.call_active_view_method('rename_selected_item'))
        self.toolbar.action_open_new_window.triggered.connect(self.open_new_window)
        self.toolbar.action_about.triggered.connect(self.show_about_dialog)
        
        # Tab Manager -> Main Window
        self.tab_manager.current_tab_changed.connect(self.connect_active_tab_signals)


    def connect_active_tab_signals(self, tab_widget):
        if not isinstance(tab_widget, FileView):
            self.toolbar.set_address_path("")
            self.toolbar.set_navigation_enabled(False, False)
            return

        # Disconnect old signals if any to prevent multiple connections
        try:
            if hasattr(self, '_active_tab_widget') and self._active_tab_widget:
                self._active_tab_widget.path_changed.disconnect()
                self._active_tab_widget.navigation_state_changed.disconnect()
                self._active_tab_widget.status_message_requested.disconnect()
        except (TypeError, RuntimeError):
            pass # Ignore errors if signals were not connected

        self._active_tab_widget = tab_widget
        tab_widget.path_changed.connect(self.toolbar.set_address_path)
        tab_widget.path_changed.connect(self.tab_manager.update_current_tab_label)
        tab_widget.navigation_state_changed.connect(self.toolbar.set_navigation_enabled)
        tab_widget.status_message_requested.connect(self.update_status_bar) # For copy/paste status

        # --- FIX START: VIEW PERSISTENCE ---
        # Apply the globally saved view mode to the newly active tab and the toolbar
        saved_mode = self.config_manager.get('view_mode', 'details')
        self.toolbar.set_view_mode(saved_mode)    # Update toolbar buttons
        tab_widget.set_view_mode(saved_mode)      # Update the view itself
        # --- FIX END: VIEW PERSISTENCE ---

        # Update UI with current tab's state
        self.toolbar.set_address_path(tab_widget.current_path)
        tab_widget._update_navigation_state()
        self.tab_manager.update_current_tab_label(tab_widget.current_path)


    def on_address_bar_submit(self, path):
        self.call_active_view_method('set_path', path)

    def call_active_view_method(self, method_name, *args):
        current_tab_widget = self.tab_manager.current_widget()
        if current_tab_widget and hasattr(current_tab_widget, method_name):
            method = getattr(current_tab_widget, method_name)
            if callable(method):
                method(*args)

    # --- FIX START: VIEW PERSISTENCE ---
    def handle_view_change(self, mode):
        """Applies the view change to the active tab and saves it to config."""
        self.call_active_view_method('set_view_mode', mode)
        self.config_manager.set('view_mode', mode) # Save the setting globally
    # --- FIX END: VIEW PERSISTENCE ---

    # --- FIX START: COPY/PASTE STATUS ---
    def update_status_bar(self, message):
        """Shows a message on the status bar for a few seconds."""
        self.status.showMessage(message, 3000) # Show for 3 seconds
    # --- FIX END: COPY/PASTE STATUS ---

    def open_folder_from_sidebar(self, folder_path):
        if not folder_path: return
        tab_label = os.path.basename(folder_path) or os.path.normpath(folder_path)
        self.tab_manager.add_tab(tab_label, folder_path)
        self.logger.ritual("📂", "open", folder_path)
        self.status.showMessage(f"Shrine opened: {folder_path}", 4000)

    def open_new_window(self):
        self.new_window = MainWindow()
        self.new_window.show()
        self.logger.ritual("✨", "new_window", "created")

    def show_about_dialog(self):
        QMessageBox.about(self, "About Macan Explorer", """<h3>Macan Explorer 🐅 v2.2.0</h3><p>Copyright © 2025 Danx Exodus.</p><p>Macan Explorer is a modern file management application designed with developers, creators, and power users in mind. Inspired by the elegance of Windows 11 Explorer and reimagined through the lens of simplicity, speed, and control — Macan Explorer brings a custom, dark-themed interface with powerful features like multi-tab navigation, smart address bar, and thumbnail previews. Built as part of the Macan Angkasa ecosystem, it’s more than just a file viewer — it’s a productivity companion crafted to support deep focus, efficient workflow, and visual clarity.</p>""")
        self.logger.ritual("ℹ️", "about", "dialog_shown")


# --- MAIN EXECUTION ---

def setup_logging():
    log_dir = os.path.join(os.path.expanduser("~"), ".macan_explorer", "logs")
    os.makedirs(log_dir, exist_ok=True)

    shrine_log_file = os.path.join(log_dir, "shrine_ritual_log.txt")
    error_log_file = os.path.join(log_dir, "error_log.txt")

    # Use rotating file handlers to prevent log files from growing indefinitely
    from logging.handlers import RotatingFileHandler
    shrine_file_handler = RotatingFileHandler(shrine_log_file, maxBytes=1048576, backupCount=5, encoding='utf-8')
    shrine_file_handler.setLevel(logging.INFO)

    error_file_handler = RotatingFileHandler(error_log_file, maxBytes=1048576, backupCount=5, encoding='utf-8')
    error_file_handler.setLevel(logging.ERROR)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
        handlers=[shrine_file_handler, error_file_handler, console_handler]
    )
    logging.getLogger('core.error_handler').setLevel(logging.ERROR)
    logging.getLogger('core.logger').setLevel(logging.INFO)

# --- MODIFIKASI START: Fungsi check_for_ffmpeg dihapus dan diganti dengan check_for_opencv ---
def check_for_opencv():
    """Memeriksa apakah OpenCV terinstal dan mengatur flag global."""
    if OPENCV_AVAILABLE:
        logging.info("Pustaka OpenCV ditemukan. Thumbnail video diaktifkan.")
    else:
        logging.warning("Pustaka OpenCV (cv2) tidak ditemukan. Thumbnail video akan dinonaktifkan.")
        logging.warning("Untuk mengaktifkan thumbnail video, silakan instal dengan menjalankan: pip install opencv-python")
# --- MODIFIKASI END ---

def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(THEME_QSS)
    
    setup_logging()
    # --- MODIFIKASI START: Memanggil fungsi check_for_opencv ---
    check_for_opencv()
    # --- MODIFIKASI END ---

    window = MainWindow()
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()