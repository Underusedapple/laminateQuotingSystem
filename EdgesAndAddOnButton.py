import json
import tkinter as tk
from tkinter import messagebox
import re


# make buttons
class Edge_and_Add_On_Button(tk.Button):
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

        new_data = {}  # data stored in dictionary

        # loop through the buttons stored in lists using one list to iterate
        for x, txtbox_list in enumerate(self.name_tboxes):
            # get level name and remove white space
            level_name = self.name_tboxes[x][0].get("1.0", tk.END).strip()
            level_name = level_name.replace(" ", "_").lower()

            # get level price and remove white space
            level_price = float(self.price_tboxes[x][0].get("1.0", tk.END).strip())

            # store that data using the iterator to name them individually
            new_data[level_name] = level_price

        # update pricing data
        self.pricing_data[self.json_locator] = new_data

        # update json (i currently have it rewriting all data just for simplicity, could only update the pricing data for effeciency)
        dumped_new_data = json.dumps(self.pricing_data, indent=4)
        with open(r"jsons\pricing_data.json", "w") as pricing_data_json:
            pricing_data_json.write(dumped_new_data)

        # this is a verification that the password saved correctly
        with open(r"jsons\pricing_data.json", "r") as pricing_data_json:
            pricing_data = json.load(pricing_data_json)

        if pricing_data[self.json_locator] == new_data:
            messagebox.showinfo("Data Saved", "Data saved successfully.")
        else:
            messagebox.showinfo(
                "Saving Error", "Unable to save data. Please try again."
            )
        self.main.edit_info_btn_page.deiconify()


        for widget in self.main.add_on_frm.winfo_children(): #clear widgets from add_on_frame
            widget.destroy()



        
        self.main.load_add_on_frame() #reload the add-on frame as there are new objects that need to be caught



        self.main.edit_info_btn_page.focus_set()
        self.edit_page_frame.destroy()

    def add_new_level(self):
        # this creates a new row

        # make new textboxes
        new_name_box = [
            Multi_data_textbox(self.edit_page_frame, height=3, width=20),
            "",
        ]
        new_price_box = [
            Multi_data_textbox(self.edit_page_frame, height=3, width=20),
            "",
        ]

        # add them to the lists
        self.name_tboxes.append(new_name_box)
        self.price_tboxes.append(new_price_box)

        # bind so that tab goes to next window
        new_name_box[0].bind("<Tab>", self.focus_next_window)
        new_price_box[0].bind("<Tab>", self.focus_next_window)
        new_price_box[0].bind("<Key>", self.validate_ent)
        new_price_box[0].bind("<KeyRelease>", self.reset_textbox)

        # grid tboxs to the frame
        new_name_box[0].grid(row=len(self.name_tboxes) - 1, column=0)
        new_price_box[0].grid(row=len(self.price_tboxes) - 1, column=1)

        # below funcitons reset the tab order by deleting and recreating the buttons

        # delete buttons
        self.submit_button.destroy()
        self.new_row_button.destroy()
        self.delete_row_button.destroy()

        # remake buttons
        self.submit_button = tk.Button(
            self.edit_page_frame, command=self.submit_cmd, text="Submit"
        )
        self.new_row_button = tk.Button(
            self.edit_page_frame, command=self.add_new_level, text="Add New Row"
        )
        self.delete_row_button = tk.Button(
            self.edit_page_frame, command=self.delete_level, text="Delete Bottom Row"
        )

        # grid buttons
        self.submit_button.grid(row=len(self.price_tboxes), column=0)
        self.new_row_button.grid(row=len(self.price_tboxes), column=1)
        self.delete_row_button.grid(row=len(self.price_tboxes) + 1, column=0)

    def delete_level(self):
        # deletes the last row
        for list in self.tbox_lists:
            # set textbox to variable
            textbox_to_delete = list[len(list) - 1][0]

            # delete tbox from list
            list.pop()

            # remove tbox from grid
            textbox_to_delete.grid_remove()

    def validate_ent(self, event):
        """Checks for numerical inputs only"""

        char = event.char

        # pass the backspace key
        if char == "\x08":
            return True

        input = event.widget.get("1.0", tk.END)
        state = "disable"
        if char in input:
            state = "normal"
        elif re.fullmatch(r"^[0-9.]$", char):
            state = "normal"
        event.widget.configure(state=state)

    def reset_textbox(self, event):
        event.widget.configure(state="normal")

    def new_price_check(self, event):
        widget = event.widget
        input = widget.get("1.0", tk.END)
        input = input.strip()
        test = re.fullmatch(r"^([0-9]?)+[.]?([0-9]?)+$", input)
        print(test)
        if re.fullmatch(r"^([0-9]?)+[.]?([0-9]?)+$", input) == None:
            messagebox.showerror("Invalid Price", "Please inser a valid float number.")
            widget.focus_set()
            widget.configure(state="normal")

    def button_do(self):
        # hide edit info buttons
        self.main.edit_info_btn_page.withdraw()
        # pull levels from pricing data

        json_data = self.pricing_data[self.json_locator]

        # create new window
        self.edit_page_frame = tk.Toplevel()
        self.edit_page_frame.title("TextBox Input")

        # TextBox Creation
        # lists to store tbox and the corresponding inputs
        self.name_tboxes = []
        self.price_tboxes = []

        # lists of the above lists
        self.tbox_lists = [self.name_tboxes, self.price_tboxes]

        # create textboxes
        for edge in json_data:

            # make tboxs as variables
            new_name_box = [
                Multi_data_textbox(self.edit_page_frame, height=3, width=20),
                edge,
            ]
            new_price_box = [
                Multi_data_textbox(self.edit_page_frame, height=3, width=20),
                json_data[edge],
            ]

            # bind tab to new focus so you can loops the objects with tab
            new_name_box[0].bind("<Tab>", self.focus_next_window)
            new_price_box[0].bind("<Tab>", self.focus_next_window)
            new_price_box[0].bind("<Key>", self.validate_ent)
            new_price_box[0].bind("<KeyRelease>", self.reset_textbox)
            new_price_box[0].bind("<FocusOut>", self.new_price_check)

            # add buttons to list
            self.name_tboxes.append(new_name_box)
            self.price_tboxes.append(new_price_box)

        for y, list_of_tbox in enumerate(self.tbox_lists):
            x = 0

            for tbox, input in list_of_tbox:

                # title and get rid of underscores
                if type(input) not in [int, float]:
                    input = input.title().replace("_", " ")
                tbox.insert(index=1.0, chars=input)

                tbox.grid(row=x, column=y)
                x += 1  # iterator for the rows

        # create buttons
        self.submit_button = tk.Button(
            self.edit_page_frame, command=self.submit_cmd, text="Submit"
        )
        self.submit_button.grid(row=x + 2, column=0)

        self.new_row_button = tk.Button(
            self.edit_page_frame, command=self.add_new_level, text="Add New Row"
        )
        self.new_row_button.grid(row=x + 1, column=0)

        self.delete_row_button = tk.Button(
            self.edit_page_frame, command=self.delete_level, text="Delete Bottom Row"
        )
        self.delete_row_button.grid(row=x + 1, column=1)

        self.edit_page_frame.mainloop()


class Multi_data_textbox(tk.Text):
    def __init__(self, window, name="", *args, **kwargs):
        self.name = tk.StringVar()
        self.name.set(name.replace("_", " ").title())
        super(Multi_data_textbox, self).__init__(window, *args, **kwargs)


if __name__ == "__main__":
    # # load data from json file
    with open(r"jsons\pricing_data.json", "r") as pricing_data_json:
        pricing_data = json.load(pricing_data_json)

    # window no frame
    window = tk.Tk()
    for z, data in enumerate(pricing_data):
        window.rowconfigure(z, weight=1)
    window.columnconfigure(0, weight=1)

    # lsit of buttons for later?
    btns = []

    # make and add buttons to list
    for data in pricing_data:
        btns.append(Edge_and_Add_On_Button(window, pricing_data, data))

    # pack buttons onto window
    for n, btn in enumerate(btns):
        btn.grid(row=n, column=0, sticky="news")
    window.mainloop()
