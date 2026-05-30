<div align="center">

# MarkItDown Desktop

**Cross-platform GUI for [microsoft/markitdown](https://github.com/microsoft/markitdown)**\
Convert PDF, Word, Excel, PowerPoint, images, audio, and more — to clean Markdown.\
No browser. No cloud. Runs locally on Windows, macOS, and Linux.

[![Release](https://img.shields.io/github/v/release/BOSSincrypto/markitdown-app?style=flat-square&color=blue&label=Latest%20Release)](https://github.com/BOSSincrypto/markitdown-app/releases/latest)
[![Downloads](https://img.shields.io/github/downloads/BOSSincrypto/markitdown-app/total?style=flat-square&color=green)](https://github.com/BOSSincrypto/markitdown-app/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey?style=flat-square)](https://github.com/BOSSincrypto/markitdown-app/releases)
[![Stars](https://img.shields.io/github/stars/BOSSincrypto/markitdown-app?style=flat-square&color=yellow)](https://github.com/BOSSincrypto/markitdown-app/stargazers)

[⬇️ Download](#️-download) · [✨ Features](#-features) · [🚀 Quick Start](#-quick-start) · [🤝 Contributing](#-contributing)

</div>


---

## 📸 Screenshots

<div align="center">
<img width="461" height="369" alt="MarkItDown Desktop — Dark Mode" src="https://github.com/user-attachments/assets/3017f17d-7001-46b8-89dc-cb04d243db8e" />
</div>
---

## ✨ Features

| Feature | Description |
|---|---|
| 📁 **Batch Conversion** | Add multiple files — convert them all at once |
| 🔗 **URL Support** | Paste YouTube or any webpage URL for instant conversion |
| 👁️ **Live Preview** | See Markdown output in real-time as files process |
| 💾 **One-Click Export** | Copy, Save, or Save All with a single click |
| 🎨 **Themes** | Dark, Light, and System theme support |
| 🖥️ **Cross-Platform** | Native binaries for Windows, macOS, and Linux |
| ⚡ **Lightweight** | Built with CustomTkinter — zero browser engine, zero Electron |
| 🔄 **Auto-Release CI** | Automated GitHub Actions builds on every version tag |

---

## 📄 Supported Formats

| Category | Formats |
|---|---|
| 📝 Documents | PDF, DOCX, PPTX, XLSX, XLS, EPUB |
| 🖼️ Images | JPG, PNG, GIF, BMP, TIFF |
| 🎵 Audio | WAV, MP3 |
| 🌐 Web | HTML, RSS, YouTube URLs |
| 📊 Data | CSV, JSON, XML |
| 📦 Other | ZIP, Outlook MSG |

---

## ⬇️ Download

> No installation required for portable builds.

| Platform | File | Type |
|---|---|---|
| 🪟 Windows | `MarkItDown-Windows-Setup.exe` | Installer (Start Menu + shortcut) |
| 🪟 Windows | `MarkItDown-Windows-Portable.exe` | Portable — run anywhere |
| 🐧 Linux | `MarkItDown-Linux` | Standalone binary |
| 🍎 macOS | `MarkItDown-macOS` | Standalone binary |

👉 **[Go to Releases →](https://github.com/BOSSincrypto/markitdown-app/releases/latest)**

---

## 🚀 Quick Start

### Run from Source

> Requires Python 3.10+

```bash
git clone https://github.com/BOSSincrypto/markitdown-app.git
cd markitdown-app
pip install -r requirements.txt
python run.py
```

### Build Executable Yourself

```bash
pip install pyinstaller
pyinstaller --onefile --windowed \
  --collect-data customtkinter \
  --collect-data magika \
  --name MarkItDown \
  run.py
```

Output: `dist/MarkItDown`

---

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|---|---|
| `Ctrl+O` | Add files |
| `Ctrl+S` | Save current output |
| `Ctrl+Shift+S` | Save all outputs |

---

## 🔄 How It Works

```
1. Add Files  →  Click "Add Files" or drag & drop (Ctrl+O)
2. Add URL    →  Paste any YouTube or webpage URL (optional)
3. Convert    →  Background threads process all items in parallel
4. Preview    →  Click any file in the list to view its Markdown
5. Export     →  Copy / Save / Save All
```

---

## 🏗️ Architecture

- **GUI**: [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) — modern Tk-based UI
- **Core**: [microsoft/markitdown](https://github.com/microsoft/markitdown) — conversion engine
- **Builds**: [PyInstaller](https://pyinstaller.org/) + GitHub Actions CI/CD
- **Distribution**: Pre-built binaries via GitHub Releases

---

## 📋 Roadmap

- [ ] Drag & drop file support
- [ ] Custom output directory
- [ ] File history / recent files
- [ ] Progress bar per file
- [ ] Plugin/extension support

---

## 🤝 Contributing

Contributions welcome!

1. Fork the repo
2. Create a branch: `git checkout -b feature/your-feature`
3. Commit: `git commit -m 'Add your feature'`
4. Push: `git push origin feature/your-feature`
5. Open a Pull Request

---

## 🔗 Related Projects

- [microsoft/markitdown](https://github.com/microsoft/markitdown) — the core conversion library this app wraps
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) — modern Python UI toolkit used for the GUI

---

## 📜 License

MIT © [BOSSincrypto](https://github.com/BOSSincrypto)

---

<div align="center">

If this tool saves you time, consider giving it a ⭐ — it helps others find it.

[![Star History Chart](https://api.star-history.com/svg?repos=BOSSincrypto/markitdown-app&type=Date)](https://star-history.com/#BOSSincrypto/markitdown-app&Date)

</div>
