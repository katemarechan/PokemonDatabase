from pathlib import Path
from tkinter import Frame, Canvas, Button, PhotoImage


class FirstGUI(Frame):
    def __init__(self, master=None, switch_callback=None):
        super().__init__(master)
        self.master = master
        self.switch_callback = switch_callback

        # Setup the initial window configuration
        self.master.geometry("600x400")
        self.master.configure(bg="#2A2522")

        # Setup assets path
        self.output_path = Path(__file__).parent
        self.assets_path = self.output_path / Path(r"assets\frame0")

        self.create_widgets()

    def relative_to_assets(self, path: str) -> Path:
        return self.assets_path / Path(path)

    def create_widgets(self):
        # Create and configure the canvas
        self.canvas = Canvas(
            self.master,
            bg="#2A2522",
            height=400,
            width=600,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        # Create bottom rectangle (white background)
        self.canvas.create_rectangle(
            0.0,
            206.0,
            600.0,
            400.0,
            fill="#F7F2F2",
            outline=""
        )

        # Create top rectangle (red background)
        self.canvas.create_rectangle(
            0.0,
            0.0,
            600.0,
            182.0,
            fill="#C01B1B",
            outline=""
        )

        # Create the main black circle
        # Slightly adjust coordinates to ensure pixel-perfect alignment
        circle_size = 100  # diameter
        center_x = 300
        center_y = 193
        radius = circle_size // 2

        self.canvas.create_oval(
            center_x - radius,
            center_y - radius,
            center_x + radius,
            center_y + radius,
            fill="#2A2522",
            outline="#2A2522",  # Match fill color exactly
            width=0  # No outline
        )

        # Create text
        self.canvas.create_text(
            175.0,
            372.0,
            anchor="nw",
            text="Press in the middle to start your journey",
            fill="#1C1512",
            font=("Mohave Regular", 15 * -1)
        )

        # Create circular button
        self.button_image = PhotoImage(
            file=self.relative_to_assets("button_1.png")
        )

        # Create the button with transparent background
        self.button = Button(
            self.master,
            image=self.button_image,
            borderwidth=0,
            highlightthickness=0,
            command=self.switch_callback,
            relief="flat",
            bg="#2A2522",
            activebackground="#2A2522"
        )

        # Center the button in the circle
        button_size = 60
        self.button.place(
            x=center_x - (button_size // 2),
            y=center_y - (button_size // 2),
            width=button_size,
            height=button_size
        )

        self.button.lift()
        self.master.resizable(False, False)

    def destroy(self):
        """Properly destroy all widgets"""
        self.canvas.destroy()
        self.button.destroy()
        super().destroy()