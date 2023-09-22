import tkinter as tk

class YourApp:
    def __init__(self):
        self.material_selection_window = tk.Toplevel()
        self.materialSelection = tk.StringVar()
        
        # Create radio buttons
        selfEdgeRadial = tk.Radiobutton(self.material_selection_window, text='Self Edge', variable=self.materialSelection, value='Self Edge')
        selfEdgeRadial.pack()
        stoneRadial = tk.Radiobutton(self.material_selection_window, text='Stone', variable=self.materialSelection, value='Stone')
        stoneRadial.pack()
        bothRadial = tk.Radiobutton(self.material_selection_window, text='Both', variable=self.materialSelection, value='Both')
        bothRadial.pack()
        
        # Create "Confirm" button with a command to call print_quote
        confirmSelectionBtn = tk.Button(self.material_selection_window, text="Confirm", command=self.print_quote)
        confirmSelectionBtn.pack()
        
        self.material_selection_window.mainloop()

    def print_quote(self):
        # Retrieve the selected value from self.materialSelection
        selected_value = self.materialSelection.get()
        print("Selected Value:", selected_value)

# Create an instance of your application
app = YourApp()
