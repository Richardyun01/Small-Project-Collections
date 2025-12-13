import os
from collections import OrderedDict
from typing import Dict, List

import requests

import tkinter as tk
from tkinter import ttk, messagebox, filedialog


GITHUB_API_BASE = "https://api.github.com/repos/github/gitignore/contents"
RAW_BASE = "https://raw.githubusercontent.com/github/gitignore/refs/heads/main"


def _github_headers() -> Dict[str, str]:
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "gitignore-merge-gui",
    }
    token = os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def github_get_json(url: str):
    resp = requests.get(url, headers=_github_headers(), timeout=10)
    if resp.status_code != 200:
        raise RuntimeError(f"GitHub API error: {resp.status_code} {resp.text}")
    return resp.json()


def list_dir(path: str = "") -> List[dict]:
    url = f"{GITHUB_API_BASE}/{path}" if path else GITHUB_API_BASE
    data = github_get_json(url)
    if not isinstance(data, list):
        raise RuntimeError(f"Unexpected API response for path '{path}': {data}")
    return data


def build_templates_index() -> Dict[str, str]:
    templates: Dict[str, str] = {}

    for item in list_dir(""):
        name = item.get("name", "")
        if name.endswith(".gitignore"):
            stem = name[:-10]
            templates.setdefault(stem, item.get("path", name))

    for item in list_dir("Global"):
        name = item.get("name", "")
        if name.endswith(".gitignore"):
            stem = name[:-10]
            templates.setdefault(stem, item.get("path", f"Global/{name}"))

    return templates


def fetch_template_text(path: str) -> str:
    url = f"{RAW_BASE}/{path}"
    resp = requests.get(url, timeout=10)
    if resp.status_code != 200:
        raise RuntimeError(f"Failed to fetch '{path}': {resp.status_code} {resp.text}")
    return resp.text


def merge_gitignores_from_paths(paths: List[str], dedup: bool = True) -> str:
    seen = set()
    out_lines: List[str] = []

    for repo_path in paths:
        text = fetch_template_text(repo_path)
        for line in text.splitlines(keepends=True):
            if line.strip() == "":
                out_lines.append(line)
                continue

            if dedup:
                if line in seen:
                    continue
                seen.add(line)

            out_lines.append(line)

    return "".join(out_lines)


class GitignoreGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("GitHub gitignore Merger")
        self.geometry("900x650")

        self.templates_index: Dict[str, str] = {}
        self.template_vars: Dict[str, tk.BooleanVar] = {}

        top = ttk.Frame(self)
        top.pack(fill="x", padx=10, pady=10)

        ttk.Label(top, text="Filter:").pack(side="left")
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(top, textvariable=self.search_var)
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(5, 10))
        self.search_entry.bind("<KeyRelease>", self.on_filter_changed)

        self.refresh_button = ttk.Button(
            top, text="Refresh", command=self.refresh_templates
        )
        self.refresh_button.pack(side="left", padx=(0, 5))

        self.select_all_button = ttk.Button(
            top, text="Select all (filtered)", command=self.select_all_filtered
        )
        self.select_all_button.pack(side="left", padx=(0, 5))

        self.clear_all_button = ttk.Button(
            top, text="Clear all", command=self.clear_all
        )
        self.clear_all_button.pack(side="left")

        self.generate_button = ttk.Button(
            top, text="Generate .gitignore", command=self.generate_gitignore
        )
        self.generate_button.pack(side="right")

        main = ttk.Panedwindow(self, orient="horizontal")
        main.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        left = ttk.Frame(main)
        main.add(left, weight=3)

        ttk.Label(left, text="All templates").pack(anchor="w", padx=5, pady=(5, 0))

        self.left_canvas = tk.Canvas(left)
        self.left_canvas.pack(
            side="left", fill="both", expand=True, padx=(5, 0), pady=5
        )

        left_scroll = ttk.Scrollbar(
            left, orient="vertical", command=self.left_canvas.yview
        )
        left_scroll.pack(side="right", fill="y", padx=(0, 5), pady=5)

        self.left_canvas.configure(yscrollcommand=left_scroll.set)
        self.left_canvas.bind(
            "<Configure>",
            lambda e: self.left_canvas.configure(
                scrollregion=self.left_canvas.bbox("all")
            ),
        )

        self.left_inner = ttk.Frame(self.left_canvas)
        self.left_canvas.create_window((0, 0), window=self.left_inner, anchor="nw")

        right = ttk.Frame(main)
        main.add(right, weight=2)

        ttk.Label(right, text="Selected templates").pack(
            anchor="w", padx=5, pady=(5, 0)
        )

        self.selected_list = tk.Listbox(right, height=10)
        self.selected_list.pack(fill="both", expand=True, padx=5, pady=5)

        right_btns = ttk.Frame(right)
        right_btns.pack(fill="x", padx=5, pady=(0, 5))

        ttk.Button(
            right_btns, text="Remove selected", command=self.remove_selected_from_right
        ).pack(side="left")
        ttk.Button(right_btns, text="Clear selected", command=self.clear_all).pack(
            side="left", padx=(5, 0)
        )

        self.refresh_templates()

    def refresh_templates(self):
        try:
            self.templates_index = build_templates_index()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch template index:\n{e}")
            return

        for child in self.left_inner.winfo_children():
            child.destroy()

        for name in sorted(self.templates_index.keys(), key=str.lower):
            if name not in self.template_vars:
                self.template_vars[name] = tk.BooleanVar(value=False)

        self.search_var.set("")
        self.render_left_list()
        self.sync_selected_right()

    def render_left_list(self):
        for child in self.left_inner.winfo_children():
            child.destroy()

        keyword = self.search_var.get().strip().lower()

        for name in sorted(self.templates_index.keys(), key=str.lower):
            if keyword and keyword not in name.lower():
                continue

            var = self.template_vars[name]
            cb = ttk.Checkbutton(
                self.left_inner,
                text=name,
                variable=var,
                command=self.sync_selected_right,
            )
            cb.pack(anchor="w", padx=5, pady=1)

    def on_filter_changed(self, event=None):
        self.render_left_list()

    def sync_selected_right(self):
        selected = [name for name, var in self.template_vars.items() if var.get()]
        selected.sort(key=str.lower)

        self.selected_list.delete(0, tk.END)
        for name in selected:
            self.selected_list.insert(tk.END, name)

    def select_all_filtered(self):
        keyword = self.search_var.get().strip().lower()
        for name, var in self.template_vars.items():
            if not keyword or keyword in name.lower():
                var.set(True)
        self.sync_selected_right()
        self.render_left_list()

    def clear_all(self):
        for var in self.template_vars.values():
            var.set(False)
        self.sync_selected_right()
        self.render_left_list()

    def remove_selected_from_right(self):
        indices = list(self.selected_list.curselection())
        if not indices:
            return

        names = [self.selected_list.get(i) for i in indices]
        for name in names:
            if name in self.template_vars:
                self.template_vars[name].set(False)

        self.sync_selected_right()
        self.render_left_list()

    def generate_gitignore(self):
        selected_names = [name for name, var in self.template_vars.items() if var.get()]
        if not selected_names:
            messagebox.showwarning(
                "No selection", "Please select at least one template."
            )
            return

        file_path = filedialog.asksaveasfilename(
            title="Save .gitignore",
            initialfile=".gitignore",
            defaultextension="",
            filetypes=[("gitignore", ".gitignore"), ("All files", "*.*")],
        )
        if not file_path:
            return

        try:
            paths = [self.templates_index[name] for name in selected_names]
            merged_text = merge_gitignores_from_paths(paths, dedup=True)
            with open(file_path, "w", encoding="utf-8", newline="\n") as f:
                f.write(merged_text)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate .gitignore:\n{e}")
            return

        messagebox.showinfo("Success", f".gitignore generated at:\n{file_path}")


def main():
    app = GitignoreGUI()
    app.minsize(900, 600)
    app.mainloop()


if __name__ == "__main__":
    main()
