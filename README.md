# MarkItDown Desktop

Cross-platform desktop GUI for [microsoft/markitdown](https://github.com/microsoft/markitdown) — convert PDF, Word, Excel, PowerPoint, images, audio, and more to Markdown.

## Features

- **Batch conversion** — add multiple files and convert them all at once
- **URL support** — paste YouTube or webpage URLs for conversion
- **Live preview** — view converted Markdown output instantly
- **Copy / Save / Save All** — export results with one click
- **Dark & Light themes** — toggle between dark, light, and system themes
- **Cross-platform** — runs on Windows, Linux, and macOS
- **Lightweight** — built with CustomTkinter, no browser engine

## Supported Formats

| Category | Extensions |
|----------|-----------|
| Documents | PDF, DOCX, PPTX, XLSX, XLS, EPUB |
| Images | JPG, PNG, GIF, BMP, TIFF |
| Audio | WAV, MP3 |
| Web | HTML, RSS, YouTube URLs |
| Data | CSV, JSON, XML |
| Other | ZIP, Outlook MSG |

## Download

Go to [Releases](../../releases) and download the binary for your platform:

| Platform | File | Description |
|----------|------|-------------|
| Windows | `MarkItDown-Windows-Setup.exe` | Installer (Start Menu + Desktop shortcut) |
| Windows | `MarkItDown-Windows-Portable.exe` | Portable (no installation needed) |
| Linux | `MarkItDown-Linux` | Standalone binary |
| macOS | `MarkItDown-macOS` | Standalone binary |

## Run from Source

Requires Python 3.10+.

```bash
pip install -r requirements.txt
python run.py
```

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| Ctrl+O | Add files |
| Ctrl+S | Save current output |
| Ctrl+Shift+S | Save all outputs |

## How It Works

1. Click **Add Files** (or Ctrl+O) to select files for conversion
2. Optionally click **Add URL** to add YouTube or webpage URLs
3. Click **Convert** to process all files in background threads
4. Click on any file in the list to view its output
5. Use **Copy**, **Save**, or **Save All** to export

## Build Executable

```bash
pip install pyinstaller
pyinstaller --onefile --windowed \
  --collect-data customtkinter \
  --collect-data magika \
  --name MarkItDown \
  run.py
```

The executable will be in the `dist/` folder.

## Auto-Release

Push a version tag to trigger automated builds for all platforms:

```bash
git tag v1.0.0
git push origin v1.0.0
```

GitHub Actions will build executables for Windows, Linux, and macOS and attach them to a GitHub Release.

## License

MIT
