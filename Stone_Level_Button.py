##TODO:make scroll bar changes to other buttons
# python 3.9.12
###made it so that tab funciton correctly, can add and delete rows that update the json correctly
# now to work on other buttons that update the data, probably wnat to start easy with the direct data buttons
# #eventually you will have to put the buttons on a different page and pass in the json data to each button, maybe you can just inport at the button level????
# look at line 37
import json
import tkinter as tk
from tkinter import messagebox


# make buttons
class Stone_Level_Button(tk.Button):
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
        quote_type = self.main.material

        new_data = {}  # data stored in dictionary

        # loop through the buttons stored in lists using one list to iterate
        for x, txtbox_list in enumerate(self.stone_level_name_box):
            # get level name and remove white space
            level_name = self.stone_level_name_box[x][0].get("1.0", tk.END).strip()

            # get level colors and remove white space
            level_colors = self.stone_level_color_box[x][0].get("1.0", tk.END)
            level_colors = level_colors.split(",")
            for y, color in enumerate(level_colors):
                level_colors[y] = color.strip()

            # get level price and remove white space
            level_price = float(self.stone_level_price_box[x][0].get("1.0", tk.END))

            # store that data using the iterator to name them individually
            new_data[f"{quote_type}_{x}"] = {
                "Name": level_name,
                "Color": level_colors,
                "Price": level_price,
            }

        # update pricing data
        if self.main.material == 'Stone':
            levels = 'stone_levels'
        elif self.main.material == 'Self Edge':
            levels = 'lam_levels'
        self.pricing_data[levels] = new_data

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

    def add_new_level(self):
        # this creates a new row for stone

        # make new textboxes
        new_name_box = [
            Multi_data_textbox(self.edit_page_frame, height=3, width=20),
            "",
        ]
        new_color_box = [
            Multi_data_textbox(self.edit_page_frame, height=3, width=20),
            "",
        ]
        new_price_box = [
            Multi_data_textbox(self.edit_page_frame, height=3, width=20),
            "",
        ]

        # add them to the lists
        self.stone_level_name_box.append(new_name_box)
        self.stone_level_color_box.append(
            new_color_box
        )  ###this will need to be a button to create individual boxes
        self.stone_level_price_box.append(new_price_box)

        # bind so that tab goes to next window
        new_name_box[0].bind("<Tab>", self.focus_next_window)
        new_color_box[0].bind("<Tab>", self.focus_next_window)
        new_price_box[0].bind("<Tab>", self.focus_next_window)

        # grid tboxs to the frame
        new_name_box[0].grid(row=len(self.stone_level_name_box) - 1, column=0)
        new_color_box[0].grid(row=len(self.stone_level_color_box) - 1, column=1)
        new_price_box[0].grid(row=len(self.stone_level_price_box) - 1, column=2)



    def delete_level(self):
        # deletes the last row
        for list in self.stone_level_textboxes:
            # set textbox to variable
            textbox_to_delete = list[len(list) - 1][0]

            # delete tbox from list
            list.pop()

            # remove tbox from grid
            textbox_to_delete.grid_remove()


    def _on_mousewheel(self, event):
        self.textbox_canvas.yview_scroll(int(-1*(event.delta/120)), "units")


    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.textbox_canvas.configure(scrollregion=self.textbox_canvas.bbox("all"))

    def button_do(self):
        # hide edit info buttons
        # self.main.edit_info_btn_page.withdraw()
        #TODO: Uncomment this line ^^

        # pull stone levels from pricing data
        json_data = self.pricing_data[self.json_locator]

        # create new window
        self.popup = tk.Toplevel()
        self.popup.resizable(False, False)
        self.popup.title("TextBox Input")

        self.popup.rowconfigure(0, weight=1) 
        self.popup.rowconfigure(1, weight=1) 

        self.popup.columnconfigure(0, weight=1)

        scrollbar=tk.Scrollbar(self.popup, orient=tk.VERTICAL)
        scrollbar.grid(row=0, column=1, sticky="ns")

        self.textbox_canvas = tk.Canvas(self.popup, width=500,
                         scrollregion=(0,0,500,800)) 
        self.textbox_canvas.grid(row=0, column=0, sticky="nsew") 
        self.textbox_canvas.bind_all("<MouseWheel>",self._on_mousewheel)


        self.edit_page_frame = tk.Frame(self.textbox_canvas)
        self.edit_page_frame.bind("<Configure>", self.onFrameConfigure)
        
        scrollbar.config(command=self.textbox_canvas.yview)
        self.textbox_canvas.config(yscrollcommand = scrollbar.set)



        self.button_frame = tk.Frame(self.popup)
        self.button_frame.columnconfigure(0,weight=1)
        self.button_frame.columnconfigure(1,weight=1)

        self.button_frame.grid(row=1,column=0, pady=5)


        self.textbox_canvas.create_window((4,4),window=self.edit_page_frame,anchor='nw',tags='self.frame')



        
        # scrollbar = tk.Scrollbar(self.popup)
        # print(len(json_data))
        # scrollbar.pack(fill=tk.Y, side=tk.RIGHT, expand=tk.FALSE)

        # self.edit_page_frame = tk.Canvas(self.popup,height=5, width=10, scrollregion=(0,0,100,200),confine=False)
        # self.edit_page_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.TRUE)


        # self.edit_page_frame.config(yscrollcommand=scrollbar.set)
        # scrollbar.configure(command=self.edit_page_frame.yview)


        # TextBox Creation
        # lists to store tbox and the corresponding inputs
        self.stone_level_name_box = []
        self.stone_level_color_box = []
        self.stone_level_price_box = []

        # lists of the above lists
        self.stone_level_textboxes = [
            self.stone_level_name_box,
            self.stone_level_color_box,
            self.stone_level_price_box,
        ]

        for input in json_data:


            # self.edit_page_frame.config(yscrollcommand = scrollbar.set)


            # scrollbar.config(command=self.edit_page_frame.yview)

            # make tboxs as variables
            new_name_box = [
                Multi_data_textbox(self.edit_page_frame, height=3, width=20),
                input,
            ]
            new_color_box = [
                Multi_data_textbox(self.edit_page_frame, height=3, width=20),
                input,
            ]
            new_price_box = [
                Multi_data_textbox(self.edit_page_frame, height=3, width=20),
                input,
            ]

            # set tab to new focus
            new_name_box[0].bind("<Tab>", self.focus_next_window)
            new_color_box[0].bind("<Tab>", self.focus_next_window)
            new_price_box[0].bind("<Tab>", self.focus_next_window)

            # add boxes to list
            self.stone_level_name_box.append(new_name_box)
            self.stone_level_color_box.append(
                new_color_box
            )  ###this will need to be a button to create individual boxes
            self.stone_level_price_box.append(new_price_box)

        input_parser = [
            "Name",
            "Color",
            "Price",
        ]  # used to parse through individual stone level data
        for y, list_of_tbox in enumerate(self.stone_level_textboxes):
            x = 0

            for tbox, input in list_of_tbox:
                # at this point json_data is the stone_levels
                # input is the level of stone
                # input parser give you either the name, color, or price for that level pending on the iterator "y"
                # and y is simultaneously used for the input parser and column since all Name boxes are column 1, Colors column 2, and Pricing Column 3
                tbox_label = str(json_data[input][input_parser[y]])
                tbox_label = (
                    tbox_label.replace("{", "")
                    .replace("}", "")
                    .replace("[", "")
                    .replace("]", "")
                    .replace("'", "")
                )
                tbox.insert(index=1.0, chars=tbox_label)
                tbox.grid(row=x, column=y)
                x += 1  # iterator for the rows

        # create buttons
        self.submit_button = tk.Button(
            self.button_frame, command=self.submit_cmd, text="Submit", height=3, width=25, background='#D0D0D0'
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

        self.popup.mainloop()


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
        btns.append(Stone_Level_Button(window, pricing_data, data, name='stone_levels'))

    # pack buttons onto window
    for n, btn in enumerate(btns):
        btn.grid(row=n, column=0, sticky="news")
    window.mainloop()
