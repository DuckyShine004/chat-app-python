import os
import time
import functools

from PySide6.QtGui import QFontMetrics


class Utility:
    @staticmethod
    def get_path(path, extended_path=None):
        new_path = list(path)

        if extended_path is not None:
            new_path.extend(extended_path)

        return os.path.join(*new_path)

    @staticmethod
    def load_file_data(path):
        data = None

        with open(path, "r", encoding="utf-8") as file:
            data = file.read()

        return data

    @staticmethod
    def get_wrapped_text(text, font, max_width):
        font_metrics = QFontMetrics(font)

        wrapped_text = ""
        line = ""

        for char in text:
            if font_metrics.horizontalAdvance(line + char) > max_width:
                wrapped_text += line + "\n"
                line = char
            else:
                line += char

        wrapped_text += line

        return wrapped_text

    @staticmethod
    def timed_event():
        def decorator(func):

            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                start_time = time.time()
                result = func(*args, **kwargs)
                end_time = time.time()

                elapsed_time = end_time - start_time

                return elapsed_time

            return wrapper

        return decorator
