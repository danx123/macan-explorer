<div align="center">

# 🐅 Macan Explorer
### Enterprise Edition · v7.5.0

**A fast, keyboard-first file manager built with PySide6 for developers, creators, and power users.**

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square&logo=python)
![PySide6](https://img.shields.io/badge/PySide6-6.x-green?style=flat-square&logo=qt)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey?style=flat-square)
![License](https://img.shields.io/badge/License-Proprietary-red?style=flat-square)
![Version](https://img.shields.io/badge/Version-7.5.0-purple?style=flat-square)

</div>

---

## Overview

Macan Explorer is an enterprise-grade file management application designed for users who need more than their operating system's default file browser. Built entirely in Python on top of the PySide6 / Qt6 framework, it delivers a clean frameless UI, multi-tab navigation, a powerful batch rename engine, a real-time activity log, and deep session persistence — all in a single self-contained Python file.

Version 7.5 — *"Rich Media & Context"* — transforms the Quick View panel into a fully interactive media workstation. Audio and video files are now playable inline with full transport controls, PDF documents render page by page, images can be set as the desktop wallpaper directly from the context menu, and right-clicking empty folder space now exposes folder properties. Every dependency remains optional and degrades gracefully.

---

## ⚠️ Source Code Availability

> **Only versions 4.3.0 and 5.0.0 are publicly available** in this repository.
>
> Versions 6.0.0, 6.5.0, 7.5.0 and beyond are **closed-source** and not distributed.
> This README documents the current feature set for reference purposes.
> If you are looking to get started, download the latest open-source release from the
> [Releases](https://github.com/danx123/macan-explorer/releases) page.

---

## Table of Contents

- [Features](#features)
- [Screenshots](#screenshots)
- [Source Code Availability](#️-source-code-availability)
- [Requirements](#requirements)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [Usage Guide](#usage-guide)
- [Keyboard Shortcuts](#keyboard-shortcuts)
- [Configuration & Persistence](#configuration--persistence)
- [File Structure](#file-structure)
- [Architecture Overview](#architecture-overview)
- [Known Limitations](#known-limitations)
- [Credits](#credits)

---

## Features

### 🗂️ Navigation
- **Multi-tab browsing** — open as many directory tabs as needed; tabs are movable and closable
- **"+" tab button** — embedded directly in the tab bar, always adjacent to the last open tab; click to open a new tab instantly
- **Tab context menu** — right-click any tab to close it or open its path in a new independent window
- **Breadcrumb navigation bar** — click any path segment to jump directly to that directory
- **Full history stack** — Back (`Alt+←`), Forward (`Alt+→`), Up (`Alt+↑`) with keyboard shortcuts
- **Address bar** — type or paste any path and press Enter to navigate instantly
- **Sidebar** with three independently resizable panels:
  - **Quick Access** — Home, Desktop, Downloads, Documents, Pictures, Music, Videos; OS-native icons via `QFileIconProvider`; right-click any entry → Properties
  - **Drives** — live drive tree with right-click → Drive Properties (disk usage, free space, progress bar)
  - **Bookmarks** — drag folders in or use the + button; supports drag-and-drop from the file view

### 📋 File Operations
- Copy, Cut, Paste with clipboard-style queue across folders and tabs
- Drag-and-drop between the file view and sidebar bookmark list
- **Move to Recycle Bin** (`Del`) — sends items to the OS Recycle Bin / Trash via `send2trash`; falls back to permanent delete with confirmation if trash is unavailable
- Rename (inline `F2`), New Folder (`Ctrl+Shift+N`), New File
- Select All (`Ctrl+A`)
- Multi-file operations with a progress dialog for large batches
- **Context menu** — full operation set with keyboard shortcut hints, plus:
  - **"🖼️ Set as Wallpaper"** — appears when right-clicking any image file; cross-platform (Windows, macOS, Linux)
  - **"Folder Properties"** — appears when right-clicking empty space; shows metadata for the currently open folder

### 🔍 View Modes
| Mode | Description |
|---|---|
| **Details** | Table view with name, size, type, and date columns; sortable headers; column widths persisted |
| **List** | Compact list view for dense directory browsing |
| **Icons** | Large icon grid with image thumbnails, video thumbnails, and folder media previews |

- View mode preference is persisted and restored per session

### 🖼️ Thumbnail Engine
- Instant image thumbnails for **PNG, JPG, JPEG, BMP, GIF, WEBP**
- Video thumbnails for **MP4, MKV, AVI, MOV, WEBM, FLV, WMV, MPG, MPEG** *(requires OpenCV)*
- **Folder media detection** — folders containing images or videos display a composite 2×2 grid preview instead of a plain folder icon
- **Video hover preview** — hovering over a video file shows a floating animated preview cycling through 8 frames sampled across the first 10 seconds; generated in a background thread, UI never blocks
- Thumbnails generated off the main thread via `QThreadPool` (up to 4 concurrent workers)
- MD5-hashed disk cache stored in `~/.macan_explorer/thumbnails/`
- **Clear Thumbnail Cache** available in the toolbar More menu

### 👁️ Quick View Panel *(F3)*
A fully interactive media preview panel — no external application needed.

- Toggled via `F3` or View → Toggle Quick View; appears as a resizable dock on the right side
- Auto-previews whichever single file is selected in the active tab
- Panel width, visibility, and audio/video volume level are persisted via QSettings

**Image viewer**
- Renders the image scaled to the panel width; re-scales live as the panel is resized
- Meta bar shows filename, pixel dimensions, and file size

**Text & code viewer**
- Monospaced reader with UTF-8 / Latin-1 auto-detection, truncated at 256 KB
- Supports 40+ extensions: `txt`, `md`, `log`, `json`, `yaml`, `toml`, `csv`, `xml`, `html`, `css`, `js`, `ts`, `py`, `java`, `c`, `cpp`, `h`, `rs`, `go`, `sh`, `bat`, `sql`, `rb`, `php` and more

**Audio player** *(requires `mutagen` + `PySide6-Addons`)*
- Supported formats: **MP3, FLAC, OGG, M4A, AAC, WAV, WMA, OPUS, AIFF**
- Displays cover art (extracted from ID3 / FLAC Picture / M4A covr tags), title, artist, and album
- Seek bar, position / duration labels, Play/Pause button, and volume slider
- Volume level persisted across sessions via QSettings

**Video player** *(requires `PySide6-Addons`)*
- Supported formats: **MP4, MKV, AVI, MOV, WEBM, FLV, WMV, MPG, MPEG**
- Embedded `QVideoWidget` with seek bar, position / duration labels, Play/Pause, and volume slider

**PDF viewer** *(requires `pypdfium2`)*
- Renders each page at 1.5× scale; all pages loaded into memory at open time
- Previous / Next page buttons with `X / N` page counter; buttons auto-disable at boundaries
- Pages auto-rescale to panel width on resize

**Unsupported types** — shows a clear "No preview available" notice

### 🔎 Inline Search *(Ctrl+F)*
- Search bar appears **inside the current file view** — no separate dialog
- Two modes via drop-down:
  - **Real-time** — filters as you type with a 300 ms debounce
  - **Manual** — results update only on `Enter` or clicking **Search**
- Search is **scoped to the current folder only** — direct children of the active path
- Live match counter (`12 matches`, `1 match`)
- Filter clears automatically when navigating to a different folder
- Mode preference persisted via QSettings
- Press `Esc` or `✕` to dismiss and restore the full file list

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

**Live Preview Table** — updates in real time as you type; renamed entries highlighted in accent color.  
**Preview Dialog** — review the full before/after diff before committing.  
**Undo Last Rename** — reverses the entire most-recent batch in one click.

> The Smart Rename panel is hidden by default. Open it with **Ctrl+R**.

### 📝 Activity Log
- Color-coded log entries: `INFO`, `NAV`, `SUCCESS`, `ERROR`, `COPY`, `MOVE`, `RENAME`, `CREATE`, `DELETE`
- Every file operation logged automatically, including wallpaper changes
- **Export** log to `.txt`, **Clear** with one click
- Monospaced font view with auto-scroll

> The Activity Log panel is hidden by default. Enable via View → Toggle Activity Log.

### 🎨 Theme System
- **Dark theme** (default) — deep navy/slate palette with purple accents (`#7C3AED`)
- **Light theme** — crisp white/slate palette with matching purple accents
- Toggle with `Ctrl+D` or the toolbar button
- All SVG icon strokes re-rendered per theme; frameless window controls adapt to both themes
- Theme preference persisted across sessions

### 💾 Session Persistence (QSettings)
All of the following survive application restart:

- Window size and position
- Dock panel visibility and layout (Activity Log, Smart Rename, Quick View)
- Main splitter width (sidebar vs content area)
- Details view column widths and sort state
- Smart Rename field values and active tab
- Inline search mode (Real-time / Manual)
- Sidebar panel proportions
- Audio / video volume level
- View mode, show/hide hidden files toggle, theme, bookmark list

### 🖥️ Terminal Integration
- **Open Terminal Here** (`Ctrl+T`) launches the system terminal in the current directory
- Auto-detects platform: `cmd.exe` (Windows), `Terminal.app` (macOS), or `gnome-terminal / xterm / konsole / xfce4-terminal / lxterminal` (Linux)

### 🪟 Multi-Window
- `Ctrl+N` opens a full independent application window
- Tab context menu → "Open in New Window" opens the tab's current path in a new window

---

## Screenshots

| Dark Theme | Light Theme |
|---|---|
| ![Dark](screenshot/dark.png) | ![Light](screenshot/light.png) |

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
| `opencv-python` | 4.x+ | Video thumbnails, video hover preview |
| `send2trash` | 1.8+ | Move deleted files to OS Recycle Bin / Trash |
| `mutagen` | 1.45+ | Audio metadata and cover art extraction |
| `pypdfium2` | 4.x+ | PDF page rendering in Quick View |
| `PySide6-Addons` | 6.x | Audio and video playback (`QtMultimedia`) |

> All optional packages degrade gracefully. The application starts without any of them and shows clear in-panel messages with install instructions where a feature requires a missing package.

---

## Installation

### 1. Clone or download

```bash
git clone https://github.com/danx123/macan-explorer.git
cd macan-explorer
```

> **Note:** Only `v4.3.0` and `v5.0.0` source files are available in this
> repository. Download the appropriate release from the
> [Releases](https://github.com/danx123/macan-explorer/releases) page.

### 2. Create a virtual environment *(recommended)*

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

**Minimum (core features only):**
```bash
pip install PySide6
```

**Recommended (most features):**
```bash
pip install PySide6 opencv-python send2trash mutagen pypdfium2
```

**Full install (including audio/video playback):**
```bash
pip install PySide6 opencv-python send2trash mutagen pypdfium2
pip install PySide6-Addons   # provides QtMultimedia for playback
```

---

## Running the Application

```bash
python macan_explorer.py
```

No build step, no resource compilation, no installer required.

---

## Usage Guide

### Basic Navigation

| Action | How |
|---|---|
| Open a folder | Double-click it in the file view |
| Go back | `Alt+←` or the back button |
| Go forward | `Alt+→` or the forward button |
| Go up one level | `Alt+↑` or the up button |
| Navigate via address bar | Type a path, press `Enter` |
| Navigate via breadcrumb | Click any segment |
| Open in a new tab | Right-click folder → Open in New Tab, or click `+` in the tab bar |
| Open in a new window | Right-click tab → Open in New Window |
| Switch tabs | Click the tab |

### File Operations

| Action | Shortcut |
|---|---|
| Copy | `Ctrl+C` |
| Cut | `Ctrl+X` |
| Paste | `Ctrl+V` |
| Rename | `F2` |
| Move to Recycle Bin | `Del` |
| Select All | `Ctrl+A` |
| New Folder | `Ctrl+Shift+N` |
| Folder Properties | Right-click empty space → Folder Properties |
| Set as Wallpaper | Right-click image file → Set as Wallpaper |

### Quick View — Media Playback

1. Press `F3` to open the Quick View panel.
2. Select a single file — preview loads automatically.
3. **Audio/Video** — click `▶` to play; click the seek bar to jump; drag the volume bar to adjust level.
4. **PDF** — use `◀` / `▶` to navigate pages.
5. Resize the panel by dragging its left edge.
6. Press `F3` again to close.

### Inline Search

1. Press `Ctrl+F` — the search bar opens inside the current file view.
2. Choose **Real-time** or **Manual** mode.
3. Type your query — only items in the **current folder** are filtered.
4. Press `Esc` or `✕` to close.

### Smart Rename Workflow

1. Navigate to the target folder; optionally select specific files.
2. Press `Ctrl+R` to open the Smart Rename panel.
3. Configure rules across the three tabs; watch the **Live Preview** update.
4. Click **Preview All** → **Apply Rename** to commit.
5. Click **Undo Last Rename** to reverse if needed.

### Bookmarks

- **Add:** Drag a folder onto the Bookmarks list, or click `+` and browse.
- **Remove:** Select a bookmark and click `−`.
- **Navigate:** Click any bookmark to open it in the current tab.

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
| `Del` | Move to Recycle Bin |
| `Ctrl+Shift+N` | Create new folder |

### Application
| Shortcut | Action |
|---|---|
| `Ctrl+R` | Open Smart Rename panel |
| `Ctrl+F` | Open inline search bar |
| `F3` | Toggle Quick View panel |
| `Ctrl+T` | Open terminal in current directory |
| `Ctrl+D` | Toggle Dark / Light theme |
| `Ctrl+H` | Toggle show / hide hidden files |

---

## Configuration & Persistence

### Application data — `~/.macan_explorer/`
```
~/.macan_explorer/
├── macan_explorer_config.json   # Bookmarks, view mode, theme, show-hidden flag
├── thumbnails/                  # MD5-hashed video thumbnail cache
└── logs/
    ├── shrine_ritual_log.txt    # General log (rotating, max 1 MB × 5 backups)
    └── error_log.txt            # Error-only log (rotating, max 1 MB × 5 backups)
```

### QSettings — OS native store

| Platform | Location |
|---|---|
| Windows | `HKEY_CURRENT_USER\Software\Macan Angkasa\Macan Explorer` |
| macOS | `~/Library/Preferences/com.macan-angkasa.Macan Explorer.plist` |
| Linux | `~/.config/Macan Angkasa/Macan Explorer.ini` |

To reset all session state, delete the relevant QSettings key or file.

---

## File Structure

```
macan_explorer.py       # Entire application — single self-contained file (~5,431 lines)
screenshot/
├── dark.png            # Dark theme screenshot
└── light.png           # Light theme screenshot
README.md
```

### Internal Module Layout

```
macan_explorer.py
│
├── SVG_ICONS / _ICON_COLORS       Embedded icons + per-theme stroke colors
├── create_icon()                  Render SVG → QIcon with theme color
├── DARK_THEME_QSS / LIGHT_THEME_QSS
│
├── WorkerSignals       QObject    Shared signal class for thread workers
├── FolderSizeWorker    QRunnable  Async folder size calculation
├── ThumbnailWorker     QRunnable  Async video thumbnail generation (OpenCV)
├── VideoPreviewWorker  QRunnable  Async video frame extraction for hover preview
│
├── ErrorHandler                   Structured error capture
├── ShrineLogger                   Rotating file logger
├── ActivityLog                    In-app log with color-coded severity levels
├── ConfigManager                  JSON-backed user config
│
├── ThumbnailIconProvider  QFileSystemModel   Image + video + folder composite thumbnails
├── SortFilterProxyModel   QSortFilterProxyModel   Scoped search + hidden-file filter
│
├── BreadcrumbBar      QWidget    Clickable path segment bar
├── CommandBar         QToolBar   Toolbar + theme-aware icon re-rendering
├── VideoHoverPreview  QLabel     Floating animated video hover overlay
├── FileView           QWidget    Core browser: tree/list/icons, inline search,
│                                 context menu (wallpaper, folder properties)
│
├── Sidebar            QWidget    QSplitter [QuickAccess | Drives | Bookmarks]
├── TabManager         QWidget    QTabWidget + "+" dummy tab + context menu
├── TitleBar           QWidget    Frameless titlebar + theme-aware controls
│
├── DrivePropertiesDialog   QDialog
├── PropertiesDialog        QDialog   File/folder metadata + inline rename
├── OperationProgressDialog QProgressDialog
│
├── RenameRule / SmartRenameEngine / RenamePreviewDialog
├── SmartRenameDock    QWidget    3-tab rename UI + live preview
│
├── AboutDialog        QDialog
├── QuickViewPanel     QWidget    Image / text / audio / video / PDF preview
│                                  + playback controls + cover art
├── ActivityLogDock    QWidget    Dockable activity log
│
└── MainWindow         QMainWindow  Root: menu, layout, QSettings, signals
```

---

## Architecture Overview

Macan Explorer follows a **signal-driven MVC-like pattern**:

- **Model layer:** `ThumbnailIconProvider` (extends `QFileSystemModel`) is the single source of truth; `SortFilterProxyModel` handles sorting, hidden-file filtering, and scoped search.
- **View layer:** `FileView` renders the model in three switchable modes; `QuickViewPanel` previews the selected file with full media playback.
- **Controller layer:** `MainWindow` wires all signals into coordinated actions.
- **Worker threads:** `FolderSizeWorker`, `ThumbnailWorker`, and `VideoPreviewWorker` run in shared `QThreadPool` instances; results consumed on the main thread via signals.
- **Persistence:** `QSettings` (session state) + `ConfigManager` JSON (bookmarks, prefs).

```
MainWindow
 ├── TitleBar              ← frameless controls, theme-aware icons
 ├── CommandBar            ← toolbar, address bar, search
 ├── BreadcrumbBar         ← path segments → navigate
 ├── Sidebar               ← QSplitter [QuickAccess | Drives | Bookmarks]
 ├── TabManager            ← n × FileView + "+" tab + context menu
 │    └── FileView         ← ThumbnailIconProvider + SortFilterProxyModel
 │         ├── InlineSearchBar     ← real-time / manual scoped filter
 │         └── VideoHoverPreview   ← floating frame-animation overlay
 ├── ActivityLogDock       ← QDockWidget, bottom, lazy-loaded
 ├── SmartRenameDock       ← QDockWidget, bottom, tabified
 └── QuickViewDock         ← QDockWidget, right, lazy-loaded
      └── QuickViewPanel   ← image / text / audio▶ / video▶ / PDF📄
```

---

## Known Limitations

- **Single-pane layout** — dual-pane (commander-style) browsing is not available.
- **Video thumbnails & hover preview require OpenCV** — generic icon shown otherwise.
- **Audio/video playback requires PySide6-Addons** — panel shows install instructions otherwise.
- **PDF preview requires pypdfium2** — panel shows install instructions otherwise.
- **Recycle Bin on network drives** — `send2trash` may fall back to permanent deletion on certain network or Linux configurations.
- **Smart Rename undo** — covers only the most recent batch; general filesystem undo is not implemented.
- **Inline search** — current folder only; recursive subdirectory search not yet available.

---

## Credits

**Developer:** Danx Exodus  
**Organization:** Macan Angkasa  
**Repository:** [github.com/danx123/macan-explorer](https://github.com/danx123/macan-explorer)  
**Built with:** [Python](https://python.org) · [PySide6 / Qt6](https://doc.qt.io/qtforpython/) · [OpenCV](https://opencv.org) · [send2trash](https://github.com/arsenetar/send2trash) · [mutagen](https://github.com/quodlibet/mutagen) · [pypdfium2](https://github.com/pypdfium2-team/pypdfium2)

Portions of the Smart Rename engine and Activity Log were adapted from the **SmartFileManager** project (internal, same author).

---

<div align="center">

*Copyright © 2026 Macan Angkasa. All rights reserved.*

</div>
