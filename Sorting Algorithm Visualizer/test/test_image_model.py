import unittest
import tempfile
from pathlib import Path
import tkinter as tk

from PIL import Image

from image_model import ImageSorterModel


class TestImageSorterModel(unittest.TestCase):
    def setUp(self):
        # Tk 루트 생성 (ImageTk.PhotoImage가 사용할 기본 root)
        try:
            self.root = tk.Tk()
            self.root.withdraw()  # 테스트 중에는 창 안 보이게 숨김
        except tk.TclError:
            self.root = None
            self.skipTest("Tkinter GUI not available in this environment")

        # 임시 이미지 파일 생성
        self.temp_dir = tempfile.TemporaryDirectory()
        self.image_path = Path(self.temp_dir.name) / "test_image.png"

        img = Image.new("RGB", (200, 100), color=(123, 222, 111))
        img.save(self.image_path)

    def tearDown(self):
        # 임시 디렉토리 정리
        self.temp_dir.cleanup()
        # Tk 루트 정리
        if self.root is not None:
            self.root.destroy()

    def test_load_image_and_slices(self):
        model = ImageSorterModel(num_slices=10)
        model.load_image(str(self.image_path))

        w, h = model.get_canvas_size()
        self.assertEqual((w, h), (200, 100))

        strips = model.get_strips_for_draw()
        self.assertEqual(len(strips), model.num_slices)

        indices = sorted(s["original_index"] for s in strips)
        self.assertEqual(indices, list(range(model.num_slices)))

    def test_sort_restores_original_order(self):
        model = ImageSorterModel(num_slices=10)
        model.load_image(str(self.image_path))

        model.set_sort_method("Bubble")  # 구현된 정렬 이름 중 하나 사용
        model.create_sort_generator()

        while model.step_sort():
            pass

        indices = [s["original_index"] for s in model.get_strips_for_draw()]
        self.assertEqual(indices, sorted(indices))

    def test_shuffle_again_keeps_same_indices(self):
        model = ImageSorterModel(num_slices=10)
        model.load_image(str(self.image_path))

        model.set_sort_method("Bubble")
        model.create_sort_generator()
        while model.step_sort():
            pass
        sorted_indices = [s["original_index"] for s in model.get_strips_for_draw()]

        model.shuffle_again()
        shuffled_indices = [s["original_index"] for s in model.get_strips_for_draw()]

        self.assertEqual(sorted(sorted_indices), sorted(shuffled_indices))


if __name__ == "__main__":
    unittest.main()
