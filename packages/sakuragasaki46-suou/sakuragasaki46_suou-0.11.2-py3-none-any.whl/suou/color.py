"""
Colors for coding artists

*New in 0.7.0*

---

Copyright (c) 2025 Sakuragasaki46.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
See LICENSE for the specific language governing permissions and
limitations under the License.

This software is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.

"""

from __future__ import annotations

from collections import namedtuple
from functools import lru_cache


class Chalk:
    """
    ANSI escape codes for terminal colors, similar to JavaScript's `chalk` library.

    Best used with Python 3.12+ that allows arbitrary nesting of f-strings.

    Yes, I am aware colorama exists.

    UNTESTED

    *New in 0.7.0*
    """
    CSI = '\x1b['
    RED = CSI + "31m"
    GREEN = CSI + "32m"
    YELLOW = CSI + "33m"
    BLUE = CSI + "34m"
    CYAN = CSI + "36m"
    PURPLE = CSI + "35m" 
    GREY = CSI + "90m"
    END_COLOR = CSI + "39m"
    BOLD = CSI + "1m"
    END_BOLD = CSI + "22m"
    FAINT = CSI + "2m"
    def __init__(self, flags = (), ends = ()):
        self._flags = tuple(flags)
        self._ends = tuple(ends)
    @lru_cache()
    def _wrap(self, beg, end):
        return Chalk(self._flags + (beg,), self._ends + (end,))
    def __call__(self, s: str) -> str:
        return ''.join(self._flags) + s + ''.join(reversed(self._ends))
    @property
    def red(self):
        return self._wrap(self.RED, self.END_COLOR)
    @property
    def green(self):
        return self._wrap(self.GREEN, self.END_COLOR)
    @property
    def blue(self):
        return self._wrap(self.BLUE, self.END_COLOR)
    @property
    def yellow(self):
        return self._wrap(self.YELLOW, self.END_COLOR)
    @property
    def cyan(self):
        return self._wrap(self.CYAN, self.END_COLOR)
    @property
    def purple(self):
        return self._wrap(self.PURPLE, self.END_COLOR)
    @property
    def grey(self):
        return self._wrap(self.GREY, self.END_COLOR)
    gray = grey
    marine = blue
    magenta = purple
    @property
    def bold(self):
        return self._wrap(self.BOLD, self.END_BOLD)
    @property
    def faint(self):
        return self._wrap(self.FAINT, self.END_BOLD)


## TODO make it lazy / an instance variable?
chalk = Chalk()


## Utilities for web colors

class WebColor(namedtuple('_WebColor', 'red green blue')):
    """
    Representation of a color in the TrueColor space (aka rgb).

    Useful for theming.
    """
    def lighten(self, *, factor = .75):
        """
        Return a whitened shade of the color.
        Factor stands between 0 and 1: 0 = total white, 1 = no change. Default is .75
        """
        return WebColor(
            255 - int((255 - self.red) * factor),
            255 - int((255 - self.green) * factor),
            255 - int((255 - self.blue) * factor),
        )
    def darken(self, *, factor = .75):
        """
        Return a darkened shade of the color.
        Factor stands between 0 and 1: 0 = total black, 1 = no change. Default is .75
        """
        return WebColor(
            int(self.red * factor),
            int(self.green * factor),
            int(self.blue * factor)
        )
    def greyen(self, *, factor = .75):
        """
        Return a desaturated shade of the color.
        Factor stands between 0 and 1: 0 = gray, 1 = no change. Default is .75
        """
        return self.darken(factor=factor) + self.lighten(factor=factor)
        
    def blend_with(self, other: WebColor):
        """
        Mix two colors, returning the average.
        """
        return WebColor (
            (self.red + other.red) // 2,
            (self.green + other.green) // 2,
            (self.blue + other.blue) // 2
        )

    __add__ = blend_with

    def __str__(self):
        return f"rgb({self.red}, {self.green}, {self.blue})"


__all__ = ('chalk', 'WebColor')

