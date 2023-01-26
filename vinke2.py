import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Image Viewer")

        # Create the "Select File" button
        select_file_button = tk.Button(self, text="Select File", command=self.select_file)
        select_file_button.pack(side=tk.TOP, anchor=tk.W)

        # Create the "Generate" button
        generate_button = tk.Button(self, text="Generate", command=self.generate)
        generate_button.pack(side=tk.TOP, anchor=tk.W)

        # Create the canvas for displaying the image
        self.canvas1 = tk.Canvas(self, width=800, height=800)
        self.canvas1.pack(side=tk.LEFT)
        self.canvas2 = tk.Canvas(self, width=800, height=800)
        self.canvas2.pack(side=tk.RIGHT)

        

    def select_file(self):
        # Open a file dialog to select an image file
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.png")])

        # Check if a file was selected
        if file_path:
            # Load the image and display it on the canvas
            image = Image.open(file_path)
            image = self.resize_image(image)
            self.display_image(image, self.canvas1)

    def generate(self):
        # Get the image on the first canvas
        image = self.get_image_on_canvas(self.canvas1)

        # Invert the colors of the image
        image = image.point(lambda x: 255 - x)

        # Display the inverted image on the second canvas
        self.display_image(image, self.canvas2)

    def display_image(self, image, canvas):
        # Convert the image to a PhotoImage object
        image = ImageTk.PhotoImage(image)

        # Calculate the center coordinates of the canvas
        center_x = canvas.winfo_width() // 2
        center_y = canvas.winfo_height() // 2

        # Display the image on the canvas
        canvas.create_image(center_x, center_y, image=image, anchor=tk.CENTER)

        # Save a reference to the image to prevent it from being garbage collected
        canvas.image = image

    def get_image_on_canvas(self, canvas):
        # Get the list of items on the canvas
        items = canvas.find_all()

        # Check if there is an image on the canvas
        if not items:
            messagebox.showerror("Error", "No image to copy")
            return

        # Get the image from the canvas
        image = canvas.image

        return image

    def resize_image(self, image):
        # Check if the image is larger than the canvas
        if image.width > 800 or image.height > 800:
            # Calculate the new size of the image to fit the canvas
            width_ratio = 800 / image.width
            height_ratio = 800 / image.height
            resize_ratio = min(width_ratio, height_ratio)
            new_size = (int(image.width * resize_ratio), int(image.height * resize_ratio))
            # Resize the image
            image = image.resize(new_size, resample=Image.LANCZOS)

        return image

if __name__ == '__main__':
    app = App()
    app.mainloop()
