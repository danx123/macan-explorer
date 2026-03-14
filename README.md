<div align="center">

# 🐅 Macan Explorer
### Enterprise Edition · v5.0.0

**A fast, keyboard-first file manager built with PySide6 for developers, creators, and power users.**

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square&logo=python)
![PySide6](https://img.shields.io/badge/PySide6-6.x-green?style=flat-square&logo=qt)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey?style=flat-square)
![License](https://img.shields.io/badge/License-Proprietary-red?style=flat-square)
![Version](https://img.shields.io/badge/Version-5.0.0-purple?style=flat-square)

</div>

---

## Overview

Macan Explorer is an enterprise-grade file management application designed for users who need more than their operating system's default file browser. Built entirely in Python on top of the PySide6 / Qt6 framework, it delivers a clean frameless UI, multi-tab navigation, a powerful batch rename engine, a real-time activity log, and deep session persistence — all in a single self-contained Python file.

Version 5.0 represents a landmark release that merges the best innovations from the **SmartFileManager** project into Macan Explorer's architecture, resulting in a fully docked panel system, a production-grade Smart Rename workflow, and a comprehensive QSettings persistence layer.

---

## Table of Contents

- [Features](#features)
- [Screenshots](#screenshots)
- [Requirements](#requirements)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [Usage Guide](#usage-guide)
- [Keyboard Shortcuts](#keyboard-shortcuts)
- [Configuration & Persistence](#configuration--persistence)
- [File Structure](#file-structure)
- [Architecture Overview](#architecture-overview)
- [Known Limitations](#known-limitations)
- [Changelog](#changelog)
- [Credits](#credits)

---

## Features

### 🗂️ Navigation
- **Multi-tab browsing** — open as many directory tabs as needed; tabs are movable and closable
- **Breadcrumb navigation bar** — click any path segment to jump directly to that directory
- **Full history stack** — Back (`Alt+←`), Forward (`Alt+→`), Up (`Alt+↑`) with keyboard shortcuts
- **Address bar** — type or paste any path and press Enter to navigate instantly
- **Sidebar** with three independently resizable panels:
  - **Quick Access** — Home, Desktop, Downloads, Documents, Pictures, Music, Videos; uses OS-native folder icons from `QFileIconProvider`
  - **Drives** — live drive tree with right-click → Drive Properties (disk usage, free space, progress bar)
  - **Bookmarks** — drag folders in or use the + button; supports drag-and-drop from the file view

### 📋 File Operations
- Copy, Cut, Paste with clipboard-style queue across folders and tabs
- Drag-and-drop between the file view and sidebar bookmark list
- Rename (inline `F2`), Delete (`Del`), New Folder (`Ctrl+Shift+N`), New File
- Select All (`Ctrl+A`)
- Multi-file operations with a progress dialog for large batches
- Context menu for all operations with keyboard shortcut hints

### 🔍 View Modes
| Mode | Description |
|---|---|
| **Details** | Table view with name, size, type, and date columns; sortable headers |
| **List** | Compact list view for dense directory browsing |
| **Icons** | Large icon grid with image and video thumbnails |

- View mode preference is persisted and restored per session

### 🖼️ Thumbnail Engine
- Instant image thumbnails for **PNG, JPG, JPEG, BMP, GIF, WEBP**
- Video thumbnails for **MP4, MKV, AVI, MOV, WEBM, FLV, WMV, MPG, MPEG** *(requires OpenCV)*
- Thumbnails generated off the main thread via `QThreadPool` (up to 4 concurrent workers) — UI never freezes
- MD5-hashed disk cache stored in `~/.macan_explorer/thumbnails/`
- **Clear Thumbnail Cache** available in the toolbar More menu

### ✏️ Smart Rename *(Ctrl+R)*
A full-featured batch rename engine with live preview and undo support.

**Tab 1 — Find & Replace**
- Multi-pattern rules in `pattern, replacement` pairs (e.g. `LK21-, , (2023), `)
- Prefix and Suffix injection
- Case conversion: No Change / lowercase / UPPERCASE / Title Case / camelCase / snake_case
- Extension override (e.g. `.txt`, `.jpg`)
- Remove special characters option
- Replace spaces with custom character option

**Tab 2 — Numbering**
- Auto-increment counter appended to each filename
- Configurable start number, zero-padding width, and separator character

**Tab 3 — Regex**
- Full Python `re`-compatible pattern matching
- Capture group substitution with `\1`, `\2`, etc.
- Enable/disable toggle so the tab is non-destructive by default

**Live Preview Table** — updates in real time as you type; renamed entries are highlighted in accent color.  
**Preview Dialog** — review the full before/after diff before committing.  
**Undo Last Rename** — reverses the entire most-recent batch in one click.

> The Smart Rename panel is hidden by default and does not consume screen space until needed. Open it with **Ctrl+R**.

### 📝 Activity Log
- Color-coded log entries by operation type: `INFO`, `NAV`, `SUCCESS`, `ERROR`, `COPY`, `MOVE`, `RENAME`, `CREATE`, `DELETE`
- Every file operation (navigate, copy, cut, paste, rename, delete, create, bookmark, terminal launch, theme switch, cache clear) is logged automatically
- **Export** log to a `.txt` file
- **Clear** log with one click
- Monospaced font view with auto-scroll

> The Activity Log panel is hidden by default. Enable it via View → Toggle Activity Log.

### 🎨 Theme System
- **Dark theme** (default) — deep navy/slate palette with purple accents (`#7C3AED`)
- **Light theme** — crisp white/slate palette with matching purple accents
- Toggle with `Ctrl+D` or the toolbar button
- All SVG icon strokes re-rendered on theme switch:
  - Dark: `#e0e0e0` (light gray on dark backgrounds)
  - Light: `#374151` (dark gray on light backgrounds)
- Frameless window controls (minimize/maximize/close) adapt to both themes
- Status bar and toolbar button text adapt to both themes
- Theme preference persisted across sessions

### 💾 Session Persistence (QSettings)
All of the following survive application restart:

- Window size and position
- Dock panel visibility (Activity Log, Smart Rename)
- Dock panel layout and positions
- Smart Rename field values (all tabs)
- Sidebar splitter proportions
- View mode (Details / List / Icons)
- Show/hide hidden files toggle
- Theme selection
- Bookmark list

### 🖥️ Terminal Integration
- **Open Terminal Here** (`Ctrl+T`) launches the system terminal in the current directory
- Platform detection:
  - **Windows** → `cmd.exe`
  - **macOS** → `Terminal.app`
  - **Linux** → auto-detects: `gnome-terminal`, `xterm`, `konsole`, `xfce4-terminal`, `lxterminal`

### 🔎 Search
- In-bar fuzzy search with `Ctrl+F` to focus the search input
- Results displayed in a `SearchResultsDialog`; double-click to navigate to the result or open its parent folder

### 🪟 Multi-Window
- Open a full independent application window with `Ctrl+N`
- Each window maintains its own tab set, settings, and navigation history

---

## Screenshots



---

## Requirements

### Required
| Dependency | Version | Purpose |
|---|---|---|
| Python | 3.10+ | Runtime |
| PySide6 | 6.x | Qt6 bindings (widgets, core, GUI, SVG) |

### Optional
| Dependency | Version | Purpose |
|---|---|---|
| opencv-python | 4.x+ | Video thumbnail generation |

> Without OpenCV, all features remain available except video thumbnails. A warning is printed to the console on startup if OpenCV is not found.

---

## Installation

### 1. Clone or download

```bash
git clone https://github.com/danx123/macan-explorer.git
cd macan-explorer
```

Or download `macan_explorer5.py` directly.

### 2. Create a virtual environment *(recommended)*

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

**Minimum (no video thumbnails):**
```bash
pip install PySide6
```

**Full install (with video thumbnails):**
```bash
pip install PySide6 opencv-python
```

---

## Running the Application

```bash
python macan_explorer5.py
```

That's it. No build step, no resource compilation, no installer required.

---

## Usage Guide

### Basic Navigation

| Action | How |
|---|---|
| Open a folder | Double-click it in the file view |
| Go back | `Alt+←` or the back button |
| Go forward | `Alt+→` or the forward button |
| Go up one level | `Alt+↑` or the up button |
| Navigate via address bar | Click the address bar, type a path, press `Enter` |
| Navigate via breadcrumb | Click any segment in the breadcrumb bar |
| Open in a new tab | Right-click a folder → Open in New Tab |
| Switch tabs | Click the tab |

### File Operations

| Action | Shortcut |
|---|---|
| Copy | `Ctrl+C` |
| Cut | `Ctrl+X` |
| Paste | `Ctrl+V` |
| Rename | `F2` |
| Delete | `Del` |
| Select All | `Ctrl+A` |
| New Folder | `Ctrl+Shift+N` |
| Properties | Right-click → Properties |

### Smart Rename Workflow

1. Navigate to the folder containing the files to rename.
2. *(Optional)* Select specific files. If none are selected, all files in the current folder are used.
3. Press `Ctrl+R` to open the Smart Rename panel.
4. Enter rules, adjust options, and watch the **Live Preview** table update in real time.
5. Click **Preview All** to review the full diff in a dialog.
6. Click **Apply Rename** to commit.
7. Click **Undo Last Rename** if you need to reverse.

### Bookmarks

- **Add:** Drag a folder from the file view onto the Bookmarks list, or click the `+` button and browse.
- **Remove:** Select a bookmark and click the `−` button.
- **Navigate:** Click any bookmark to open that folder in the current tab.

### Drive Properties

Right-click any drive in the **Drives** sidebar panel and select **Drive Properties** to view:
- Total disk capacity
- Used and free space (formatted)
- Usage percentage with a visual progress bar

---

## Keyboard Shortcuts

### Navigation
| Shortcut | Action |
|---|---|
| `Alt+←` | Go back |
| `Alt+→` | Go forward |
| `Alt+↑` | Go up one directory |
| `F5` | Refresh current view |
| `Ctrl+Tab` | Open new tab |
| `Ctrl+N` | Open new window |

### File Operations
| Shortcut | Action |
|---|---|
| `Ctrl+C` | Copy selected items |
| `Ctrl+X` | Cut selected items |
| `Ctrl+V` | Paste |
| `Ctrl+A` | Select all |
| `F2` | Rename selected item |
| `Del` | Delete selected items |
| `Ctrl+Shift+N` | Create new folder |

### Application
| Shortcut | Action |
|---|---|
| `Ctrl+R` | Open Smart Rename panel |
| `Ctrl+F` | Focus search bar |
| `Ctrl+T` | Open terminal in current directory |
| `Ctrl+D` | Toggle Dark / Light theme |
| `Ctrl+H` | Toggle show / hide hidden files |

---

## Configuration & Persistence

Macan Explorer stores its data in two locations:

### Application data — `~/.macan_explorer/`
```
~/.macan_explorer/
├── macan_explorer_config.json   # Bookmarks, view mode, theme, show-hidden flag
└── logs/
    ├── shrine_ritual_log.txt    # General application log (rotating, max 1 MB × 5 backups)
    └── error_log.txt            # Error-only log (rotating, max 1 MB × 5 backups)
```

### QSettings — OS native store
Session state (window geometry, dock layout, Smart Rename field values, sidebar splitter sizes) is stored via Qt's `QSettings` under:

| Platform | Location |
|---|---|
| Windows | `HKEY_CURRENT_USER\Software\Macan Angkasa\Macan Explorer` |
| macOS | `~/Library/Preferences/com.macan-angkasa.Macan Explorer.plist` |
| Linux | `~/.config/Macan Angkasa/Macan Explorer.ini` |

To reset all session state, delete the relevant QSettings key or file.

---

## File Structure

```
macan_explorer5.py          # Entire application — single self-contained file
```

### Internal Module Layout

```
macan_explorer5.py
│
├── SVG_ICONS               dict       Embedded SVG icon data
├── _ICON_COLORS            dict       Per-theme stroke colors (dark / light)
├── create_icon()           function   Render SVG to QIcon with theme color
├── DARK_THEME_QSS          str        Qt stylesheet for dark theme
├── LIGHT_THEME_QSS         str        Qt stylesheet for light theme
│
├── WorkerSignals           QObject    Shared signal class for thread workers
├── FolderSizeWorker        QRunnable  Async folder size calculation
├── ThumbnailWorker         QRunnable  Async video thumbnail generation (OpenCV)
│
├── ErrorHandler                       Structured error capture
├── ShrineLogger                       Rotating file logger setup
├── ActivityLog                        In-app log with color-coded levels
├── ConfigManager                      JSON-backed user config (bookmarks, prefs)
│
├── ThumbnailIconProvider  QFileSystemModel   Custom model with image+video thumbnails
├── SortFilterProxyModel   QSortFilterProxyModel   Search/filter proxy
│
├── BreadcrumbBar          QWidget    Clickable path segment bar
├── CommandBar             QToolBar   Main toolbar with all actions + update_icons()
├── FileView               QWidget    Core file browser (tree/list/icons + operations)
│
├── Sidebar                QWidget    Resizable QSplitter: Quick Access | Drives | Bookmarks
├── TabManager             QWidget    QTabWidget wrapper with add/close/rename logic
├── TitleBar               QWidget    Custom frameless titlebar + update_icons()
│
├── DrivePropertiesDialog  QDialog    Disk usage info for a drive root
├── SearchResultsDialog    QDialog    Search results with navigate-on-click
├── PropertiesDialog       QDialog    File/folder metadata + inline rename
├── OperationProgressDialog QProgressDialog  Progress for multi-file ops
│
├── RenameRule                         Single find/replace rule pair
├── SmartRenameEngine                  Multi-rule batch rename logic
├── RenamePreviewDialog    QDialog    Before/after diff preview
├── SmartRenameDock        QWidget    Dockable Smart Rename UI (3 tabs + live preview)
│
├── AboutDialog            QDialog    Application info dialog
├── ActivityLogDock        QWidget    Dockable Activity Log UI
│
└── MainWindow             QMainWindow  Root window — menu, layout, QSettings, signals
```

---

## Architecture Overview

Macan Explorer is structured around a **signal-driven MVC-like pattern**:

- **Model layer:** `ThumbnailIconProvider` (extends `QFileSystemModel`) is the single source of truth for directory data; proxy model handles sorting and filtering.
- **View layer:** `FileView` renders the model in three switchable view modes via `QTreeView` / `QListView`; all interaction emits signals upward.
- **Controller layer:** `MainWindow` wires signals from `FileView`, `CommandBar`, `Sidebar`, `TabManager`, and both dock panels into coordinated actions.
- **Worker threads:** `FolderSizeWorker` and `ThumbnailWorker` run in a shared `QThreadPool`; results are emitted via `Signal` and consumed on the main thread.
- **Persistence:** `QSettings` handles session state; `ConfigManager` (JSON) handles user data (bookmarks, preferences).

```
MainWindow
 ├── TitleBar          ← drag move, window controls, theme-aware icons
 ├── CommandBar        ← toolbar actions, address bar, search, theme-aware icons
 ├── BreadcrumbBar     ← path segments → navigate signal
 ├── Sidebar           ← QSplitter [QuickAccess | Drives | Bookmarks]
 ├── TabManager        ← n × FileView tabs
 │    └── FileView     ← ThumbnailIconProvider + SortFilterProxyModel
 ├── ActivityLogDock   ← QDockWidget (bottom, lazy-loaded)
 └── SmartRenameDock   ← QDockWidget (bottom, tabified, lazy-loaded)
```

---

## Known Limitations

- **Single-pane layout** — dual-pane (commander-style) browsing is not available in v5.
- **No network/FTP paths** — remote path browsing is not supported; local filesystem only.
- **Video thumbnails require OpenCV** — if `cv2` is not installed, video files show a generic icon.
- **Undo scope** — the undo feature in Smart Rename covers only the last batch operation; general filesystem undo (copy/paste/delete) is not implemented.
- **Search is filename-only** — full-text content search inside files is not available.

---

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for the full version history.

**v5.0.0 highlights:** Smart Rename Engine, Activity Log, Breadcrumb Bar, Resizable Sidebar, Drive Properties, OS-native Quick Access icons, QSettings persistence, per-theme SVG icon rendering, Light theme readability fixes.

---

## Credits

**Developer:** Danx Exodus  
**Organization:** Macan Angkasa  
**Built with:** [Python](https://python.org) · [PySide6 / Qt6](https://doc.qt.io/qtforpython/) · [OpenCV](https://opencv.org) *(optional)*

Portions of the Smart Rename engine and Activity Log were adapted from the **SmartFileManager** project (internal, same author).

---

<div align="center">

*Copyright © 2026 Danx Exodus — Macan Angkasa. All rights reserved.*

</div>
