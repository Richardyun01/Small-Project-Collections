import tkinter as tk
from tkinter import filedialog, messagebox

from image_model import ImageSorterModel
from sorter import SORT_ALGORITHMS, ALGO_DESCRIPTIONS


PLACEHOLDER_ALGO = "Select Algorithm"
HIDDEN_IMAGE_PATH = "assets/hidden.png"


class ImageSortApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Sorting Visualizer")

        self.model = ImageSorterModel(num_slices=50)

        self.sorting = False
        self.sort_after_id = None

        self.shuffle_easter_count = 0

        self._build_ui()

    def _build_ui(self):
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(main_frame, bg="black")
        self.canvas.pack(
            side=tk.LEFT,
            fill="both",
            expand=True,
            padx=10,
            pady=10,
        )

        right_frame = tk.Frame(main_frame, width=260)
        right_frame.pack(
            side=tk.RIGHT,
            fill="y",
            padx=10,
            pady=10,
        )
        right_frame.pack_propagate(False)

        btn_style = {
            "width": 14,
            "height": 2,
            "font": ("Arial", 11, "bold"),
        }

        tk.Label(
            right_frame, text="Sorting Algorithm:", font=("Arial", 11, "bold")
        ).pack(
            anchor="n",
            pady=(0, 5),
        )

        self.sort_var = tk.StringVar()
        self.sort_var.set(PLACEHOLDER_ALGO)

        algo_options = [PLACEHOLDER_ALGO] + list(SORT_ALGORITHMS.keys())
        self.sort_menu = tk.OptionMenu(right_frame, self.sort_var, *algo_options)
        self.sort_menu.config(width=16, font=("Arial", 11))
        self.sort_menu.pack(fill="x", pady=(0, 15))

        self.sort_var.trace_add("write", self.on_algorithm_change)

        self.btn_load = tk.Button(
            right_frame,
            text="Upload Image",
            command=self.on_load_image,
            **btn_style,
        )
        self.btn_load.pack(fill="x", pady=5)

        self.btn_sort = tk.Button(
            right_frame,
            text="Sorting Start",
            command=self.on_start_sort,
            state=tk.DISABLED,
            **btn_style,
        )
        self.btn_sort.pack(fill="x", pady=5)

        self.btn_shuffle = tk.Button(
            right_frame,
            text="Shuffle Image",
            command=self.on_shuffle,
            # state=tk.DISABLED,
            **btn_style,
        )
        self.btn_shuffle.pack(fill="x", pady=5)

        self.desc_label = tk.Label(
            right_frame,
            text="",
            font=("Arial", 10),
            justify="left",
            anchor="nw",
            wraplength=230,
        )
        self.desc_label.pack(fill="x", pady=(15, 10))

        self.status_label = tk.Label(
            right_frame,
            text="Upload the image.",
            font=("Arial", 10),
            width=30,
            anchor="w",
            justify="left",
            wraplength=250,
        )
        self.status_label.pack(side=tk.BOTTOM, pady=(20, 0), anchor="s")

    # ---------------- Easter Egg ----------------

    def _reset_shuffle_easter(self):
        self.shuffle_easter_count = 0

    def _trigger_shuffle_easter(self):
        self._reset_shuffle_easter()
        try:
            self.model.load_image(HIDDEN_IMAGE_PATH)
        except Exception as e:
            messagebox.showerror(
                "ERROR", f"An error occurred while loading an image:\n{e}"
            )
            return

        w, h = self.model.get_canvas_size()
        self.canvas.config(width=w, height=h)
        self._draw_image()

        self.btn_sort.config(state=tk.NORMAL)
        self.status_label.config(
            text="You've discovered the hidden image! Select an algorithm and press 'Sorting Start'."
        )

    # ---------------- Event Handler ----------------

    def on_algorithm_change(self, *args):
        self._reset_shuffle_easter()

        name = self.sort_var.get()
        if name in ALGO_DESCRIPTIONS:
            self.desc_label.config(text=ALGO_DESCRIPTIONS[name])
        else:
            self.desc_label.config(text="")

    def on_load_image(self):
        self._reset_shuffle_easter()

        filetypes = [
            ("Image files", "*.png *.jpg *.jpeg *.bmp *.gif"),
            ("All files", "*.*"),
        ]
        path = filedialog.askopenfilename(title="Choose Image", filetypes=filetypes)
        if not path:
            return

        self._cancel_sort_animation()

        try:
            self.model.load_image(path)
        except Exception as e:
            messagebox.showerror(
                "ERROR", f"An error occurred while loading an image:\n{e}"
            )
            return

        w, h = self.model.get_canvas_size()
        self.canvas.config(width=w, height=h)

        self._draw_image()

        self.btn_sort.config(state=tk.NORMAL)
        self.btn_shuffle.config(state=tk.NORMAL)
        self.status_label.config(
            text="The image is mixed. Select an algorithm and press 'Sorting Start'."
        )
        self.sorting = False

    def on_start_sort(self):
        self._reset_shuffle_easter()

        if self.sorting:
            return

        if not self.model.strips:
            messagebox.showinfo("WARNING", "Upload an image first.")
            return

        selected_algorithm = self.sort_var.get()

        if selected_algorithm not in SORT_ALGORITHMS:
            messagebox.showinfo("WARNING", "Choose a sorting algorithm first.")
            return

        self.model.set_sort_method(selected_algorithm)

        self.status_label.config(text=f"{selected_algorithm} Sorting...")
        self.sorting = True

        self.model.create_sort_generator()
        self._schedule_next_sort_step()

    def on_shuffle(self):
        if not self.model.strips:
            self.shuffle_easter_count += 1

            if self.shuffle_easter_count >= 15:
                self._trigger_shuffle_easter()
            return

        self._reset_shuffle_easter()

        if not self.model.strips:
            return

        self._cancel_sort_animation()

        self.model.shuffle_again()
        self._draw_image()

        self.status_label.config(
            text="The image is mixed. Select an algorithm and press 'Sorting Start'."
        )

    # ---------------- Sort Animation Loop ----------------

    def _schedule_next_sort_step(self):
        if not self.sorting:
            return

        still_sorting = self.model.step_sort()
        self._draw_image()

        if still_sorting:
            self.sort_after_id = self.root.after(10, self._schedule_next_sort_step)
        else:
            self.sorting = False
            self.sort_after_id = None
            self.status_label.config(text="Sorting Complete!")

    def _cancel_sort_animation(self):
        self.sorting = False
        if self.sort_after_id is not None:
            self.root.after_cancel(self.sort_after_id)
            self.sort_after_id = None

    # ---------------- Draw Canvas ----------------

    def _draw_image(self):
        self.canvas.delete("all")
        for strip in self.model.get_strips_for_draw():
            self.canvas.create_image(
                strip["x"], 0, anchor="nw", image=strip["tk_image"]
            )


def main():
    root = tk.Tk()
    app = ImageSortApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
