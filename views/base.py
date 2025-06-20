import tkinter as tk
from tkinter import ttk, messagebox
from .style import STYLE

class BaseTab(ttk.Frame):
    """قالب موحّد لكل التبويبات—يطبّق القيم من STYLE."""

    def __init__(self, parent, *services, **kwargs):
        super().__init__(parent, **kwargs)
        self.configure(style="TFrame")  # خلفية موحّدة
        self.services = services
        self._create_widgets()

    def _create_widgets(self):
        raise NotImplementedError

    # نافذة رسائل منبثقة
    def flash(self, msg, title="تنبيه", kind="info"):
        func = getattr(messagebox, kind)
        func(title, msg)
