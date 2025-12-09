import unittest
import tkinter as tk

from app import ImageSortApp


class TestImageSortApp(unittest.TestCase):
    def test_app_creation_and_destroy(self):
        try:
            root = tk.Tk()
        except tk.TclError:
            self.skipTest("Tkinter GUI not available in this environment")

        app = ImageSortApp(root)
        self.assertIsNotNone(app.canvas)
        self.assertIsNotNone(app.btn_load)
        self.assertIsNotNone(app.btn_sort)
        self.assertIsNotNone(app.btn_shuffle)

        root.update_idletasks()
        root.destroy()


if __name__ == "__main__":
    unittest.main()
