import os
import tkinter as tk
from tkinter import filedialog, messagebox
from pypdf import PdfWriter


class PdfMergerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Merger")

        self.drag_start_index = None

        label = tk.Label(
            root,
            text="Add PDF files and select the order by drag & drop.",
        )
        label.pack(pady=(10, 5))

        list_frame = tk.Frame(root)
        list_frame.pack(padx=10, pady=5, fill="both", expand=True)

        scrollbar = tk.Scrollbar(list_frame, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        self.file_listbox = tk.Listbox(list_frame, selectmode="extended", height=8)
        self.file_listbox.pack(side="left", fill="both", expand=True)
        self.file_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.file_listbox.yview)

        self.file_listbox.bind("<Button-1>", self.on_listbox_click)
        self.file_listbox.bind("<B1-Motion>", self.on_listbox_drag)

        btn_frame = tk.Frame(root)
        btn_frame.pack(padx=10, pady=5, fill="x")

        add_button = tk.Button(btn_frame, text="Add PDF", command=self.add_files)
        add_button.pack(side="left", padx=5)

        remove_button = tk.Button(
            btn_frame, text="Delete Selection", command=self.remove_selected
        )
        remove_button.pack(side="left", padx=5)

        clear_button = tk.Button(btn_frame, text="Erase all", command=self.clear_all)
        clear_button.pack(side="left", padx=5)

        merge_button = tk.Button(root, text="Merge PDF", command=self.merge_pdfs)
        merge_button.pack(pady=(5, 10))

        info_label = tk.Label(root, text="Merge with at least 2 files.")
        info_label.pack(pady=(0, 5))

    # ---------------- Drag & Drop ---------------- #
    def on_listbox_click(self, event):
        self.drag_start_index = self.file_listbox.nearest(event.y)

    def on_listbox_drag(self, event):
        if self.drag_start_index is None:
            return

        new_index = self.file_listbox.nearest(event.y)

        if new_index != self.drag_start_index:
            item = self.file_listbox.get(self.drag_start_index)
            self.file_listbox.delete(self.drag_start_index)
            self.file_listbox.insert(new_index, item)
            self.drag_start_index = new_index

    # ---------------- Manipulate Files ---------------- #
    def add_files(self):
        file_paths = filedialog.askopenfilenames(
            title="Select PDF file", filetypes=[("PDF files", "*.pdf")]
        )
        if not file_paths:
            return

        for path in file_paths:
            if path not in self.file_listbox.get(0, tk.END):
                self.file_listbox.insert(tk.END, path)

    def remove_selected(self):
        selected_indices = list(self.file_listbox.curselection())
        if not selected_indices:
            return
        for index in reversed(selected_indices):
            self.file_listbox.delete(index)

    def clear_all(self):
        self.file_listbox.delete(0, tk.END)

    # ---------------- Merge PDF ----------------
    def merge_pdfs(self):
        pdf_paths = list(self.file_listbox.get(0, tk.END))

        if len(pdf_paths) < 2:
            messagebox.showwarning(
                "WARNING", "You need to upload at least 2 PDF files."
            )
            return

        for path in pdf_paths:
            if not os.path.exists(path):
                messagebox.showerror("ERROR", f"File not in the path:\n{path}")
                return

        out_path = filedialog.asksaveasfilename(
            title="Save Merged PDF As",
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            initialfile="merged.pdf",
        )
        if not out_path:
            return

        try:
            merger = PdfWriter()
            for path in pdf_paths:
                merger.append(path)

            with open(out_path, "wb") as f:
                merger.write(f)

            messagebox.showinfo(
                "COMPLETE", f"PDF merging complete.\n\nSaved path:\n{out_path}"
            )
        except Exception as e:
            messagebox.showerror("ERROR", f"An error occured while merging.\n\n{e}")


if __name__ == "__main__":
    root = tk.Tk()
    root.minsize(600, 550)
    app = PdfMergerApp(root)
    root.mainloop()
