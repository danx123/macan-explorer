# 🐅 Macan Explorer

Macan Explorer is a modern file manager application based on PySide6, designed with a premium frameless UI to provide a cleaner, lighter, and more efficient file browsing experience.

Macan Explorer was developed as a modern alternative to the standard file explorer, with a touch of minimalist UI and intuitive features.

---

## ✨ Key Features
- 📂 **Modern File Navigation** — clean and frameless.
- 🗂️ **Multi-tab Support** — open multiple folders in one window.
- 🔍 **Quick Search** — faster file/folder search.
- 🎨 **Modern UI** — clean, lightweight, and premium themes.

---

## 📸 Screenshot
<img width="1061" height="644" alt="Screenshot 2025-10-21 193230" src="https://github.com/user-attachments/assets/5f5a8733-c5e6-4fb0-9d29-798ee5369b12" />
<img width="1200" height="1920" alt="macan-explorer-v250" src="https://github.com/user-attachments/assets/20458e54-3eaf-4d67-8a12-2d2bb93935ff" />



---

## 📜 Changelog v2.5.0
Changelog:

- Drag and Drop:
You can now drag a file or folder (single or multiple) from within Mac Explorer to an external window (e.g., to the Desktop or another folder).
You can also drop a file or folder from outside the Mac Explorer window into the Mac Explorer window. This will trigger a copy-paste operation to the active folder, complete with a progress dialog.

- More Informative Status Bar:
The status bar at the bottom now displays detailed information about the items you select.
If nothing is selected, it displays the total number of items in the folder.
If a single item is selected, it displays: File Name | Type: File Type | Size: File Size.
If multiple items are selected, it displays: X items selected | Total Size: Total Combined Size.

- New Refresh Icon:
The SVG icon for the Refresh button has been replaced with a new icon (rotate-cw).

---  

  

## 📦 Release Notes
- **Source Code (this repo):** contains the **base version** of Macan Explorer.
- **Release (Binary):** contains the latest version with full features, ready to use.

👉 To try the latest version immediately, please download the **binary release** from the [Releases](../../releases) page.

---

## 🛠️ Installation (from Source)
### Prerequisites
- Python 3.10+
- Python Dependencies:
```bash
pip install -r requirements.txt
