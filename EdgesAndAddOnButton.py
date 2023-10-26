import json
import tkinter as tk
from tkinter import messagebox
import re


# make buttons
class Edge_and_Add_On_Button(tk.Button):
    def __init__(self, window, pricing_data, material, main, name="", *args, **kwargs):
        self.name = tk.StringVar()
        self.name.set(name.replace("_", " ").title())
        self.json_locator = name  # this is used to parse the json data for the "name" assigned for the button
        self.main = main  # this is main(self)
        self.pricing_data = pricing_data[material]
        self.material = material
        super().__init__(
            window, *args, textvariable=self.name, command=self.button_do, **kwargs
        )

    def focus_next_window(self, event):
        # makes it so that tab in a textbox will go to the next textbox insted of creating a tabbe dspace
        event.widget.tk_focusNext().focus()
        return "break"

    def submit_cmd(self):
        # command for the submitbutton

        newPricing = {}  # data stored in dictionary
        # loop through the buttons stored in lists using one list to iterate
        for x, txtbox_list in enumerate(self.name_tboxes):
            # get level name and remove white space
            level_name = self.name_tboxes[x][0].get("1.0", tk.END).strip()
            level_name = level_name.replace(" ", "_").lower()

            # get level price and remove white space
            level_price = float(self.price_tboxes[x][0].get("1.0", tk.END).strip())

            # store that data using the iterator to name them individually
            newPricing[level_name] = level_price

        # update pricing data
        for key in list(newPricing[self.json_locator].keys()):
            if key in newPricing:
                newPricing[self.json_locator][key] = newPricing[key]
            else:
                del newPricing[self.json_locator][key]

        # update json (i currently have it rewriting all data just for simplicity, could only update the pricing data for effeciency)
        dumped_new_data = json.dumps(self.pricing_data, indent=4)
        with open(self.main.data_jsons[self.material], "w") as pricing_data_json:
            pricing_data_json.write(dumped_new_data)

        # this is a verification that the password saved correctly
        with open(self.main.data_jsons[self.material], "r") as pricing_data_json:
            pricing_data = json.load(pricing_data_json)

        if pricing_data[self.json_locator] == newPricing:
            messagebox.showinfo("Data Saved", "Data saved successfully.")
        else:
            messagebox.showinfo(
                "Saving Error", "Unable to save data. Please try again."
            )


        #below is unique to this button as the add-on tab needs to be reloaded in case of added parameters
        tab = self.main.pricingTabs[self.material]
        
        self.main.edit_info_btn_page.deiconify()#TODO: I think this is wrong

        for widget in tab.winfo_children(): #clear widgets from add_on_frame
            widget.destroy()



        
        self.main.load_add_on_frame(tab,self.material) #reload the add-on frame as there are new objects that need to be caught



        self.main.edit_info_btn_page.focus_set()
        self.popup.destroy()

    def add_new_level(self):
        # this creates a new row

        # make new textboxes
        new_name_box = [
            Multi_data_textbox(self.edit_page_frame, height=3, width=31),
            "",
        ]
        new_price_box = [
            Multi_data_textbox(self.edit_page_frame, height=3, width=30),
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
        if re.fullmatch(r"^([0-9]?)+[.]?([0-9]?)+$", input) == None:
            messagebox.showerror("Invalid Price", "Please inser a valid float number.")
            widget.focus_set()
            widget.configure(state="normal")


    def _on_mousewheel(self, event):
        self.textbox_canvas.yview_scroll(int(-1*(event.delta/120)), "units")


    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.textbox_canvas.configure(scrollregion=self.textbox_canvas.bbox("all"))
        

    def button_do(self):
        # hide edit info buttons
        self.main.edit_info_btn_page.withdraw()
        # pull levels from pricing data

        json_data = self.pricing_data[self.json_locator]

        # create new window
        self.popup = tk.Toplevel()
        self.popup.iconbitmap(r'icon\app.ico')

        self.popup.resizable(False,False)
        self.popup.title("TextBox Input")

        self.scrollbar = tk.Scrollbar(self.popup, orient=tk.VERTICAL)
        self.scrollbar.grid(row=0, column=1, sticky="ns")

        self.textbox_canvas = tk.Canvas(self.popup, width=500,
                         scrollregion=(0,0,500,800)) 
        self.textbox_canvas.grid(row=0, column=0, sticky="nsew") 
        self.textbox_canvas.bind_all("<MouseWheel>",self._on_mousewheel)

        self.edit_page_frame = tk.Frame(self.textbox_canvas)
        self.edit_page_frame.bind("<Configure>", self.onFrameConfigure)



        self.scrollbar.config(command=self.textbox_canvas.yview)
        self.textbox_canvas.config(yscrollcommand = self.scrollbar.set)



        self.button_frame = tk.Frame(self.popup)
        self.button_frame.columnconfigure(0,weight=1)
        self.button_frame.columnconfigure(1,weight=1)

        self.button_frame.grid(row=1,column=0, pady=5)


        self.textbox_canvas.create_window((4,4),window=self.edit_page_frame,anchor='nw',tags='self.frame')
       
       
       
        # TextBox Creation
        # lists to store tbox and the corresponding inputs
        self.name_tboxes = []
        self.price_tboxes = []

        # lists of the above lists
        self.tbox_lists = [self.name_tboxes, self.price_tboxes]

        # create textboxes
        for add_on in json_data:

            # make tboxs as variables
            new_name_box = [
                Multi_data_textbox(self.edit_page_frame, height=3, width=31),
                add_on,
            ]
            new_price_box = [
                Multi_data_textbox(self.edit_page_frame, height=3, width=30),
                json_data[add_on],
            ]

            # bind tab to new focus so you can loops the objects with tab
            new_name_box[0].bind("<Tab>", self.focus_next_window)
            new_price_box[0].bind("<Tab>", self.focus_next_window)
            new_price_box[0].bind("<Key>", self.validate_ent)
            new_price_box[0].bind("<KeyRelease>", self.reset_textbox)
            new_price_box[0].bind("<FocusOut>", self.new_price_check) #TODO: ugh is this something i need to add to the material button?

            # add buttons to list
            self.name_tboxes.append(new_name_box)
            self.price_tboxes.append(new_price_box)




        nameLabel = tk.Label(self.edit_page_frame, text = "Name").grid(row=0,column=0)
        priceLabel = tk.Label(self.edit_page_frame, text = "Price").grid(row=0,column=1)

        for y, list_of_tbox in enumerate(self.tbox_lists):
            x = 1

            for tbox, input in list_of_tbox:

                # title and get rid of underscores
                if type(input) not in [int, float]:
                    input = input.title().replace("_", " ")
                tbox.insert(index=1.0, chars=input)

                tbox.grid(row=x, column=y)
                x += 1  # iterator for the rows

        # create buttons
        self.submit_button = tk.Button(
            self.button_frame, command=self.submit_cmd, text="Submit", height=3, width=25, background='#DDDDDD'
        )
        self.submit_button.grid(row=1, column=0,columnspan=2,padx=20,pady=5)

        self.new_row_button = tk.Button(
            self.button_frame, command=self.add_new_level, text="Add New Row", height=2, width=15
        )
        self.new_row_button.grid(row=0, column=1,padx=20,pady=5)

        self.delete_row_button = tk.Button(
            self.button_frame, command=self.delete_level, text="Delete Bottom Row", height=2, width=15
        )
        self.delete_row_button.grid(row=0, column=0)

        self.edit_page_frame.mainloop()


class Multi_data_textbox(tk.Text):
    def __init__(self, window, name="", *args, **kwargs):
        self.name = tk.StringVar()
        self.name.set(name.replace("_", " ").title())
        super(Multi_data_textbox, self).__init__(window, *args, **kwargs)


if __name__ == "__main__":
    # # load data from json file
    with open(r"jsons\stone_pricing_data.json", "r") as pricing_data_json:
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
        btns.append(Edge_and_Add_On_Button(window, pricing_data, data, name='add_ons'))

    # pack buttons onto window
    for n, btn in enumerate(btns):
        btn.grid(row=n, column=0, sticky="news")
    window.mainloop()
