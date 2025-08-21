# qt_shim.py

try:
    from PyQt6.QtGui import QAction
except ImportError:
    try:
        from PyQt6.QtGui import QAction
    except ImportError:
        QAction = None
        print("⛔ QAction import gagal. Cek versi PyQt6.")