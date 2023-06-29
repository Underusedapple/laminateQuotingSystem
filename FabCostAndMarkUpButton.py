import json
import tkinter as tk
from tkinter import messagebox


# make buttons
class Fab_Cost_Mark_Up_button(tk.Button):
    def __init__(self, window, pricing_data, main, name="", *args, **kwargs):
        self.name = tk.StringVar()
        self.name.set(name.replace("_", " ").title())
        self.json_locator = name  # this is used to parse the json data for the "name" assigned for the button
        self.main = main  # this is main(self)
        self.pricing_data = pricing_data

        super().__init__(
            window, *args, textvariable=self.name, command=self.button_do, **kwargs
        )

    def focus_next_window(self, event):
        # makes it so that tab in a textbox will go to the next textbox insted of creating a tabbe dspace
        event.widget.tk_focusNext().focus()
        return "break"

    def submit_cmd(self):
        # command for the submitbutton

        new_data = float(self.data_ent.get())

        # update pricing data
        self.pricing_data[self.json_locator] = new_data

        # update json (i currently have it rewriting all data just for simplicity, could only update the pricing data for effeciency)
        dumped_new_data = json.dumps(self.pricing_data, indent=4)
        with open(self.main.data_json, "w") as pricing_data_json:
            pricing_data_json.write(dumped_new_data)

        # this is a verification that the password saved correctly
        with open(self.main.data_json, "r") as pricing_data_json:
            pricing_data = json.load(pricing_data_json)

        if pricing_data[self.json_locator] == new_data:
            messagebox.showinfo("Data Saved", "Data saved successfully.")
        else:
            messagebox.showinfo(
                "Saving Error", "Unable to save data. Please try again."
            )
        self.main.edit_info_btn_page.deiconify()
        self.main.edit_info_btn_page.focus_set()
        self.edit_page_frame.destroy()

    def button_do(self):
        # hide edit info buttons
        self.main.edit_info_btn_page.withdraw()

        # pull levels from pricing data
        json_data = self.pricing_data[self.json_locator]

        # create new window
        self.edit_page_frame = tk.Tk()
        self.edit_page_frame.resizable(False,False)
        self.edit_page_frame.title("TextBox Input")

        # TextBox Creation
        # lists to store tbox and the corresponding inputs
        self.name_tboxes = []
        self.price_tboxes = []

        # lists of the above lists
        self.tbox_lists = [self.name_tboxes, self.price_tboxes]

        # create entry
        self.data_label = tk.Label(
            self.edit_page_frame, text=self.json_locator.replace("_", " ").title()
        )
        self.data_label.grid(row=0, column=0, pady=5, padx=5)

        self.data_ent = tk.Entry(self.edit_page_frame)
        self.data_ent.insert(0, json_data)
        self.data_ent.grid(row=0, column=1, pady=5, padx=5)

        # create buttons
        self.submit_button = tk.Button(
            self.edit_page_frame, command=self.submit_cmd, text="Submit", background='#DDDDDD'
        )
        self.submit_button.grid(row=1, column=0, columnspan=2, pady=5)

        self.edit_page_frame.mainloop()


if __name__ == "__main__":
    # # load data from json file
    with open(r"jsons\stone_pricing_data.json", "r") as pricing_data_json:
        pricing_data = json.load(pricing_data_json)

    # window no frame
    window = tk.Toplevel()
    for z, data in enumerate(pricing_data):
        window.rowconfigure(z, weight=1)
    window.columnconfigure(0, weight=1)

    # lsit of buttons for later?
    btns = []

    # make and add buttons to list
    for data in pricing_data:
        btns.append(Fab_Cost_Mark_Up_button(window, pricing_data, data,name='fabrication_cost'))

    # pack buttons onto window
    for n, btn in enumerate(btns):
        btn.grid(row=n, column=0, sticky="news")
    window.mainloop()
