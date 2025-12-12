#!/usr/bin/env python3
"""Find and display diffs for fuzzy entries in pofile.
diff are displayed in the order of the pofile.
GUI version
"""

import os
import sys
import textwrap
import tkinter as tk
from datetime import datetime
from difflib import HtmlDiff
from tkinter import filedialog, messagebox, ttk

from pygit2 import Oid, Repository

from .core import core_parser

try:
    from tkinterweb import HtmlFrame
except (ImportError, ModuleNotFoundError) as exc:
    raise ImportError(
        'tkinterweb is required for GUI. install it with  pip install "pofuzzy-helper[gui]"'
    ) from exc

from .core import FileFuzzies, get_fuzzy_entries, populate


class PoFuzzyViewer:
    """Managing graphical user interface"""

    def __init__(
        self,
        root,
        file_fuzzies: FileFuzzies,
        file_id: Oid,
        width: int,
    ):
        self.root = root
        self.repo = file_fuzzies.repo
        self.width = width
        if file_fuzzies.file_path:
            self.file_path = file_fuzzies.file_path
            self.file_id = file_id
            self.current_index = 0
            self.diffs = file_fuzzies.diffs
        else:
            self.file_path = ""
            self.choose_file()

        # Window Configuration
        self.root.title("Fuzzy Diff Viewer")
        self.root.geometry(f"{20+19*self.width}x400")

        self.lbl_commit = tk.Label(self.root, text="Commit:")
        self.lbl_commit.pack(side="top")
        self.txt_commit_id = tk.Text(self.root, height=1)
        self.txt_commit_id.pack(side="top", padx=5, fill=tk.X)

        # Menu
        menu = tk.Menu(self.root)
        menu_file = tk.Menu(menu, tearoff=0)
        menu_file.add_command(label="Open", command=self.choose_file)
        menu_file.add_separator()
        menu_file.add_command(label="Exit", command=self.root.quit)
        menu.add_cascade(label="File", menu=menu_file)
        self.root.config(menu=menu)

        # navigation buttons
        self.button_frame = ttk.Frame(self.root)
        self.button_frame.pack(fill=tk.X, padx=10, pady=5)

        self.prev_button = ttk.Button(
            self.button_frame, text="↑", command=self.show_previous_diff
        )
        self.prev_button.pack(side=tk.LEFT, padx=5)
        self.next_button = ttk.Button(
            self.button_frame, text="↓", command=self.show_next_diff
        )
        self.next_button.pack(side=tk.LEFT, padx=5)
        self.lbl_filename = tk.Label(self.button_frame, text=f"{self.file_path} -")
        self.lbl_filename.pack(side=tk.LEFT, padx=5, fill=tk.X)
        self.lbl_entry = tk.Label(self.button_frame, text="line:")
        self.lbl_entry.pack(side=tk.LEFT, fill=tk.X)

        self.diff_frame = HtmlFrame(self.root, messages_enabled=False)
        self.diff_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.show_current_diff()

    def choose_file(self):
        file_path = filedialog.askopenfilename(
            title="Choose a .po file",
            filetypes=[("Translation files", ".po")],
        )
        if file_path:
            file_rel_path = os.path.relpath(
                file_path, start=os.path.dirname(self.repo.path[:-1])
            )
            need_redraw = "" != self.file_path
            if file_rel_path != self.file_path:
                self.file_path = file_rel_path
                self.file_id = (
                    self.repo.get(self.repo.head.target).tree[self.file_path].id
                )
                self.diffs = [
                    {"linenum": linenum}
                    for linenum in get_fuzzy_entries(self.repo, self.file_id)
                ]
                if len(self.diffs) == 0:
                    resp = messagebox.askyesno(
                        "Choosing a file",
                        f"{file_rel_path} has no diffs\nQuit?",
                    )
                    if resp:
                        sys.exit()
                self.current_index = 0
                if need_redraw:
                    self.lbl_filename.config(text=file_rel_path + " -")
                    self.show_current_diff()
            return
        if not self.file_path:
            sys.exit()

    def show_current_diff(self):
        if not self.diffs:
            return
        cur_diff = self.diffs[self.current_index]
        linenum, blame, current, old, tzinfo = populate(
            self.repo, self.file_path, self.file_id, cur_diff
        )
        self.lbl_commit.config(
            text=f"{datetime.fromtimestamp(blame.final_committer.time, tzinfo)} "
            f"by {blame.final_committer.name}"
        )
        self.txt_commit_id.delete(1.0, tk.END)
        self.txt_commit_id.insert(tk.END, str(blame.final_commit_id))
        self.lbl_entry.config(
            text=f"line: {linenum} ({self.current_index+1}/{len(self.diffs)})"
        )
        html_diff = HtmlDiff().make_file(
            textwrap.fill(old, self.width).split("\n"),
            textwrap.fill(current, self.width).split("\n"),
            fromdesc="Old version",
            todesc="Current version",
            context=True,
            numlines=3,
        )
        self.diff_frame.load_html(html_diff)

    def show_next_diff(self):
        if self.current_index < len(self.diffs) - 1:
            self.current_index += 1
            self.show_current_diff()

    def show_previous_diff(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.show_current_diff()


def parse_args():
    parser = core_parser(__doc__)
    parser.add_argument("filename", nargs="?", help="relative path to file to parse")
    return parser.parse_args()


def main():
    args = parse_args()
    repo = Repository(args.repo)
    if args.filename:
        file_id = repo.get(repo.head.target).tree[args.filename].id
        diffs = [{"linenum": linenum} for linenum in get_fuzzy_entries(repo, file_id)]
    else:
        file_id = None
        diffs = None
    root = tk.Tk()
    file_fuzzies = FileFuzzies(repo, args.filename, diffs)
    app = PoFuzzyViewer(root, file_fuzzies, file_id, args.width)
    root.mainloop()


if __name__ == "__main__":
    main()
