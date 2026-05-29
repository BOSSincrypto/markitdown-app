import sys
import os


def main():
    # Magika ONNX: prefer pure-Python backend in frozen builds
    if getattr(sys, "frozen", False):
        os.environ.setdefault("MAGIKA_USE_PYTHON", "1")

    from .ui import MainWindow

    window = MainWindow()
    window.mainloop()


if __name__ == "__main__":
    main()
