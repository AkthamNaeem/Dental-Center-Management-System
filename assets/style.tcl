ttk::style theme create clinic_theme -parent clam -settings {
    ttk::style configure TNotebook    -background "#F5F7FA"
    ttk::style configure TFrame       -background "#F5F7FA"
    ttk::style configure TLabel       -background "#F5F7FA" -font "Segoe UI 10"
    ttk::style configure TButton      -padding 6 -font "Segoe UI 10 bold"
    ttk::style map TButton            -background [list active "#2B85D3"  disabled "#AAA"]
}
