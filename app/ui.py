import os
import platform
import queue
from pathlib import Path
from tkinter import filedialog

import customtkinter as ctk

from .converter import ConverterEngine, ConversionResult, Status

SUPPORTED_EXTENSIONS = [
    (
        "All Supported",
        "*.pdf *.docx *.doc *.pptx *.ppt *.xlsx *.xls "
        "*.html *.htm *.csv *.json *.xml *.zip *.epub "
        "*.jpg *.jpeg *.png *.gif *.bmp *.tiff "
        "*.wav *.mp3 *.msg",
    ),
    ("PDF", "*.pdf"),
    ("Word", "*.docx *.doc"),
    ("PowerPoint", "*.pptx *.ppt"),
    ("Excel", "*.xlsx *.xls"),
    ("Images", "*.jpg *.jpeg *.png *.gif *.bmp *.tiff"),
    ("Audio", "*.wav *.mp3"),
    ("Web", "*.html *.htm"),
    ("Data", "*.csv *.json *.xml"),
    ("Archives", "*.zip"),
    ("eBooks", "*.epub"),
    ("All Files", "*.*"),
]

MONO_FONT = {
    "Windows": "Consolas",
    "Darwin": "Menlo",
}.get(platform.system(), "monospace")


class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("MarkItDown")
        self.geometry("900x700")
        self.minsize(640, 480)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self._engine = ConverterEngine()
        self._files: list[str] = []
        self._results: dict[str, ConversionResult] = {}
        self._selected_file: str = ""
        self._result_queue: queue.Queue = queue.Queue()
        self._total = 0
        self._done_count = 0

        self._build_ui()
        self._bind_shortcuts()

    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        # --- Header ---
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, padx=16, pady=(16, 8), sticky="ew")
        header.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            header, text="MarkItDown", font=ctk.CTkFont(size=20, weight="bold")
        ).grid(row=0, column=0, sticky="w")

        btn_frame = ctk.CTkFrame(header, fg_color="transparent")
        btn_frame.grid(row=0, column=2, sticky="e")

        ctk.CTkButton(
            btn_frame, text="Add Files", width=110, command=self._add_files
        ).grid(row=0, column=0, padx=(0, 6))

        ctk.CTkButton(
            btn_frame,
            text="Add URL",
            width=90,
            fg_color="#555555",
            hover_color="#666666",
            command=self._add_url,
        ).grid(row=0, column=1)

        # --- File list ---
        self._file_frame = ctk.CTkScrollableFrame(self, height=110, label_text="Files")
        self._file_frame.grid(row=1, column=0, padx=16, pady=(0, 8), sticky="ew")
        self._file_frame.grid_columnconfigure(0, weight=1)

        self._empty_label = ctk.CTkLabel(
            self._file_frame,
            text="No files added. Click 'Add Files' or press Ctrl+O.",
            text_color="gray",
        )
        self._empty_label.grid(row=0, column=0, pady=8)

        # --- Convert + progress ---
        action_row = ctk.CTkFrame(self, fg_color="transparent")
        action_row.grid(row=2, column=0, padx=16, pady=(0, 8), sticky="ew")
        action_row.grid_columnconfigure(1, weight=1)

        self._convert_btn = ctk.CTkButton(
            action_row,
            text="Convert",
            width=130,
            height=36,
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self._convert_all,
        )
        self._convert_btn.grid(row=0, column=0)

        self._progress = ctk.CTkProgressBar(action_row)
        self._progress.grid(row=0, column=1, padx=(12, 0), sticky="ew")
        self._progress.set(0)

        self._progress_label = ctk.CTkLabel(action_row, text="", width=50)
        self._progress_label.grid(row=0, column=2, padx=(8, 0))

        # --- Output ---
        out_frame = ctk.CTkFrame(self)
        out_frame.grid(row=3, column=0, padx=16, pady=(0, 8), sticky="nsew")
        out_frame.grid_columnconfigure(0, weight=1)
        out_frame.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(
            out_frame,
            text="Output",
            font=ctk.CTkFont(size=13, weight="bold"),
        ).grid(row=0, column=0, padx=12, pady=(8, 0), sticky="w")

        self._output = ctk.CTkTextbox(
            out_frame,
            wrap="word",
            font=ctk.CTkFont(family=MONO_FONT, size=13),
        )
        self._output.grid(row=1, column=0, padx=8, pady=8, sticky="nsew")
        self._output.insert("1.0", "Converted markdown will appear here...")
        self._output.configure(state="disabled")

        # --- Bottom bar ---
        bottom = ctk.CTkFrame(self, fg_color="transparent")
        bottom.grid(row=4, column=0, padx=16, pady=(0, 8), sticky="ew")
        bottom.grid_columnconfigure(3, weight=1)

        ctk.CTkButton(bottom, text="Copy", width=80, command=self._copy_output).grid(
            row=0, column=0
        )
        ctk.CTkButton(bottom, text="Save", width=80, command=self._save_output).grid(
            row=0, column=1, padx=(6, 0)
        )
        ctk.CTkButton(bottom, text="Save All", width=90, command=self._save_all).grid(
            row=0, column=2, padx=(6, 0)
        )

        ctk.CTkOptionMenu(
            bottom,
            values=["Dark", "Light", "System"],
            width=90,
            command=self._change_theme,
        ).grid(row=0, column=4)

        # --- Status ---
        self._status = ctk.CTkLabel(self, text="Ready", text_color="gray", anchor="w")
        self._status.grid(row=5, column=0, padx=16, pady=(0, 8), sticky="ew")

    def _bind_shortcuts(self):
        self.bind("<Control-o>", lambda e: self._add_files())
        self.bind("<Control-s>", lambda e: self._save_output())
        self.bind("<Control-Shift-S>", lambda e: self._save_all())

    # --- File management ---

    def _add_files(self):
        paths = filedialog.askopenfilenames(
            title="Select files to convert",
            filetypes=SUPPORTED_EXTENSIONS,
        )
        for p in paths:
            if p and p not in self._files:
                self._files.append(p)
        self._refresh_file_list()

    def _add_url(self):
        dialog = ctk.CTkInputDialog(
            text="Enter URL (YouTube, webpage, etc.):", title="Add URL"
        )
        url = dialog.get_input()
        if url and url.strip():
            url = url.strip()
            if url not in self._files:
                self._files.append(url)
                self._refresh_file_list()

    def _remove_file(self, index: int):
        path = self._files.pop(index)
        self._results.pop(path, None)
        if self._selected_file == path:
            self._selected_file = ""
            self._set_output("")
        self._refresh_file_list()

    def _select_file(self, path: str):
        self._selected_file = path
        result = self._results.get(path)
        if result and result.status == Status.DONE:
            self._set_output(result.markdown)
        elif result and result.status == Status.ERROR:
            self._set_output(f"Error: {result.error}")
        else:
            self._set_output("")

    def _refresh_file_list(self):
        for widget in self._file_frame.winfo_children():
            widget.destroy()

        if not self._files:
            self._empty_label = ctk.CTkLabel(
                self._file_frame,
                text="No files added. Click 'Add Files' or press Ctrl+O.",
                text_color="gray",
            )
            self._empty_label.grid(row=0, column=0, pady=8)
            return

        for i, f in enumerate(self._files):
            row = ctk.CTkFrame(self._file_frame, fg_color="transparent")
            row.grid(row=i, column=0, sticky="ew", pady=1)
            row.grid_columnconfigure(1, weight=1)

            status = self._results.get(f)
            if status and status.status == Status.DONE:
                icon, color = "OK", "#4CAF50"
            elif status and status.status == Status.ERROR:
                icon, color = "!!", "#F44336"
            elif status and status.status == Status.CONVERTING:
                icon, color = "..", "#2196F3"
            else:
                icon, color = "--", "gray"

            ctk.CTkLabel(row, text=icon, text_color=color, width=24).grid(
                row=0, column=0, padx=(4, 4)
            )

            display = os.path.basename(f) if not f.startswith("http") else f
            lbl = ctk.CTkLabel(row, text=display, anchor="w", cursor="hand2")
            lbl.grid(row=0, column=1, sticky="ew")
            lbl.bind("<Button-1>", lambda e, path=f: self._select_file(path))

            idx = i
            ctk.CTkButton(
                row,
                text="x",
                width=28,
                height=28,
                fg_color="#555",
                hover_color="#F44336",
                command=lambda idx=idx: self._remove_file(idx),
            ).grid(row=0, column=2, padx=(4, 4))

    # --- Conversion ---

    def _convert_all(self):
        if not self._files:
            return

        self._convert_btn.configure(state="disabled")
        self._progress.set(0)
        self._progress_label.configure(text="")
        self._total = len(self._files)
        self._done_count = 0
        self._status.configure(text=f"Converting 0/{self._total}...")

        for f in self._files:
            self._results[f] = ConversionResult(
                file_path=f, status=Status.CONVERTING
            )
            self._engine.convert_async(f, self._result_queue)

        self._refresh_file_list()
        self._poll_results()

    def _poll_results(self):
        try:
            while True:
                result = self._result_queue.get_nowait()
                self._on_done(result)
        except queue.Empty:
            pass

        if self._done_count < self._total:
            self.after(100, self._poll_results)

    def _on_done(self, result: ConversionResult):
        self._results[result.file_path] = result
        self._done_count += 1

        progress = self._done_count / max(self._total, 1)
        self._progress.set(progress)
        self._progress_label.configure(text=f"{self._done_count}/{self._total}")

        name = os.path.basename(result.file_path)
        if result.status == Status.DONE:
            self._status.configure(text=f"Converted: {name}")
        else:
            self._status.configure(text=f"Error: {name}")

        if self._done_count == 1 or self._selected_file == result.file_path:
            self._selected_file = result.file_path
            if result.status == Status.DONE:
                self._set_output(result.markdown)
            else:
                self._set_output(f"Error converting {name}:\n{result.error}")

        self._refresh_file_list()

        if self._done_count >= self._total:
            errors = sum(
                1 for r in self._results.values() if r.status == Status.ERROR
            )
            ok = self._total - errors
            if errors:
                self._status.configure(text=f"Done: {ok} converted, {errors} errors")
            else:
                self._status.configure(text=f"Done: {ok} file(s) converted")
            self._convert_btn.configure(state="normal")

    # --- Output actions ---

    def _set_output(self, text: str):
        self._output.configure(state="normal")
        self._output.delete("1.0", "end")
        self._output.insert("1.0", text)
        self._output.configure(state="disabled")

    def _copy_output(self):
        self._output.configure(state="normal")
        text = self._output.get("1.0", "end").strip()
        self._output.configure(state="disabled")
        if text:
            self.clipboard_clear()
            self.clipboard_append(text)
            self._status.configure(text="Copied to clipboard")

    def _save_output(self):
        self._output.configure(state="normal")
        text = self._output.get("1.0", "end").strip()
        self._output.configure(state="disabled")
        if not text:
            return

        default_name = "output.md"
        if self._selected_file:
            base = os.path.basename(self._selected_file)
            default_name = Path(base).stem + ".md"

        path = filedialog.asksaveasfilename(
            defaultextension=".md",
            filetypes=[("Markdown", "*.md"), ("Text", "*.txt")],
            initialfile=default_name,
        )
        if path:
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(text)
            self._status.configure(text=f"Saved: {os.path.basename(path)}")

    def _save_all(self):
        done = [r for r in self._results.values() if r.status == Status.DONE]
        if not done:
            return

        directory = filedialog.askdirectory(title="Select output directory")
        if not directory:
            return

        count = 0
        for result in done:
            name = Path(os.path.basename(result.file_path)).stem + ".md"
            out_path = os.path.join(directory, name)
            with open(out_path, "w", encoding="utf-8") as fh:
                fh.write(result.markdown)
            count += 1

        self._status.configure(text=f"Saved {count} file(s) to {directory}")

    def _change_theme(self, choice: str):
        ctk.set_appearance_mode(choice.lower())
