import queue
import re
import sys
import threading
import traceback
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from yt_dlp.utils import DownloadError

from youtube_to_mp3 import configure_bundled_ffmpeg, download_mp3, resource_path


APP_NAME = "MP3 Ship"
QUALITIES = ("128", "192", "256", "320")
URL_PATTERN = re.compile(r"https?://[^\s,;]+")

I18N = {
    "en": {
        "language_button": "Русский",
        "description": "Download YouTube videos and playlists as MP3 files in one self-contained Windows app.",
        "links": "YouTube links",
        "save_to": "Save to",
        "browse": "Browse",
        "quality": "MP3 quality",
        "download": "Download MP3",
        "clear_log": "Clear log",
        "ready": "Ready",
        "ready_log": "Ready. Paste one or many YouTube links, choose a folder, then press Download MP3.",
        "missing_links": "Paste at least one YouTube link.",
        "missing_output": "Choose an output folder.",
        "choose_output": "Choose output folder",
        "downloading": "Downloading...",
        "starting": "Starting download...",
        "done": "Done.",
        "download_error": "Download error: ",
        "error": "Error:",
        "downloading_file": "Downloading",
        "converting_file": "Converting",
        "to_mp3": "to MP3...",
    },
    "ru": {
        "language_button": "English",
        "description": "Скачивает видео и плейлисты YouTube в MP3 внутри одного автономного Windows-приложения.",
        "links": "Ссылки YouTube",
        "save_to": "Сохранить в",
        "browse": "Обзор",
        "quality": "Качество MP3",
        "download": "Скачать MP3",
        "clear_log": "Очистить журнал",
        "ready": "Готово",
        "ready_log": "Готово. Вставьте одну или много ссылок YouTube, выберите папку и нажмите Скачать MP3.",
        "missing_links": "Вставьте хотя бы одну ссылку YouTube.",
        "missing_output": "Выберите папку для сохранения.",
        "choose_output": "Выберите папку для сохранения",
        "downloading": "Скачивание...",
        "starting": "Запуск скачивания...",
        "done": "Готово.",
        "download_error": "Ошибка скачивания: ",
        "error": "Ошибка:",
        "downloading_file": "Скачивается",
        "converting_file": "Конвертация",
        "to_mp3": "в MP3...",
    },
}

COLORS = {
    "bg": "#101418",
    "panel": "#171e24",
    "field": "#202a32",
    "border": "#34414b",
    "text": "#f4f7f8",
    "muted": "#aebbc3",
    "accent": "#19a7a8",
    "accent_hot": "#22c6bd",
    "button": "#22313a",
    "button_active": "#2d444e",
    "error": "#ff756e",
}


def enable_high_dpi():
    if sys.platform != "win32":
        return
    try:
        import ctypes

        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except Exception:
            ctypes.windll.user32.SetProcessDPIAware()
    except Exception:
        pass


class GuiLogger:
    def __init__(self, log_queue):
        self.log_queue = log_queue

    def debug(self, message):
        pass

    def warning(self, message):
        self.log_queue.put(message + "\n")

    def error(self, message):
        self.log_queue.put(message + "\n")


class MP3ShipApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_NAME)
        self.minsize(760, 560)
        self.geometry("860x640")
        self.configure(bg=COLORS["bg"])

        icon = resource_path("assets/mp3_ship_icon_exact.ico")
        if icon.exists():
            self.iconbitmap(str(icon))

        self.urls_var = tk.StringVar()
        self.output_var = tk.StringVar(value=str(Path.home() / "Music"))
        self.quality_var = tk.StringVar(value="192")
        self.language = "ru"
        self.localized_widgets = []
        self.status_var = tk.StringVar()
        self.worker = None
        self.log_queue = queue.Queue()

        self._configure_style()
        self._bind_edit_shortcuts()
        self._build_ui()
        self._apply_language(clear_log=True)
        self.after(100, self._drain_log_queue)

    def t(self, key):
        return I18N[self.language][key]

    def _configure_style(self):
        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        self.style.configure(".", background=COLORS["bg"], foreground=COLORS["text"])
        self.style.configure("TFrame", background=COLORS["bg"])
        self.style.configure("Panel.TFrame", background=COLORS["panel"])
        self.style.configure("TLabel", background=COLORS["bg"], foreground=COLORS["text"], font=("Segoe UI", 10))
        self.style.configure("Muted.TLabel", background=COLORS["bg"], foreground=COLORS["muted"], font=("Segoe UI", 10))
        self.style.configure("Title.TLabel", background=COLORS["bg"], foreground=COLORS["text"], font=("Segoe UI", 24, "bold"))
        self.style.configure("TButton", background=COLORS["button"], foreground=COLORS["text"], borderwidth=1, padding=(12, 8), font=("Segoe UI", 10))
        self.style.map("TButton", background=[("active", COLORS["button_active"]), ("pressed", COLORS["accent"])])
        self.style.configure("Accent.TButton", background=COLORS["accent"], foreground="#ffffff", font=("Segoe UI", 10, "bold"))
        self.style.map("Accent.TButton", background=[("active", COLORS["accent_hot"]), ("pressed", "#11888d")])
        self.style.configure("TEntry", fieldbackground=COLORS["field"], foreground=COLORS["text"], insertcolor=COLORS["text"], bordercolor=COLORS["border"], padding=6)
        self.style.configure("TCombobox", fieldbackground=COLORS["field"], foreground=COLORS["text"], arrowcolor=COLORS["accent"], bordercolor=COLORS["border"], padding=6)
        self.style.map("TCombobox", fieldbackground=[("readonly", COLORS["field"])], foreground=[("readonly", COLORS["text"])])
        self.style.configure("Horizontal.TProgressbar", background=COLORS["accent"], troughcolor=COLORS["field"], bordercolor=COLORS["border"])

    def _build_ui(self):
        root = ttk.Frame(self, padding=20)
        root.pack(fill=tk.BOTH, expand=True)
        root.columnconfigure(0, weight=1)
        root.rowconfigure(3, weight=1)

        header = ttk.Frame(root)
        header.grid(row=0, column=0, sticky="ew", pady=(0, 18))
        header.columnconfigure(0, weight=1)
        ttk.Label(header, text=APP_NAME, style="Title.TLabel").grid(row=0, column=0, sticky="w")
        self.description_label = ttk.Label(
            header,
            style="Muted.TLabel",
            wraplength=720,
        )
        self.description_label.grid(row=1, column=0, sticky="w", pady=(4, 0))
        self.localized_widgets.append((self.description_label, "description"))
        self.language_button = ttk.Button(header, command=self._toggle_language)
        self.language_button.grid(row=0, column=1, sticky="ne", padx=(12, 0))
        self.localized_widgets.append((self.language_button, "language_button"))

        form = ttk.Frame(root, style="Panel.TFrame", padding=16)
        form.grid(row=1, column=0, sticky="ew")
        form.columnconfigure(1, weight=1)

        self.links_label = ttk.Label(form, background=COLORS["panel"])
        self.links_label.grid(row=0, column=0, sticky="nw", pady=(2, 8))
        self.localized_widgets.append((self.links_label, "links"))
        self.urls_text = tk.Text(
            form,
            height=6,
            wrap="word",
            undo=True,
            bg=COLORS["field"],
            fg=COLORS["text"],
            insertbackground=COLORS["text"],
            relief="solid",
            borderwidth=1,
            highlightthickness=1,
            highlightbackground=COLORS["border"],
            font=("Segoe UI", 10),
        )
        self.urls_text.grid(row=0, column=1, columnspan=2, sticky="ew", padx=(12, 0), pady=(0, 10))

        self.save_to_label = ttk.Label(form, background=COLORS["panel"])
        self.save_to_label.grid(row=1, column=0, sticky="w", pady=6)
        self.localized_widgets.append((self.save_to_label, "save_to"))
        ttk.Entry(form, textvariable=self.output_var).grid(row=1, column=1, sticky="ew", padx=(12, 8), pady=6)
        self.browse_button = ttk.Button(form, command=self._choose_output)
        self.browse_button.grid(row=1, column=2, sticky="e", pady=6)
        self.localized_widgets.append((self.browse_button, "browse"))

        self.quality_label = ttk.Label(form, background=COLORS["panel"])
        self.quality_label.grid(row=2, column=0, sticky="w", pady=6)
        self.localized_widgets.append((self.quality_label, "quality"))
        ttk.Combobox(form, textvariable=self.quality_var, values=QUALITIES, state="readonly", width=12).grid(row=2, column=1, sticky="w", padx=(12, 0), pady=6)

        buttons = ttk.Frame(root)
        buttons.grid(row=2, column=0, sticky="ew", pady=14)
        buttons.columnconfigure(0, weight=1)
        self.run_button = ttk.Button(buttons, command=self._run, style="Accent.TButton")
        self.run_button.grid(row=0, column=1, padx=(8, 0))
        self.localized_widgets.append((self.run_button, "download"))
        self.clear_button = ttk.Button(buttons, command=self._clear_log)
        self.clear_button.grid(row=0, column=2, padx=(8, 0))
        self.localized_widgets.append((self.clear_button, "clear_log"))

        log_frame = ttk.Frame(root)
        log_frame.grid(row=3, column=0, sticky="nsew")
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(1, weight=1)
        ttk.Label(log_frame, textvariable=self.status_var, style="Muted.TLabel").grid(row=0, column=0, sticky="w", pady=(0, 8))
        self.progress = ttk.Progressbar(log_frame, mode="indeterminate")
        self.progress.grid(row=0, column=1, sticky="ew", pady=(0, 8))
        self.log = tk.Text(
            log_frame,
            height=16,
            wrap="word",
            undo=True,
            bg="#0b0f12",
            fg=COLORS["text"],
            insertbackground=COLORS["text"],
            relief="solid",
            borderwidth=1,
            highlightthickness=1,
            highlightbackground=COLORS["border"],
            font=("Consolas", 10),
        )
        self.log.grid(row=1, column=0, columnspan=2, sticky="nsew")
        scrollbar = ttk.Scrollbar(log_frame, command=self.log.yview)
        scrollbar.grid(row=1, column=2, sticky="ns")
        self.log.configure(yscrollcommand=scrollbar.set)

    def _bind_edit_shortcuts(self):
        for sequence, handler in {
            "<Control-a>": self._select_all,
            "<Control-A>": self._select_all,
            "<Control-c>": self._copy,
            "<Control-C>": self._copy,
            "<Control-x>": self._cut,
            "<Control-X>": self._cut,
            "<Control-v>": self._paste,
            "<Control-V>": self._paste,
            "<Control-z>": self._undo,
            "<Control-Z>": self._undo,
            "<Shift-Insert>": self._paste,
        }.items():
            self.bind_all(sequence, handler, add="+")
        self.bind_all("<Control-KeyPress>", self._keycode_fallback, add="+")

    def _keycode_fallback(self, event):
        if not event.state & 0x4:
            return None
        keycode_map = {
            65: self._select_all,
            67: self._copy,
            86: self._paste,
            88: self._cut,
            90: self._undo,
        }
        handler = keycode_map.get(event.keycode)
        if handler:
            return handler(event)
        return None

    def _focused_edit_widget(self):
        widget = self.focus_get()
        if widget is not None and widget.winfo_class() in {"Entry", "TEntry", "Text", "TCombobox"}:
            return widget
        return None

    def _select_all(self, _event=None):
        widget = self._focused_edit_widget()
        if widget is None:
            return None
        if widget.winfo_class() == "Text":
            widget.tag_add("sel", "1.0", "end-1c")
        else:
            widget.selection_range(0, tk.END)
            widget.icursor(tk.END)
        return "break"

    def _copy(self, _event=None):
        widget = self._focused_edit_widget()
        if widget is None:
            return None
        try:
            if widget.winfo_class() == "Text":
                selected = widget.get("sel.first", "sel.last")
            else:
                selected = widget.selection_get()
            self.clipboard_clear()
            self.clipboard_append(selected)
            return "break"
        except tk.TclError:
            return None

    def _cut(self, _event=None):
        widget = self._focused_edit_widget()
        if widget is None:
            return None
        try:
            if widget.winfo_class() == "Text":
                selected = widget.get("sel.first", "sel.last")
                widget.delete("sel.first", "sel.last")
            else:
                selected = widget.selection_get()
                widget.delete("sel.first", "sel.last")
            self.clipboard_clear()
            self.clipboard_append(selected)
            return "break"
        except tk.TclError:
            return None

    def _paste(self, _event=None):
        widget = self._focused_edit_widget()
        if widget is None:
            return None
        try:
            text = self.clipboard_get()
            if widget.winfo_class() == "Text":
                try:
                    widget.delete("sel.first", "sel.last")
                except tk.TclError:
                    pass
                widget.insert(tk.INSERT, text)
            else:
                try:
                    widget.delete("sel.first", "sel.last")
                except tk.TclError:
                    pass
                widget.insert(tk.INSERT, text)
            return "break"
        except tk.TclError:
            return None

    def _undo(self, _event=None):
        return self._generate_edit_event("<<Undo>>")

    def _generate_edit_event(self, event_name):
        widget = self._focused_edit_widget()
        if widget is None:
            return None
        widget.event_generate(event_name)
        return "break"

    def _choose_output(self):
        path = filedialog.askdirectory(title=self.t("choose_output"))
        if path:
            self.output_var.set(path)

    def _extract_urls(self):
        text = self.urls_text.get("1.0", tk.END)
        urls = URL_PATTERN.findall(text)
        return [url.rstrip(").]}>\"'") for url in urls]

    def _run(self):
        if self.worker and self.worker.is_alive():
            return
        urls = self._extract_urls()
        output = self.output_var.get().strip()
        if not urls:
            messagebox.showerror(APP_NAME, self.t("missing_links"))
            return
        if not output:
            messagebox.showerror(APP_NAME, self.t("missing_output"))
            return

        self.run_button.configure(state=tk.DISABLED)
        self.progress.start(12)
        self.status_var.set(self.t("downloading"))
        self._write_log("\n" + self.t("starting") + "\n")
        args = (urls, output, self.quality_var.get())
        self.worker = threading.Thread(target=self._worker_run, args=args, daemon=True)
        self.worker.start()

    def _worker_run(self, urls, output, quality):
        try:
            download_mp3(
                urls,
                output,
                quality,
                progress_hooks=[self._progress_hook],
                logger=GuiLogger(self.log_queue),
            )
            self.log_queue.put("\n" + self.t("done") + "\n")
        except DownloadError as error:
            self.log_queue.put("\n" + self.t("download_error") + str(error) + "\n")
        except Exception:
            self.log_queue.put("\n" + self.t("error") + "\n" + traceback.format_exc())
        finally:
            self.log_queue.put(("__DONE__", None))

    def _progress_hook(self, info):
        status = info.get("status")
        if status == "downloading":
            name = info.get("filename") or info.get("tmpfilename") or "audio"
            percent = info.get("_percent_str", "").strip()
            speed = info.get("_speed_str", "").strip()
            self.log_queue.put(f"{self.t('downloading_file')} {Path(name).name} {percent} {speed}\n")
        elif status == "finished":
            name = info.get("filename") or "audio"
            self.log_queue.put(f"{self.t('converting_file')} {Path(name).name} {self.t('to_mp3')}\n")

    def _drain_log_queue(self):
        try:
            while True:
                item = self.log_queue.get_nowait()
                if isinstance(item, tuple) and item[0] == "__DONE__":
                    self.progress.stop()
                    self.run_button.configure(state=tk.NORMAL)
                    self.status_var.set(self.t("ready"))
                else:
                    self._write_log(item)
        except queue.Empty:
            pass
        self.after(100, self._drain_log_queue)

    def _write_log(self, text):
        self.log.insert(tk.END, text)
        self.log.see(tk.END)

    def _clear_log(self):
        self.log.delete("1.0", tk.END)

    def _toggle_language(self):
        self.language = "en" if self.language == "ru" else "ru"
        self._apply_language(clear_log=False)

    def _apply_language(self, clear_log=False):
        self.title(APP_NAME)
        for widget, key in self.localized_widgets:
            widget.configure(text=self.t(key))
        self.status_var.set(self.t("ready"))
        if clear_log:
            self.log.delete("1.0", tk.END)
            self._write_log(self.t("ready_log") + "\n")


if __name__ == "__main__":
    enable_high_dpi()
    configure_bundled_ffmpeg()
    app = MP3ShipApp()
    app.mainloop()
