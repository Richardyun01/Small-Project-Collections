import random
from PIL import Image, ImageTk

from sorter import get_sort_generator


class ImageSorterModel:
    def __init__(self, num_slices=50):
        self.num_slices = num_slices
        self.image = None
        self.width = 0
        self.height = 0
        self.slice_width = 0
        self.strips = []
        self._sort_generator = None
        self.sort_method = "Bubble"

    def set_sort_method(self, name: str):
        self.sort_method = name

    def load_image(self, path):
        self.image = Image.open(path).convert("RGB")
        self.width, self.height = self.image.size

        self.slice_width = max(1, self.width // self.num_slices)
        self.num_slices = self.width // self.slice_width

        self.strips = []
        for i in range(self.num_slices):
            left = i * self.slice_width
            right = left + self.slice_width
            crop = self.image.crop((left, 0, right, self.height))
            tk_img = ImageTk.PhotoImage(crop)
            self.strips.append(
                {
                    "tk_image": tk_img,
                    "original_index": i,
                    "x": i * self.slice_width,
                }
            )

        random.shuffle(self.strips)
        self._update_positions()
        self._sort_generator = None

    def create_sort_generator(self):
        if not self.strips:
            return None

        self._sort_generator = get_sort_generator(
            self.sort_method, self.strips, key=lambda s: s["original_index"]
        )
        return self._sort_generator

    def step_sort(self):
        if self._sort_generator is None:
            self.create_sort_generator()

        try:
            next(self._sort_generator)
            self._update_positions()
            return True
        except StopIteration:
            self._sort_generator = None
            self._update_positions()
            return False

    def _update_positions(self):
        for idx, strip in enumerate(self.strips):
            strip["x"] = idx * self.slice_width

    def get_canvas_size(self):
        return self.width, self.height

    def get_strips_for_draw(self):
        return self.strips

    def create_sort_generator(self):
        if not self.strips:
            return None
        self._sort_generator = get_sort_generator(
            self.sort_method, self.strips, key=lambda s: s["original_index"]
        )
        return self._sort_generator

    def step_sort(self):
        if self._sort_generator is None:
            self.create_sort_generator()

        try:
            next(self._sort_generator)
            self._update_positions()
            return True
        except StopIteration:
            self._sort_generator = None
            self._update_positions()
            return False

    def shuffle_again(self):
        if not self.strips:
            return

        random.shuffle(self.strips)
        self._update_positions()
        self._sort_generator = None
