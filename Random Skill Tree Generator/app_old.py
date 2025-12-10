# import random
# import matplotlib.pyplot as plt
# from matplotlib.patches import Rectangle

# import tkinter as tk
# from tkinter import ttk, filedialog, messagebox

# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# def generate_levels(start_count, end_count, height, max_width):
#     if start_count < 1:
#         raise ValueError("Starting count to small. Minimum is 1.")
#     if start_count > max_width:
#         raise ValueError("Starting count cannot be larger than max width.")
#     if end_count < 1:
#         raise ValueError("Ending count to small. Minimum is 1.")
#     if end_count > max_width:
#         raise ValueError("Ending count cannot be larger than max width.")
#     if height < 2:
#         raise ValueError("Height to small. Minimum is 2.")
#     if height > 30:
#         raise ValueError("Height to large. Maximum is 30.")
#     if max_width < 1:
#         raise ValueError("Width to small. Minimum is 1.")
#     if max_width > 30:
#         raise ValueError("Width to large. Maximum is 30.")

#     levels = []

#     levels.append([f"L0_N{i}" for i in range(start_count)])

#     for h in range(1, height - 1):
#         count = random.randint(1, max_width)
#         levels.append([f"L{h}_N{i}" for i in range(count)])

#     levels.append([f"L{height - 1}_N{i}" for i in range(end_count)])

#     return levels


# def generate_random_edges(levels, extra_edge_prob=0.3, max_index_diff=None):
#     height = len(levels)

#     parent_count = {}
#     child_count = {}

#     for L, nodes in enumerate(levels):
#         for i in range(len(nodes)):
#             parent_count[(L, i)] = 0
#             child_count[(L, i)] = 0

#     edges = []

#     for L in range(height - 1):
#         num_parents = len(levels[L])
#         num_children = len(levels[L + 1])

#         # 각 부모가 최소 1개의 자식
#         for i in range(num_parents):
#             # 제약을 만족하는 자식 후보 리스트
#             if max_index_diff is not None:
#                 candidate_children = [
#                     j for j in range(num_children) if abs(i - j) <= max_index_diff
#                 ]
#             else:
#                 candidate_children = list(range(num_children))

#             # 만약 제약 때문에 후보가 하나도 없다면, 제약을 잠시 무시하고 전체에서 선택
#             if not candidate_children:
#                 candidate_children = list(range(num_children))

#             j = random.choice(candidate_children)
#             edge = ((L, i), (L + 1, j))
#             edges.append(edge)
#             parent_count[(L + 1, j)] += 1
#             child_count[(L, i)] += 1

#         for j in range(num_children):
#             if parent_count[(L + 1, j)] == 0:
#                 if max_index_diff is not None:
#                     candidate_parents = [
#                         i for i in range(num_parents) if abs(i - j) <= max_index_diff
#                     ]
#                 else:
#                     candidate_parents = list(range(num_parents))

#                 # 제약으로 인해 후보가 없으면 전체 부모에서 선택
#                 if not candidate_parents:
#                     candidate_parents = list(range(num_parents))

#                 i = random.choice(candidate_parents)
#                 edge = ((L, i), (L + 1, j))
#                 edges.append(edge)
#                 parent_count[(L + 1, j)] += 1
#                 child_count[(L, i)] += 1

#         for i in range(num_parents):
#             for j in range(num_children):
#                 # 인덱스 거리 제약 검사
#                 if max_index_diff is not None and abs(i - j) > max_index_diff:
#                     continue

#                 if random.random() < extra_edge_prob:
#                     if ((L, i), (L + 1, j)) not in edges:
#                         edges.append(((L, i), (L + 1, j)))
#                         parent_count[(L + 1, j)] += 1
#                         child_count[(L, i)] += 1

#     return edges


# def compute_positions(
#     levels,
#     node_size=0.6,
#     h_gap=1.8,
#     v_gap=2.0,
#     level_gaps=None,
#     orientation="top_down",
# ):
#     positions = {}

#     if level_gaps is not None:
#         gaps = level_gaps
#     else:
#         gaps = [v_gap] * (len(levels) - 1)

#     if orientation in ("top_down", "bottom_up"):
#         y_levels = [0.0]
#         for g in gaps:
#             if orientation == "top_down":
#                 y_levels.append(y_levels[-1] - g)
#             else:
#                 y_levels.append(y_levels[-1] + g)

#         for L, level_nodes in enumerate(levels):
#             n = len(level_nodes)
#             y = y_levels[L]
#             for i in range(n):
#                 x = (i - (n - 1) / 2) * h_gap
#                 positions[(L, i)] = (x, y)

#     elif orientation == "left_right":
#         x_levels = [0.0]
#         for g in gaps:
#             x_levels.append(x_levels[-1] + g)

#         for L, level_nodes in enumerate(levels):
#             n = len(level_nodes)
#             x = x_levels[L]
#             for i in range(n):
#                 y = (i - (n - 1) / 2) * h_gap
#                 positions[(L, i)] = (x, y)

#     else:
#         raise ValueError(f"Unknown orientation: {orientation}")

#     return positions


# def create_tree_figure(
#     levels,
#     edges,
#     orientation="top_down",
#     fig_width=None,
#     fig_height=None,
# ):
#     num_layers = len(levels)
#     max_width = max(len(lvl) for lvl in levels) if levels else 1

#     complexity = max(num_layers, max_width)
#     spacing_scale = 1.0 + 0.25 * max(complexity - 4, 0)
#     spacing_scale = min(spacing_scale, 4.0)

#     base_node_size = 1.3
#     node_size = base_node_size * min(spacing_scale, 3)

#     base_fontsize = 8
#     fontsize = max(4, int(base_fontsize / spacing_scale))

#     base_h_gap = 1.8
#     base_v_gap = 3.0
#     h_gap = base_h_gap * spacing_scale

#     base_gap = base_v_gap * spacing_scale
#     edge_factor = 0.05 * spacing_scale
#     max_gap = 5.0 * spacing_scale

#     edges_by_layer_count = {(L, L + 1): 0 for L in range(num_layers - 1)}
#     for (L1, i1), (L2, i2) in edges:
#         if L2 == L1 + 1:
#             edges_by_layer_count[(L1, L2)] += 1

#     level_gaps = []
#     for L in range(num_layers - 1):
#         ecount = edges_by_layer_count.get((L, L + 1), 0)
#         gap = base_gap + edge_factor * ecount
#         gap = min(gap, max_gap)
#         level_gaps.append(gap)

#     positions = compute_positions(
#         levels,
#         node_size=node_size,
#         h_gap=h_gap,
#         level_gaps=level_gaps,
#         orientation=orientation,
#     )

#     all_x = [pos[0] for pos in positions.values()]
#     all_y = [pos[1] for pos in positions.values()]

#     span_x = max(all_x) - min(all_x) if all_x else 1.0
#     span_y = max(all_y) - min(all_y) if all_y else 1.0

#     fig_scale = 0.7 * (spacing_scale**0.5)

#     min_w, min_h = 6.0, 4.0
#     max_w, max_h = 30.0, 20.0

#     auto_fig_w = max(min_w, min(max_w, span_x * fig_scale))
#     auto_fig_h = max(min_h, min(max_h, span_y * fig_scale))

#     if fig_width is not None and fig_height is not None:
#         fig_w, fig_h = fig_width, fig_height
#     else:
#         fig_w, fig_h = auto_fig_w, auto_fig_h

#     fig, ax = plt.subplots(figsize=(fig_w, fig_h))

#     for (L, i), (x, y) in positions.items():
#         rect = Rectangle(
#             (x - node_size / 2, y - node_size / 2),
#             node_size,
#             node_size,
#             fill=True,
#             edgecolor="black",
#             linewidth=1.2,
#         )
#         ax.add_patch(rect)
#         ax.text(
#             x,
#             y,
#             f"{L},{i}",
#             ha="center",
#             va="center",
#             fontsize=fontsize,
#         )

#     edges_group = {}
#     for (L1, i1), (L2, i2) in edges:
#         key = (L1, L2)
#         edges_group.setdefault(key, []).append(((L1, i1), (L2, i2)))

#     if orientation in ("top_down", "bottom_up"):
#         vertical_spacing = 0.25 * spacing_scale
#         margin_y = 0.05 * spacing_scale

#         for (L1, L2), edge_list in edges_group.items():
#             m = len(edge_list)

#             for k, ((pL, pi), (cL, ci)) in enumerate(edge_list):
#                 x1, y1 = positions[(pL, pi)]
#                 x2, y2 = positions[(cL, ci)]

#                 y_low, y_high = sorted([y1, y2])
#                 lower_rect_top = y_low + node_size / 2
#                 upper_rect_bottom = y_high - node_size / 2

#                 safe_min_y = lower_rect_top + margin_y
#                 safe_max_y = upper_rect_bottom - margin_y

#                 if safe_min_y >= safe_max_y:
#                     safe_mid = (lower_rect_top + upper_rect_bottom) / 2.0
#                     safe_min_y = safe_mid
#                     safe_max_y = safe_mid

#                 base_mid_y = (y1 + y2) / 2.0
#                 offset = (k - (m - 1) / 2) * vertical_spacing
#                 mid_y = base_mid_y + offset

#                 if mid_y < safe_min_y:
#                     mid_y = safe_min_y
#                 elif mid_y > safe_max_y:
#                     mid_y = safe_max_y

#                 if y2 < y1:
#                     y_start = y1 - node_size / 2
#                     y_end = y2 + node_size / 2
#                 else:
#                     y_start = y1 + node_size / 2
#                     y_end = y2 - node_size / 2

#                 x_start = x1
#                 x_end = x2

#                 x_mid1, y_mid1 = x1, mid_y
#                 x_mid2, y_mid2 = x2, mid_y

#                 ax.plot([x_start, x_mid1], [y_start, y_mid1], linewidth=0.8)
#                 ax.plot([x_mid1, x_mid2], [y_mid1, y_mid2], linewidth=0.8)
#                 ax.plot([x_mid2, x_end], [y_mid2, y_end], linewidth=0.8)

#     elif orientation == "left_right":
#         horizontal_spacing = 0.25 * spacing_scale
#         margin_x = 0.05 * spacing_scale

#         for (L1, L2), edge_list in edges_group.items():
#             m = len(edge_list)

#             for k, ((pL, pi), (cL, ci)) in enumerate(edge_list):
#                 x1, y1 = positions[(pL, pi)]
#                 x2, y2 = positions[(cL, ci)]

#                 parent_right = x1 + node_size / 2
#                 child_left = x2 - node_size / 2

#                 safe_min_x = parent_right + margin_x
#                 safe_max_x = child_left - margin_x

#                 if safe_min_x >= safe_max_x:
#                     safe_mid = (parent_right + child_left) / 2.0
#                     safe_min_x = safe_mid
#                     safe_max_x = safe_mid

#                 base_mid_x = (x1 + x2) / 2.0
#                 offset = (k - (m - 1) / 2) * horizontal_spacing
#                 mid_x = base_mid_x + offset

#                 if mid_x < safe_min_x:
#                     mid_x = safe_min_x
#                 elif mid_x > safe_max_x:
#                     mid_x = safe_max_x

#                 x_start = x1 + node_size / 2
#                 y_start = y1

#                 x_end = x2 - node_size / 2
#                 y_end = y2

#                 x_mid1, y_mid1 = mid_x, y1
#                 x_mid2, y_mid2 = mid_x, y2

#                 ax.plot([x_start, x_mid1], [y_start, y_mid1], linewidth=0.8)
#                 ax.plot([x_mid1, x_mid2], [y_mid1, y_mid2], linewidth=0.8)
#                 ax.plot([x_mid2, x_end], [y_mid2, y_end], linewidth=0.8)
#     else:
#         raise ValueError(f"Unknown orientation: {orientation}")

#     ax.set_aspect("equal")
#     ax.axis("off")

#     margin_units = node_size * (3.0 * spacing_scale)
#     ax.set_xlim(min(all_x) - margin_units, max(all_x) + margin_units)
#     ax.set_ylim(min(all_y) - margin_units, max(all_y) + margin_units)

#     plt.tight_layout()
#     return fig


# def draw_tree(levels, edges, output_file="tree.png", orientation="top_down"):
#     fig = create_tree_figure(levels, edges, orientation=orientation)
#     fig.savefig(output_file, dpi=200)
#     plt.close(fig)


# # ================== Tkinter GUI ================== #
# class TreeGUI:
#     def __init__(self, root):
#         self.root = root
#         root.title("Random Skill Tree Generator")

#         self.current_levels = None
#         self.current_edges = None
#         self.current_orientation = None

#         self.preview_canvas = None

#         container = ttk.Frame(root)
#         container.grid(row=0, column=0, sticky="nsew")
#         root.columnconfigure(0, weight=1)
#         root.rowconfigure(0, weight=1)

#         container.columnconfigure(0, weight=0)
#         container.columnconfigure(1, weight=1)

#         self.preview_size = 400
#         self.preview_frame = ttk.Frame(
#             container,
#             width=self.preview_size,
#             height=self.preview_size,
#             relief="sunken",
#         )
#         self.preview_frame.grid(row=0, column=0, padx=(10, 5), pady=10, sticky="n")
#         self.preview_frame.grid_propagate(False)

#         main = ttk.Frame(container, padding=10)
#         main.grid(row=0, column=1, sticky="nsew")
#         main.columnconfigure(1, weight=1)

#         ttk.Label(main, text="Tree Position").grid(row=0, column=0, sticky="w")

#         self.orientation_var = tk.StringVar(value="top_down")

#         orient_frame = ttk.Frame(main)
#         orient_frame.grid(row=0, column=1, sticky="w")

#         ttk.Radiobutton(
#             orient_frame,
#             text="Top-Down",
#             variable=self.orientation_var,
#             value="top_down",
#         ).pack(side="left")

#         ttk.Radiobutton(
#             orient_frame,
#             text="Bottom-Up",
#             variable=self.orientation_var,
#             value="bottom_up",
#         ).pack(side="left")

#         ttk.Radiobutton(
#             orient_frame,
#             text="Left-Right",
#             variable=self.orientation_var,
#             value="left_right",
#         ).pack(side="left")

#         ttk.Label(main, text="Starting Value (Number of initial nodes)").grid(
#             row=1, column=0, sticky="w"
#         )
#         self.start_var = tk.StringVar(value="3")
#         ttk.Entry(main, textvariable=self.start_var, width=10).grid(row=1, column=1)

#         ttk.Label(main, text="End Value (Number of final nodes)").grid(
#             row=2, column=0, sticky="w"
#         )
#         self.end_var = tk.StringVar(value="3")
#         ttk.Entry(main, textvariable=self.end_var, width=10).grid(row=2, column=1)

#         ttk.Label(main, text="Total Height (Minimum 2, Maximum 30)").grid(
#             row=3, column=0, sticky="w"
#         )
#         self.height_var = tk.StringVar(value="4")
#         ttk.Entry(main, textvariable=self.height_var, width=10).grid(row=3, column=1)

#         ttk.Label(main, text="Max Width (Minimum 1, Maximum 30)").grid(
#             row=4, column=0, sticky="w"
#         )
#         self.width_var = tk.StringVar(value="5")
#         ttk.Entry(main, textvariable=self.width_var, width=10).grid(row=4, column=1)

#         ttk.Label(main, text="Max index distance (optional)").grid(
#             row=5, column=0, sticky="w"
#         )
#         self.max_diff_var = tk.StringVar(value="")
#         ttk.Entry(main, textvariable=self.max_diff_var, width=10).grid(row=5, column=1)

#         preview_btn = ttk.Button(main, text="Preview Tree", command=self.on_preview)
#         preview_btn.grid(row=6, column=0, pady=10, sticky="ew")

#         save_btn = ttk.Button(main, text="Save Tree", command=self.on_save)
#         save_btn.grid(row=6, column=1, pady=10, sticky="ew")

#         self.status_label = ttk.Label(main, text="Ready")
#         self.status_label.grid(row=7, column=0, columnspan=2, sticky="w")

#     def on_preview(self):
#         try:
#             start_count = int(self.start_var.get())
#             end_count = int(self.end_var.get())
#             height = int(self.height_var.get())
#             max_width = int(self.width_var.get())
#         except ValueError:
#             messagebox.showerror("Input Error", "All values must be integer values.")
#             return

#         orientation = self.orientation_var.get()

#         max_diff_str = self.max_diff_var.get().strip()
#         if max_diff_str == "":
#             max_diff = None
#         else:
#             try:
#                 max_diff = int(max_diff_str)
#                 if max_diff < 0:
#                     raise ValueError
#             except ValueError:
#                 messagebox.showerror(
#                     "Input Error",
#                     "Max index distance must be a non-negative integer or left empty.",
#                 )
#                 return

#         try:
#             levels = generate_levels(start_count, end_count, height, max_width)
#             edges = generate_random_edges(levels, max_index_diff=max_diff)
#             fig = create_tree_figure(
#                 levels,
#                 edges,
#                 orientation=orientation,
#                 fig_width=4,
#                 fig_height=4,
#             )
#         except Exception as e:
#             messagebox.showerror(
#                 "ERROR", f"An error occured while generating the tree:\n{e}"
#             )
#             return

#         self.current_levels = levels
#         self.current_edges = edges
#         self.current_orientation = orientation

#         if self.preview_canvas is not None:
#             self.preview_canvas.get_tk_widget().destroy()
#             self.preview_canvas = None

#         self.preview_canvas = FigureCanvasTkAgg(fig, master=self.preview_frame)
#         self.preview_canvas.draw()
#         widget = self.preview_canvas.get_tk_widget()
#         widget.config(width=self.preview_size, height=self.preview_size)
#         widget.pack(fill="both", expand=True)

#         self.status_label.config(text="Preview updated")

#     def on_save(self):
#         if self.current_levels is None or self.current_edges is None:
#             messagebox.showwarning("No Tree", "Please generate a preview first.")
#             return

#         filename = filedialog.asksaveasfilename(
#             title="Save Tree Image",
#             defaultextension=".png",
#             filetypes=[("PNG Image", "*.png"), ("All Files", "*.*")],
#         )
#         if not filename:
#             return

#         try:
#             draw_tree(
#                 self.current_levels,
#                 self.current_edges,
#                 output_file=filename,
#                 orientation=self.current_orientation,
#             )
#         except Exception as e:
#             messagebox.showerror(
#                 "ERROR", f"An error occured while saving the tree:\n{e}"
#             )
#             return

#         self.status_label.config(text=f"Save complete: {filename}")
#         messagebox.showinfo("COMPLETE", f"The tree image have been saved:\n{filename}")


# def main():
#     root = tk.Tk()
#     root.minsize(800, 450)
#     TreeGUI(root)
#     root.mainloop()


# if __name__ == "__main__":
#     main()
