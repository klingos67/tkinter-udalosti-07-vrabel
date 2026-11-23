import tkinter as tk


class PresuvanieTvarovApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Téma 7: Presúvanie tvarov (Tkinter)")
        self.root.geometry("820x560")
        self.root.minsize(640, 440)

        self.spawn_mode = "circle"
        self.dragged_item = None
        self.last_x = 0
        self.last_y = 0
        self.created_count = 0

        self._build_ui()

    def _build_ui(self) -> None:
        self.controls_frame = tk.Frame(self.root, padx=8, pady=6)
        self.controls_frame.pack(fill=tk.X)

        self.guide_label = tk.Label(
            self.root,
            text=(
                "Ovládanie: Ľavé tlačidlo + ťahanie = presun tvaru | "
                "Pravé tlačidlo na tvar = zmaže tvar | "
                "Dvojklik = pridá tvar | Klávesy: C (kruh), S (štvorec), Space, Delete"
            ),
            anchor="w",
            padx=10,
            pady=4,
            wraplength=790,
            justify=tk.LEFT,
        )
        self.guide_label.pack(fill=tk.X)

        self.canvas = tk.Canvas(
            self.root,
            bg="#18221d",
            highlightthickness=1,
            highlightbackground="#2e473b",
        )
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=8, pady=(0, 6))

        self.status_label = tk.Label(
            self.root,
            text="Stav: Pripravené | Režim: Kruh",
            anchor="w",
            padx=10,
            pady=4,
        )
        self.status_label.pack(fill=tk.X)

    def _update_status(self, message: str) -> None:
        rezim = "Kruh" if self.spawn_mode == "circle" else "Štvorec"
        self.status_label.config(text=f"Stav: {message} | Režim: {rezim}")


def main() -> None:
    root = tk.Tk()
    PresuvanieTvarovApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()