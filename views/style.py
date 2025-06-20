import tkinter as tk
from tkinter import ttk

# ========================
# مركزيّة قيم التصميم
# ========================
STYLE = {
    # ---------- خطوط ----------
    "font_header": ("Segoe UI", 14, "bold"),   # عناوين رئيسية
    "font_default": ("Segoe UI", 10),            # نصوص افتراضية

    # ---------- ألوان ----------
    "color_bg": "#F5F7FA",       # خلفية عامة
    "color_primary": "#2B85D3",  # لون أساسي للأزرار مثلاً

    # ---------- هوامش ----------
    "pad_x": 15,
    "pad_y": 10,
    "pad_section": 20,            # مسافة قبل/بعد الأقسام الرئيسية

    # ---------- أبعاد النافذة ----------
    "window_width": 1200,
    "window_height": 700,
    "window_min_width": 1024,
    "window_min_height": 600,

    # ---------- حقول الإدخال ----------
    "entry_width": 40,
    "combo_width": 12,

    # ---------- الجداول ----------
    "table_height": 18,
    "table_column_width": {
        "id": 50,
        "default": 200,
        "secondary": 300,
    },
}


def apply_styles(root):
    """تطبيق الثيم العام استنادًا إلى القيم أعلاه (اختياري)."""
    style = ttk.Style(root)
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass

    style.configure("TFrame", background=STYLE["color_bg"])
    style.configure("TLabel", background=STYLE["color_bg"], font=STYLE["font_default"])
    style.configure("Header.TLabel", background=STYLE["color_bg"], font=STYLE["font_header"])
    style.configure("TButton", padding=6, font=STYLE["font_default"])
