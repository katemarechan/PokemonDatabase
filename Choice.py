from pathlib import Path
from tkinter import Frame, Canvas, Button, PhotoImage


class SecondGUI(Frame):
    def __init__(self, master=None, switch_callback=None):
        super().__init__(master)
        self.master = master
        self.switch_callback = switch_callback

        # Setup the initial window configuration
        self.master.geometry("600x400")
        self.master.configure(bg="#F8EFEF")

        # Setup assets path
        self.output_path = Path(__file__).parent
        self.assets_path = self.output_path / Path(r"assets\frame1")

        self.create_widgets()

    def relative_to_assets(self, path: str) -> Path:
        return self.assets_path / Path(path)

    def create_widgets(self):
        # Create and configure the canvas
        self.canvas = Canvas(
            self.master,
            bg="#F8EFEF",
            height=400,
            width=600,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        # Load and create all images
        self.image_1 = PhotoImage(
            file=self.relative_to_assets("image_1.png"))
        self.canvas.create_image(
            227.0,
            200.0,
            image=self.image_1
        )

        # Create rectangles
        self.canvas.create_rectangle(
            164.0,
            0.0,
            236.0,
            400.0,
            fill="#1E1E1E",
            outline=""
        )

        self.canvas.create_rectangle(
            0.0,
            0.0,
            217.0,
            400.0,
            fill="#C01B1B",
            outline=""
        )

        # Create additional images
        self.image_2 = PhotoImage(
            file=self.relative_to_assets("image_2.png"))
        self.canvas.create_image(
            217.0,
            200.0,
            image=self.image_2
        )

        # Create welcome text
        self.canvas.create_text(
            387.0,
            12.0,
            anchor="nw",
            text="Welcome to ",
            fill="#000000",
            font=("Mohave Regular", 20 * -1)
        )

        self.image_3 = PhotoImage(
            file=self.relative_to_assets("image_3.png"))
        self.canvas.create_image(
            424.0,
            81.0,
            image=self.image_3
        )

        # Create sign in/up text
        self.canvas.create_text(
            344.0,
            207.0,
            anchor="nw",
            text="Sign In",
            fill="#000000",
            font=("Mohave Regular", 15 * -1)
        )

        self.canvas.create_text(
            346.0,
            260.0,
            anchor="nw",
            text="Sign Up",
            fill="#000000",
            font=("Mohave Regular", 15 * -1)
        )

        # Create all buttons with text directly on them
        self.button_1_image = PhotoImage(
            file=self.relative_to_assets("button_1.png"))
        self.button_1 = Button(
            self.master,
            text="Continue without login",
            font=("Mohave Regular", 11),
            fg="black",
            image=self.button_1_image,
            compound="center",
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_1 clicked"),
            relief="flat"
        )
        self.button_1.place(
            x=30.0,
            y=357.0,
            width=170.0,
            height=24.0
        )

        self.button_2_image = PhotoImage(
            file=self.relative_to_assets("button_2.png"))
        self.button_2 = Button(
            self.master,
            image=self.button_2_image,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_2 clicked"),
            relief="flat"
        )
        self.button_2.place(
            x=346.0,
            y=232.0,
            width=170.0,
            height=24.0
        )

        self.button_3_image = PhotoImage(
            file=self.relative_to_assets("button_3.png"))
        self.button_3 = Button(
            self.master,
            image=self.button_3_image,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_3 clicked"),
            relief="flat"
        )
        self.button_3.place(
            x=346.0,
            y=284.0,
            width=170.0,
            height=24.0
        )

        self.master.resizable(False, False)

    def destroy(self):
        """Properly destroy all widgets"""
        self.canvas.destroy()
        self.button_1.destroy()
        self.button_2.destroy()
        self.button_3.destroy()
        super().destroy()


# Example usage
if __name__ == "__main__":
    from tkinter import Tk

    root = Tk()
    app = SecondGUI(root)
    root.mainloop()