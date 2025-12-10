import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from skill_tree_core import TreeConfig, SkillTree, SkillTreeRenderer


class TreeGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        root.title("Random Skill Tree Generator")

        # 렌더러 (재사용)
        self.renderer = SkillTreeRenderer()

        # 현재 트리 상태
        self.current_tree: SkillTree | None = None
        self.current_orientation: str = "top_down"

        # 미리보기 캔버스
        self.preview_canvas: FigureCanvasTkAgg | None = None
        self.preview_size = 400

        # 레이아웃
        self._build_layout()

    # --------- 레이아웃 구성 --------- #
    def _build_layout(self):
        container = ttk.Frame(self.root)
        container.grid(row=0, column=0, sticky="nsew")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        container.columnconfigure(0, weight=0)
        container.columnconfigure(1, weight=1)

        # 좌측: 미리보기 프레임
        self.preview_frame = ttk.Frame(
            container,
            width=self.preview_size,
            height=self.preview_size,
            relief="sunken",
        )
        self.preview_frame.grid(row=0, column=0, padx=(10, 5), pady=10, sticky="n")
        self.preview_frame.grid_propagate(False)

        # 우측: 컨트롤 UI
        main = ttk.Frame(container, padding=10)
        main.grid(row=0, column=1, sticky="nsew")
        main.columnconfigure(1, weight=1)

        ttk.Label(main, text="Tree Position").grid(row=0, column=0, sticky="w")
        self.orientation_var = tk.StringVar(value="top_down")

        orient_frame = ttk.Frame(main)
        orient_frame.grid(row=0, column=1, sticky="w")

        ttk.Radiobutton(
            orient_frame,
            text="Top-Down",
            variable=self.orientation_var,
            value="top_down",
        ).pack(side="left")

        ttk.Radiobutton(
            orient_frame,
            text="Bottom-Up",
            variable=self.orientation_var,
            value="bottom_up",
        ).pack(side="left")

        ttk.Radiobutton(
            orient_frame,
            text="Left-Right",
            variable=self.orientation_var,
            value="left_right",
        ).pack(side="left")

        ttk.Label(main, text="Starting Value (Number of initial nodes)").grid(
            row=1, column=0, sticky="w"
        )
        self.start_var = tk.StringVar(value="3")
        ttk.Entry(main, textvariable=self.start_var, width=10).grid(row=1, column=1)

        ttk.Label(main, text="End Value (Number of final nodes)").grid(
            row=2, column=0, sticky="w"
        )
        self.end_var = tk.StringVar(value="3")
        ttk.Entry(main, textvariable=self.end_var, width=10).grid(row=2, column=1)

        ttk.Label(main, text="Total Height (Minimum 2, Maximum 30)").grid(
            row=3, column=0, sticky="w"
        )
        self.height_var = tk.StringVar(value="4")
        ttk.Entry(main, textvariable=self.height_var, width=10).grid(row=3, column=1)

        ttk.Label(main, text="Max Width (Minimum 1, Maximum 30)").grid(
            row=4, column=0, sticky="w"
        )
        self.width_var = tk.StringVar(value="5")
        ttk.Entry(main, textvariable=self.width_var, width=10).grid(row=4, column=1)

        ttk.Label(main, text="Max index distance (optional)").grid(
            row=5, column=0, sticky="w"
        )
        self.max_diff_var = tk.StringVar(value="")
        ttk.Entry(main, textvariable=self.max_diff_var, width=10).grid(row=5, column=1)

        preview_btn = ttk.Button(main, text="Preview Tree", command=self.on_preview)
        preview_btn.grid(row=6, column=0, pady=10, sticky="ew")

        save_btn = ttk.Button(main, text="Save Tree", command=self.on_save)
        save_btn.grid(row=6, column=1, pady=10, sticky="ew")

        self.status_label = ttk.Label(main, text="Ready")
        self.status_label.grid(row=7, column=0, columnspan=2, sticky="w")

    # --------- 입력 → TreeConfig 빌드 --------- #
    def _build_config_from_inputs(self) -> TreeConfig | None:
        try:
            start_count = int(self.start_var.get())
            end_count = int(self.end_var.get())
            height = int(self.height_var.get())
            max_width = int(self.width_var.get())
        except ValueError:
            messagebox.showerror("Input Error", "All values must be integer values.")
            return None

        max_diff_str = self.max_diff_var.get().strip()
        if max_diff_str == "":
            max_diff = None
        else:
            try:
                max_diff = int(max_diff_str)
                if max_diff < 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror(
                    "Input Error",
                    "Max index distance must be a non-negative integer or left empty.",
                )
                return None

        config = TreeConfig(
            start_count=start_count,
            end_count=end_count,
            height=height,
            max_width=max_width,
            extra_edge_prob=0.3,
            max_index_diff=max_diff,
        )
        return config

    # --------- 미리보기 버튼 --------- #
    def on_preview(self):
        config = self._build_config_from_inputs()
        if config is None:
            return

        orientation = self.orientation_var.get()

        try:
            tree = SkillTree(config)
            tree.generate()  # levels & edges 생성
            fig = self.renderer.create_figure(
                tree,
                orientation=orientation,
                fig_width=4,
                fig_height=4,
            )
        except Exception as e:
            messagebox.showerror(
                "ERROR", f"An error occured while generating the tree:\n{e}"
            )
            return

        self.current_tree = tree
        self.current_orientation = orientation

        # 이전 미리보기 제거
        if self.preview_canvas is not None:
            self.preview_canvas.get_tk_widget().destroy()
            self.preview_canvas = None

        # 새 미리보기
        self.preview_canvas = FigureCanvasTkAgg(fig, master=self.preview_frame)
        self.preview_canvas.draw()
        widget = self.preview_canvas.get_tk_widget()
        widget.config(width=self.preview_size, height=self.preview_size)
        widget.pack(fill="both", expand=True)

        self.status_label.config(text="Preview updated")

    # --------- 저장 버튼 --------- #
    def on_save(self):
        if self.current_tree is None:
            messagebox.showwarning("No Tree", "Please generate a preview first.")
            return

        filename = filedialog.asksaveasfilename(
            title="Save Tree Image",
            defaultextension=".png",
            filetypes=[("PNG Image", "*.png"), ("All Files", "*.*")],
        )
        if not filename:
            return

        try:
            self.renderer.save_png(
                self.current_tree,
                filename,
                orientation=self.current_orientation,
            )
        except Exception as e:
            messagebox.showerror(
                "ERROR", f"An error occured while saving the tree:\n{e}"
            )
            return

        self.status_label.config(text=f"Save complete: {filename}")
        messagebox.showinfo("COMPLETE", f"The tree image has been saved:\n{filename}")


def main():
    root = tk.Tk()
    root.minsize(800, 450)
    TreeGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
