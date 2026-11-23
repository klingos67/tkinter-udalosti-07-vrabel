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
        self._bind_events()
        self._spawn_initial_shapes()

    def _build_ui(self) -> None:
        top_frame = tk.Frame(self.root, padx=8, pady=6)
        top_frame.pack(fill=tk.X)

        self.btn_mode_circle = tk.Button(
            top_frame,
            text="Režim: Kruh (C)",
            command=lambda: self.set_spawn_mode("circle"),
        )
        self.btn_mode_circle.pack(side=tk.LEFT, padx=(0, 6))

        self.btn_mode_square = tk.Button(
            top_frame,
            text="Režim: Štvorec (S)",
            command=lambda: self.set_spawn_mode("square"),
        )
        self.btn_mode_square.pack(side=tk.LEFT, padx=(0, 6))

        self.btn_add_center = tk.Button(
            top_frame,
            text="Pridať do stredu (Space)",
            command=self.add_shape_center,
        )
        self.btn_add_center.pack(side=tk.LEFT, padx=(0, 6))

        self.btn_clear = tk.Button(
            top_frame,
            text="Zmazať všetko (Delete)",
            command=self.clear_canvas,
        )
        self.btn_clear.pack(side=tk.LEFT)

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

    def _bind_events(self) -> None:
        self.canvas.bind("<ButtonPress-1>", self.on_left_press)
        self.canvas.bind("<B1-Motion>", self.on_left_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_left_release)
        self.canvas.bind("<Double-Button-1>", self.on_double_click)
        self.canvas.bind("<ButtonPress-3>", self.on_right_click)
        self.canvas.bind("<ButtonPress-2>", self.on_right_click)
        self.root.bind("<KeyPress>", self.on_key_press)

    def _spawn_initial_shapes(self) -> None:
        self._create_shape(180, 180, shape_type="circle", fill="#2ecc71")
        self._create_shape(360, 210, shape_type="square", fill="#27ae60")
        self._update_status("Načítané ukážkové tvary. Skús ich potiahnuť alebo zmazať pravým klikom.")

    def _create_shape(self, x: int, y: int, shape_type: str | None = None, fill: str | None = None) -> int:
        kind = shape_type if shape_type in ("circle", "square") else self.spawn_mode
        radius = 36
        palette_circles = ["#2ecc71", "#1abc9c", "#3498db", "#58d68d"]
        palette_squares = ["#27ae60", "#16a085", "#2980b9", "#52be80"]

        if fill is None:
            pool = palette_circles if kind == "circle" else palette_squares
            fill = pool[self.created_count % len(pool)]

        if kind == "circle":
            item_id = self.canvas.create_oval(
                x - radius,
                y - radius,
                x + radius,
                y + radius,
                fill=fill,
                outline="#e8f8f5",
                width=2,
                tags=("movable_shape", "circle"),
            )
        else:
            item_id = self.canvas.create_rectangle(
                x - radius,
                y - radius,
                x + radius,
                y + radius,
                fill=fill,
                outline="#e8f8f5",
                width=2,
                tags=("movable_shape", "square"),
            )

        self.created_count += 1
        return item_id

    def _find_top_shape_at(self, x: int, y: int) -> int | None:
        overlapping = self.canvas.find_overlapping(x, y, x, y)
        for item_id in reversed(overlapping):
            if "movable_shape" in self.canvas.gettags(item_id):
                return item_id
        return None

    def set_spawn_mode(self, mode: str) -> None:
        if mode in ("circle", "square"):
            self.spawn_mode = mode
            nazov = "Kruh" if mode == "circle" else "Štvorec"
            self._update_status(f"Zmenený režim pridávania tvarov na: {nazov}")

    def add_shape_center(self) -> None:
        try:
            w = max(self.canvas.winfo_width(), 200)
            h = max(self.canvas.winfo_height(), 200)
            cx, cy = w // 2, h // 2
            item_id = self._create_shape(cx, cy)
            self._update_status(f"Pridaný tvar #{item_id} do stredu plátna ({cx}, {cy}).")
        except Exception as exc:
            self._update_status(f"Upozornenie pri pridávaní tvaru: {exc}")

    def clear_canvas(self) -> None:
        try:
            self.canvas.delete("movable_shape")
            self.dragged_item = None
            self._update_status("Všetky tvary boli vymazané.")
        except Exception as exc:
            self._update_status(f"Upozornenie pri mazaní plátna: {exc}")

    # Callback 1: Reaguje na stlačenie ľavého tlačidla myši (<ButtonPress-1>) na plátne
    def on_left_press(self, event: tk.Event) -> None:
        try:
            x, y = event.x, event.y
            target = self._find_top_shape_at(x, y)
            if target is not None:
                self.dragged_item = target
                self.last_x = x
                self.last_y = y
                self.canvas.tag_raise(self.dragged_item)
                self._update_status(f"Presúvam tvar #{self.dragged_item} na súradniciach ({x}, {y}).")
            else:
                self.dragged_item = None
                self._update_status(f"Kliknutie na prázdne miesto ({x}, {y}). Dvojklik pridá nový tvar.")
        except Exception as exc:
            self.dragged_item = None
            self._update_status(f"Ošetrená chyba pri kliknutí: {exc}")

    # Callback 2: Reaguje na ťahanie myšou so stlačeným ľavým tlačidlom (<B1-Motion>)
    def on_left_drag(self, event: tk.Event) -> None:
        try:
            if self.dragged_item is None:
                return
            x, y = event.x, event.y
            dx = x - self.last_x
            dy = y - self.last_y
            self.canvas.move(self.dragged_item, dx, dy)
            self.last_x = x
            self.last_y = y
            self._update_status(f"Tvar #{self.dragged_item} -> pozícia ({x}, {y}).")
        except Exception as exc:
            self.dragged_item = None
            self._update_status(f"Ošetrená chyba pri presúvaní: {exc}")

    # Callback 3: Reaguje na uvoľnenie ľavého tlačidla myši (<ButtonRelease-1>)
    def on_left_release(self, event: tk.Event) -> None:
        try:
            if self.dragged_item is not None:
                released_id = self.dragged_item
                self.dragged_item = None
                self._update_status(f"Uložená pozícia tvaru #{released_id} na ({event.x}, {event.y}).")
        except Exception as exc:
            self.dragged_item = None
            self._update_status(f"Ošetrená chyba pri uvoľnení tlačidla: {exc}")

    # Callback 4: Reaguje na kliknutie pravým tlačidlom myši (<ButtonPress-3> / <ButtonPress-2>) – maže tvar
    def on_right_click(self, event: tk.Event) -> None:
        try:
            x, y = event.x, event.y
            target = self._find_top_shape_at(x, y)
            if target is not None:
                if self.dragged_item == target:
                    self.dragged_item = None
                self.canvas.delete(target)
                self._update_status(f"Zmazaný tvar #{target} na súradniciach ({x}, {y}).")
            else:
                self._update_status(f"Pravý klik na ({x}, {y}) – pod kurzorom nie je žiadny tvar.")
        except Exception as exc:
            self._update_status(f"Ošetrená chyba pri mazaní tvaru: {exc}")

    # Callback 5: Reaguje na dvojklik ľavým tlačidlom myši (<Double-Button-1>) – pridá nový tvar
    def on_double_click(self, event: tk.Event) -> None:
        try:
            x, y = event.x, event.y
            item_id = self._create_shape(x, y)
            self._update_status(f"Pridaný nový tvar #{item_id} na ({x}, {y}).")
        except Exception as exc:
            self._update_status(f"Ošetrená chyba pri pridávaní tvaru: {exc}")

    # Callback 6: Reaguje na stlačenie ľubovoľnej klávesy (<KeyPress>) na okne
    def on_key_press(self, event: tk.Event) -> None:
        try:
            key = (event.keysym or "").lower()
            if key == "c":
                self.set_spawn_mode("circle")
            elif key == "s":
                self.set_spawn_mode("square")
            elif key == "space":
                self.add_shape_center()
            elif key in ("delete", "backspace"):
                self.clear_canvas()
            else:
                self._update_status(f"Stlačený kláves '{event.keysym}' (bez priradenej akcie).")
        except Exception as exc:
            self._update_status(f"Ošetrená chyba pri spracovaní klávesy: {exc}")

    def _update_status(self, message: str) -> None:
        rezim = "Kruh" if self.spawn_mode == "circle" else "Štvorec"
        self.status_label.config(text=f"Stav: {message} | Režim: {rezim}")


def main() -> None:
    root = tk.Tk()
    PresuvanieTvarovApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()