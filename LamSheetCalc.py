import tkinter as tk
from tkinter import Entry, Label, Button, Scrollbar, Canvas
import math

class LamSheetCalculator:
    def __init__(self):
        self.requiredSheets = None

    def NonstockLamMaterialWindow(self, nonstockDict, fabSqft):
        # Sample dictionary of Frame objects (replace this with your actual data)
        nonstockDict = nonstockDict
        fabSqft = fabSqft
        margin = 1.5
        minSheets = math.ceil((fabSqft * margin) / 60)
        print(minSheets)
        entryWidgetDict = {}

        def submit():
            self.requiredSheets = {key: entryWidgetDict[key].get() for key in entryWidgetDict}

        def cancel():
            root.destroy()

        root = tk.Tk()
        root.title("Frame Viewer")

        canvas = Canvas(root)
        scrollbar = Scrollbar(root, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        canvas.pack(side="left", fill="both", expand=True)
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        for i, (key, frame) in enumerate(nonstockDict.items()):
            label = Label(scrollable_frame, text=f"{key}:")
            label.grid(row=i, column=0, sticky="w")

            sheets_entry = Entry(scrollable_frame)
            sheets_entry.insert(0, minSheets)  # Populate with default value
            sheets_entry.grid(row=i, column=1, sticky="w")
            entryWidgetDict[key] = sheets_entry

        submit_button = Button(root, text="Submit", command=submit)
        submit_button.pack(side="left")

        cancel_button = Button(root, text="Cancel", command=cancel)
        cancel_button.pack(side="right")

        root.mainloop()