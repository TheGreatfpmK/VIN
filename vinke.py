import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

class FileSelector(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.parent.title("File Selector")

        self.button = tk.Button(self, text="Select File", command=self.onButtonClick)
        self.button.pack(side='left')

        self.generate_button = tk.Button(self, text="Generate")
        self.generate_button.pack(side='left')

        # create the canvases
        self.canvas1 = tk.Canvas(self, width=800, height=800)
        self.canvas1.pack(side='left')

        self.canvas2 = tk.Canvas(self, width=800, height=800)
        self.canvas2.pack(side='left')

    def onButtonClick(self):
        filepath = filedialog.askopenfilename()
        if filepath.endswith('.jpg') or filepath.endswith('.png'):
            # load the image and display it on the canvas
            image = Image.open(filepath)
            width, height = image.size
            if width > 800 or height > 800:
                # scale down the image to fit the canvas
                if width > height:
                    # landscape image
                    new_height = int(800 * height / width)
                    image = image.resize((800, new_height), Image.ANTIALIAS)
                else:
                    # portrait or square image
                    new_width = int(800 * width / height)
                    image = image.resize((new_width, 800), Image.ANTIALIAS)
            # center the image on the canvas
            x = (800 - image.size[0]) // 2
            y = (800 - image.size[1]) // 2
            image = ImageTk.PhotoImage(image)
            self.canvas1.create_image(x + image.width() // 2, y + image.height() // 2, image=image)
            self.image = image
        else:
            # show a warning message
            tk.messagebox.showwarning("Warning", "Selected file is not a .jpg or .png file")

def main():
    root = tk.Tk()
    app = FileSelector(root)
    app.pack()
    root.mainloop()

if __name__ == '__main__':
    main()