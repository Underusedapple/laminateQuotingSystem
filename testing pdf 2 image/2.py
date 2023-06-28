import tkinter as tk
import glob
from PIL import ImageTk, Image,ImageOps
from pdf2image import convert_from_path
import os
import math

pdf_path = r"Pricing_Testing_Job.pdf"
output_path = os.path.abspath(os.getcwd()) + r"\testing pdf 2 image\output_directory"

print(output_path)

images = convert_from_path(pdf_path, output_folder=output_path, fmt='jpg')

class PDFViewerApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("PDF Viewer")

        self.bind("<Configure>", self.resize_image)


        glob_pattern = output_path + r'\*.jpg'
        print(glob_pattern)
        # Load the converted images and display the first page
        self.pages = []
        self.imgpaths = []
        for image_path in sorted(glob.glob(glob_pattern)):
            image = Image.open(image_path)
            self.imgpaths.append(image_path)
            self.pages.append(ImageTk.PhotoImage(image))





        self.current_page = 0
        # photo = ImageTk.PhotoImage(Image.open(glob_pattern))
        h = self.pages[self.current_page].height()
        w = self.pages[self.current_page].width()


        # Create a canvas to display the PDF pages
        self.canvas = tk.Canvas(self, width=w, height=h, highlightthickness=0)
        self.canvas.pack()

        # self.canvas.create_image(0, 0, anchor=tk.NW, image=self.pages[self.current_page])


        # Bind key events to navigate through the pages
        self.bind("<Right>", self.next_page)
        self.bind("<Left>", self.previous_page)

    def next_page(self, event):
        if self.current_page < len(self.pages) - 1:
            self.current_page += 1
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.pages[self.current_page])

    def previous_page(self, event):
        if self.current_page > 0:
            self.current_page -= 1
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.pages[self.current_page])


    def resize_image(self,e):
        
        
        global image, resized, image2
        # open image to resize it
        image = Image.open(self.imgpaths[self.current_page])

        resized = ImageOps.contain(image,(e.width,e.height))

        image2 = ImageTk.PhotoImage(resized)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=image2)


if __name__ == "__main__":
    app = PDFViewerApp()
    app.mainloop()
