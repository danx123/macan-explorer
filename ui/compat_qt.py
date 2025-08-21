# compat_qt.py — Guardian of Import Realms

try:
    from PyQt6.QtWidgets import QFileSystemModel
except ImportError:
    try:
        from PyQt6.QtGui import QFileSystemModel
    except ImportError:
        QFileSystemModel = None
        print("⛔ QFileSystemModel not found in PyQt6. Check your installation.")