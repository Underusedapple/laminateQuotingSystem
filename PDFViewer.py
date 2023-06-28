import tkinter as tk
from PIL import ImageTk, Image
import glob
# from pdf2image import convert_from_path
from pdf2image import *
import pdf2image
import os



pdf_path = "Pricing_Testing_Job.pdf"
output_path = "tempIMGFiles/"

images = convert_from_path(pdf_path, output_folder=output_path)


class PDFViewerApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("PDF Viewer")

        # Create a canvas to display the PDF pages
        self.canvas = tk.Canvas(self, width=600, height=800)
        self.canvas.pack()

        # Load the converted images and display the first page
        self.pages = []
        for image_path in sorted(glob.glob(output_path + "*.jpg")):
            image = Image.open(image_path)
            self.pages.append(ImageTk.PhotoImage(image))

        self.current_page = 0
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.pages[self.current_page])

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

if __name__ == "__main__":
    app = PDFViewerApp()
    app.mainloop()
