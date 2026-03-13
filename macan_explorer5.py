#!/usr/bin/env python3
"""
Macan Explorer v5.0 — Enterprise Edition
An enterprise-grade file management application built with PySide6.
Features: multi-tab navigation, activity log, breadcrumb bar, smart rename,
          bookmark manager, preview panel, theme switching (dark/light),
          keyboard shortcuts, terminal integration, and more.

Copyright © 2026 Danx Exodus - Macan Angkasa.
"""

import sys
import os
import re
import json
import shutil
import logging
import platform
import subprocess
import traceback
import math
import mimetypes
import datetime
import hashlib
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional, List, Dict

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
    QFormLayout, QProgressDialog, QFileSystemModel, QTextEdit, QPlainTextEdit,
    QScrollArea, QGroupBox, QComboBox, QCheckBox, QTableView, QHeaderView,
    QAbstractItemView, QMenuBar, QDockWidget, QProgressBar, QStyledItemDelegate,
    QTabBar, QSpacerItem, QGridLayout, QFileIconProvider, QScrollArea
)
from PySide6.QtCore import (
    Qt, QSize, Signal, QDir, QUrl, QFileInfo, QSortFilterProxyModel,
    QModelIndex, QPoint, QRect, QEvent, QTimer, QMimeData, QObject,
    QRunnable, QThreadPool, Slot, QFileSystemWatcher, QSettings,
    QStandardPaths, QAbstractTableModel, QDateTime, QItemSelectionModel
)
from PySide6.QtGui import (
    QAction, QIcon, QActionGroup, QDesktopServices, QPixmap,
    QPainter, QMouseEvent, QColor, QKeySequence, QFont, QFontMetrics,
    QStandardItemModel, QStandardItem, QDrag, QCursor, QBrush, QPen
)
from PySide6.QtSvg import QSvgRenderer


# ─────────────────────────────────────────────────────────────────────────────
#  SVG ICONS
# ─────────────────────────────────────────────────────────────────────────────

SVG_ICONS = {
    "app_icon": """<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M4 6C4 4.89543 4.89543 4 6 4H18C19.1046 4 20 4.89543 20 6V18C20 19.1046 19.1046 20 18 20H6C4.89543 20 4 19.1046 4 18V6Z" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M12 4V20" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M4 12H20" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>""",
    "back": """<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M19 12H5" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M12 19L5 12L12 5" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>""",
    "forward": """<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M5 12H19" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M12 5L19 12L12 19" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>""",
    "up": """<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M12 19V5" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M5 12L12 5L19 12" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>""",
    "refresh": """<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M23 4V10H17" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M20.49 15C19.82 18.23 16.94 20.5 13.5 20.5C9.36 20.5 6 17.14 6 13C6 8.86 9.36 5.5 13.5 5.5C15.48 5.5 17.24 6.3 18.5 7.5L23 3" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>""",
    "search": """<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M11 19C15.4183 19 19 15.4183 19 11C19 6.58172 15.4183 3 11 3C6.58172 3 3 6.58172 3 11C3 15.4183 6.58172 19 11 19Z" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M21 21L16.65 16.65" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>""",
    "view_details": """<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M8 6H21" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M8 12H21" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M8 18H21" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M3 6H3.01" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M3 12H3.01" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M3 18H3.01" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>""",
    "view_list": """<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M3 12H21" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M3 6H21" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M3 18H21" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>""",
    "view_icons": """<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><rect x="4" y="4" width="6" height="6" rx="1" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><rect x="14" y="4" width="6" height="6" rx="1" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><rect x="4" y="14" width="6" height="6" rx="1" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><rect x="14" y="14" width="6" height="6" rx="1" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>""",
    "folder-closed": """<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M22 11V6C22 4.89543 21.1046 4 20 4H12L10 2H4C2.89543 2 2 2.89543 2 4V18C2 19.1046 2.89543 20 4 20H12" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>""",
    "new_file": """<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M14 2H6C5.46957 2 4.96086 2.21071 4.58579 2.58579C4.21071 2.96086 4 3.46957 4 4V20C4 20.5304 4.21071 21.0391 4.58579 21.4142C4.96086 21.7893 5.46957 22 6 22H18C18.5304 22 19.0391 21.7893 19.4142 21.4142C19.7893 21.0391 20 20.5304 20 20V8L14 2Z" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M14 2V8H20" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M12 18V12" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M9 15H15" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>""",
    "rename": """<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M20 16.5L16.5 20L13 16.5" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M16.5 20V4H6.5C5.96957 4 5.46086 4.21071 5.08579 4.58579C4.71071 4.96086 4.5 5.46957 4.5 6V11" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>""",
    "delete": """<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M3 6H5H21" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M8 6V4C8 3.46957 8.21071 2.96086 8.58579 2.58579C8.96086 2.21071 9.46957 2 10 2H14C14.5304 2 15.0391 2.21071 15.4142 2.58579C15.7893 2.96086 16 3.46957 16 4V6M19 6V20C19 20.5304 18.7893 21.0391 18.4142 21.4142C18.0391 21.7893 17.5304 22 17 22H7C6.46957 22 5.96086 21.7893 5.58579 21.4142C5.21071 21.0391 5 20.5304 5 20V6H19Z" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>""",
    "more-horizontal": """<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><circle cx="12" cy="12" r="1.5" fill="#e0e0e0"/><circle cx="19" cy="12" r="1.5" fill="#e0e0e0"/><circle cx="5" cy="12" r="1.5" fill="#e0e0e0"/></svg>""",
    "new_window": """<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M14 2H6C4.89543 2 4 2.89543 4 4V20C4 21.1046 4.89543 22 6 22H18C19.1046 22 20 21.1046 20 20V8L14 2Z" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>""",
    "about": """<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M12 22C17.5228 22 22 17.5228 22 12C22 6.47715 17.5228 2 12 2C6.47715 2 2 6.47715 2 12C2 17.5228 6.47715 22 12 22Z" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M12 16V12" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M12 8H12.01" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>""",
    "add_folder": """<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M20 12H12M12 12H4M12 12V4M12 12V20" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round"/></svg>""",
    "remove_folder": """<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M20 12H4" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round"/></svg>""",
    "tab_glyph": """<svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M4 7V17C4 18.1046 4.89543 19 6 19H18C19.1046 19 20 18.1046 20 17V7" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M2 7H22" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>""",
    "minimize": """<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M5 12H19" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>""",
    "maximize": """<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><rect x="5" y="5" width="14" height="14" rx="2" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>""",
    "restore": """<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M8 16H4V4H16V8" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M8 12H20V20H8V12Z" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>""",
    "close": """<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M18 6L6 18" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M6 6L18 18" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>""",
    "terminal": """<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><polyline points="4 17 10 11 4 5" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><line x1="12" y1="19" x2="20" y2="19" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>""",
    "bookmark": """<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M19 21L12 16L5 21V5C5 4.46957 5.21071 3.96086 5.58579 3.58579C5.96086 3.21071 6.46957 3 7 3H17C17.5304 3 18.0391 3.21071 18.4142 3.58579C18.7893 3.96086 19 4.46957 19 5V21Z" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>""",
    "bookmark_filled": """<svg width="24" height="24" viewBox="0 0 24 24" fill="#7C3AED" xmlns="http://www.w3.org/2000/svg"><path d="M19 21L12 16L5 21V5C5 3.89543 5.89543 3 7 3H17C18.1046 3 19 3.89543 19 5V21Z" stroke="#7C3AED" stroke-width="2"/></svg>""",
    "theme_dark": """<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>""",
    "theme_light": """<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><circle cx="12" cy="12" r="5" stroke="#e0e0e0" stroke-width="2"/><line x1="12" y1="1" x2="12" y2="3" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round"/><line x1="12" y1="21" x2="12" y2="23" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round"/><line x1="1" y1="12" x2="3" y2="12" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round"/><line x1="21" y1="12" x2="23" y2="12" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round"/></svg>""",
    "cut": """<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><circle cx="6" cy="20" r="2" stroke="#e0e0e0" stroke-width="2"/><circle cx="6" cy="4" r="2" stroke="#e0e0e0" stroke-width="2"/><line x1="8.12" y1="18.12" x2="20" y2="4" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round"/><line x1="20" y1="20" x2="8.12" y2="5.88" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round"/><line x1="14.5" y1="12.5" x2="20" y2="12" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round"/></svg>""",
    "copy": """<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><rect x="9" y="9" width="13" height="13" rx="2" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M5 15H4C2.89543 15 2 14.1046 2 13V4C2 2.89543 2.89543 2 4 2H13C14.1046 2 15 2.89543 15 4V5" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>""",
    "paste": """<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M16 4H18C18.5304 4 19.0391 4.21071 19.4142 4.58579C19.7893 4.96086 20 5.46957 20 6V20C20 20.5304 19.7893 21.0391 19.4142 21.4142C19.0391 21.7893 18.5304 22 18 22H6C5.46957 22 4.96086 21.7893 4.58579 21.4142C4.21071 21.0391 4 20.5304 4 20V6C4 5.46957 4.21071 4.96086 4.58579 4.58579C4.96086 4.21071 5.46957 4 6 4H8" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><rect x="8" y="2" width="8" height="4" rx="1" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>""",
    "log": """<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M14 2H6C5.46957 2 4.96086 2.21071 4.58579 2.58579C4.21071 2.96086 4 3.46957 4 4V20C4 20.5304 4.21071 21.0391 4.58579 21.4142C4.96086 21.7893 5.46957 22 6 22H18C18.5304 22 19.0391 21.7893 19.4142 21.4142C19.7893 21.0391 20 20.5304 20 20V8L14 2Z" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><polyline points="16 17 12 13 8 17" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><line x1="12" y1="13" x2="12" y2="21" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round"/></svg>""",
    "play_overlay": """<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><circle cx="12" cy="12" r="10" fill="#00000088"/><path d="M10 8L16 12L10 16V8Z" fill="#ffffff"/></svg>""",
    "home": """<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M3 9L12 2L21 9V20C21 20.5304 20.7893 21.0391 20.4142 21.4142C20.0391 21.7893 19.5304 22 19 22H5C4.46957 22 3.96086 21.7893 3.58579 21.4142C3.21071 21.0391 3 20.5304 3 20V9Z" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><polyline points="9 22 9 12 15 12 15 22" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>""",
    "desktop": """<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><rect x="2" y="3" width="20" height="14" rx="2" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><line x1="8" y1="21" x2="16" y2="21" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><line x1="12" y1="17" x2="12" y2="21" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>""",
    "downloads": """<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M21 15V19C21 19.5304 20.7893 20.0391 20.4142 20.4142C20.0391 20.7893 19.5304 21 19 21H5C4.46957 21 3.96086 20.7893 3.58579 20.4142C3.21071 20.0391 3 19.5304 3 19V15" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><polyline points="7 10 12 15 17 10" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><line x1="12" y1="15" x2="12" y2="3" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>""",
    "drive": """<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><ellipse cx="12" cy="5" rx="9" ry="3" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M21 12C21 13.66 16.97 15 12 15C7.03 15 3 13.66 3 12" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M3 5V19C3 20.66 7.03 22 12 22C16.97 22 21 20.66 21 19V5" stroke="#e0e0e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>""",
    "settings": """<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><circle cx="12" cy="12" r="3" stroke="#e0e0e0" stroke-width="2"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z" stroke="#e0e0e0" stroke-width="2"/></svg>""",
}


def get_overlay_icon(size=24):
    renderer = QSvgRenderer(SVG_ICONS["play_overlay"].encode('utf-8'))
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    renderer.render(painter)
    painter.end()
    return pixmap


# SVG stroke color per theme — dark uses light strokes, light uses dark strokes
_ICON_COLORS = {
    "dark":  "#e0e0e0",   # existing light-gray for dark bg
    "light": "#374151",   # dark-gray for light bg
}

def create_icon(key, color=None, theme=None):
    """Creates a QIcon from embedded SVG data with optional color / theme override."""
    if key not in SVG_ICONS:
        return QIcon()
    svg_data = SVG_ICONS[key]
    # Determine stroke color: explicit color > theme > keep original (#e0e0e0)
    stroke = color or ((_ICON_COLORS.get(theme)) if theme else None)
    if stroke:
        svg_data = svg_data.replace('#e0e0e0', stroke)
    renderer = QSvgRenderer(svg_data.encode('utf-8'))
    pixmap = QPixmap(24, 24)
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    renderer.render(painter)
    painter.end()
    return QIcon(pixmap)


# ─────────────────────────────────────────────────────────────────────────────
#  THEME SYSTEM
# ─────────────────────────────────────────────────────────────────────────────

DARK_THEME_QSS = """
/* ── GLOBAL ─────────────────────────────────────────── */
* {
    font-family: "Segoe UI", "SF Pro Display", "Ubuntu", sans-serif;
    font-size: 13px;
    outline: none;
}
QMainWindow, QDialog {
    background-color: #0F1117;
}
QWidget {
    background-color: #0F1117;
    color: #E2E8F0;
}

/* ── TITLEBAR ─────────────────────────────────────────── */
TitleBar {
    background-color: #0A0D14;
    border-bottom: 1px solid #1E2235;
}
TitleBar #TitleLabel {
    color: #CBD5E1;
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 0.5px;
    padding-left: 8px;
}
TitleBar QToolButton {
    background-color: transparent;
    border: none;
    padding: 5px 7px;
    border-radius: 4px;
    color: #94A3B8;
    icon-size: 14px;
}
TitleBar QToolButton:hover {
    background-color: #1E2435;
    color: #E2E8F0;
}
TitleBar QToolButton#CloseButton:hover {
    background-color: #DC2626;
    color: #ffffff;
}

/* ── MENUBAR ─────────────────────────────────────────── */
QMenuBar {
    background-color: #0A0D14;
    color: #CBD5E1;
    border-bottom: 1px solid #1E2235;
    padding: 2px 0px;
    font-size: 13px;
}
QMenuBar::item {
    background: transparent;
    padding: 5px 12px;
    border-radius: 4px;
}
QMenuBar::item:selected, QMenuBar::item:pressed {
    background-color: #1E2435;
    color: #A78BFA;
}

/* ── MENUS ───────────────────────────────────────────── */
QMenu {
    background-color: #131622;
    border: 1px solid #1E2435;
    border-radius: 8px;
    padding: 4px;
    color: #E2E8F0;
}
QMenu::item {
    padding: 7px 20px 7px 12px;
    border-radius: 5px;
    margin: 1px 2px;
    font-size: 13px;
}
QMenu::item:selected {
    background-color: #1E2435;
    color: #A78BFA;
}
QMenu::separator {
    height: 1px;
    background-color: #1E2235;
    margin: 4px 8px;
}
QMenu::indicator {
    width: 16px;
    height: 16px;
}

/* ── TOOLBAR ─────────────────────────────────────────── */
QToolBar {
    background-color: #0D1018;
    border: none;
    border-bottom: 1px solid #1A1D2E;
    spacing: 3px;
    padding: 4px 8px;
}
QToolBar::separator {
    width: 1px;
    background-color: #1E2235;
    margin: 4px 6px;
}
QToolButton {
    background-color: transparent;
    border: 1px solid transparent;
    border-radius: 6px;
    padding: 5px 7px;
    color: #94A3B8;
    icon-size: 18px;
}
QToolButton:hover {
    background-color: #1E2435;
    border-color: #2D3748;
    color: #E2E8F0;
}
QToolButton:pressed {
    background-color: #253048;
}
QToolButton:checked {
    background-color: #1E1938;
    border-color: #7C3AED;
    color: #A78BFA;
}
QToolButton:disabled {
    color: #374151;
}

/* ── STATUSBAR ───────────────────────────────────────── */
QStatusBar {
    background-color: #0A0D14;
    border-top: 1px solid #1A1D2E;
    color: #64748B;
    padding: 0px 8px;
    font-size: 12px;
}
QStatusBar::item {
    border: none;
}
QStatusBar QLabel {
    color: #64748B;
    font-size: 12px;
    padding: 0 4px;
}

/* ── TREEVIEW ────────────────────────────────────────── */
QTreeView {
    background-color: #0B0E16;
    border: none;
    outline: none;
    selection-background-color: transparent;
    alternate-background-color: #0D1019;
    color: #CBD5E1;
}
QTreeView::item {
    height: 28px;
    padding-left: 4px;
    border-radius: 5px;
    margin: 1px 4px;
}
QTreeView::item:hover {
    background-color: #161B2C;
}
QTreeView::item:selected {
    background-color: #1E2848;
    color: #A78BFA;
}
QTreeView::item:selected:hover {
    background-color: #243055;
}
QTreeView::branch {
    background-color: transparent;
}
QHeaderView::section {
    background-color: #0D1018;
    color: #64748B;
    padding: 6px 10px;
    border: none;
    border-right: 1px solid #1A1D2E;
    border-bottom: 1px solid #1A1D2E;
    font-weight: 600;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
QHeaderView::section:hover {
    background-color: #1A1D2E;
    color: #E2E8F0;
}

/* ── TABLEVIEW ───────────────────────────────────────── */
QTableView {
    background-color: #0B0E16;
    border: none;
    outline: none;
    gridline-color: #0F1117;
    selection-background-color: #1E2848;
    selection-color: #E2E8F0;
    alternate-background-color: #0D1019;
    color: #CBD5E1;
}
QTableView::item {
    padding: 4px 8px;
    border-bottom: 1px solid #0F1117;
}
QTableView::item:hover {
    background-color: #161B2C;
}
QTableView::item:selected {
    background-color: #1E2848;
    color: #A78BFA;
}

/* ── LISTWIDGET ──────────────────────────────────────── */
QListWidget {
    background-color: #0B0E16;
    border: none;
    padding: 4px;
    color: #CBD5E1;
    outline: none;
}
QListWidget::item {
    padding: 6px 8px;
    border-radius: 5px;
    margin: 1px 2px;
}
QListWidget::item:selected {
    background-color: #1E2848;
    color: #A78BFA;
}
QListWidget::item:hover {
    background-color: #161B2C;
}

/* ── SCROLLBAR ───────────────────────────────────────── */
QScrollBar:vertical {
    background-color: transparent;
    width: 7px;
    border-radius: 4px;
    margin: 0;
}
QScrollBar::handle:vertical {
    background-color: #1E2435;
    border-radius: 4px;
    min-height: 30px;
}
QScrollBar::handle:vertical:hover {
    background-color: #374151;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
QScrollBar:horizontal {
    background-color: transparent;
    height: 7px;
    border-radius: 4px;
    margin: 0;
}
QScrollBar::handle:horizontal {
    background-color: #1E2435;
    border-radius: 4px;
    min-width: 30px;
}
QScrollBar::handle:horizontal:hover {
    background-color: #374151;
}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal { width: 0; }

/* ── BUTTONS ─────────────────────────────────────────── */
QPushButton {
    background-color: #161C2C;
    border: 1px solid #1E2848;
    border-radius: 7px;
    padding: 7px 16px;
    color: #CBD5E1;
    font-weight: 500;
}
QPushButton:hover {
    background-color: #1E2848;
    border-color: #2D3F6E;
}
QPushButton:pressed {
    background-color: #253055;
}
QPushButton:disabled {
    background-color: #0F1117;
    color: #374151;
    border-color: #1A1D2E;
}
QPushButton#primaryBtn {
    background-color: #5B21B6;
    border: 1px solid #4C1D95;
    color: white;
    font-weight: 600;
}
QPushButton#primaryBtn:hover {
    background-color: #6D28D9;
}
QPushButton#primaryBtn:pressed {
    background-color: #4C1D95;
}
QPushButton#dangerBtn {
    background-color: #7F1D1D;
    border: 1px solid #991B1B;
    color: #FCA5A5;
}
QPushButton#dangerBtn:hover {
    background-color: #991B1B;
}

/* ── LINEEDIT ────────────────────────────────────────── */
QLineEdit {
    background-color: #0D1018;
    border: 1px solid #1E2235;
    border-radius: 7px;
    padding: 6px 12px;
    color: #E2E8F0;
    selection-background-color: #5B21B6;
}
QLineEdit:focus {
    border-color: #7C3AED;
    background-color: #0F1320;
}
QLineEdit#addressBar {
    background-color: #0D1018;
    border: 1px solid #1E2235;
    border-radius: 7px;
    padding: 5px 14px;
    font-family: "Consolas", "Courier New", monospace;
    font-size: 12px;
    color: #A78BFA;
}
QLineEdit#addressBar:focus {
    border-color: #7C3AED;
    color: #E2E8F0;
}

/* ── COMBOBOX ────────────────────────────────────────── */
QComboBox {
    background-color: #0D1018;
    border: 1px solid #1E2235;
    border-radius: 6px;
    padding: 5px 10px;
    color: #CBD5E1;
    min-width: 80px;
}
QComboBox:hover { border-color: #2D3748; }
QComboBox:focus { border-color: #7C3AED; }
QComboBox::drop-down { border: none; width: 24px; }
QComboBox::down-arrow {
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 5px solid #64748B;
}
QComboBox QAbstractItemView {
    background-color: #131622;
    border: 1px solid #1E2435;
    border-radius: 6px;
    selection-background-color: #1E2848;
    color: #CBD5E1;
    padding: 4px;
}

/* ── CHECKBOX ────────────────────────────────────────── */
QCheckBox {
    spacing: 8px;
    color: #94A3B8;
}
QCheckBox::indicator {
    width: 15px;
    height: 15px;
    border-radius: 4px;
    border: 1px solid #374151;
    background-color: #0D1018;
}
QCheckBox::indicator:checked {
    background-color: #7C3AED;
    border-color: #7C3AED;
}

/* ── TEXTEDIT / PLAINTEXTEDIT ──────────────────────── */
QTextEdit, QPlainTextEdit {
    background-color: #080A10;
    border: 1px solid #1E2235;
    border-radius: 6px;
    padding: 8px;
    color: #94A3B8;
    selection-background-color: #5B21B6;
}
QTextEdit:focus, QPlainTextEdit:focus {
    border-color: #7C3AED;
}

/* ── TABWIDGET ───────────────────────────────────────── */
QTabWidget::pane {
    border: 1px solid #1A1D2E;
    border-radius: 8px;
    background-color: #0D1018;
    top: -1px;
}
QTabBar::tab {
    background-color: #0D1018;
    border: 1px solid #1A1D2E;
    border-bottom: none;
    border-radius: 6px 6px 0 0;
    padding: 7px 16px;
    color: #64748B;
    margin-right: 2px;
    font-size: 12px;
}
QTabBar::tab:selected {
    background-color: #0F1320;
    color: #A78BFA;
    border-bottom: 1px solid #0F1320;
}
QTabBar::tab:hover:!selected {
    background-color: #141826;
    color: #94A3B8;
}

/* ── PROGRESSBAR ─────────────────────────────────────── */
QProgressBar {
    border: 1px solid #1E2235;
    border-radius: 5px;
    background-color: #0D1018;
    text-align: center;
    color: #CBD5E1;
    height: 8px;
}
QProgressBar::chunk {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #6D28D9, stop:1 #0891B2);
    border-radius: 4px;
}

/* ── SPLITTER ────────────────────────────────────────── */
QSplitter::handle {
    background-color: #1A1D2E;
    width: 2px;
    height: 2px;
}
QSplitter::handle:hover {
    background-color: #7C3AED;
}

/* ── DOCKWIDGET ──────────────────────────────────────── */
QDockWidget {
    background-color: #0F1117;
    color: #E2E8F0;
    titlebar-close-icon: url(none);
}
QDockWidget::title {
    background-color: #0A0D14;
    border-bottom: 1px solid #1A1D2E;
    padding: 7px 12px;
    font-weight: 700;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    color: #64748B;
}
QDockWidget::close-button, QDockWidget::float-button {
    background: transparent;
    border: none;
    padding: 2px;
    border-radius: 3px;
}
QDockWidget::close-button:hover, QDockWidget::float-button:hover {
    background-color: #1E2435;
}

/* ── GROUPBOX ────────────────────────────────────────── */
QGroupBox {
    border: 1px solid #1E2235;
    border-radius: 8px;
    margin-top: 14px;
    padding-top: 8px;
    color: #64748B;
    font-weight: 700;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.8px;
}
QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 0 8px;
    left: 12px;
    color: #7C3AED;
}

/* ── FRAME ───────────────────────────────────────────── */
QFrame[frameShape="4"], QFrame[frameShape="5"] {
    color: #1E2235;
}

/* ── DIALOG ──────────────────────────────────────────── */
QMessageBox, QDialog {
    background-color: #0F1320;
    color: #E2E8F0;
    border: 1px solid #1E2848;
    border-radius: 10px;
}
QMessageBox QLabel, QDialog QLabel { color: #CBD5E1; }
QMessageBox QPushButton, QDialog QPushButton {
    background-color: #5B21B6;
    border: 1px solid #4C1D95;
    color: white;
    min-width: 80px;
    font-weight: 600;
}
QMessageBox QPushButton:hover, QDialog QPushButton:hover {
    background-color: #6D28D9;
}

/* ── BREADCRUMB ─────────────────────────────────────── */
QWidget#BreadcrumbBar {
    background-color: #080A10;
    border-bottom: 1px solid #1A1D2E;
    min-height: 32px;
}

/* ── SIDEBAR ─────────────────────────────────────────── */
QWidget#Sidebar {
    background-color: #090C13;
    border-right: 1px solid #1A1D2E;
}

/* ── LOG VIEW ────────────────────────────────────────── */
QPlainTextEdit#logView {
    background-color: #06080D;
    border: none;
    font-family: "Consolas", "Courier New", monospace;
    font-size: 11px;
    color: #4B5563;
    padding: 8px 10px;
}

/* ── CENTRAL FRAME ─────────────────────────────────── */
#CentralFrame {
    border: 1px solid #1E2235;
}

/* ── FORMWIDGET ─────────────────────────────────────── */
QFormLayout QLabel {
    font-weight: 600;
    color: #64748B;
}
"""

LIGHT_THEME_QSS = """
* {
    font-family: "Segoe UI", "SF Pro Display", "Ubuntu", sans-serif;
    font-size: 13px;
    outline: none;
}
QMainWindow, QDialog { background-color: #F8FAFC; }
QWidget { background-color: #F8FAFC; color: #1E293B; }

TitleBar { background-color: #FFFFFF; border-bottom: 1px solid #E2E8F0; }
TitleBar #TitleLabel { color: #374151; font-size: 12px; font-weight: 600; letter-spacing: 0.5px; padding-left: 8px; }
TitleBar QToolButton { background-color: transparent; border: none; padding: 5px 7px; border-radius: 4px; color: #6B7280; icon-size: 14px; }
TitleBar QToolButton:hover { background-color: #F1F5F9; color: #111827; }
TitleBar QToolButton#CloseButton:hover { background-color: #DC2626; color: #ffffff; }

QMenuBar { background-color: #FFFFFF; color: #374151; border-bottom: 1px solid #E2E8F0; padding: 2px 0px; }
QMenuBar::item { background: transparent; padding: 5px 12px; border-radius: 4px; }
QMenuBar::item:selected, QMenuBar::item:pressed { background-color: #F1F5F9; color: #7C3AED; }
QMenu { background-color: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 8px; padding: 4px; }
QMenu::item { padding: 7px 20px 7px 12px; border-radius: 5px; margin: 1px 2px; color: #374151; }
QMenu::item:selected { background-color: #F1F5F9; color: #7C3AED; }
QMenu::separator { height: 1px; background-color: #E2E8F0; margin: 4px 8px; }

QToolBar { background-color: #FFFFFF; border: none; border-bottom: 1px solid #E2E8F0; spacing: 3px; padding: 4px 8px; }
QToolBar::separator { width: 1px; background-color: #E2E8F0; margin: 4px 6px; }
QToolButton { background-color: transparent; border: 1px solid transparent; border-radius: 6px; padding: 5px 7px; color: #1E293B; icon-size: 18px; }
QToolButton:hover { background-color: #F1F5F9; border-color: #CBD5E1; color: #111827; }
QToolButton:pressed { background-color: #E2E8F0; }
QToolButton:checked { background-color: #EDE9FE; border-color: #7C3AED; color: #7C3AED; }
QToolButton:disabled { color: #CBD5E1; }

QStatusBar { background-color: #FFFFFF; border-top: 1px solid #E2E8F0; color: #1E293B; padding: 0px 8px; font-size: 12px; }
QStatusBar::item { border: none; }
QStatusBar QLabel { color: #374151; font-size: 12px; padding: 0 4px; }

QTreeView { background-color: #F8FAFC; border: none; outline: none; selection-background-color: transparent; alternate-background-color: #F1F5F9; color: #374151; }
QTreeView::item { height: 28px; padding-left: 4px; border-radius: 5px; margin: 1px 4px; }
QTreeView::item:hover { background-color: #F1F5F9; }
QTreeView::item:selected { background-color: #EDE9FE; color: #7C3AED; }
QTreeView::item:selected:hover { background-color: #DDD6FE; }
QTreeView::branch { background-color: transparent; }

QHeaderView::section { background-color: #F8FAFC; color: #94A3B8; padding: 6px 10px; border: none; border-right: 1px solid #E2E8F0; border-bottom: 1px solid #E2E8F0; font-weight: 700; font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px; }
QHeaderView::section:hover { background-color: #F1F5F9; color: #374151; }

QTableView { background-color: #FFFFFF; border: none; outline: none; gridline-color: #F1F5F9; selection-background-color: #EDE9FE; selection-color: #374151; alternate-background-color: #F8FAFC; color: #374151; }
QTableView::item { padding: 4px 8px; border-bottom: 1px solid #F1F5F9; }
QTableView::item:hover { background-color: #F5F3FF; }
QTableView::item:selected { background-color: #EDE9FE; color: #7C3AED; }

QListWidget { background-color: #F8FAFC; border: none; padding: 4px; color: #374151; outline: none; }
QListWidget::item { padding: 6px 8px; border-radius: 5px; margin: 1px 2px; }
QListWidget::item:selected { background-color: #EDE9FE; color: #7C3AED; }
QListWidget::item:hover { background-color: #F1F5F9; }

QScrollBar:vertical { background-color: transparent; width: 7px; border-radius: 4px; margin: 0; }
QScrollBar::handle:vertical { background-color: #CBD5E1; border-radius: 4px; min-height: 30px; }
QScrollBar::handle:vertical:hover { background-color: #94A3B8; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
QScrollBar:horizontal { background-color: transparent; height: 7px; border-radius: 4px; margin: 0; }
QScrollBar::handle:horizontal { background-color: #CBD5E1; border-radius: 4px; min-width: 30px; }
QScrollBar::handle:horizontal:hover { background-color: #94A3B8; }
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal { width: 0; }

QPushButton { background-color: #F1F5F9; border: 1px solid #CBD5E1; border-radius: 7px; padding: 7px 16px; color: #374151; font-weight: 500; }
QPushButton:hover { background-color: #E2E8F0; border-color: #94A3B8; }
QPushButton:pressed { background-color: #CBD5E1; }
QPushButton#primaryBtn { background-color: #7C3AED; border: 1px solid #6D28D9; color: white; font-weight: 600; }
QPushButton#primaryBtn:hover { background-color: #8B5CF6; }
QPushButton#dangerBtn { background-color: #FEE2E2; border: 1px solid #FECACA; color: #DC2626; }
QPushButton#dangerBtn:hover { background-color: #FECACA; }

QLineEdit { background-color: #FFFFFF; border: 1px solid #CBD5E1; border-radius: 7px; padding: 6px 12px; color: #1E293B; selection-background-color: #7C3AED; }
QLineEdit:focus { border-color: #7C3AED; }
QLineEdit#addressBar { background-color: #F8FAFC; border: 1px solid #CBD5E1; border-radius: 7px; padding: 5px 14px; font-family: "Consolas", monospace; font-size: 12px; color: #7C3AED; }
QLineEdit#addressBar:focus { border-color: #7C3AED; color: #1E293B; }

QComboBox { background-color: #FFFFFF; border: 1px solid #CBD5E1; border-radius: 6px; padding: 5px 10px; color: #374151; }
QComboBox:focus { border-color: #7C3AED; }
QComboBox::drop-down { border: none; width: 24px; }
QComboBox::down-arrow { border-left: 4px solid transparent; border-right: 4px solid transparent; border-top: 5px solid #6B7280; }
QComboBox QAbstractItemView { background-color: #FFFFFF; border: 1px solid #CBD5E1; border-radius: 6px; selection-background-color: #EDE9FE; color: #374151; padding: 4px; }

QCheckBox { spacing: 8px; color: #374151; }
QCheckBox::indicator { width: 15px; height: 15px; border-radius: 4px; border: 1px solid #CBD5E1; background-color: #FFFFFF; }
QCheckBox::indicator:checked { background-color: #7C3AED; border-color: #7C3AED; }

QTextEdit, QPlainTextEdit { background-color: #F8FAFC; border: 1px solid #CBD5E1; border-radius: 6px; padding: 8px; color: #374151; selection-background-color: #7C3AED; }

QTabWidget::pane { border: 1px solid #E2E8F0; border-radius: 8px; background-color: #FFFFFF; top: -1px; }
QTabBar::tab { background-color: #F8FAFC; border: 1px solid #E2E8F0; border-bottom: none; border-radius: 6px 6px 0 0; padding: 7px 16px; color: #94A3B8; margin-right: 2px; font-size: 12px; }
QTabBar::tab:selected { background-color: #FFFFFF; color: #7C3AED; border-bottom: 1px solid #FFFFFF; }
QTabBar::tab:hover:!selected { background-color: #F1F5F9; color: #374151; }

QProgressBar { border: 1px solid #E2E8F0; border-radius: 5px; background-color: #F1F5F9; text-align: center; height: 8px; }
QProgressBar::chunk { background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #7C3AED, stop:1 #0891B2); border-radius: 4px; }

QSplitter::handle { background-color: #E2E8F0; width: 2px; height: 2px; }
QSplitter::handle:hover { background-color: #7C3AED; }

QDockWidget { background-color: #F8FAFC; color: #1E293B; titlebar-close-icon: url(none); }
QDockWidget::title { background-color: #FFFFFF; border-bottom: 1px solid #E2E8F0; padding: 7px 12px; font-weight: 700; font-size: 11px; text-transform: uppercase; letter-spacing: 0.8px; color: #94A3B8; }

QGroupBox { border: 1px solid #E2E8F0; border-radius: 8px; margin-top: 14px; padding-top: 8px; color: #94A3B8; font-weight: 700; font-size: 11px; text-transform: uppercase; letter-spacing: 0.8px; }
QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top left; padding: 0 8px; left: 12px; color: #7C3AED; }

QFrame[frameShape="4"], QFrame[frameShape="5"] { color: #E2E8F0; }

QMessageBox, QDialog { background-color: #FFFFFF; border: 1px solid #CBD5E1; border-radius: 10px; }
QMessageBox QLabel, QDialog QLabel { color: #374151; }
QMessageBox QPushButton, QDialog QPushButton { background-color: #7C3AED; border: 1px solid #6D28D9; color: white; min-width: 80px; font-weight: 600; }
QMessageBox QPushButton:hover, QDialog QPushButton:hover { background-color: #8B5CF6; }

QWidget#BreadcrumbBar { background-color: #FFFFFF; border-bottom: 1px solid #E2E8F0; min-height: 32px; }
QWidget#Sidebar { background-color: #FFFFFF; border-right: 1px solid #E2E8F0; }
QPlainTextEdit#logView { background-color: #F8FAFC; border: none; font-family: "Consolas", monospace; font-size: 11px; color: #64748B; padding: 8px 10px; }
#CentralFrame { border: 1px solid #E2E8F0; }
QFormLayout QLabel { font-weight: 600; color: #6B7280; }
"""


# ─────────────────────────────────────────────────────────────────────────────
#  HELPER FUNCTIONS
# ─────────────────────────────────────────────────────────────────────────────

def _format_size(size_bytes):
    if size_bytes == 0:
        return "0 B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    i = min(i, len(size_name) - 1)
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
            break
    except OSError:
        pass
    return file_count, folder_count


def _get_file_type_label(name):
    ext = Path(name).suffix.lower()
    type_map = {
        ".txt": "Text File", ".md": "Markdown", ".pdf": "PDF Document",
        ".doc": "Word Document", ".docx": "Word Document",
        ".xls": "Excel Spreadsheet", ".xlsx": "Excel Spreadsheet",
        ".ppt": "Presentation", ".pptx": "Presentation",
        ".jpg": "JPEG Image", ".jpeg": "JPEG Image", ".png": "PNG Image",
        ".gif": "GIF Image", ".bmp": "Bitmap Image", ".svg": "SVG Vector",
        ".webp": "WebP Image",
        ".mp3": "MP3 Audio", ".wav": "WAV Audio", ".flac": "FLAC Audio",
        ".mp4": "MP4 Video", ".avi": "AVI Video", ".mkv": "MKV Video",
        ".mov": "QuickTime Video", ".webm": "WebM Video",
        ".zip": "ZIP Archive", ".rar": "RAR Archive", ".7z": "7-Zip Archive",
        ".tar": "TAR Archive", ".gz": "GZ Archive",
        ".py": "Python Script", ".js": "JavaScript", ".ts": "TypeScript",
        ".html": "HTML File", ".css": "CSS Stylesheet",
        ".json": "JSON File", ".xml": "XML File", ".csv": "CSV File",
        ".exe": "Executable", ".sh": "Shell Script",
        ".c": "C Source", ".cpp": "C++ Source", ".h": "C Header",
        ".java": "Java Source", ".kt": "Kotlin Source",
        ".rs": "Rust Source", ".go": "Go Source",
    }
    return type_map.get(ext, (ext[1:].upper() + " File") if ext else "File")


def _get_file_emoji(name):
    ext = Path(name).suffix.lower()
    icon_map = {
        ".py": "🐍", ".js": "📜", ".ts": "📘", ".html": "🌐", ".css": "🎨",
        ".json": "📋", ".xml": "📋", ".csv": "📊",
        ".jpg": "🖼️", ".jpeg": "🖼️", ".png": "🖼️", ".gif": "🖼️",
        ".svg": "🖼️", ".webp": "🖼️",
        ".mp3": "🎵", ".wav": "🎵", ".flac": "🎵",
        ".mp4": "🎬", ".avi": "🎬", ".mkv": "🎬", ".mov": "🎬",
        ".pdf": "📕", ".doc": "📝", ".docx": "📝", ".txt": "📄",
        ".xls": "📊", ".xlsx": "📊", ".ppt": "📊", ".pptx": "📊",
        ".zip": "🗜️", ".rar": "🗜️", ".7z": "🗜️", ".tar": "🗜️",
        ".exe": "⚙️", ".sh": "⚡", ".c": "⚡", ".cpp": "⚡",
        ".h": "📎", ".java": "☕", ".go": "🐹", ".rs": "🦀",
        ".kt": "📘", ".md": "📋",
    }
    return icon_map.get(ext, "📄")


# ─────────────────────────────────────────────────────────────────────────────
#  WORKER SIGNALS & WORKERS
# ─────────────────────────────────────────────────────────────────────────────

class WorkerSignals(QObject):
    finished = Signal(str, object)
    error = Signal(str, str)
    progress = Signal(str, object)


class FolderSizeWorker(QRunnable):
    def __init__(self, job_id, paths_to_scan):
        super().__init__()
        self.job_id = job_id
        self.paths = paths_to_scan
        self.signals = WorkerSignals()

    @Slot()
    def run(self):
        try:
            total_size = 0
            for path in self.paths:
                if os.path.isdir(path):
                    for dirpath, _, filenames in os.walk(path):
                        for f in filenames:
                            try:
                                fp = os.path.join(dirpath, f)
                                if not os.path.islink(fp):
                                    total_size += os.path.getsize(fp)
                            except OSError:
                                continue
                elif os.path.isfile(path):
                    try:
                        total_size += os.path.getsize(path)
                    except OSError:
                        continue
            self.signals.finished.emit(self.job_id, total_size)
        except Exception as e:
            self.signals.error.emit(self.job_id, traceback.format_exc())


class ThumbnailWorker(QRunnable):
    def __init__(self, job_id, video_path, thumbnail_path):
        super().__init__()
        self.job_id = job_id
        self.video_path = video_path
        self.thumbnail_path = thumbnail_path
        self.signals = WorkerSignals()

    @Slot()
    def run(self):
        try:
            if not OPENCV_AVAILABLE:
                raise RuntimeError("OpenCV not available")
            cap = cv2.VideoCapture(self.video_path)
            if not cap.isOpened():
                raise IOError(f"Cannot open: {self.video_path}")
            cap.set(cv2.CAP_PROP_POS_MSEC, 2000)
            success, frame = cap.read()
            if not success:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                success, frame = cap.read()
            result = False
            if success:
                h, w, _ = frame.shape
                if w > 0:
                    target_w = 96
                    ratio = target_w / w
                    target_h = int(h * ratio)
                    resized = cv2.resize(frame, (target_w, target_h), interpolation=cv2.INTER_AREA)
                    cv2.imwrite(self.thumbnail_path, resized, [cv2.IMWRITE_JPEG_QUALITY, 90])
                    result = True
            cap.release()
            if not result:
                raise RuntimeError("Failed to read valid frame")
            self.signals.finished.emit(self.job_id, self.thumbnail_path)
        except Exception as e:
            if 'cap' in locals() and cap.isOpened():
                cap.release()
            self.signals.error.emit(self.job_id, traceback.format_exc())


# ─────────────────────────────────────────────────────────────────────────────
#  CORE HELPERS
# ─────────────────────────────────────────────────────────────────────────────

class ErrorHandler:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def handle(self, error, context=""):
        error_type = type(error).__name__
        error_msg = str(error)
        trace = traceback.format_exc()
        full_log = f"[ERROR] in {context} | {error_type}: {error_msg}"
        self.logger.error(full_log)
        return full_log


class ShrineLogger:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def log(self, message, level="info", tag=None):
        full_message = f"[{tag}] {message}" if tag else message
        getattr(self.logger, level, self.logger.info)(full_message)

    def ritual(self, emoji, ritual_type, target):
        self.log(f"{emoji} Ritual {ritual_type} on {target}", tag="RITUAL")


class ActivityLog:
    """Activity log for tracking all file operations."""
    INFO    = "ℹ️"
    SUCCESS = "✅"
    WARNING = "⚠️"
    ERROR   = "❌"
    RENAME  = "✏️"
    DELETE  = "🗑️"
    COPY    = "📋"
    MOVE    = "✂️"
    CREATE  = "➕"
    NAV     = "📂"

    def __init__(self, log_widget: QPlainTextEdit):
        self.widget = log_widget
        self.entries = []

    def log(self, message: str, level: str = INFO):
        ts = datetime.datetime.now().strftime("%H:%M:%S")
        entry = f"[{ts}]  {level}  {message}"
        self.entries.append(entry)
        self.widget.appendPlainText(entry)
        sb = self.widget.verticalScrollBar()
        sb.setValue(sb.maximum())

    def clear(self):
        self.entries.clear()
        self.widget.clear()

    def export(self, parent_widget=None):
        path, _ = QFileDialog.getSaveFileName(
            parent_widget, "Export Activity Log",
            os.path.join(QDir.homePath(), "macan_activity_log.txt"),
            "Text Files (*.txt)"
        )
        if path:
            with open(path, 'w', encoding='utf-8') as f:
                f.write("\n".join(self.entries))


class ConfigManager:
    def __init__(self, config_file="macan_explorer_config.json"):
        self.config_path = os.path.join(os.path.expanduser("~"), ".macan_explorer", config_file)
        self.config_data = {}
        self._load_config()

    def _load_config(self):
        base_dir = os.path.dirname(self.config_path)
        os.makedirs(base_dir, exist_ok=True)
        thumbnail_cache_dir = os.path.join(base_dir, "thumbnails")
        os.makedirs(thumbnail_cache_dir, exist_ok=True)
        self.thumbnail_cache_path = thumbnail_cache_dir

        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    self.config_data = json.load(f)
            except Exception:
                self.config_data = {}
        else:
            self.config_data = {
                "added_folders": [],
                "bookmarks": [],
                "view_mode": "details",
                "theme": "dark",
                "show_hidden": False,
                "window_state": None,
            }
            self._save_config()

    def _save_config(self):
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config_data, f, indent=4)
        except Exception as e:
            logging.error(f"Config save failed: {e}")

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


# ─────────────────────────────────────────────────────────────────────────────
#  THUMBNAIL ICON PROVIDER
# ─────────────────────────────────────────────────────────────────────────────

class ThumbnailIconProvider(QFileSystemModel):
    thumbnail_ready = Signal(str)

    def __init__(self, config_manager):
        super().__init__()
        self.config_manager = config_manager
        self.icon_cache = {}
        self.logger = ShrineLogger()
        self.VIDEO_EXTENSIONS = ['mp4', 'mkv', 'avi', 'mov', 'webm', 'flv', 'wmv', 'mpg', 'mpeg']
        self.IMAGE_EXTENSIONS = ['png', 'jpg', 'jpeg', 'bmp', 'gif', 'webp']
        self.thumbnail_thread_pool = QThreadPool()
        self.thumbnail_thread_pool.setMaxThreadCount(4)
        self.pending_thumbnails = set()
        self.thumbnail_ready.connect(self._on_thumbnail_finished)

    def _get_cached_thumbnail_path(self, video_path):
        filename = hashlib.md5(video_path.encode('utf-8')).hexdigest() + ".jpg"
        return os.path.join(self.config_manager.thumbnail_cache_path, filename)

    @Slot(str, object)
    def _on_worker_finished(self, video_path, thumbnail_path):
        if video_path in self.pending_thumbnails:
            self.pending_thumbnails.remove(video_path)
        self.thumbnail_ready.emit(video_path)

    @Slot(str, str)
    def _on_worker_error(self, video_path, error_message):
        if video_path in self.pending_thumbnails:
            self.pending_thumbnails.remove(video_path)

    @Slot(str)
    def _on_thumbnail_finished(self, video_path):
        thumbnail_path = self._get_cached_thumbnail_path(video_path)
        if not os.path.exists(thumbnail_path):
            return
        pixmap = QPixmap(thumbnail_path)
        if not pixmap.isNull():
            overlay = get_overlay_icon(24)
            painter = QPainter(pixmap)
            painter.drawPixmap(pixmap.width() - overlay.width(), pixmap.height() - overlay.height(), overlay)
            painter.end()
            icon = QIcon(pixmap)
            self.icon_cache[video_path] = icon
            index_to_update = self.index(video_path)
            if index_to_update.isValid():
                self.dataChanged.emit(index_to_update, index_to_update, [Qt.ItemDataRole.DecorationRole])

    def data(self, index, role):
        if role == Qt.ItemDataRole.DecorationRole and index.column() == 0:
            file_path = self.filePath(index)
            if file_path in self.icon_cache:
                return self.icon_cache[file_path]
            file_info = QFileInfo(file_path)
            if file_info.isDir():
                return super().data(index, role)
            suffix = file_info.suffix().lower()
            if suffix in self.IMAGE_EXTENSIONS:
                pixmap = QPixmap(file_path)
                if not pixmap.isNull():
                    icon = QIcon(pixmap.scaled(96, 96, Qt.AspectRatioMode.KeepAspectRatio,
                                               Qt.TransformationMode.SmoothTransformation))
                    self.icon_cache[file_path] = icon
                    return icon
            if OPENCV_AVAILABLE and suffix in self.VIDEO_EXTENSIONS:
                thumbnail_path = self._get_cached_thumbnail_path(file_path)
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
                    pass
                if file_path not in self.pending_thumbnails:
                    self.pending_thumbnails.add(file_path)
                    worker = ThumbnailWorker(file_path, file_path, thumbnail_path)
                    worker.signals.finished.connect(self._on_worker_finished)
                    worker.signals.error.connect(self._on_worker_error)
                    self.thumbnail_thread_pool.start(worker)
        return super().data(index, role)


# ─────────────────────────────────────────────────────────────────────────────
#  SORT FILTER PROXY
# ─────────────────────────────────────────────────────────────────────────────

class SortFilterProxyModel(QSortFilterProxyModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._show_hidden = False

    def set_show_hidden(self, show: bool):
        self._show_hidden = show
        self.invalidateFilter()

    def filterAcceptsRow(self, source_row, source_parent):
        if not self._show_hidden:
            source_model = self.sourceModel()
            index = source_model.index(source_row, 0, source_parent)
            name = source_model.fileName(index)
            if name.startswith('.'):
                return False
        return super().filterAcceptsRow(source_row, source_parent)

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


# ─────────────────────────────────────────────────────────────────────────────
#  BREADCRUMB BAR
# ─────────────────────────────────────────────────────────────────────────────

class BreadcrumbBar(QWidget):
    path_clicked = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("BreadcrumbBar")
        self.setFixedHeight(34)
        self._layout = QHBoxLayout(self)
        self._layout.setContentsMargins(10, 4, 10, 4)
        self._layout.setSpacing(2)
        self._layout.addStretch()
        self._current_path = ""
        self._theme = "dark"

    def set_theme(self, theme):
        self._theme = theme
        self.update_path(self._current_path)

    def update_path(self, path):
        self._current_path = path
        # Clear existing
        while self._layout.count():
            item = self._layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        if not path:
            self._layout.addStretch()
            return

        parts = list(Path(path).parts)
        if not parts:
            self._layout.addStretch()
            return

        full = ""
        hover_bg = "rgba(124,58,237,0.15)" if self._theme == "dark" else "#EDE9FE"
        hover_color = "#A78BFA" if self._theme == "dark" else "#7C3AED"
        sep_color = "#374151" if self._theme == "dark" else "#CBD5E1"
        text_color = "#64748B" if self._theme == "dark" else "#6B7280"

        for i, part in enumerate(parts):
            if platform.system() == "Windows" and i == 0:
                full = part + "\\"
            else:
                full = os.path.join(full, part) if full else part

            btn = QPushButton(part)
            btn.setFlat(True)
            btn.setStyleSheet(
                f"QPushButton {{ padding: 2px 7px; border-radius: 4px; font-size: 12px; color: {text_color}; border: none; }}"
                f"QPushButton:hover {{ background: {hover_bg}; color: {hover_color}; }}"
            )
            p = full
            btn.clicked.connect(lambda _, p=p: self.path_clicked.emit(p))
            self._layout.addWidget(btn)

            if i < len(parts) - 1:
                sep = QLabel("›")
                sep.setStyleSheet(f"color: {sep_color}; padding: 0 1px; font-size: 13px;")
                self._layout.addWidget(sep)

        self._layout.addStretch()


# ─────────────────────────────────────────────────────────────────────────────
#  COMMAND BAR (TOOLBAR)
# ─────────────────────────────────────────────────────────────────────────────

class CommandBar(QToolBar):
    back_requested     = Signal()
    forward_requested  = Signal()
    up_requested       = Signal()
    refresh_requested  = Signal()
    address_submitted  = Signal(str)
    search_requested   = Signal(str)
    new_folder_requested = Signal()
    new_file_requested   = Signal()
    delete_item_requested = Signal()
    rename_item_requested = Signal()
    view_mode_changed  = Signal(str)
    clear_cache_requested = Signal()
    theme_toggle_requested = Signal()
    terminal_requested = Signal()
    show_hidden_toggled = Signal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setIconSize(QSize(18, 18))
        self.setMovable(False)
        self.setObjectName("CommandBar")

        # Navigation
        self.action_back = QAction(create_icon("back"), "Back  (Alt+Left)", self)
        self.action_forward = QAction(create_icon("forward"), "Forward  (Alt+Right)", self)
        self.action_up = QAction(create_icon("up"), "Up  (Alt+Up)", self)
        self.action_refresh = QAction(create_icon("refresh"), "Refresh  (F5)", self)

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
        self.address_bar.setObjectName("addressBar")
        self.address_bar.setPlaceholderText("Enter path or URL...")
        self.address_bar.returnPressed.connect(self._on_address_submit)
        self.addWidget(self.address_bar)
        self.addSeparator()

        # Search
        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText("Search files...")
        self.search_input.setFixedWidth(190)
        self.search_input.returnPressed.connect(self._on_search_clicked)
        self.addWidget(self.search_input)

        self.search_button = QToolButton(self)
        self.search_button.setIcon(create_icon("search"))
        self.search_button.setToolTip("Search  (Ctrl+F)")
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

        # Terminal button
        self.terminal_button = QToolButton(self)
        self.terminal_button.setIcon(create_icon("terminal"))
        self.terminal_button.setToolTip("Open Terminal Here  (Ctrl+T)")
        self.terminal_button.clicked.connect(self.terminal_requested.emit)
        self.addWidget(self.terminal_button)
        self.addSeparator()

        # Organize Menu
        self.organize_button = QToolButton(self)
        self.organize_button.setText("Organize")
        self.organize_button.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        self.organize_button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.organize_button.setIcon(create_icon("folder-closed"))
        organize_menu = QMenu(self)
        self.action_new_folder = QAction(create_icon("folder-closed"), "New Folder  (Ctrl+Shift+N)", self)
        self.action_new_file = QAction(create_icon("new_file"), "New File", self)
        self.action_rename = QAction(create_icon("rename"), "Rename  (F2)", self)
        self.action_delete = QAction(create_icon("delete"), "Delete  (Del)", self)
        self.action_cut = QAction(create_icon("cut"), "Cut  (Ctrl+X)", self)
        self.action_copy_files = QAction(create_icon("copy"), "Copy  (Ctrl+C)", self)
        self.action_paste_files = QAction(create_icon("paste"), "Paste  (Ctrl+V)", self)
        self.action_new_folder.triggered.connect(self.new_folder_requested.emit)
        self.action_new_file.triggered.connect(self.new_file_requested.emit)
        self.action_rename.triggered.connect(self.rename_item_requested.emit)
        self.action_delete.triggered.connect(self.delete_item_requested.emit)
        organize_menu.addAction(self.action_new_folder)
        organize_menu.addAction(self.action_new_file)
        organize_menu.addSeparator()
        organize_menu.addAction(self.action_cut)
        organize_menu.addAction(self.action_copy_files)
        organize_menu.addAction(self.action_paste_files)
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
        self.action_show_hidden = QAction("Show Hidden Files  (Ctrl+H)", self)
        self.action_show_hidden.setCheckable(True)
        self.action_show_hidden.toggled.connect(self.show_hidden_toggled.emit)
        self.action_theme_toggle = QAction(create_icon("theme_dark"), "Toggle Theme", self)
        self.action_theme_toggle.triggered.connect(self.theme_toggle_requested.emit)
        self.action_open_new_window = QAction(create_icon("new_window"), "Open New Window  (Ctrl+N)", self)
        self.action_clear_cache = QAction(create_icon("delete"), "Clear Thumbnail Cache", self)
        self.action_clear_cache.triggered.connect(self.clear_cache_requested.emit)
        self.action_about = QAction(create_icon("about"), "About Macan Explorer", self)
        more_menu.addAction(self.action_show_hidden)
        more_menu.addAction(self.action_theme_toggle)
        more_menu.addSeparator()
        more_menu.addAction(self.action_open_new_window)
        more_menu.addAction(self.action_clear_cache)
        more_menu.addSeparator()
        more_menu.addAction(self.action_about)
        self.more_button.setMenu(more_menu)
        self.addWidget(self.more_button)

    def _on_address_submit(self):
        path = self.address_bar.text()
        if path:
            self.address_submitted.emit(path)

    def update_icons(self, theme: str):
        """Re-render all toolbar icons for the current theme."""
        self.action_back.setIcon(create_icon("back", theme=theme))
        self.action_forward.setIcon(create_icon("forward", theme=theme))
        self.action_up.setIcon(create_icon("up", theme=theme))
        self.action_refresh.setIcon(create_icon("refresh", theme=theme))
        self.search_button.setIcon(create_icon("search", theme=theme))
        self.action_view_details.setIcon(create_icon("view_details", theme=theme))
        self.action_view_list.setIcon(create_icon("view_list", theme=theme))
        self.action_view_icons.setIcon(create_icon("view_icons", theme=theme))
        self.terminal_button.setIcon(create_icon("terminal", theme=theme))
        self.organize_button.setIcon(create_icon("folder-closed", theme=theme))
        self.action_new_folder.setIcon(create_icon("folder-closed", theme=theme))
        self.action_new_file.setIcon(create_icon("new_file", theme=theme))
        self.action_rename.setIcon(create_icon("rename", theme=theme))
        self.action_delete.setIcon(create_icon("delete", theme=theme))
        self.action_cut.setIcon(create_icon("cut", theme=theme))
        self.action_copy_files.setIcon(create_icon("copy", theme=theme))
        self.action_paste_files.setIcon(create_icon("paste", theme=theme))
        self.more_button.setIcon(create_icon("more-horizontal", theme=theme))
        self.action_open_new_window.setIcon(create_icon("new_window", theme=theme))
        self.action_clear_cache.setIcon(create_icon("delete", theme=theme))
        self.action_about.setIcon(create_icon("about", theme=theme))
        # Theme toggle icon stays the same regardless of current theme
        icon_key = "theme_dark" if theme == "dark" else "theme_light"
        self.action_theme_toggle.setIcon(create_icon(icon_key, theme=theme))

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

    def set_view_mode(self, mode):
        if mode == "details":
            self.action_view_details.setChecked(True)
        elif mode == "list":
            self.action_view_list.setChecked(True)
        elif mode == "icons":
            self.action_view_icons.setChecked(True)

    def _on_search_clicked(self):
        query = self.search_input.text()
        if query:
            self.search_requested.emit(query)


# ─────────────────────────────────────────────────────────────────────────────
#  FILE VIEW (MAIN CONTENT AREA)
# ─────────────────────────────────────────────────────────────────────────────

class FileView(QWidget):
    path_changed                = Signal(str)
    navigation_state_changed    = Signal(bool, bool)
    status_message_requested    = Signal(str)
    selection_info_requested    = Signal(str)
    open_in_new_tab_requested   = Signal(str)
    activity_log_requested      = Signal(str, str)  # message, level

    def __init__(self, config_manager, folder_path=None, parent=None):
        super().__init__(parent)
        self._history = []
        self._history_index = -1
        self.config_manager = config_manager
        self.size_thread_pool = QThreadPool()
        self.size_thread_pool.setMaxThreadCount(2)
        self.current_size_job_id = None

        initial_path = folder_path if folder_path and os.path.exists(folder_path) else QDir.homePath()
        self.current_path = ""
        self.setAcceptDrops(True)

        # Model
        self.model = ThumbnailIconProvider(config_manager)
        self.model.setRootPath(QDir.rootPath())
        self.model.setOption(QFileSystemModel.Option.DontWatchForChanges, False)
        self.model.setFilter(QDir.Filter.AllEntries | QDir.Filter.NoDotAndDotDot | QDir.Filter.Hidden)

        # Proxy Model
        self.proxy_model = SortFilterProxyModel(self)
        self.proxy_model.setSourceModel(self.model)

        # File system watcher for auto-refresh
        self.fs_watcher = QFileSystemWatcher()
        self.fs_watcher.directoryChanged.connect(self._on_directory_changed)

        # Views
        self.tree_view = QTreeView(self)
        self.list_view = QListView(self)

        self.tree_view.setModel(self.proxy_model)
        self.list_view.setModel(self.proxy_model)

        # TreeView settings
        self.tree_view.setSortingEnabled(True)
        self.tree_view.sortByColumn(0, Qt.SortOrder.AscendingOrder)
        self.tree_view.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tree_view.customContextMenuRequested.connect(self._on_context_menu)
        self.tree_view.doubleClicked.connect(self._on_double_click)
        self.tree_view.setAlternatingRowColors(True)
        self.tree_view.setSelectionMode(QTreeView.SelectionMode.ExtendedSelection)
        self.tree_view.header().setStretchLastSection(True)
        self.tree_view.setDragEnabled(True)
        self.tree_view.setDragDropMode(QTreeView.DragDropMode.DragOnly)

        # ListView settings
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
        self.list_view.setDragEnabled(True)
        self.list_view.setDragDropMode(QListView.DragDropMode.DragOnly)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.tree_view)
        layout.addWidget(self.list_view)
        self.setLayout(layout)

        # Set initial view mode
        initial_view_mode = self.config_manager.get('view_mode', 'details')
        self.set_view_mode(initial_view_mode)
        self.set_path(initial_path, initial_load=True)

        # Keyboard shortcuts
        copy_action = QAction("Copy", self)
        copy_action.setShortcut(QKeySequence.StandardKey.Copy)
        copy_action.triggered.connect(self.copy_selected_items)
        self.addAction(copy_action)

        cut_action = QAction("Cut", self)
        cut_action.setShortcut(QKeySequence.StandardKey.Cut)
        cut_action.triggered.connect(self.cut_selected_items)
        self.addAction(cut_action)

        paste_action = QAction("Paste", self)
        paste_action.setShortcut(QKeySequence.StandardKey.Paste)
        paste_action.triggered.connect(self.paste_items)
        self.addAction(paste_action)

        delete_action = QAction("Delete", self)
        delete_action.setShortcut(QKeySequence.StandardKey.Delete)
        delete_action.triggered.connect(self.delete_selected_items)
        self.addAction(delete_action)

        rename_action = QAction("Rename", self)
        rename_action.setShortcut(Qt.Key.Key_F2)
        rename_action.triggered.connect(self.rename_selected_item)
        self.addAction(rename_action)

        select_all_action = QAction("Select All", self)
        select_all_action.setShortcut(QKeySequence.StandardKey.SelectAll)
        select_all_action.triggered.connect(self.select_all)
        self.addAction(select_all_action)

        # Selection change
        self.tree_view.selectionModel().selectionChanged.connect(self._on_selection_changed)
        self.list_view.selectionModel().selectionChanged.connect(self._on_selection_changed)

        # Cut clipboard tracking
        self._cut_paths = []

    @property
    def active_view(self):
        return self.tree_view if self.tree_view.isVisible() else self.list_view

    def _on_directory_changed(self, path):
        if path == self.current_path:
            QTimer.singleShot(200, lambda: self.set_path(self.current_path, add_to_history=False))

    def set_path(self, path, add_to_history=True, initial_load=False):
        path = os.path.normpath(path)
        if not os.path.exists(path) or not os.path.isdir(path):
            QMessageBox.warning(self, "Invalid Path", f"Folder '{path}' does not exist.")
            if initial_load:
                path = QDir.homePath()
            else:
                return

        self.current_path = path

        # Update watcher
        if self.fs_watcher.directories():
            self.fs_watcher.removePaths(self.fs_watcher.directories())
        self.fs_watcher.addPath(path)

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
        self._on_selection_changed()

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
        self.set_path(self.current_path, add_to_history=False)

    def set_show_hidden(self, show: bool):
        self.proxy_model.set_show_hidden(show)

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

    def select_all(self):
        self.active_view.selectAll()

    def _on_double_click(self, index):
        source_index = self.proxy_model.mapToSource(index)
        if source_index.column() != 0:
            source_index = source_index.sibling(source_index.row(), 0)
        path = self.model.filePath(source_index)
        if self.model.isDir(source_index):
            self.set_path(path)
            self.activity_log_requested.emit(f"Navigated to: {path}", ActivityLog.NAV)
        else:
            if os.path.exists(path):
                QDesktopServices.openUrl(QUrl.fromLocalFile(path))
                self.activity_log_requested.emit(f"Opened: {os.path.basename(path)}", ActivityLog.INFO)
            else:
                QMessageBox.warning(self, "File Not Found", f"'{path}' was not found.")

    def _on_context_menu(self, position):
        view = self.active_view
        proxy_index = view.indexAt(position)
        menu = QMenu(self)

        if proxy_index.isValid():
            source_index = self.proxy_model.mapToSource(proxy_index)
            path = self.model.filePath(source_index)
            is_dir = self.model.isDir(source_index)

            menu.addAction("Open").triggered.connect(lambda: self._on_double_click(proxy_index))
            if is_dir:
                menu.addAction("Open in New Tab").triggered.connect(
                    lambda checked=False, p=path: self.open_in_new_tab_requested.emit(p)
                )
            menu.addSeparator()
            menu.addAction(create_icon("cut"), "Cut  Ctrl+X").triggered.connect(self.cut_selected_items)
            menu.addAction(create_icon("copy"), "Copy  Ctrl+C").triggered.connect(self.copy_selected_items)
            menu.addSeparator()
            menu.addAction("Rename  F2").triggered.connect(self.rename_selected_item)
            menu.addAction(create_icon("delete"), "Delete  Del").triggered.connect(self.delete_selected_items)
            menu.addSeparator()
            menu.addAction("Copy Path").triggered.connect(lambda: QApplication.clipboard().setText(path))
            if is_dir:
                menu.addAction("Bookmark This Folder").triggered.connect(
                    lambda checked=False, p=path: self._bookmark_folder(p)
                )
            menu.addSeparator()
            menu.addAction("Properties").triggered.connect(lambda: self.show_properties(proxy_index))
            menu.addSeparator()

        paste_action = menu.addAction(create_icon("paste"), "Paste  Ctrl+V")
        paste_action.triggered.connect(self.paste_items)
        if not QApplication.clipboard().mimeData().hasUrls():
            paste_action.setEnabled(False)
        menu.addSeparator()
        menu.addAction("New Folder  Ctrl+Shift+N").triggered.connect(self.create_new_folder)
        menu.addAction("New File").triggered.connect(self.create_new_file)
        menu.exec(view.viewport().mapToGlobal(position))

    def _bookmark_folder(self, path):
        if self.config_manager.add_to_list("bookmarks", path):
            self.status_message_requested.emit(f"Bookmarked: {os.path.basename(path)}")
            self.activity_log_requested.emit(f"Bookmarked: {path}", ActivityLog.SUCCESS)

    def _on_selection_changed(self, selected=None, deselected=None):
        try:
            root = self.active_view.rootIndex()
            total_items_in_view = self.proxy_model.rowCount(root)
            selected_indexes = self.active_view.selectionModel().selectedIndexes()
            source_indexes = [self.proxy_model.mapToSource(idx) for idx in selected_indexes]
            paths = list(set([self.model.filePath(idx.sibling(idx.row(), 0)) for idx in source_indexes]))
            num_selected = len(paths)
            self.current_size_job_id = None

            if num_selected == 0:
                self.selection_info_requested.emit(f"{total_items_in_view} items")
            elif num_selected == 1:
                path = paths[0]
                info = QFileInfo(path)
                name = info.fileName()
                if info.isDir():
                    size_str = "Calculating..."
                    self.current_size_job_id = f"job_{path}"
                    self._start_size_calculation(self.current_size_job_id, paths)
                    self.selection_info_requested.emit(f"1 item selected: {name}  |  Folder  |  Size: {size_str}")
                else:
                    type_desc = _get_file_type_label(name)
                    size_bytes = info.size()
                    size_str = _format_size(size_bytes)
                    self.selection_info_requested.emit(f"1 item: {name}  |  {type_desc}  |  {size_str}")
            else:
                size_str = "Calculating..."
                job_id_str = "+".join(sorted(paths))
                self.current_size_job_id = f"job_{hash(job_id_str)}"
                self._start_size_calculation(self.current_size_job_id, paths)
                self.selection_info_requested.emit(f"{num_selected} items selected  |  Total: {size_str}")
        except Exception:
            self.selection_info_requested.emit("")

    def _start_size_calculation(self, job_id, paths):
        worker = FolderSizeWorker(job_id, paths)
        worker.signals.finished.connect(self._on_size_calculation_finished)
        worker.signals.error.connect(self._on_size_calculation_error)
        self.size_thread_pool.start(worker)

    def _on_size_calculation_finished(self, job_id, total_size):
        if job_id != self.current_size_job_id:
            return
        size_str = _format_size(total_size)
        selected_indexes = self.active_view.selectionModel().selectedIndexes()
        source_indexes = [self.proxy_model.mapToSource(idx) for idx in selected_indexes]
        paths = list(set([self.model.filePath(idx.sibling(idx.row(), 0)) for idx in source_indexes]))
        num_selected = len(paths)
        if num_selected == 1:
            info = QFileInfo(paths[0])
            name = info.fileName()
            type_desc = "Folder" if info.isDir() else _get_file_type_label(name)
            self.selection_info_requested.emit(f"1 item: {name}  |  {type_desc}  |  {size_str}")
        elif num_selected > 1:
            self.selection_info_requested.emit(f"{num_selected} items selected  |  Total: {size_str}")
        self.current_size_job_id = None

    def _on_size_calculation_error(self, job_id, error_message):
        if job_id != self.current_size_job_id:
            return
        selected_indexes = self.active_view.selectionModel().selectedIndexes()
        source_indexes = [self.proxy_model.mapToSource(idx) for idx in selected_indexes]
        paths = list(set([self.model.filePath(idx.sibling(idx.row(), 0)) for idx in source_indexes]))
        num_selected = len(paths)
        if num_selected == 1:
            info = QFileInfo(paths[0])
            self.selection_info_requested.emit(f"1 item: {info.fileName()}  |  Size: N/A")
        elif num_selected > 1:
            self.selection_info_requested.emit(f"{num_selected} items selected")
        self.current_size_job_id = None

    def search_files(self, query):
        results = []
        query_lower = query.lower()
        try:
            for root, dirs, files in os.walk(self.current_path):
                for name in dirs:
                    if query_lower in name.lower():
                        results.append(os.path.join(root, name))
                for name in files:
                    if query_lower in name.lower():
                        results.append(os.path.join(root, name))
        except Exception as e:
            QMessageBox.critical(self, "Search Error", str(e))
            return
        if results:
            dialog = SearchResultsDialog(results, query, self)
            dialog.result_selected.connect(self.set_path)
            dialog.exec()
        else:
            QMessageBox.information(self, "Search Results", f"No results found for '{query}'.")

    def _get_selected_proxy_indexes(self):
        return self.active_view.selectionModel().selectedIndexes()

    def get_selected_paths(self) -> List[str]:
        """Return a deduplicated list of full paths for the currently selected items."""
        idxs = self._get_selected_proxy_indexes()
        if not idxs:
            return []
        source_idxs = [self.proxy_model.mapToSource(i) for i in idxs]
        return list(set([self.model.filePath(i.sibling(i.row(), 0)) for i in source_idxs]))

    def copy_selected_items(self):
        selected_proxy_indexes = self._get_selected_proxy_indexes()
        if not selected_proxy_indexes:
            return
        source_indexes = [self.proxy_model.mapToSource(idx) for idx in selected_proxy_indexes]
        paths = list(set([self.model.filePath(idx.sibling(idx.row(), 0)) for idx in source_indexes]))
        if not paths:
            return
        self._cut_paths = []  # Clear cut
        urls = [QUrl.fromLocalFile(p) for p in paths]
        mime_data = QMimeData()
        mime_data.setUrls(urls)
        QApplication.clipboard().setMimeData(mime_data)
        self.status_message_requested.emit(f"Copied {len(paths)} item(s).")
        self.activity_log_requested.emit(f"Copied {len(paths)} item(s) from {self.current_path}", ActivityLog.COPY)

    def cut_selected_items(self):
        selected_proxy_indexes = self._get_selected_proxy_indexes()
        if not selected_proxy_indexes:
            return
        source_indexes = [self.proxy_model.mapToSource(idx) for idx in selected_proxy_indexes]
        paths = list(set([self.model.filePath(idx.sibling(idx.row(), 0)) for idx in source_indexes]))
        if not paths:
            return
        self._cut_paths = paths
        urls = [QUrl.fromLocalFile(p) for p in paths]
        mime_data = QMimeData()
        mime_data.setUrls(urls)
        QApplication.clipboard().setMimeData(mime_data)
        self.status_message_requested.emit(f"Cut {len(paths)} item(s) — ready to paste.")
        self.activity_log_requested.emit(f"Cut {len(paths)} item(s)", ActivityLog.MOVE)

    def paste_items(self):
        clipboard = QApplication.clipboard()
        mime_data = clipboard.mimeData()
        if not mime_data.hasUrls():
            self.status_message_requested.emit("Nothing to paste.")
            return
        is_cut = bool(self._cut_paths)
        self._perform_paste_operation(mime_data.urls(), move=is_cut)
        if is_cut:
            self._cut_paths = []

    def _perform_paste_operation(self, urls, move=False):
        dest_dir = self.current_path
        total_items = len(urls)
        op = "Moving" if move else "Pasting"
        progress_dialog = OperationProgressDialog(f"{op} {total_items} items", self)
        progress_dialog.setRange(0, total_items)
        progress_dialog.show()
        for i, url in enumerate(urls):
            QApplication.processEvents()
            if progress_dialog.wasCanceled():
                self.status_message_requested.emit(f"{op} canceled.")
                break
            if url.isLocalFile():
                src_path = url.toLocalFile()
                base_name = os.path.basename(src_path)
                progress_dialog.setLabelText(f"{op}: {base_name}")
                dest_path = os.path.join(dest_dir, base_name)
                if os.path.normpath(src_path) == os.path.normpath(dest_dir):
                    continue
                if os.path.isdir(src_path) and os.path.normpath(dest_path).startswith(os.path.normpath(src_path)):
                    QMessageBox.warning(self, "Paste Error", f"Cannot copy '{base_name}' into itself.")
                    continue
                if os.path.exists(dest_path) and not move:
                    base, ext = os.path.splitext(base_name)
                    copy_num = 1
                    while os.path.exists(dest_path):
                        dest_path = os.path.join(dest_dir, f"{base} - copy ({copy_num}){ext}")
                        copy_num += 1
                try:
                    if move:
                        shutil.move(src_path, dest_path)
                        self.activity_log_requested.emit(f"Moved: {base_name} → {dest_dir}", ActivityLog.MOVE)
                    elif os.path.isdir(src_path):
                        shutil.copytree(src_path, dest_path)
                        self.activity_log_requested.emit(f"Copied dir: {base_name}", ActivityLog.COPY)
                    else:
                        shutil.copy2(src_path, dest_path)
                        self.activity_log_requested.emit(f"Copied: {base_name}", ActivityLog.COPY)
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Failed: {base_name}\n{e}")
                    progress_dialog.cancel()
                    break
            progress_dialog.setValue(i + 1)
        else:
            self.status_message_requested.emit("Operation complete.")
        progress_dialog.setValue(total_items)
        QTimer.singleShot(200, self.refresh)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dragMoveEvent(self, event):
        event.acceptProposedAction()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            self._perform_paste_operation(event.mimeData().urls())
            event.acceptProposedAction()

    def create_new_folder(self):
        folder_name, ok = QInputDialog.getText(self, "New Folder", "Enter folder name:")
        if ok and folder_name:
            try:
                os.makedirs(os.path.join(self.current_path, folder_name))
                self.refresh()
                self.activity_log_requested.emit(f"Created folder: {folder_name}", ActivityLog.CREATE)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed: {e}")

    def create_new_file(self):
        file_name, ok = QInputDialog.getText(self, "New File", "Enter file name:")
        if ok and file_name:
            try:
                with open(os.path.join(self.current_path, file_name), 'w') as f:
                    f.write("")
                self.refresh()
                self.activity_log_requested.emit(f"Created file: {file_name}", ActivityLog.CREATE)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed: {e}")

    def delete_selected_items(self):
        selected_proxy_indexes = self._get_selected_proxy_indexes()
        if not selected_proxy_indexes:
            return
        source_indexes = [self.proxy_model.mapToSource(idx) for idx in selected_proxy_indexes]
        paths_to_delete = list(set([self.model.filePath(idx.sibling(idx.row(), 0)) for idx in source_indexes]))
        total_items = len(paths_to_delete)
        reply = QMessageBox.question(
            self, 'Confirm Deletion',
            f"Permanently delete {total_items} item(s)?\nThis cannot be undone.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            progress_dialog = OperationProgressDialog(f"Deleting {total_items} items", self)
            progress_dialog.setRange(0, total_items)
            progress_dialog.show()
            for i, path in enumerate(paths_to_delete):
                QApplication.processEvents()
                if progress_dialog.wasCanceled():
                    self.status_message_requested.emit("Delete canceled.")
                    break
                base_name = os.path.basename(path)
                progress_dialog.setLabelText(f"Deleting: {base_name}")
                try:
                    if os.path.isdir(path):
                        shutil.rmtree(path)
                    else:
                        os.remove(path)
                    self.activity_log_requested.emit(f"Deleted: {base_name}", ActivityLog.DELETE)
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Failed to delete '{base_name}': {e}")
                    progress_dialog.cancel()
                    break
                progress_dialog.setValue(i + 1)
            else:
                self.status_message_requested.emit("Deletion complete.")
            progress_dialog.setValue(total_items)
            QTimer.singleShot(200, self.refresh)

    def rename_selected_item(self):
        selected_proxy_indexes = self._get_selected_proxy_indexes()
        if not selected_proxy_indexes:
            return
        proxy_index = selected_proxy_indexes[0]
        source_index = self.proxy_model.mapToSource(proxy_index)
        source_index_col0 = source_index.sibling(source_index.row(), 0)
        old_path = self.model.filePath(source_index_col0)
        old_name = os.path.basename(old_path)
        new_name, ok = QInputDialog.getText(self, "Rename", "New name:", QLineEdit.EchoMode.Normal, old_name)
        if ok and new_name and new_name != old_name:
            new_path = os.path.join(os.path.dirname(old_path), new_name)
            try:
                os.rename(old_path, new_path)
                self.refresh()
                self.activity_log_requested.emit(f"Renamed: {old_name} → {new_name}", ActivityLog.RENAME)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to rename: {e}")

    def show_properties(self, proxy_index):
        if not proxy_index.isValid():
            return
        source_index = self.proxy_model.mapToSource(proxy_index)
        source_index_col0 = source_index.sibling(source_index.row(), 0)
        path = self.model.filePath(source_index_col0)
        try:
            icon = self.model.fileIcon(source_index_col0)
            dialog = PropertiesDialog(path, icon, self)
            if dialog.exec():
                if dialog.name_changed:
                    self.refresh()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not get properties: {e}")


# ─────────────────────────────────────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────

class Sidebar(QWidget):
    def __init__(self, open_folder_callback, config_manager, parent=None):
        super().__init__(parent)
        self.setObjectName("Sidebar")
        self.open_folder_callback = open_folder_callback
        self.config_manager = config_manager
        self._init_ui()
        self.load_bookmarks()

    def _init_ui(self):
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.setSpacing(0)

        # QSplitter: Quick Access | Drives | Bookmarks — all resizable
        self._splitter = QSplitter(Qt.Orientation.Vertical)
        self._splitter.setHandleWidth(3)
        self._splitter.setChildrenCollapsible(False)

        # ── Quick Access ─────────────────────────────────────────────────────
        qa_container = QWidget()
        qa_layout = QVBoxLayout(qa_container)
        qa_layout.setContentsMargins(0, 0, 0, 0)
        qa_layout.setSpacing(0)

        qa_label = QLabel("  QUICK ACCESS")
        qa_label.setStyleSheet("font-size: 10px; font-weight: 700; letter-spacing: 1px; color: #64748B; padding: 12px 8px 5px 8px;")
        qa_layout.addWidget(qa_label)

        qa_scroll = QScrollArea()
        qa_scroll.setWidgetResizable(True)
        qa_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        qa_scroll.setFrameShape(QFrame.Shape.NoFrame)
        qa_inner = QWidget()
        qa_inner_layout = QVBoxLayout(qa_inner)
        qa_inner_layout.setContentsMargins(0, 0, 0, 0)
        qa_inner_layout.setSpacing(0)

        # Use OS default icon via QFileIconProvider
        icon_provider = QFileIconProvider()

        qa_locations = [
            ("Home",      QStandardPaths.StandardLocation.HomeLocation),
            ("Desktop",   QStandardPaths.StandardLocation.DesktopLocation),
            ("Downloads", QStandardPaths.StandardLocation.DownloadLocation),
            ("Documents", QStandardPaths.StandardLocation.DocumentsLocation),
            ("Pictures",  QStandardPaths.StandardLocation.PicturesLocation),
            ("Music",     QStandardPaths.StandardLocation.MusicLocation),
            ("Videos",    QStandardPaths.StandardLocation.MoviesLocation),
        ]

        for name, std_loc in qa_locations:
            if std_loc == QStandardPaths.StandardLocation.HomeLocation:
                path = QDir.homePath()
            else:
                path = QStandardPaths.writableLocation(std_loc)
            if not path or not os.path.exists(path):
                continue
            # Grab OS default icon for the folder
            fi = QFileInfo(path)
            os_icon = icon_provider.icon(fi)
            btn = QPushButton(f"  {name}")
            btn.setFlat(True)
            btn.setIcon(os_icon)
            btn.setIconSize(QSize(16, 16))
            btn.setStyleSheet("""
                QPushButton { text-align: left; padding: 6px 12px; border-radius: 0; border: none; font-size: 13px; }
                QPushButton:hover { background-color: rgba(124,58,237,0.08); }
            """)
            p = path
            btn.clicked.connect(lambda checked=False, p=p: self.open_folder_callback(p))
            qa_inner_layout.addWidget(btn)

        qa_inner_layout.addStretch()
        qa_scroll.setWidget(qa_inner)
        qa_layout.addWidget(qa_scroll)
        self._splitter.addWidget(qa_container)

        # ── Drives ───────────────────────────────────────────────────────────
        drives_container = QWidget()
        drives_layout = QVBoxLayout(drives_container)
        drives_layout.setContentsMargins(0, 0, 0, 0)
        drives_layout.setSpacing(0)

        drives_label = QLabel("  DRIVES")
        drives_label.setStyleSheet("font-size: 10px; font-weight: 700; letter-spacing: 1px; color: #64748B; padding: 12px 8px 5px 8px;")
        drives_layout.addWidget(drives_label)

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
        self.system_tree_view.setIndentation(12)
        self.system_tree_view.clicked.connect(self._on_system_drive_activated)
        self.system_tree_view.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.system_tree_view.customContextMenuRequested.connect(self._on_system_tree_context_menu)
        drives_layout.addWidget(self.system_tree_view)
        self._splitter.addWidget(drives_container)

        # ── Bookmarks ────────────────────────────────────────────────────────
        bk_container = QWidget()
        bk_layout = QVBoxLayout(bk_container)
        bk_layout.setContentsMargins(0, 0, 0, 0)
        bk_layout.setSpacing(0)

        bk_header = QHBoxLayout()
        bk_header.setContentsMargins(8, 12, 8, 5)
        bk_label = QLabel("BOOKMARKS")
        bk_label.setStyleSheet("font-size: 10px; font-weight: 700; letter-spacing: 1px; color: #64748B;")
        bk_header.addWidget(bk_label)
        bk_header.addStretch()

        self.add_folder_button = QToolButton()
        self.add_folder_button.setIcon(create_icon("add_folder"))
        self.add_folder_button.setToolTip("Add folder to bookmarks")
        self.add_folder_button.setFixedSize(22, 22)
        self.add_folder_button.clicked.connect(self.select_folder)
        bk_header.addWidget(self.add_folder_button)

        self.remove_folder_button = QToolButton()
        self.remove_folder_button.setIcon(create_icon("remove_folder"))
        self.remove_folder_button.setToolTip("Remove selected bookmark")
        self.remove_folder_button.setFixedSize(22, 22)
        self.remove_folder_button.clicked.connect(self.remove_folder)
        bk_header.addWidget(self.remove_folder_button)

        bk_header_widget = QWidget()
        bk_header_widget.setLayout(bk_header)
        bk_layout.addWidget(bk_header_widget)

        self.folder_list_widget = QListWidget(self)
        self.folder_list_widget.setObjectName("FolderList")
        self.folder_list_widget.setAcceptDrops(True)
        self.folder_list_widget.installEventFilter(self)
        self.folder_list_widget.itemClicked.connect(self._on_folder_clicked)
        self.folder_list_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        bk_layout.addWidget(self.folder_list_widget)
        self._splitter.addWidget(bk_container)

        # Restore splitter sizes from QSettings (default 1:1:2)
        s = QSettings("Macan Angkasa", "Macan Explorer")
        splitter_state = s.value("sidebar/splitter_state")
        if splitter_state:
            self._splitter.restoreState(splitter_state)
        else:
            self._splitter.setSizes([180, 140, 240])

        self._splitter.splitterMoved.connect(self._save_splitter_state)
        outer_layout.addWidget(self._splitter)

    def _save_splitter_state(self):
        s = QSettings("Macan Angkasa", "Macan Explorer")
        s.setValue("sidebar/splitter_state", self._splitter.saveState())
        s.sync()

    def load_bookmarks(self):
        self.folder_list_widget.clear()
        # Merge added_folders and bookmarks for display
        folders = list(dict.fromkeys(
            self.config_manager.get("added_folders", []) +
            self.config_manager.get("bookmarks", [])
        ))
        for folder in folders:
            item = QListWidgetItem(create_icon("bookmark"), os.path.basename(folder) or folder)
            item.setToolTip(folder)
            item.setData(Qt.ItemDataRole.UserRole, folder)
            self.folder_list_widget.addItem(item)

    def _on_system_drive_activated(self, index):
        path = self.file_system_model.filePath(index)
        if os.path.isdir(path):
            self.open_folder_callback(path)

    def select_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder to Bookmark")
        if folder_path:
            if self.config_manager.add_to_list("added_folders", folder_path):
                self.load_bookmarks()

    def remove_folder(self):
        current_item = self.folder_list_widget.currentItem()
        if not current_item:
            QMessageBox.warning(self, "Remove Bookmark", "Please select a bookmark to remove.")
            return
        folder_path = current_item.data(Qt.ItemDataRole.UserRole) or current_item.text()
        reply = QMessageBox.question(
            self, 'Remove Bookmark',
            f"Remove '{os.path.basename(folder_path)}' from bookmarks?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.config_manager.remove_from_list("added_folders", folder_path)
            self.config_manager.remove_from_list("bookmarks", folder_path)
            self.load_bookmarks()

    def _on_folder_clicked(self, item):
        path = item.data(Qt.ItemDataRole.UserRole) or item.text()
        self.open_folder_callback(path)

    def _on_system_tree_context_menu(self, position):
        index = self.system_tree_view.indexAt(position)
        if not index.isValid():
            return
        path = self.file_system_model.filePath(index)
        info = QFileInfo(path)
        if not info.isRoot():
            return
        menu = QMenu(self)
        menu.addAction("Drive Properties").triggered.connect(lambda: self._show_drive_properties(path))
        menu.exec(self.system_tree_view.viewport().mapToGlobal(position))

    def _show_drive_properties(self, path):
        try:
            usage = shutil.disk_usage(path)
            total_str = _format_size(usage.total)
            free_str = _format_size(usage.free)
            used_str = _format_size(usage.used)
            used_pct = (usage.used / usage.total * 100) if usage.total > 0 else 0
            dialog = DrivePropertiesDialog(path, total_str, used_str, free_str, used_pct, self)
            dialog.exec()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not retrieve drive info: {e}")

    def eventFilter(self, obj, event):
        if obj == self.folder_list_widget:
            if event.type() == QEvent.Type.DragEnter:
                if event.mimeData().hasUrls():
                    event.acceptProposedAction()
                else:
                    event.ignore()
                return True
            if event.type() == QEvent.Type.Drop:
                if event.mimeData().hasUrls():
                    added = False
                    for url in event.mimeData().urls():
                        if url.isLocalFile():
                            path = url.toLocalFile()
                            if os.path.isdir(path):
                                if self.config_manager.add_to_list("added_folders", path):
                                    added = True
                    if added:
                        self.load_bookmarks()
                    event.acceptProposedAction()
                return True
            if event.type() == QEvent.Type.DragMove:
                event.acceptProposedAction()
                return True
        return super().eventFilter(obj, event)


# ─────────────────────────────────────────────────────────────────────────────
#  TAB MANAGER
# ─────────────────────────────────────────────────────────────────────────────

class TabManager(QWidget):
    current_tab_changed = Signal(object)

    def __init__(self, config_manager, parent=None):
        super().__init__(parent)
        self.config_manager = config_manager
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.setMovable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.currentChanged.connect(self._on_tab_change)

        close_icon_path = "close_icon_temp.png"
        create_icon("close").pixmap(QSize(14, 14)).save(close_icon_path)
        self.tabs.setStyleSheet(
            f"QTabBar::close-button {{ image: url({close_icon_path}); }}"
            "QTabBar::close-button:hover { background-color: #e74c3c; border-radius: 7px; }"
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.tabs)
        self.setLayout(layout)

        self.logger = ShrineLogger()
        self.add_tab("Home", folder_path=None)

        if os.path.exists(close_icon_path):
            QTimer.singleShot(1000, lambda: os.remove(close_icon_path) if os.path.exists(close_icon_path) else None)

    def _on_tab_change(self, index):
        self.current_tab_changed.emit(self.tabs.widget(index))

    def add_tab(self, label, folder_path=None):
        try:
            file_view = FileView(self.config_manager, folder_path)
            index = self.tabs.addTab(file_view, create_icon("tab_glyph"), label)
            self.tabs.setCurrentIndex(index)
            self.tabs.setTabToolTip(index, folder_path or QDir.homePath())
            self.logger.ritual("📂", "open_tab", label)
        except Exception as e:
            traceback.print_exc()
            ErrorHandler().handle(e, context=f"TabManager:add_tab({label})")

    def close_tab(self, index):
        if self.tabs.count() > 1:
            widget = self.tabs.widget(index)
            if widget:
                widget.deleteLater()
            self.tabs.removeTab(index)
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


# ─────────────────────────────────────────────────────────────────────────────
#  CUSTOM TITLE BAR
# ─────────────────────────────────────────────────────────────────────────────

class TitleBar(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent_window = parent
        self.setObjectName("TitleBar")
        self.pressing = False
        self.start_pos = None

        layout = QHBoxLayout()
        layout.setContentsMargins(8, 0, 0, 0)
        layout.setSpacing(4)

        self.icon_label = QLabel()
        self.icon_label.setPixmap(create_icon("app_icon").pixmap(QSize(16, 16)))
        layout.addWidget(self.icon_label)

        self.title_label = QLabel(parent.windowTitle())
        self.title_label.setObjectName("TitleLabel")
        layout.addWidget(self.title_label)
        layout.addStretch()

        self.minimize_button = QToolButton(self)
        self.minimize_button.setIcon(create_icon("minimize"))
        self.minimize_button.setToolTip("Minimize")
        self.minimize_button.setFixedSize(36, 28)
        self.minimize_button.clicked.connect(self.parent_window.showMinimized)
        layout.addWidget(self.minimize_button)

        self.maximize_button = QToolButton(self)
        self.maximize_button.setIcon(create_icon("maximize"))
        self.maximize_button.setToolTip("Maximize")
        self.maximize_button.setFixedSize(36, 28)
        self.maximize_button.clicked.connect(self.toggle_maximize)
        layout.addWidget(self.maximize_button)

        self.close_button = QToolButton(self)
        self.close_button.setObjectName("CloseButton")
        self.close_button.setIcon(create_icon("close"))
        self.close_button.setToolTip("Close")
        self.close_button.setFixedSize(46, 28)
        self.close_button.clicked.connect(self.parent_window.close)
        layout.addWidget(self.close_button)

        self.setLayout(layout)
        self.setFixedHeight(34)

    def update_icons(self, theme: str):
        """Re-render all title bar icons for the current theme."""
        self.icon_label.setPixmap(create_icon("app_icon", theme=theme).pixmap(QSize(16, 16)))
        self.minimize_button.setIcon(create_icon("minimize", theme=theme))
        close_icon_color = "#374151" if theme == "light" else "#e0e0e0"
        self.close_button.setIcon(create_icon("close", color=close_icon_color))
        if self.parent_window.isMaximized():
            self.maximize_button.setIcon(create_icon("restore", theme=theme))
        else:
            self.maximize_button.setIcon(create_icon("maximize", theme=theme))

    def toggle_maximize(self):
        if self.parent_window.isMaximized():
            self.parent_window.showNormal()
            self.maximize_button.setIcon(create_icon("maximize"))
            self.maximize_button.setToolTip("Maximize")
        else:
            self.parent_window.showMaximized()
            self.maximize_button.setIcon(create_icon("restore"))
            self.maximize_button.setToolTip("Restore")

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


# ─────────────────────────────────────────────────────────────────────────────
#  DIALOGS
# ─────────────────────────────────────────────────────────────────────────────

class DrivePropertiesDialog(QDialog):
    def __init__(self, path, total, used, free, used_pct, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Drive Properties: {path}")
        self.setMinimumWidth(400)
        layout = QVBoxLayout(self)
        layout.setSpacing(14)
        layout.setContentsMargins(18, 16, 18, 14)

        title = QLabel(f"💾  {path}")
        title.setStyleSheet(
            "font-size: 15px; font-weight: 700; padding: 4px 0;"
            "background: transparent;"
        )
        layout.addWidget(title)

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        layout.addWidget(sep)

        form = QFormLayout()
        form.setSpacing(10)
        form.setContentsMargins(4, 0, 4, 0)
        for label, value in [("Total Size:", total), ("Used Space:", used), ("Free Space:", free)]:
            lbl = QLabel(label)
            lbl.setStyleSheet(
                "font-weight: 600; color: #64748B;"
                "background: transparent;"
            )
            val = QLabel(value)
            val.setStyleSheet("background: transparent;")
            form.addRow(lbl, val)
        layout.addLayout(form)

        # Progress bar with readable label above
        pct_label = QLabel(f"{used_pct:.1f}% used  —  {used} used of {total}  ({free} free)")
        pct_label.setStyleSheet(
            "font-size: 11px; color: #94A3B8;"
            "background: transparent;"
            "padding: 2px 0;"
        )
        layout.addWidget(pct_label)

        bar = QProgressBar()
        bar.setValue(int(used_pct))
        bar.setFormat("")          # text drawn by label above, bar stays clean
        bar.setFixedHeight(14)
        bar.setTextVisible(False)
        layout.addWidget(bar)

        btns = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        btns.accepted.connect(self.accept)
        layout.addWidget(btns)


class SearchResultsDialog(QDialog):
    result_selected = Signal(str)

    def __init__(self, results, query, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Search: '{query}'")
        self.setMinimumSize(650, 420)
        layout = QVBoxLayout(self)

        header = QLabel(f"Found {len(results)} result(s) for <b>'{query}'</b>")
        header.setStyleSheet("font-size: 13px; padding: 4px;")
        layout.addWidget(header)

        self.list_widget = QListWidget()
        for r in results:
            if os.path.isdir(r):
                item = QListWidgetItem(create_icon("folder-closed"), r)
            else:
                item = QListWidgetItem(r)
                item.setToolTip(r)
            self.list_widget.addItem(item)
        self.list_widget.itemDoubleClicked.connect(self._on_item_double_clicked)
        layout.addWidget(self.list_widget)

        btns = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        btns.rejected.connect(self.reject)
        layout.addWidget(btns)

    def _on_item_double_clicked(self, item):
        full_path = item.text()
        if os.path.isdir(full_path):
            self.result_selected.emit(full_path)
        else:
            QDesktopServices.openUrl(QUrl.fromLocalFile(full_path))
            self.result_selected.emit(os.path.dirname(full_path))
        self.accept()


class PropertiesDialog(QDialog):
    def __init__(self, path, icon, parent=None):
        super().__init__(parent)
        self.path = path
        self.icon = icon
        self.file_info = QFileInfo(path)
        self.original_name = self.file_info.fileName()
        self.name_changed = False
        self.setWindowTitle(f"Properties")
        self.setMinimumWidth(460)
        self._init_ui()
        self._populate_data()

    def _init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(12)

        top_layout = QHBoxLayout()
        icon_label = QLabel()
        icon_label.setPixmap(self.icon.pixmap(QSize(48, 48)))
        icon_label.setStyleSheet("background: transparent;")
        self.name_edit = QLineEdit(self.original_name)
        self.name_edit.setStyleSheet("font-size: 14px; font-weight: 600;")
        top_layout.addWidget(icon_label)
        top_layout.addWidget(self.name_edit)
        main_layout.addLayout(top_layout)

        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        main_layout.addWidget(line)

        self.form_layout = QFormLayout()
        self.form_layout.setSpacing(10)
        self.form_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.addLayout(self.form_layout)
        main_layout.addStretch()

        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.button(QDialogButtonBox.StandardButton.Ok).setObjectName("primaryBtn")
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        main_layout.addWidget(button_box)

    def _populate_data(self):
        _tp = "background: transparent;"

        def _lbl(text, selectable=False):
            l = QLabel(text)
            l.setStyleSheet(_tp)
            if selectable:
                l.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
            return l

        def _row_lbl(text):
            l = QLabel(text)
            l.setStyleSheet(f"font-weight: 600; color: #64748B; {_tp}")
            return l

        if self.file_info.isDir():
            type_desc = "File Folder"
        else:
            type_desc = _get_file_type_label(self.original_name)
        self.form_layout.addRow(_row_lbl("Type:"), _lbl(type_desc))

        location = os.path.dirname(self.file_info.absoluteFilePath())
        loc_label = _lbl(location, selectable=True)
        loc_label.setWordWrap(True)
        self.form_layout.addRow(_row_lbl("Location:"), loc_label)

        if self.file_info.isDir():
            size_bytes = _get_folder_size(self.path)
        else:
            size_bytes = self.file_info.size()
        size_formatted = f"{_format_size(size_bytes)} ({size_bytes:,} bytes)"
        self.form_layout.addRow(_row_lbl("Size:"), _lbl(size_formatted))

        if self.file_info.isDir():
            num_files, num_folders = _get_folder_contents_count(self.path)
            self.form_layout.addRow(_row_lbl("Contains:"), _lbl(f"{num_files} files, {num_folders} folders"))

        try:
            stat_info = os.stat(self.path)
            for label, ts in [
                ("Created:", stat_info.st_ctime),
                ("Modified:", stat_info.st_mtime),
                ("Accessed:", stat_info.st_atime),
            ]:
                dt_str = datetime.datetime.fromtimestamp(ts).strftime("%d %B %Y, %H:%M:%S")
                self.form_layout.addRow(_row_lbl(label), _lbl(dt_str, selectable=True))
        except Exception:
            pass

    def accept(self):
        new_name = self.name_edit.text()
        if new_name and new_name != self.original_name:
            new_path = os.path.join(os.path.dirname(self.path), new_name)
            if os.path.exists(new_path):
                QMessageBox.critical(self, "Error", f"'{new_name}' already exists.")
                return
            try:
                os.rename(self.path, new_path)
                self.name_changed = True
            except Exception as e:
                QMessageBox.critical(self, "Rename Error", str(e))
                return
        super().accept()


class OperationProgressDialog(QProgressDialog):
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setWindowModality(Qt.WindowModality.WindowModal)
        self.setMinimumDuration(0)
        self.setCancelButtonText("Cancel")
        self.setValue(0)
        self.setAutoClose(True)
        self.setAutoReset(True)
        self.setMinimumWidth(380)


# ─────────────────────────────────────────────────────────────────────────────
#  SMART RENAME ENGINE
# ─────────────────────────────────────────────────────────────────────────────

class RenameRule:
    def __init__(self, pattern: str, replacement: str):
        self.pattern = pattern
        self.replacement = replacement

    def apply(self, name: str) -> str:
        stem = Path(name).stem
        ext = Path(name).suffix
        new_stem = stem.replace(self.pattern, self.replacement)
        return new_stem + ext


class SmartRenameEngine:
    """Multi-pattern rename engine with preview support."""

    @staticmethod
    def parse_rules(rule_str: str) -> List[RenameRule]:
        """Parse comma-separated pairs: pattern, replacement, pattern2, replacement2, ..."""
        rules = []
        parts = [p.strip() for p in rule_str.split(",")]
        i = 0
        while i < len(parts) - 1:
            pattern = parts[i]
            replacement = parts[i + 1]
            if pattern:
                rules.append(RenameRule(pattern, replacement))
            i += 2
        return rules

    @staticmethod
    def apply_rules(
        name: str,
        rules: List[RenameRule],
        prefix: str = "",
        suffix: str = "",
        numbering: bool = False,
        num_start: int = 1,
        num_padding: int = 2,
        num_sep: str = "_",
        counter: int = 0,
        change_ext: str = "",
        case_mode: str = "none",
        remove_special: bool = False,
        remove_spaces: bool = False,
        space_replacement: str = "_",
    ) -> str:
        stem = Path(name).stem
        ext = Path(name).suffix

        for rule in rules:
            stem = stem.replace(rule.pattern, rule.replacement)

        if remove_special:
            stem = re.sub(r'[^\w\s\-.]', '', stem)

        if remove_spaces:
            stem = stem.replace(" ", space_replacement)

        if case_mode == "lower":
            stem = stem.lower()
        elif case_mode == "upper":
            stem = stem.upper()
        elif case_mode == "title":
            stem = stem.title()
        elif case_mode == "camel":
            words = stem.split()
            stem = words[0].lower() + "".join(w.title() for w in words[1:]) if words else stem
        elif case_mode == "snake":
            stem = "_".join(stem.lower().split())

        if numbering:
            num = num_start + counter
            num_str = str(num).zfill(num_padding)
            stem = f"{stem}{num_sep}{num_str}"

        if prefix:
            stem = prefix + stem
        if suffix:
            stem = stem + suffix

        if change_ext:
            ext = change_ext if change_ext.startswith(".") else "." + change_ext

        return stem + ext


class RenamePreviewDialog(QDialog):
    """Confirmation dialog showing all rename pairs before applying."""

    def __init__(self, renames: List[tuple], parent=None):
        super().__init__(parent)
        self.setWindowTitle("Rename Preview — Confirm Changes")
        self.setMinimumSize(700, 460)
        self.renames = renames
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        lbl = QLabel(f"⚠️  {len(self.renames)} file(s) will be renamed. Please confirm.")
        lbl.setStyleSheet("font-size: 13px; font-weight: 600; padding: 4px; background: transparent;")
        layout.addWidget(lbl)

        table = QTableView()
        model = QStandardItemModel(len(self.renames), 2)
        model.setHorizontalHeaderLabels(["Original Name", "New Name"])
        for i, (old, new) in enumerate(self.renames):
            old_item = QStandardItem(old)
            new_item = QStandardItem(new)
            old_item.setEditable(False)
            new_item.setEditable(False)
            if old != new:
                new_item.setForeground(QColor("#6EE7B7"))
            else:
                new_item.setForeground(QColor("#EF4444"))
                new_item.setText("(no change)")
            model.setItem(i, 0, old_item)
            model.setItem(i, 1, new_item)
        table.setModel(model)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table.setAlternatingRowColors(True)
        table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        layout.addWidget(table)

        btns = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        btns.button(QDialogButtonBox.StandardButton.Ok).setText("✅  Apply Rename")
        btns.button(QDialogButtonBox.StandardButton.Ok).setObjectName("primaryBtn")
        btns.accepted.connect(self.accept)
        btns.rejected.connect(self.reject)
        layout.addWidget(btns)


class SmartRenameDock(QWidget):
    """Dock widget panel for Smart Rename with Find&Replace, Numbering, and Regex tabs."""

    # Signal emitted when rename is applied so MainWindow can refresh
    rename_applied = Signal(str)   # log message
    rename_error   = Signal(str)   # error message

    def __init__(self, get_current_path_fn, get_selected_paths_fn, refresh_fn, parent=None):
        super().__init__(parent)
        self._get_current_path  = get_current_path_fn
        self._get_selected_paths = get_selected_paths_fn
        self._refresh           = refresh_fn
        self._last_rename_ops: List[tuple] = []
        self._current_theme = "dark"
        self._build()

    def set_theme(self, theme: str):
        self._current_theme = theme

    # ── Build UI ─────────────────────────────────────────────────────────────

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(8)
        layout.setContentsMargins(10, 10, 10, 10)

        tabs = QTabWidget()

        # ── Tab 1: Find & Replace ────────────────────────────────────────────
        tab1 = QWidget()
        t1 = QVBoxLayout(tab1)
        t1.setSpacing(8)

        row1 = QHBoxLayout()
        lbl_rules = QLabel("RULES")
        lbl_rules.setStyleSheet("font-weight:700; font-size:11px; letter-spacing:0.8px; background:transparent;")
        row1.addWidget(lbl_rules)
        row1.addStretch()
        help_lbl = QLabel("Format: pattern, replacement, pattern2, replacement2, …")
        help_lbl.setStyleSheet("color: #64748B; font-size: 11px; background:transparent;")
        row1.addWidget(help_lbl)
        t1.addLayout(row1)

        self.rule_input = QLineEdit()
        self.rule_input.setPlaceholderText("LK21-DE, (2023)-")
        self.rule_input.textChanged.connect(self._update_preview)
        t1.addWidget(self.rule_input)

        opts = QGridLayout()
        opts.setSpacing(8)

        opts.addWidget(QLabel("Prefix:"), 0, 0)
        self.prefix_input = QLineEdit()
        self.prefix_input.setPlaceholderText("Add prefix…")
        self.prefix_input.textChanged.connect(self._update_preview)
        opts.addWidget(self.prefix_input, 0, 1)

        opts.addWidget(QLabel("Suffix:"), 0, 2)
        self.suffix_input = QLineEdit()
        self.suffix_input.setPlaceholderText("Add suffix…")
        self.suffix_input.textChanged.connect(self._update_preview)
        opts.addWidget(self.suffix_input, 0, 3)

        opts.addWidget(QLabel("Case:"), 1, 0)
        self.case_combo = QComboBox()
        self.case_combo.addItems(["No Change", "lowercase", "UPPERCASE", "Title Case", "camelCase", "snake_case"])
        self.case_combo.currentIndexChanged.connect(self._update_preview)
        opts.addWidget(self.case_combo, 1, 1)

        opts.addWidget(QLabel("Extension:"), 1, 2)
        self.ext_input = QLineEdit()
        self.ext_input.setPlaceholderText(".txt, .jpg, …")
        self.ext_input.textChanged.connect(self._update_preview)
        opts.addWidget(self.ext_input, 1, 3)

        t1.addLayout(opts)

        checks = QHBoxLayout()
        self.chk_remove_special = QCheckBox("Remove special chars")
        self.chk_remove_special.stateChanged.connect(self._update_preview)
        self.chk_remove_spaces = QCheckBox("Replace spaces with:")
        self.chk_remove_spaces.stateChanged.connect(self._update_preview)
        self.space_rep = QLineEdit("_")
        self.space_rep.setMaximumWidth(50)
        self.space_rep.textChanged.connect(self._update_preview)
        checks.addWidget(self.chk_remove_special)
        checks.addWidget(self.chk_remove_spaces)
        checks.addWidget(self.space_rep)
        checks.addStretch()
        t1.addLayout(checks)

        tabs.addTab(tab1, "🔍 Find & Replace")

        # ── Tab 2: Numbering ─────────────────────────────────────────────────
        tab2 = QWidget()
        t2 = QFormLayout(tab2)
        t2.setSpacing(8)
        t2.setContentsMargins(10, 10, 10, 10)

        self.chk_numbering = QCheckBox("Enable auto-numbering")
        self.chk_numbering.stateChanged.connect(self._update_preview)
        t2.addRow(self.chk_numbering)

        self.num_start = QLineEdit("1")
        self.num_start.textChanged.connect(self._update_preview)
        t2.addRow("Start from:", self.num_start)

        self.num_padding = QLineEdit("2")
        self.num_padding.textChanged.connect(self._update_preview)
        t2.addRow("Zero padding:", self.num_padding)

        self.num_sep = QLineEdit("_")
        self.num_sep.textChanged.connect(self._update_preview)
        t2.addRow("Separator:", self.num_sep)

        tabs.addTab(tab2, "🔢 Numbering")

        # ── Tab 3: Regex ─────────────────────────────────────────────────────
        tab3 = QWidget()
        t3 = QVBoxLayout(tab3)
        t3.setSpacing(8)
        t3.setContentsMargins(10, 10, 10, 10)

        self.regex_pattern = QLineEdit()
        self.regex_pattern.setPlaceholderText(r"Regex pattern (e.g. \d{4})")
        self.regex_pattern.textChanged.connect(self._update_preview)
        self.regex_replace = QLineEdit()
        self.regex_replace.setPlaceholderText(r"Replacement (use \1, \2 for groups)")
        self.regex_replace.textChanged.connect(self._update_preview)

        t3.addWidget(QLabel("Pattern:"))
        t3.addWidget(self.regex_pattern)
        t3.addWidget(QLabel("Replacement:"))
        t3.addWidget(self.regex_replace)

        self.chk_regex_enabled = QCheckBox("Enable regex mode")
        self.chk_regex_enabled.stateChanged.connect(self._update_preview)
        t3.addWidget(self.chk_regex_enabled)
        t3.addStretch()

        tabs.addTab(tab3, "⚡ Regex")

        layout.addWidget(tabs)

        # ── Live Preview ─────────────────────────────────────────────────────
        preview_lbl = QLabel("LIVE PREVIEW")
        preview_lbl.setStyleSheet("font-weight:700; font-size:11px; letter-spacing:0.8px; background:transparent;")
        layout.addWidget(preview_lbl)

        self.preview_table = QTableView()
        self.preview_model = QStandardItemModel()
        self.preview_model.setHorizontalHeaderLabels(["Original", "→", "Renamed"])
        self.preview_table.setModel(self.preview_model)
        self.preview_table.setMaximumHeight(110)
        self.preview_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.preview_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.preview_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.preview_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.preview_table.setAlternatingRowColors(True)
        self.preview_table.verticalHeader().setVisible(False)
        layout.addWidget(self.preview_table)

        # ── Action Buttons ───────────────────────────────────────────────────
        btn_row = QHBoxLayout()
        btn_row.setSpacing(8)

        btn_apply = QPushButton("✅  Apply Rename")
        btn_apply.setObjectName("primaryBtn")
        btn_apply.clicked.connect(self._apply_rename)
        btn_row.addWidget(btn_apply)

        btn_preview = QPushButton("👁  Preview All")
        btn_preview.clicked.connect(self._show_full_preview)
        btn_row.addWidget(btn_preview)

        btn_undo = QPushButton("↩  Undo Last Rename")
        btn_undo.setObjectName("dangerBtn")
        btn_undo.clicked.connect(self._undo_last_rename)
        btn_row.addWidget(btn_undo)

        btn_row.addStretch()
        layout.addLayout(btn_row)

    # ── Rename Logic ─────────────────────────────────────────────────────────

    def _get_params(self) -> dict:
        case_map = {0: "none", 1: "lower", 2: "upper", 3: "title", 4: "camel", 5: "snake"}
        try:
            num_start = int(self.num_start.text() or 1)
        except ValueError:
            num_start = 1
        try:
            num_padding = int(self.num_padding.text() or 2)
        except ValueError:
            num_padding = 2
        return {
            "rules":            SmartRenameEngine.parse_rules(self.rule_input.text()),
            "prefix":           self.prefix_input.text(),
            "suffix":           self.suffix_input.text(),
            "case_mode":        case_map.get(self.case_combo.currentIndex(), "none"),
            "numbering":        self.chk_numbering.isChecked(),
            "num_start":        num_start,
            "num_padding":      num_padding,
            "num_sep":          self.num_sep.text() or "_",
            "change_ext":       self.ext_input.text(),
            "remove_special":   self.chk_remove_special.isChecked(),
            "remove_spaces":    self.chk_remove_spaces.isChecked(),
            "space_replacement": self.space_rep.text() or "_",
            "regex_enabled":    self.chk_regex_enabled.isChecked(),
            "regex_pattern":    self.regex_pattern.text(),
            "regex_replace":    self.regex_replace.text(),
        }

    def _compute_new_name(self, name: str, params: dict, counter: int = 0) -> str:
        new_name = name
        if params.get("regex_enabled") and params.get("regex_pattern"):
            try:
                stem = Path(new_name).stem
                ext  = Path(new_name).suffix
                stem = re.sub(params["regex_pattern"], params.get("regex_replace", ""), stem)
                new_name = stem + ext
            except re.error:
                pass
        return SmartRenameEngine.apply_rules(
            new_name,
            rules=params["rules"],
            prefix=params["prefix"],
            suffix=params["suffix"],
            numbering=params["numbering"],
            num_start=params["num_start"],
            num_padding=params["num_padding"],
            num_sep=params["num_sep"],
            counter=counter,
            change_ext=params["change_ext"],
            case_mode=params["case_mode"],
            remove_special=params["remove_special"],
            remove_spaces=params["remove_spaces"],
            space_replacement=params["space_replacement"],
        )

    def refresh_preview(self):
        """Call this when the current folder / selection changes."""
        self._update_preview()

    def _update_preview(self):
        params = self._get_params()
        selected = self._get_selected_paths()
        if selected:
            names = [os.path.basename(p) for p in selected[:10]]
        else:
            cur = self._get_current_path()
            if cur and os.path.isdir(cur):
                try:
                    all_entries = os.listdir(cur)
                    names = all_entries[:5]
                except OSError:
                    names = []
            else:
                names = []

        self.preview_model.clear()
        self.preview_model.setHorizontalHeaderLabels(["Original", "→", "Renamed"])

        for i, name in enumerate(names):
            new_name  = self._compute_new_name(name, params, i)
            old_item  = QStandardItem(name)
            arrow     = QStandardItem("→")
            new_item  = QStandardItem(new_name)
            old_item.setEditable(False)
            arrow.setEditable(False)
            arrow.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            new_item.setEditable(False)
            if new_name != name:
                new_item.setForeground(QColor("#6EE7B7" if self._current_theme == "dark" else "#16A34A"))
            else:
                new_item.setForeground(QColor("#64748B"))
            self.preview_model.appendRow([old_item, arrow, new_item])

    def _apply_rename(self):
        params   = self._get_params()
        selected = self._get_selected_paths()
        cur_path = self._get_current_path()

        if not selected:
            reply = QMessageBox.question(
                self, "Apply Rename",
                "No files selected. Rename all files in current folder?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.No:
                return
            if cur_path and os.path.isdir(cur_path):
                try:
                    selected = [os.path.join(cur_path, n) for n in os.listdir(cur_path)]
                except OSError:
                    selected = []

        renames = []
        for i, path in enumerate(selected):
            old_name = os.path.basename(path)
            new_name = self._compute_new_name(old_name, params, i)
            if new_name != old_name:
                renames.append((old_name, new_name, path))

        if not renames:
            QMessageBox.information(self, "No Changes", "No files would be renamed with current rules.")
            return

        dlg = RenamePreviewDialog([(old, new) for old, new, _ in renames], self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            self._last_rename_ops = []
            errors = []
            for old_name, new_name, old_path in renames:
                new_path = os.path.join(os.path.dirname(old_path), new_name)
                try:
                    os.rename(old_path, new_path)
                    self._last_rename_ops.append((new_path, old_path))
                    self.rename_applied.emit(f"Renamed: {old_name} → {new_name}")
                except Exception as e:
                    errors.append(f"{old_name}: {e}")
                    self.rename_error.emit(f"Rename error {old_name}: {e}")
            self._refresh()
            if errors:
                QMessageBox.warning(self, "Some Errors", "\n".join(errors))
            else:
                self.rename_applied.emit(f"Batch rename complete: {len(renames)} files")
            self._update_preview()

    def _show_full_preview(self):
        params   = self._get_params()
        selected = self._get_selected_paths()
        cur_path = self._get_current_path()
        if not selected and cur_path and os.path.isdir(cur_path):
            try:
                selected = [os.path.join(cur_path, n) for n in os.listdir(cur_path)]
            except OSError:
                selected = []
        pairs = [(os.path.basename(p), self._compute_new_name(os.path.basename(p), params, i))
                 for i, p in enumerate(selected)]
        RenamePreviewDialog(pairs, self).exec()

    def _undo_last_rename(self):
        if not self._last_rename_ops:
            QMessageBox.information(self, "Undo", "No rename operations to undo.")
            return
        errors = []
        for new_path, old_path in self._last_rename_ops:
            try:
                os.rename(new_path, old_path)
                self.rename_applied.emit(f"Undone rename: → {os.path.basename(old_path)}")
            except Exception as e:
                errors.append(str(e))
        self._last_rename_ops = []
        self._refresh()
        if errors:
            QMessageBox.warning(self, "Undo Errors", "\n".join(errors))
        self._update_preview()


class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About Macan Explorer")
        self.setMinimumWidth(460)
        self.setMinimumHeight(320)
        layout = QVBoxLayout(self)
        layout.setSpacing(14)
        layout.setContentsMargins(28, 24, 28, 20)

        _lbl_style = "background: transparent; border: none;"

        title = QLabel("🐅  Macan Explorer")
        title.setStyleSheet(f"{_lbl_style} font-size: 22px; font-weight: 700; letter-spacing: 0.5px;")
        layout.addWidget(title)

        ver = QLabel("Enterprise Edition  ·  v5.0.0")
        ver.setStyleSheet(f"{_lbl_style} font-size: 12px; color: #7C3AED; font-weight: 600;")
        layout.addWidget(ver)

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        layout.addWidget(sep)

        desc = QLabel(
            "Macan Explorer is an enterprise-grade file management application for developers, "
            "creators, and power users. Built on PySide6 with a focus on speed, clarity, and control.\n\n"
            "Features: Multi-tab navigation  ·  Smart Rename  ·  Activity log  ·  Bookmark manager\n"
            "Breadcrumb navigation  ·  Thumbnail previews  ·  Terminal integration\n"
            "Light/Dark themes  ·  Drag & Drop  ·  Smart search  ·  File operations"
        )
        desc.setWordWrap(True)
        desc.setStyleSheet(f"{_lbl_style} font-size: 12px;")
        layout.addWidget(desc)

        sep2 = QFrame()
        sep2.setFrameShape(QFrame.Shape.HLine)
        layout.addWidget(sep2)

        copy_label = QLabel("Copyright © 2026 Danx Exodus — Macan Angkasa")
        copy_label.setStyleSheet(f"{_lbl_style} color: #64748B; font-size: 11px;")
        layout.addWidget(copy_label)

        btns = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        btns.button(QDialogButtonBox.StandardButton.Ok).setObjectName("primaryBtn")
        btns.accepted.connect(self.accept)
        layout.addWidget(btns)


# ─────────────────────────────────────────────────────────────────────────────
#  ACTIVITY LOG DOCK WIDGET
# ─────────────────────────────────────────────────────────────────────────────

class ActivityLogDock(QWidget):
    """The UI container for the activity log."""
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Toolbar
        toolbar = QHBoxLayout()
        toolbar.setContentsMargins(8, 6, 8, 6)
        toolbar.setSpacing(6)

        lbl = QLabel("Activity Log")
        lbl.setStyleSheet("font-weight: 700; font-size: 11px; text-transform: uppercase; letter-spacing: 0.8px;")
        toolbar.addWidget(lbl)
        toolbar.addStretch()

        self.export_btn = QPushButton("Export")
        self.export_btn.setMaximumHeight(24)
        self.export_btn.setMaximumWidth(60)
        self.export_btn.setStyleSheet("font-size: 11px;")
        toolbar.addWidget(self.export_btn)

        self.clear_btn = QPushButton("Clear")
        self.clear_btn.setMaximumHeight(24)
        self.clear_btn.setMaximumWidth(50)
        self.clear_btn.setObjectName("dangerBtn")
        self.clear_btn.setStyleSheet("font-size: 11px;")
        toolbar.addWidget(self.clear_btn)

        tb_widget = QWidget()
        tb_widget.setLayout(toolbar)
        tb_widget.setStyleSheet("background-color: transparent; border-bottom: 1px solid #1A1D2E;")
        layout.addWidget(tb_widget)

        # Log area
        self.log_view = QPlainTextEdit()
        self.log_view.setObjectName("logView")
        self.log_view.setReadOnly(True)
        log_font = QFont("Consolas", 10)
        log_font.setStyleHint(QFont.StyleHint.Monospace)
        self.log_view.setFont(log_font)
        layout.addWidget(self.log_view)

        self.activity_log = ActivityLog(self.log_view)
        self.export_btn.clicked.connect(lambda: self.activity_log.export(self))
        self.clear_btn.clicked.connect(self.activity_log.clear)

    def log(self, message, level=ActivityLog.INFO):
        self.activity_log.log(message, level)


# ─────────────────────────────────────────────────────────────────────────────
#  MAIN WINDOW
# ─────────────────────────────────────────────────────────────────────────────

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Macan Explorer — Enterprise Edition")
        self.setMinimumSize(1100, 650)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setWindowIcon(create_icon("app_icon"))

        self.errors = ErrorHandler()
        self.logger = ShrineLogger()
        self.config_manager = ConfigManager()
        self.current_theme = self.config_manager.get("theme", "dark")

        # Central frame for border
        self.central_frame = QFrame(self)
        self.central_frame.setObjectName("CentralFrame")
        super().setCentralWidget(self.central_frame)

        self.main_layout = QVBoxLayout(self.central_frame)
        self.main_layout.setContentsMargins(1, 1, 1, 1)
        self.main_layout.setSpacing(0)

        # Title bar
        self.title_bar = TitleBar(self)
        self.installEventFilter(self.title_bar)
        self.main_layout.addWidget(self.title_bar)

        # Menu bar
        self._build_menu_bar()
        self.main_layout.addWidget(self.menu_bar_widget)

        # Toolbar
        self.toolbar = CommandBar(self)
        self.main_layout.addWidget(self.toolbar)

        # Breadcrumb
        self.breadcrumb = BreadcrumbBar(self)
        self.main_layout.addWidget(self.breadcrumb)

        # Content area
        self.sidebar = Sidebar(self.open_folder_from_sidebar, self.config_manager)
        self.tab_manager = TabManager(self.config_manager, self)

        # Activity log dock
        self.log_dock_widget = QDockWidget("Activity Log", self)
        self.log_dock_widget.setFeatures(
            QDockWidget.DockWidgetFeature.DockWidgetMovable |
            QDockWidget.DockWidgetFeature.DockWidgetClosable |
            QDockWidget.DockWidgetFeature.DockWidgetFloatable
        )
        self.log_dock_container = ActivityLogDock()
        self.log_dock_widget.setWidget(self.log_dock_container)
        self.log_dock_widget.setMinimumHeight(120)
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self.log_dock_widget)
        self.log_dock_widget.hide()   # not auto-load — restored later via QSettings

        # Smart Rename dock — tabified with Activity Log
        self.rename_dock_widget = QDockWidget("Smart Rename", self)
        self.rename_dock_widget.setFeatures(
            QDockWidget.DockWidgetFeature.DockWidgetMovable |
            QDockWidget.DockWidgetFeature.DockWidgetClosable |
            QDockWidget.DockWidgetFeature.DockWidgetFloatable
        )
        self.smart_rename_panel = SmartRenameDock(
            get_current_path_fn=self._get_current_path_for_rename,
            get_selected_paths_fn=self._get_selected_paths_for_rename,
            refresh_fn=self._refresh_active_view,
        )
        self.smart_rename_panel.rename_applied.connect(
            lambda msg: self.log_dock_container.log(msg, ActivityLog.SUCCESS)
        )
        self.smart_rename_panel.rename_error.connect(
            lambda msg: self.log_dock_container.log(msg, ActivityLog.ERROR)
        )
        self.rename_dock_widget.setWidget(self.smart_rename_panel)
        self.rename_dock_widget.setMinimumHeight(160)
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self.rename_dock_widget)
        self.tabifyDockWidget(self.log_dock_widget, self.rename_dock_widget)
        self.rename_dock_widget.hide()  # not auto-load — restored later via QSettings

        # Splitter
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(self.sidebar)
        splitter.addWidget(self.tab_manager)
        splitter.setSizes([210, 890])
        splitter.setHandleWidth(3)

        container = QWidget()
        content_layout = QVBoxLayout(container)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        content_layout.addWidget(splitter)

        self.main_layout.addWidget(container)

        # Status bar
        self.status = QStatusBar()
        self.status_label = QLabel("  Macan Explorer ready")
        self.status_path_label = QLabel()
        self.status.addPermanentWidget(self.status_label, 1)
        self.status.addPermanentWidget(self.status_path_label)
        self.setStatusBar(self.status)

        # Apply theme
        self._apply_theme(self.current_theme)

        # Connect signals
        self._connect_signals()
        self.connect_active_tab_signals(self.tab_manager.current_widget())

        # Set initial show_hidden
        show_hidden = self.config_manager.get("show_hidden", False)
        self.toolbar.action_show_hidden.setChecked(show_hidden)

        self._active_tab_widget = None

        # Restore QSettings (window geometry, dock visibility, smart rename state)
        self._restore_settings()


    # ── QSettings: save / restore ─────────────────────────────────────────────

    def _qsettings(self) -> QSettings:
        return QSettings("Macan Angkasa", "Macan Explorer")

    def _save_settings(self):
        """Persist window geometry, dock states, and Smart Rename field values."""
        s = self._qsettings()

        # Window geometry & dock layout
        s.setValue("window/geometry", self.saveGeometry())
        s.setValue("window/state",    self.saveState())

        # Dock visibility
        s.setValue("dock/activity_log_visible",  self.log_dock_widget.isVisible())
        s.setValue("dock/smart_rename_visible",  self.rename_dock_widget.isVisible())

        # Smart Rename — Find & Replace tab
        p = self.smart_rename_panel
        s.setValue("smart_rename/rules",           p.rule_input.text())
        s.setValue("smart_rename/prefix",          p.prefix_input.text())
        s.setValue("smart_rename/suffix",          p.suffix_input.text())
        s.setValue("smart_rename/case_index",      p.case_combo.currentIndex())
        s.setValue("smart_rename/extension",       p.ext_input.text())
        s.setValue("smart_rename/remove_special",  p.chk_remove_special.isChecked())
        s.setValue("smart_rename/remove_spaces",   p.chk_remove_spaces.isChecked())
        s.setValue("smart_rename/space_rep",       p.space_rep.text())

        # Smart Rename — Numbering tab
        s.setValue("smart_rename/numbering",       p.chk_numbering.isChecked())
        s.setValue("smart_rename/num_start",       p.num_start.text())
        s.setValue("smart_rename/num_padding",     p.num_padding.text())
        s.setValue("smart_rename/num_sep",         p.num_sep.text())

        # Smart Rename — Regex tab
        s.setValue("smart_rename/regex_enabled",   p.chk_regex_enabled.isChecked())
        s.setValue("smart_rename/regex_pattern",   p.regex_pattern.text())
        s.setValue("smart_rename/regex_replace",   p.regex_replace.text())

        s.sync()

    def _restore_settings(self):
        """Restore window geometry, dock states, and Smart Rename field values."""
        s = self._qsettings()

        # Window geometry & dock layout
        geom = s.value("window/geometry")
        if geom:
            self.restoreGeometry(geom)
        state = s.value("window/state")
        if state:
            self.restoreState(state)

        # Dock visibility — default both to hidden (False) if key absent
        log_vis    = s.value("dock/activity_log_visible",  False, type=bool)
        rename_vis = s.value("dock/smart_rename_visible",  False, type=bool)
        self.log_dock_widget.setVisible(log_vis)
        self.rename_dock_widget.setVisible(rename_vis)

        # Smart Rename — Find & Replace tab
        p = self.smart_rename_panel
        if s.contains("smart_rename/rules"):
            p.rule_input.setText(s.value("smart_rename/rules", ""))
        if s.contains("smart_rename/prefix"):
            p.prefix_input.setText(s.value("smart_rename/prefix", ""))
        if s.contains("smart_rename/suffix"):
            p.suffix_input.setText(s.value("smart_rename/suffix", ""))
        if s.contains("smart_rename/case_index"):
            p.case_combo.setCurrentIndex(int(s.value("smart_rename/case_index", 0)))
        if s.contains("smart_rename/extension"):
            p.ext_input.setText(s.value("smart_rename/extension", ""))
        if s.contains("smart_rename/remove_special"):
            p.chk_remove_special.setChecked(s.value("smart_rename/remove_special", False, type=bool))
        if s.contains("smart_rename/remove_spaces"):
            p.chk_remove_spaces.setChecked(s.value("smart_rename/remove_spaces", False, type=bool))
        if s.contains("smart_rename/space_rep"):
            p.space_rep.setText(s.value("smart_rename/space_rep", "_"))

        # Smart Rename — Numbering tab
        if s.contains("smart_rename/numbering"):
            p.chk_numbering.setChecked(s.value("smart_rename/numbering", False, type=bool))
        if s.contains("smart_rename/num_start"):
            p.num_start.setText(s.value("smart_rename/num_start", "1"))
        if s.contains("smart_rename/num_padding"):
            p.num_padding.setText(s.value("smart_rename/num_padding", "2"))
        if s.contains("smart_rename/num_sep"):
            p.num_sep.setText(s.value("smart_rename/num_sep", "_"))

        # Smart Rename — Regex tab
        if s.contains("smart_rename/regex_enabled"):
            p.chk_regex_enabled.setChecked(s.value("smart_rename/regex_enabled", False, type=bool))
        if s.contains("smart_rename/regex_pattern"):
            p.regex_pattern.setText(s.value("smart_rename/regex_pattern", ""))
        if s.contains("smart_rename/regex_replace"):
            p.regex_replace.setText(s.value("smart_rename/regex_replace", ""))

    def closeEvent(self, event):
        """Save all settings before the window closes."""
        self._save_settings()
        super().closeEvent(event)

    def _build_menu_bar(self):
        """Build the application menu bar."""
        self.menu_bar_widget = QMenuBar(self)
        self.menu_bar_widget.setNativeMenuBar(False)

        # File menu
        file_menu = self.menu_bar_widget.addMenu("File")
        file_menu.addAction("New Tab\tCtrl+Tab").triggered.connect(lambda: self.open_path_in_new_tab(None))
        file_menu.addAction("New Window\tCtrl+N").triggered.connect(self.open_new_window)
        file_menu.addSeparator()
        file_menu.addAction("New Folder\tCtrl+Shift+N").triggered.connect(lambda: self.call_active_view_method('create_new_folder'))
        file_menu.addAction("New File").triggered.connect(lambda: self.call_active_view_method('create_new_file'))
        file_menu.addSeparator()
        file_menu.addAction("Open Terminal Here\tCtrl+T").triggered.connect(self._open_terminal)
        file_menu.addSeparator()
        file_menu.addAction("Exit").triggered.connect(self.close)

        # Edit menu
        edit_menu = self.menu_bar_widget.addMenu("Edit")
        edit_menu.addAction("Cut\tCtrl+X").triggered.connect(lambda: self.call_active_view_method('cut_selected_items'))
        edit_menu.addAction("Copy\tCtrl+C").triggered.connect(lambda: self.call_active_view_method('copy_selected_items'))
        edit_menu.addAction("Paste\tCtrl+V").triggered.connect(lambda: self.call_active_view_method('paste_items'))
        edit_menu.addSeparator()
        edit_menu.addAction("Select All\tCtrl+A").triggered.connect(lambda: self.call_active_view_method('select_all'))
        edit_menu.addSeparator()
        edit_menu.addAction("Delete\tDel").triggered.connect(lambda: self.call_active_view_method('delete_selected_items'))
        edit_menu.addAction("Rename\tF2").triggered.connect(lambda: self.call_active_view_method('rename_selected_item'))
        edit_menu.addSeparator()
        edit_menu.addAction("Smart Rename…\tCtrl+R").triggered.connect(self._show_smart_rename)

        # View menu
        view_menu = self.menu_bar_widget.addMenu("View")
        view_menu.addAction("Details View").triggered.connect(lambda: self.handle_view_change("details"))
        view_menu.addAction("List View").triggered.connect(lambda: self.handle_view_change("list"))
        view_menu.addAction("Icons View").triggered.connect(lambda: self.handle_view_change("icons"))
        view_menu.addSeparator()
        view_menu.addAction("Toggle Activity Log").triggered.connect(
            lambda: self.log_dock_widget.setVisible(not self.log_dock_widget.isVisible())
        )
        view_menu.addAction("Smart Rename\tCtrl+R").triggered.connect(self._show_smart_rename)
        view_menu.addSeparator()
        view_menu.addAction("Toggle Theme\tCtrl+D").triggered.connect(self._toggle_theme)
        view_menu.addSeparator()
        view_menu.addAction("Show Hidden Files\tCtrl+H").triggered.connect(
            lambda: self.toolbar.action_show_hidden.toggle()
        )
        view_menu.addSeparator()
        view_menu.addAction("Refresh\tF5").triggered.connect(lambda: self.call_active_view_method('refresh'))

        # Tools menu
        tools_menu = self.menu_bar_widget.addMenu("Tools")
        tools_menu.addAction("Clear Thumbnail Cache").triggered.connect(self.clear_thumbnail_cache)
        tools_menu.addSeparator()
        tools_menu.addAction("Search\tCtrl+F").triggered.connect(self._focus_search)

        # Help menu
        help_menu = self.menu_bar_widget.addMenu("Help")
        help_menu.addAction("About Macan Explorer").triggered.connect(self.show_about_dialog)

    def _apply_theme(self, theme):
        self.current_theme = theme
        self.config_manager.set("theme", theme)
        qss = DARK_THEME_QSS if theme == "dark" else LIGHT_THEME_QSS
        QApplication.instance().setStyleSheet(qss)
        self.breadcrumb.set_theme(theme)
        self.smart_rename_panel.set_theme(theme)
        # Update all toolbar + title bar icons for the new theme
        self.toolbar.update_icons(theme)
        self.title_bar.update_icons(theme)
        # Ensure status bar text is readable in both themes
        if theme == "light":
            self.status.setStyleSheet(
                "QStatusBar { color: #1E293B; } QStatusBar QLabel { color: #374151; }"
            )
            self.status_label.setStyleSheet("color: #1E293B;")
            self.status_path_label.setStyleSheet("color: #374151;")
        else:
            self.status.setStyleSheet("")
            self.status_label.setStyleSheet("")
            self.status_path_label.setStyleSheet("")

    def _toggle_theme(self):
        new_theme = "light" if self.current_theme == "dark" else "dark"
        self._apply_theme(new_theme)
        self.log_dock_container.log(f"Theme switched to: {new_theme}", ActivityLog.INFO)

    def _focus_search(self):
        self.toolbar.search_input.setFocus()
        self.toolbar.search_input.selectAll()

    # ── Smart Rename helper callbacks ────────────────────────────────────────

    def _get_current_path_for_rename(self) -> str:
        tab = self.tab_manager.current_widget()
        if tab and hasattr(tab, 'current_path'):
            return tab.current_path
        return ""

    def _get_selected_paths_for_rename(self) -> List[str]:
        tab = self.tab_manager.current_widget()
        if tab and hasattr(tab, 'get_selected_paths'):
            return tab.get_selected_paths()
        return []

    def _refresh_active_view(self):
        self.call_active_view_method('refresh')

    def _show_smart_rename(self):
        """Show Smart Rename dock and bring it to front."""
        self.rename_dock_widget.setVisible(True)
        self.rename_dock_widget.raise_()
        self.smart_rename_panel.refresh_preview()

    def _connect_signals(self):
        self.toolbar.back_requested.connect(lambda: self.call_active_view_method('go_back'))
        self.toolbar.forward_requested.connect(lambda: self.call_active_view_method('go_forward'))
        self.toolbar.up_requested.connect(lambda: self.call_active_view_method('go_up'))
        self.toolbar.refresh_requested.connect(lambda: self.call_active_view_method('refresh'))
        self.toolbar.address_submitted.connect(self.on_address_bar_submit)
        self.toolbar.view_mode_changed.connect(self.handle_view_change)
        self.toolbar.search_requested.connect(lambda q: self.call_active_view_method('search_files', q))
        self.toolbar.new_folder_requested.connect(lambda: self.call_active_view_method('create_new_folder'))
        self.toolbar.new_file_requested.connect(lambda: self.call_active_view_method('create_new_file'))
        self.toolbar.delete_item_requested.connect(lambda: self.call_active_view_method('delete_selected_items'))
        self.toolbar.rename_item_requested.connect(lambda: self.call_active_view_method('rename_selected_item'))
        self.toolbar.action_open_new_window.triggered.connect(self.open_new_window)
        self.toolbar.clear_cache_requested.connect(self.clear_thumbnail_cache)
        self.toolbar.action_about.triggered.connect(self.show_about_dialog)
        self.toolbar.theme_toggle_requested.connect(self._toggle_theme)
        self.toolbar.terminal_requested.connect(self._open_terminal)
        self.toolbar.show_hidden_toggled.connect(self._on_show_hidden_toggled)
        self.tab_manager.current_tab_changed.connect(self.connect_active_tab_signals)
        self.breadcrumb.path_clicked.connect(self.on_address_bar_submit)

        # Global keyboard shortcuts
        back_sc = QAction(self)
        back_sc.setShortcut(QKeySequence("Alt+Left"))
        back_sc.triggered.connect(lambda: self.call_active_view_method('go_back'))
        self.addAction(back_sc)

        fwd_sc = QAction(self)
        fwd_sc.setShortcut(QKeySequence("Alt+Right"))
        fwd_sc.triggered.connect(lambda: self.call_active_view_method('go_forward'))
        self.addAction(fwd_sc)

        up_sc = QAction(self)
        up_sc.setShortcut(QKeySequence("Alt+Up"))
        up_sc.triggered.connect(lambda: self.call_active_view_method('go_up'))
        self.addAction(up_sc)

        f5_action = QAction(self)
        f5_action.setShortcut(Qt.Key.Key_F5)
        f5_action.triggered.connect(lambda: self.call_active_view_method('refresh'))
        self.addAction(f5_action)

        new_tab_action = QAction(self)
        new_tab_action.setShortcut(QKeySequence("Ctrl+Tab"))
        new_tab_action.triggered.connect(lambda: self.open_path_in_new_tab(None))
        self.addAction(new_tab_action)

        new_win_action = QAction(self)
        new_win_action.setShortcut(QKeySequence("Ctrl+N"))
        new_win_action.triggered.connect(self.open_new_window)
        self.addAction(new_win_action)

        terminal_action = QAction(self)
        terminal_action.setShortcut(QKeySequence("Ctrl+T"))
        terminal_action.triggered.connect(self._open_terminal)
        self.addAction(terminal_action)

        theme_action = QAction(self)
        theme_action.setShortcut(QKeySequence("Ctrl+D"))
        theme_action.triggered.connect(self._toggle_theme)
        self.addAction(theme_action)

        hidden_action = QAction(self)
        hidden_action.setShortcut(QKeySequence("Ctrl+H"))
        hidden_action.triggered.connect(lambda: self.toolbar.action_show_hidden.toggle())
        self.addAction(hidden_action)

        search_action = QAction(self)
        search_action.setShortcut(QKeySequence("Ctrl+F"))
        search_action.triggered.connect(self._focus_search)
        self.addAction(search_action)

        rename_panel_action = QAction(self)
        rename_panel_action.setShortcut(QKeySequence("Ctrl+R"))
        rename_panel_action.triggered.connect(self._show_smart_rename)
        self.addAction(rename_panel_action)

    def _on_show_hidden_toggled(self, show: bool):
        self.config_manager.set("show_hidden", show)
        self.call_active_view_method('set_show_hidden', show)

    def connect_active_tab_signals(self, tab_widget):
        if not isinstance(tab_widget, FileView):
            self.toolbar.set_address_path("")
            self.toolbar.set_navigation_enabled(False, False)
            self.update_permanent_status("")
            return

        try:
            if hasattr(self, '_active_tab_widget') and self._active_tab_widget:
                self._active_tab_widget.path_changed.disconnect()
                self._active_tab_widget.navigation_state_changed.disconnect()
                self._active_tab_widget.status_message_requested.disconnect()
                self._active_tab_widget.selection_info_requested.disconnect()
                self._active_tab_widget.open_in_new_tab_requested.disconnect()
                self._active_tab_widget.activity_log_requested.disconnect()
        except (TypeError, RuntimeError):
            pass

        self._active_tab_widget = tab_widget
        tab_widget.path_changed.connect(self.toolbar.set_address_path)
        tab_widget.path_changed.connect(self.tab_manager.update_current_tab_label)
        tab_widget.path_changed.connect(self.breadcrumb.update_path)
        tab_widget.path_changed.connect(self._on_path_changed_in_status)
        tab_widget.path_changed.connect(lambda _: self.smart_rename_panel.refresh_preview())
        tab_widget.navigation_state_changed.connect(self.toolbar.set_navigation_enabled)
        tab_widget.status_message_requested.connect(self.update_status_bar)
        tab_widget.selection_info_requested.connect(self.update_permanent_status)
        tab_widget.open_in_new_tab_requested.connect(self.open_path_in_new_tab)
        tab_widget.activity_log_requested.connect(self.log_dock_container.log)

        saved_mode = self.config_manager.get('view_mode', 'details')
        self.toolbar.set_view_mode(saved_mode)
        tab_widget.set_view_mode(saved_mode)

        show_hidden = self.config_manager.get("show_hidden", False)
        tab_widget.set_show_hidden(show_hidden)

        self.toolbar.set_address_path(tab_widget.current_path)
        self.breadcrumb.update_path(tab_widget.current_path)
        tab_widget._update_navigation_state()
        self.tab_manager.update_current_tab_label(tab_widget.current_path)
        tab_widget._on_selection_changed()

    def _on_path_changed_in_status(self, path):
        self.status_path_label.setText(f"  {path}  ")

    def on_address_bar_submit(self, path):
        self.call_active_view_method('set_path', path)

    def call_active_view_method(self, method_name, *args):
        current_tab_widget = self.tab_manager.current_widget()
        if current_tab_widget and hasattr(current_tab_widget, method_name):
            method = getattr(current_tab_widget, method_name)
            if callable(method):
                method(*args)

    def handle_view_change(self, mode):
        self.call_active_view_method('set_view_mode', mode)
        self.config_manager.set('view_mode', mode)
        self.toolbar.set_view_mode(mode)

    def update_permanent_status(self, message):
        self.status_label.setText(f"  {message}")

    def update_status_bar(self, message):
        self.status.showMessage(message, 3500)

    def open_folder_from_sidebar(self, folder_path):
        if not folder_path:
            return
        active_widget = self.tab_manager.current_widget()
        if isinstance(active_widget, FileView):
            active_widget.set_path(folder_path)
            self.log_dock_container.log(f"Navigated to: {folder_path}", ActivityLog.NAV)
        else:
            self.open_path_in_new_tab(folder_path)

    def open_path_in_new_tab(self, folder_path):
        tab_label = "New Tab"
        if folder_path:
            tab_label = os.path.basename(folder_path) or os.path.normpath(folder_path)
        self.tab_manager.add_tab(tab_label, folder_path)
        self.log_dock_container.log(f"Opened new tab: {folder_path or 'Home'}", ActivityLog.INFO)

    def open_new_window(self):
        self.new_window = MainWindow()
        self.new_window.show()
        self.log_dock_container.log("New window opened", ActivityLog.INFO)

    def _open_terminal(self):
        """Open the system terminal in the current directory."""
        current_widget = self.tab_manager.current_widget()
        path = current_widget.current_path if isinstance(current_widget, FileView) else QDir.homePath()
        try:
            if platform.system() == "Windows":
                subprocess.Popen(["cmd"], cwd=path)
            elif platform.system() == "Darwin":
                subprocess.Popen(["open", "-a", "Terminal", path])
            else:
                for term in ["gnome-terminal", "xterm", "konsole", "xfce4-terminal", "lxterminal"]:
                    try:
                        subprocess.Popen([term], cwd=path)
                        break
                    except FileNotFoundError:
                        continue
            self.update_status_bar(f"Terminal opened in: {path}")
            self.log_dock_container.log(f"Terminal opened at: {path}", ActivityLog.INFO)
        except Exception as e:
            QMessageBox.critical(self, "Terminal Error", f"Failed to open terminal: {e}")

    def clear_thumbnail_cache(self):
        cache_path = self.config_manager.thumbnail_cache_path
        if not os.path.exists(cache_path):
            QMessageBox.information(self, "Clear Cache", "Cache directory not found.")
            return
        try:
            total_size = 0
            file_count = 0
            for filename in os.listdir(cache_path):
                filepath = os.path.join(cache_path, filename)
                if os.path.isfile(filepath):
                    try:
                        total_size += os.path.getsize(filepath)
                        file_count += 1
                    except OSError:
                        continue
            if file_count == 0:
                QMessageBox.information(self, "Clear Cache", "Thumbnail cache is already empty.")
                return
            size_str = _format_size(total_size)
            reply = QMessageBox.question(
                self, 'Clear Thumbnail Cache',
                f"Delete {file_count} cached thumbnails ({size_str})?\nThumbnails will be regenerated when browsing.",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                deleted = 0
                failed = 0
                for filename in os.listdir(cache_path):
                    filepath = os.path.join(cache_path, filename)
                    try:
                        if os.path.isfile(filepath):
                            os.remove(filepath)
                            deleted += 1
                    except Exception:
                        failed += 1
                self.clear_all_memory_caches()
                self.log_dock_container.log(f"Cache cleared: {deleted} files deleted", ActivityLog.SUCCESS)
                QMessageBox.information(self, "Cache Cleared",
                    f"Deleted {deleted} files.\nFailed: {failed}.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Cache clear failed: {e}")

    def clear_all_memory_caches(self):
        for i in range(self.tab_manager.tabs.count()):
            widget = self.tab_manager.tabs.widget(i)
            if isinstance(widget, FileView):
                try:
                    widget.model.icon_cache = {}
                    widget.refresh()
                except Exception:
                    pass

    def show_about_dialog(self):
        dialog = AboutDialog(self)
        dialog.exec()


# ─────────────────────────────────────────────────────────────────────────────
#  MAIN EXECUTION
# ─────────────────────────────────────────────────────────────────────────────

def setup_logging():
    log_dir = os.path.join(os.path.expanduser("~"), ".macan_explorer", "logs")
    os.makedirs(log_dir, exist_ok=True)
    shrine_handler = RotatingFileHandler(
        os.path.join(log_dir, "shrine_ritual_log.txt"),
        maxBytes=1048576, backupCount=5, encoding='utf-8'
    )
    shrine_handler.setLevel(logging.INFO)
    error_handler = RotatingFileHandler(
        os.path.join(log_dir, "error_log.txt"),
        maxBytes=1048576, backupCount=5, encoding='utf-8'
    )
    error_handler.setLevel(logging.ERROR)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
        handlers=[shrine_handler, error_handler, console_handler]
    )


def check_for_opencv():
    if OPENCV_AVAILABLE:
        logging.info("OpenCV found. Video thumbnails enabled.")
    else:
        logging.warning("OpenCV (cv2) not found. Video thumbnails disabled.")
        logging.warning("Install with: pip install opencv-python")


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Macan Explorer")
    app.setApplicationVersion("5.0.0")
    app.setOrganizationName("Macan Angkasa")

    setup_logging()
    check_for_opencv()

    window = MainWindow()
    window.resize(1280, 760)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()