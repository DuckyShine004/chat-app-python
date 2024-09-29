"""This module provides useful global static methods for all classes."""

import os
import time
import functools

from typing import Any, Callable, List, Optional

from PySide6.QtGui import QFont, QFontMetrics


class Utility:
    """Utility class for providing useful global static methods."""

    @staticmethod
    def get_path(path: List[str], extended_path: Optional[List[str]] = None) -> str:
        """Get a converted path based on the OS.

        Args:
            path: a path
            extended_path: an extended path to be added to the path

        Returns: the OS independent path
        """

        copy_path = list(path)

        if extended_path is not None:
            copy_path.extend(extended_path)

        return os.path.join(*copy_path)

    @staticmethod
    def load_file_data(path: str) -> str:
        """Returns the read data from a file.

        Args:
            path: the path to the file

        Returns: the read data
        """

        data = None

        with open(path, "r", encoding="utf-8") as file:
            data = file.read()

        return data

    @staticmethod
    def get_wrapped_text(text: str, font: QFont, max_width: int) -> str:
        """Returns the wrapped text for the original text.

        Args:
            text: the original text
            font: the font that the text uses
            max_width: the width of the text before wrapping

        Returns: the wrapped text of the original text
        """

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
    def timed_event() -> Callable[[Callable[..., Any]], Callable[..., float]]:
        """A decorator factory that creates a decorator to measure the
        execution time of methods.

        Returns: a decorator that wraps a method to measure the execution time
        """

        def decorator(func: Callable[..., Any]) -> Callable[..., float]:
            """Decorator that measures the execution time of the wrapped
            method.

            Args:
                func: the method to be wrapped and executed

            Returns: the wrapped method that returns the elapsed time of the original method
            """

            @functools.wraps(func)
            def wrapper(*args, **kwargs) -> float:
                """Wrapped method that executes the original method and
                measures its execution time.

                Args:
                    *args: variable length argument list for the original method
                    **kwargs: arbitrary keyword arguments for the original method

                Returns: the elapsed time that the original method took to execute
                """

                start_time = time.time()
                func(*args, **kwargs)
                end_time = time.time()

                elapsed_time = end_time - start_time

                return elapsed_time

            return wrapper

        return decorator
