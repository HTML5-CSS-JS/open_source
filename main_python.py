# -*- coding: utf-8 -*-
import hangul
import sys
import os
import subprocess
import threading
import queue
import time
import tempfile
import tkinter as tk
from tkinter import filedialog, messagebox

import customtkinter as ctk
import pygame  # pygame-ce

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# 색상 선택 함수
def get_theme_color(value):
    if isinstance(value, (list, tuple)):
        if ctk.get_appearance_mode() == "Dark":
            return value[1]
        else:
            return value[0]
    return value


# -----------------------
# 줄번호 표시
# -----------------------
class LineNumbers(ctk.CTkCanvas):
    def __init__(self, master, text_widget, **kwargs):
        super().__init__(master, width=40, **kwargs)
        self.text_widget = text_widget
        self.text_widget.bind("<KeyRelease>", self.redraw)
        self.text_widget.bind("<MouseWheel>", self.redraw)
        self.text_widget.bind("<Button-1>", self.redraw)
        self.text_widget.bind("<Configure>", self.redraw)
        self.configure(bg=get_theme_color(ctk.ThemeManager.theme["CTkFrame"]["fg_color"]))
        self.redraw()

    def redraw(self, event=None):
        self.delete("all")
        i = self.text_widget.index("@0,0")
        while True:
            dline = self.text_widget.dlineinfo(i)
            if dline is None:
                break
            y = dline[1]
            linenum = str(i).split(".")[0]
            self.create_text(30, y, anchor="ne",
                             text=linenum,
                             fill=get_theme_color(ctk.ThemeManager.theme["CTkLabel"]["text_color"]))
            i = self.text_widget.index(f"{i}+1line")


# -----------------------
# 에디터 (문법 하이라이팅 포함)
# -----------------------
class Editor(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.text = tk.Text(
            self, wrap="none", undo=True, font=("Consolas", 12),
            bg=get_theme_color(ctk.ThemeManager.theme["CTkFrame"]["fg_color"]),
            fg=get_theme_color(ctk.ThemeManager.theme["CTkLabel"]["text_color"]),
            insertbackground=get_theme_color(ctk.ThemeManager.theme["CTkLabel"]["text_color"]),
            highlightthickness=0, bd=0
        )
        self.vscroll = ctk.CTkScrollbar(self, command=self.text.yview)
        self.hscroll = ctk.CTkScrollbar(self, command=self.text.xview, orientation="horizontal")
        self.text.configure(yscrollcommand=self.vscroll.set, xscrollcommand=self.hscroll.set)

        self.line_numbers = LineNumbers(self, self.text)
        self.line_numbers.grid(row=0, column=0, sticky="ns")
        self.text.grid(row=0, column=1, sticky="nsew")
        self.vscroll.grid(row=0, column=2, sticky="ns")
        self.hscroll.grid(row=1, column=1, sticky="ew")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # 문법 태그
        self.text.tag_configure("keyword", foreground="#7aa2f7")
        self.text.tag_configure("string", foreground="#9ece6a")
        self.text.tag_configure("comment", foreground="#565f89", font=("Consolas", 12, "italic"))
        self.text.tag_configure("number", foreground="#f7768e")
        self.text.tag_configure("decorator", foreground="#bb9af7")

        self.keywords = {
            "def", "class", "import", "from", "return", "if", "elif", "else",
            "for", "while", "try", "except", "finally", "with", "as", "pass",
            "break", "continue", "yield", "lambda", "True", "False", "None",
            "global", "nonlocal", "assert", "raise", "del", "in", "is", "and", "or", "not"
        }

        self.text.bind("<KeyRelease>", self._syntax_highlight)

    def _syntax_highlight(self, event=None):
        current_line = self.text.index("insert").split(".")[0]
        start = f"{current_line}.0"
        end = f"{current_line}.end"
        line_text = self.text.get(start, end)

        # 태그 제거
        for tag in ["keyword", "string", "comment", "number", "decorator"]:
            self.text.tag_remove(tag, start, end)

        # 문자열
        import re
        for m in re.finditer(r"(\".*?\"|\'.*?\')", line_text):
            self.text.tag_add("string", f"{current_line}.{m.start()}", f"{current_line}.{m.end()}")

        # 주석
        c = line_text.find("#")
        if c != -1:
            self.text.tag_add("comment", f"{current_line}.{c}", end)

        # 데코레이터
        if line_text.strip().startswith("@"):
            self.text.tag_add("decorator", start, end)

        # 숫자
        for m in re.finditer(r"\b\d+\b", line_text):
            self.text.tag_add("number", f"{current_line}.{m.start()}", f"{current_line}.{m.end()}")

        # 키워드
        for kw in self.keywords:
            for m in re.finditer(rf"\b{kw}\b", line_text):
                self.text.tag_add("keyword", f"{current_line}.{m.start()}", f"{current_line}.{m.end()}")

        self.line_numbers.redraw()


# -----------------------
# 메인 IDE
# -----------------------
class MiniIDE(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Mini IDE (Dark Mode)")
        self.geometry("1000x700")

        self.tabs = ctk.CTkTabview(self)
        self.tabs.pack(fill="both", expand=True)

        self.new_tab(initial_text="# -*- coding: utf-8 -*-\nimport hangul\nimport sys\nimport os\nimport customtkinter\nimport pygame  # pygame-ce\n\nprint('Hello from Mini IDE!')\n")

    def new_tab(self, initial_text=""):
        name = f"Untitled {len(self.tabs._tab_dict) + 1}"
        tab = self.tabs.add(name)
        editor = Editor(tab)
        editor.pack(fill="both", expand=True, padx=6, pady=6)
        if initial_text:
            editor.text.insert("1.0", initial_text)


if __name__ == "__main__":
    app = MiniIDE()
    app.mainloop()
