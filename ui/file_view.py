# file: ui/file_view.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTreeView, QListView,
    QInputDialog, QMessageBox, QMenu, QLineEdit,
    QApplication, QFileIconProvider
)
from PyQt6.QtCore import (
    QDir, Qt, QUrl, QSize, QFileInfo, pyqtSignal,
    QSortFilterProxyModel
)
from PyQt6.QtGui import (
    QAction, QDesktopServices, QIcon, QFileSystemModel, QPixmap
)
import os
import shutil
import math
from datetime import datetime

class ThumbnailIconProvider(QFileIconProvider):
    def icon(self, fileInfo):
        if fileInfo.isDir():
            return super().icon(fileInfo)

        suffix = fileInfo.suffix().lower()
        if suffix in ['png', 'jpg', 'jpeg', 'bmp', 'gif', 'mp4', 'mov', 'mpeg', 'mov', 'mkv', 'webm', 'avi']:
            pixmap = QPixmap(fileInfo.filePath())
            if not pixmap.isNull():
                return QIcon(pixmap.scaled(96, 96, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))

        return super().icon(fileInfo)

# --- KELAS PROXY UNTUK SORTIR KUSTOM ---
class SortFilterProxyModel(QSortFilterProxyModel):
    """Proxy model untuk menyediakan sortir case-insensitive dan direktori di atas."""
    def lessThan(self, left, right):
        # 'left' dan 'right' adalah QModelIndex dari source model
        source_model = self.sourceModel()
        
        # Terapkan logika kustom hanya untuk kolom "Name" (kolom 0)
        if self.sortColumn() == 0:
            left_info = QFileInfo(source_model.filePath(left))
            right_info = QFileInfo(source_model.filePath(right))

            # Prioritas utama: direktori selalu di atas file
            is_left_dir = left_info.isDir()
            is_right_dir = right_info.isDir()

            if is_left_dir != is_right_dir:
                # Jika ascending, direktori didahulukan (True jika kiri adalah dir)
                return is_left_dir if self.sortOrder() == Qt.SortOrder.AscendingOrder else not is_left_dir

            # Prioritas kedua: sortir nama secara case-insensitive
            return left_info.fileName().lower() < right_info.fileName().lower()
        
        # Untuk kolom lain, gunakan perilaku sortir default
        return super().lessThan(left, right)

class FileView(QWidget):
    path_changed = pyqtSignal(str)
    navigation_state_changed = pyqtSignal(bool, bool)

    def __init__(self, folder_path=None, parent=None):
        super().__init__(parent)
        
        self._history = []
        self._history_index = -1
        
        initial_path = folder_path if folder_path and os.path.exists(folder_path) else QDir.homePath()
        self.current_path = "" 

        # 1. Buat source model (QFileSystemModel)
        self.model = QFileSystemModel()
        self.model.setIconProvider(ThumbnailIconProvider())
        self.model.setRootPath(QDir.rootPath()) # Set root path di model

        # 2. Buat proxy model dan hubungkan ke source model
        self.proxy_model = SortFilterProxyModel(self)
        self.proxy_model.setSourceModel(self.model)

        self.tree_view = QTreeView(self)
        self.list_view = QListView(self)

        # 3. Set proxy model ke view, bukan source model
        self.tree_view.setModel(self.proxy_model)
        self.list_view.setModel(self.proxy_model)
        
        # --- PENGATURAN SORTIR (DITERAPKAN PADA VIEW) ---
        self.tree_view.setSortingEnabled(True)
        # Atur sortir default berdasarkan nama (kolom 0) secara menaik (Ascending)
        self.tree_view.sortByColumn(0, Qt.SortOrder.AscendingOrder)

        self.tree_view.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tree_view.customContextMenuRequested.connect(self._on_context_menu)
        self.tree_view.doubleClicked.connect(self._on_double_click)
        self.tree_view.setAlternatingRowColors(True)
        self.tree_view.setSelectionMode(QTreeView.SelectionMode.ExtendedSelection)

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

        self.set_view_mode("details")
        self.set_path(initial_path, initial_load=True)

    @property
    def active_view(self):
        return self.tree_view if not self.tree_view.isHidden() else self.list_view

    def set_path(self, path, add_to_history=True, initial_load=False):
        path = os.path.normpath(path)
        if not os.path.exists(path) or not os.path.isdir(path):
            QMessageBox.warning(self, "Path Tidak Valid", f"Folder '{path}' tidak ditemukan atau bukan direktori.")
            if initial_load:
                 path = QDir.homePath()
            else:
                return
        
        if path == self.current_path and not initial_load:
            self.refresh()
            return

        self.current_path = path
        
        # Dapatkan index dari source model, lalu map ke proxy model
        source_index = self.model.index(path)
        proxy_index = self.proxy_model.mapFromSource(source_index)
        
        # Set root index di view menggunakan proxy index
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
        # Terapkan kembali sortir yang sedang aktif
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
            path = self._history[self._history_index]
            self.set_path(path, add_to_history=False)

    def go_forward(self):
        if self._history_index < len(self._history) - 1:
            self._history_index += 1
            path = self._history[self._history_index]
            self.set_path(path, add_to_history=False)
            
    def go_up(self):
        parent_path = os.path.dirname(self.current_path)
        if parent_path != self.current_path:
            self.set_path(parent_path)

    def refresh(self):
        # Refresh dilakukan pada source model
        self.model.refresh(self.model.index(self.current_path))
    
    def set_view_mode(self, mode):
        # Menggunakan kolom dari proxy model untuk menyembunyikan
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

    def _on_double_click(self, index): # 'index' adalah dari proxy model
        # Map proxy index ke source index untuk mendapatkan info file
        source_index = self.proxy_model.mapToSource(index)
        
        # Pastikan kita bekerja dengan kolom pertama (nama file)
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
            # Map ke source index untuk mendapatkan path
            source_index = self.proxy_model.mapToSource(proxy_index)
            path = self.model.filePath(source_index)

            menu.addAction("Open").triggered.connect(lambda: self._on_double_click(proxy_index))
            menu.addAction("Rename").triggered.connect(self.rename_selected_item)
            menu.addAction("Delete").triggered.connect(self.delete_selected_items)
            menu.addSeparator()
            menu.addAction("Copy Path").triggered.connect(lambda: self._copy_path(path))
            menu.addSeparator()
            menu.addAction("Properties").triggered.connect(self.show_properties)
            menu.addSeparator()

        menu.addAction("New Folder").triggered.connect(self.create_new_folder)
        menu.addAction("New File").triggered.connect(self.create_new_file)
        
        menu.exec(view.viewport().mapToGlobal(position))

    def _copy_path(self, path):
        QApplication.clipboard().setText(path)

    def _get_selected_proxy_indexes(self):
        return self.active_view.selectionModel().selectedIndexes()

    def search_files(self, query):
        directory = QDir(self.current_path)
        name_filters = [f"*{query}*"]
        filters = QDir.Filter.Files | QDir.Filter.Dirs | QDir.Filter.NoDotAndDotDot
        iterator = directory.entryList(name_filters, filters)
        
        if iterator:
            QMessageBox.information(self, "Search Results", f"Found '{query}':\n" + "\n".join(iterator))
        else:
            QMessageBox.information(self, "Search Results", f"No results found for '{query}'.")

    def create_new_folder(self):
        folder_name, ok = QInputDialog.getText(self, "Create New Folder", "Enter new folder name:")
        if ok and folder_name:
            try:
                os.makedirs(os.path.join(self.current_path, folder_name))
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to create folder: {e}")

    def create_new_file(self):
        file_name, ok = QInputDialog.getText(self, "Create New File", "Enter new file name:")
        if ok and file_name:
            try:
                with open(os.path.join(self.current_path, file_name), 'w') as f:
                    f.write("")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to create file: {e}")

    def delete_selected_items(self):
        selected_proxy_indexes = self._get_selected_proxy_indexes()
        if not selected_proxy_indexes: return

        # Dapatkan path unik dari item yang dipilih dengan mapping ke source model
        source_indexes = [self.proxy_model.mapToSource(idx) for idx in selected_proxy_indexes]
        paths_to_delete = list(set([self.model.filePath(idx.sibling(idx.row(), 0)) for idx in source_indexes]))

        reply = QMessageBox.question(self, 'Confirm Deletion',
                                     f"Are you sure you want to delete {len(paths_to_delete)} selected item(s)?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, 
                                     QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            for path in paths_to_delete:
                try:
                    if os.path.isdir(path):
                        shutil.rmtree(path)
                    else:
                        os.remove(path)
                except Exception as e:
                    QMessageBox.critical(self, "Deletion Error", f"Failed to delete '{os.path.basename(path)}': {e}")
            
    def rename_selected_item(self):
        selected_proxy_indexes = self._get_selected_proxy_indexes()
        if not selected_proxy_indexes: return
        
        # Ambil proxy index pertama, map ke source, lalu dapatkan path
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
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to rename '{old_name}': {e}")

    def show_properties(self):
        selected_proxy_indexes = self._get_selected_proxy_indexes()
        if not selected_proxy_indexes:
            return

        # Ambil proxy index pertama, map ke source, lalu dapatkan path
        proxy_index = selected_proxy_indexes[0]
        source_index = self.proxy_model.mapToSource(proxy_index)
        source_index_col0 = source_index.sibling(source_index.row(), 0)
        path = self.model.filePath(source_index_col0)
        
        try:
            file_info = QFileInfo(path)
            
            name = file_info.fileName()
            location = os.path.dirname(file_info.absoluteFilePath())
            
            if file_info.isDir():
                type_desc = "File Folder"
                size_bytes = self._get_folder_size(path)
            else:
                type_desc = f"{file_info.suffix().upper()} File" if file_info.suffix() else "File"
                size_bytes = file_info.size()

            size_formatted = self._format_size(size_bytes)
            
            modified_date = file_info.lastModified().toString("dd MMMM yyyy hh:mm:ss")
            created_date_ts = os.path.getctime(path)
            created_date = datetime.fromtimestamp(created_date_ts).strftime("%d %B %Y %H:%M:%S")

            info_text = (
                f"<b>Name:</b> {name}\n\n"
                f"<b>Type:</b> {type_desc}\n"
                f"<b>Location:</b> {location}\n"
                f"<b>Size:</b> {size_formatted} ({size_bytes:,} bytes)\n\n"
                f"<b>Date Modified:</b> {modified_date}\n"
                f"<b>Date Created:</b> {created_date}"
            )

            QMessageBox.information(self, f"Properties for {name}", info_text)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not retrieve properties: {e}")

    def _get_folder_size(self, path):
        total_size = 0
        try:
            for dirpath, dirnames, filenames in os.walk(path):
                for f in filenames:
                    fp = os.path.join(dirpath, f)
                    if not os.path.islink(fp):
                        total_size += os.path.getsize(fp)
        except OSError:
            pass
        return total_size

    def _format_size(self, size_bytes):
        if size_bytes == 0:
            return "0 B"
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return f"{s} {size_name[i]}"