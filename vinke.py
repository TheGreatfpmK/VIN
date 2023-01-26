import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os
import time

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Vinke")
        
        self.minsize(1250, 900)

        self.option = tk.StringVar(self)
        self.options = ["Grid", "Columns", "Rows", "Noise", "Noise2", "Noise3", "Splice", "Weird Repeat", "Squares"]
        self.option.set(self.options[0])
        self.value = tk.IntVar(self)
        self.values = list(range(2,21))
        self.value.set(self.values[3])

        select_file_button1 = tk.Button(self, text="Select Image #1", command=self.select_file)
        select_file_button1.grid(row=0,column=0, sticky=tk.N,padx=10, pady=10)

        select_file_button2 = tk.Button(self, text="Select Image #2", command=self.select_file2)
        select_file_button2.grid(row=0,column=1, sticky=tk.N,padx=10, pady=10)

        option_menu = tk.OptionMenu(self, self.option, *self.options)
        option_menu.grid(row=0,column=2, sticky=tk.N,padx=10, pady=10)

        value_menu = tk.OptionMenu(self, self.value, *self.values)
        value_menu.grid(row=0,column=3, sticky=tk.N,padx=10, pady=10)

        generate_button = tk.Button(self, text="Generate", command=self.generate)
        generate_button.grid(row=0,column=4, sticky=tk.N,padx=10, pady=10)

        save_button = tk.Button(self, text="Save", command=self.save)
        save_button.grid(row=0,column=5, sticky=tk.N,padx=10, pady=10)

        # Create the canvas for displaying the image
        self.canvas1 = tk.Canvas(self, width=400, height=400, borderwidth=0, relief=tk.FLAT)
        self.canvas1.grid(row=1,column=0, sticky=tk.N,padx=10, pady=10)
        self.canvas2 = tk.Canvas(self, width=400, height=400, borderwidth=0, relief=tk.FLAT)
        self.canvas2.grid(row=2,column=0, sticky=tk.N,padx=10, pady=10)
        self.canvas_result  = tk.Canvas(self, width=800, height=800)
        self.canvas_result.grid(row=1,column=1, sticky=tk.N,padx=10, pady=10, rowspan=2, columnspan=5)

        self.image1 = None
        self.image2 = None
        self.image2_resized = None

        self.image_result = None


        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.save_folder = os.fsencode(dir_path + '/saves/')
        

    
    def startup(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        image1 = Image.open(os.fsencode(dir_path + '/examples/example8.jpg'))
        image2 = Image.open(os.fsencode(dir_path + '/examples/example9.jpg'))

        self.image1 = image1
        self.image2 = image2
        self.image2_resized = image2

        image_can1 = self.resize_image_for_canvas(self.image1, self.canvas1)
        image_can2 = self.resize_image_for_canvas(self.image2_resized, self.canvas2)

        self.display_image(image_can1, self.canvas1)
        self.display_image(image_can2, self.canvas2)

        self.generate()


        

    def select_file(self):
        # Open a file dialog to select an image file
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.png")])

        # Check if a file was selected
        if file_path:
            # Load the image and display it on the canvas
            image = Image.open(file_path)
            self.image1 = image

            if self.image2 is not None:
                self.image2_resized = self.image2.resize(size=(self.image1.width, self.image1.height), resample=Image.LANCZOS)
                image_can2 = self.resize_image_for_canvas(self.image2_resized, self.canvas2)
                self.display_image(image_can2, self.canvas2)

            image = self.resize_image_for_canvas(image, self.canvas1)
            self.display_image(image, self.canvas1)

    def select_file2(self):
        # Open a file dialog to select an image file
        if self.image1 is None:
            messagebox.showerror("Error", "Select first image!")
            return

        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.png")])

        # Check if a file was selected
        if file_path:
            # Load the image and display it on the canvas
            image = Image.open(file_path)
            self.image2 = image
            
            image = image.resize(size=(self.image1.width, self.image1.height), resample=Image.LANCZOS)
            self.image2_resized = image

            image = self.resize_image_for_canvas(image, self.canvas2)

            self.display_image(image, self.canvas2)

    def generate(self):
        image1 = self.image1
        image2 = self.image2_resized

        if image1 is None or image2 is None:
            messagebox.showerror("Error", "Select both images!")
            return

        option = self.option.get()
        value = self.value.get()

        width = image1.width
        height = image1.height

        column_size = int(width/value)
        row_size = int(height/value)

        pixels1 = list(image1.getdata())
        pixels2 = list(image2.getdata())

        image = Image.new(image1.mode, image1.size)
        out_pixels = []

        if option == "Noise":
            for i in range(value):
                for j in range(value):
                    for x in range(column_size):
                        for y in range(row_size):
                            index = (j*row_size+y)*width + (i*column_size+x)
                            if (i+j) % 2 == 0:
                                out_pixels.append(pixels1[index])
                            else:
                                out_pixels.append(pixels2[index])
        elif option == "Weird Repeat":
            for j in range(value):
                for i in range(value):
                    for y in range(row_size):
                        for x in range(column_size):
                            index = (j*row_size+y)*width + (i*column_size+x)
                            if (i+j) % 2 == 0:
                                out_pixels.append(pixels1[index])
                            else:
                                out_pixels.append(pixels2[index])
        elif option == "Noise2":
            for x in range(column_size):
                for j in range(value):
                    for i in range(value):
                        for y in range(row_size):
                            index = (j*row_size+y)*width + (i*column_size+x)
                            if (i+j) % 2 == 0:
                                out_pixels.append(pixels1[index])
                            else:
                                out_pixels.append(pixels2[index])
        elif option == "Noise3":
            for y in range(row_size):
                for x in range(column_size):
                    for i in range(value):
                        for j in range(value):
                            index = (j*row_size+y)*width + (i*column_size+x)
                            if (i+j) % 2 == 0:
                                out_pixels.append(pixels1[index])
                            else:
                                out_pixels.append(pixels2[index])
        elif option == "Grid":
            for j in range(value):
                for y in range(row_size):
                    for i in range(value):
                        for x in range(column_size):
                            index = (j*row_size+y)*width + (i*column_size+x)
                            if (i+j) % 2 == 0:
                                out_pixels.append(pixels1[index])
                            else:
                                out_pixels.append(pixels2[index])
        elif option == "Squares":
            for j in range(value):
                for y in range(row_size):
                    for i in range(value):
                        for x in range(column_size):
                            index = (j*row_size+y)*width + (i*column_size+x)
                            if i*j % 2 == 0:
                                out_pixels.append(pixels1[index])
                            else:
                                out_pixels.append(pixels2[index])    
        elif option == "Columns":
            for j in range(value):
                for y in range(row_size):
                    for i in range(value):
                        for x in range(column_size):
                            index = (j*row_size+y)*width + (i*column_size+x)
                            if i % 2 == 0:
                                out_pixels.append(pixels1[index])
                            else:
                                out_pixels.append(pixels2[index])
        elif option == "Splice":
            for j in range(value):
                for y in range(row_size):
                    for i in range(value):
                        for x in range(column_size):
                            index = (j*row_size+y)*width + (i*column_size+x)
                            if x % 2 == 0:
                                out_pixels.append(pixels1[index])
                            else:
                                out_pixels.append(pixels2[index])
        elif option == "Rows":
            for j in range(value):
                for y in range(row_size):
                    for i in range(value):
                        for x in range(column_size):
                            index = (j*row_size+y)*width + (i*column_size+x)
                            if j % 2 == 0:
                                out_pixels.append(pixels1[index])
                            else:
                                out_pixels.append(pixels2[index])

        image.putdata(out_pixels)

        self.image_result = image

        image = self.resize_image_for_canvas(image, self.canvas_result)
        self.display_image(image, self.canvas_result)

    def save(self):
        timestr = time.strftime("%Y%m%d-%H%M%S")
        path = self.save_folder.decode("utf8") + timestr + ".jpg"

        self.image_result.save(path)

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
            return None

        # Get the image from the canvas
        image = canvas.image

        return image

    def resize_image_for_canvas(self, image, canvas):
        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()
        # Check if the image is larger than the canvas
        if image.width > canvas_width or image.height > canvas_height:
            # Calculate the new size of the image to fit the canvas
            width_ratio = canvas_width / image.width
            height_ratio = canvas_height / image.height
            resize_ratio = min(width_ratio, height_ratio)
            new_size = (int(image.width * resize_ratio), int(image.height * resize_ratio))
            # Resize the image
            image = image.resize(new_size, resample=Image.LANCZOS)

        return image

if __name__ == '__main__':
    app = App()
    app.after(200,app.startup)
    app.mainloop()
