import pygetwindow
from abc import ABC

class BasedQuestion(ABC):
    def __init__(self, window: pygetwindow.Win32Window):
        self.window: pygetwindow.Win32Window = window
        self.origin = (self.window.left, self.window.top)
    
    def __call__(self, *args, **kwds):
        pass