import tkinter as tk

class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Main Window")
        self.root.columnconfigure(0,weight=1)
        self.root.rowconfigure(1,weight=1)
        self.root.rowconfigure(0,weight=1)
        # Create buttons    
        self.self_edge_btn = tk.Button(self.root, text="Stocked Self-Edge Quote", command=self.stocked_self_edge_quote)
        self.self_edge_btn.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)

        self.stone_quote_btn = tk.Button(self.root, text="Stocked Stone Quote", command=self.stocked_stone_quote)
        self.stone_quote_btn.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)


    def stocked_self_edge_quote(self):
        # Function for Stocked Self-Edge Quote button
        pass  # Add your code here

    def stocked_stone_quote(self):
        # Function for Stocked Stone Quote button
        pass  # Add your code here

    def run(self):
        self.root.mainloop()

# Create an instance of the MainWindow class
window = MainWindow()
window.run()
