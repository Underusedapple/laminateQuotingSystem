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
class Nonstocked_Stone_Material_Level_Button(tk.Button):
    def __init__(self, window, pricing_data,material, main, name="", *args, **kwargs):
        self.name = tk.StringVar()
        self.name.set(name.replace("_", " ").title())
        self.main = main  # this is main(self)
        
        #the convention of passing the pricing data and a json locator
        #while unconvential is necessary because of the loop
        #when buttons are created in open_info_edit() from main.py
        #all data is given becasue the same data is passed to all buttons
        #rather than creating a case for each button, each button is given all
        #and extacts necessary data

        self.pricing_data = pricing_data[material]

        self.json_locator = name  # this is used to parse the json data for the "name" assigned for the button

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
        material = self.material

        new_data = {}  # data stored in dictionary

        # loop through the buttons stored in lists using one list to iterate
        for x, txtbox_list in enumerate(self.stone_level_name_box):
            # get level name and remove white space
            level_name = self.stone_level_name_box[x][0].get("1.0", tk.END).strip()

            # get level height and remove white space
            level_height = float(self.stone_level_height_box[x][0].get("1.0", tk.END).strip())

            # get level height and remove white space
            level_width = float(self.stone_level_width_box[x][0].get("1.0", tk.END).strip())

            # get level price and remove white space
            level_price = float(self.stone_level_price_box[x][0].get("1.0", tk.END))






            # store that data using the iterator to name them individually
            new_data[f"{material}_{x}"] = {
                "Name": level_name,
                "Size": {"Height":level_height,
                         "Width":level_width},
                "Price": level_price
            }



        #load existing json data
        with open(self.main.data_jsons[self.material], "r") as pricing_data_json:
            newPricing = json.load(pricing_data_json)

        #update level pricing
        for key in list(newPricing[self.json_locator].keys()):
            if key in new_data:
                newPricing[self.json_locator][key] = new_data[key]
            else:
                del newPricing[self.json_locator][key]



            



        


        # update json (i currently have it rewriting all data just for simplicity, could only update the pricing data for effeciency)
        dumpedNewPricing = json.dumps(newPricing, indent=4)
        with open(self.main.data_jsons[self.material], "w") as pricing_data_json:
            pricing_data_json.write(dumpedNewPricing)

        # this is a verification that the password saved correctly
        with open(self.main.data_jsons[self.material], "r") as pricing_data_json:
            loadedPricing = json.load(pricing_data_json)

        if loadedPricing[self.json_locator] == new_data:
            messagebox.showinfo("Data Saved", "Data saved successfully.")
        else:
            messagebox.showinfo(
                "Saving Error", "Unable to save data. Please try again."
            )
        self.main.edit_info_btn_page.deiconify()
        self.main.edit_info_btn_page.focus_set()
        self.popup.destroy()

    def add_new_level(self):
        # this creates a new row for stone

        # make new textboxes
        new_name_box = [
            Multi_data_textbox(self.edit_page_frame, height=3, width=20),
            "",
        ]
        new_height_box = [
            Multi_data_textbox(self.edit_page_frame, height=3, width=20),
            "",
        ]
        new_width_box = [
            Multi_data_textbox(self.edit_page_frame, height=3, width=20),
            "",
        ]
        new_price_box = [
            Multi_data_textbox(self.edit_page_frame, height=3, width=20),
            "",
        ]

        # add them to the lists
        self.stone_level_name_box.append(new_name_box)
        self.stone_level_height_box.append(new_height_box) 
        self.stone_level_width_box.append(new_width_box) 
        self.stone_level_price_box.append(new_price_box)

        # bind so that tab goes to next window
        new_name_box[0].bind("<Tab>", self.focus_next_window)
        new_height_box[0].bind("<Tab>", self.focus_next_window)
        new_width_box[0].bind("<Tab>", self.focus_next_window)
        new_price_box[0].bind("<Tab>", self.focus_next_window)

        # grid tboxs to the frame
        new_name_box[0].grid(row=len(self.stone_level_name_box) - 1, column=0)
        new_height_box[0].grid(row=len(self.stone_level_height_box) - 1, column=1)
        new_width_box[0].grid(row=len(self.stone_level_width_box) - 1, column=2)
        new_price_box[0].grid(row=len(self.stone_level_price_box) - 1, column=3)



    def delete_level(self):
        # deletes the last row
        for list in self.stone_level_textboxes:
            # set textbox to variable
            textbox_to_delete = list[- 1][0]

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

        # pull stone levels from pricing data
        json_data = self.pricing_data[self.json_locator]

        # create new window
        self.popup = tk.Toplevel()
        self.popup.iconbitmap(r'icon\app.ico')

        # self.popup.resizable(False, False)
        self.popup.title("TextBox Input")

        self.scrollbar=tk.Scrollbar(self.popup, orient=tk.VERTICAL)
        self.scrollbar.grid(row=0, column=1, sticky="ns")

        self.textbox_canvas = tk.Canvas(self.popup, width=750,
                         scrollregion=(0,0,750,800)) 
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
        self.stone_level_name_box = []
        self.stone_level_height_box = []
        self.stone_level_width_box = []
        self.stone_level_price_box = []

        # lists of the above lists
        self.stone_level_textboxes = [
            self.stone_level_name_box,
            self.stone_level_height_box,
            self.stone_level_width_box,
            self.stone_level_price_box
        ]

        for input in json_data:


            # make tboxs as variables
            new_name_box = [
                Multi_data_textbox(self.edit_page_frame, height=3, width=20),
                input
            ]
            new_height_box = [
                Multi_data_textbox(self.edit_page_frame, height=3, width=20),
                input
            ]
            new_width_box = [
                Multi_data_textbox(self.edit_page_frame, height=3, width=20),
                input
            ]            
            new_price_box = [
                Multi_data_textbox(self.edit_page_frame, height=3, width=20),
                input
            ]

            

            # set tab to new focus
            new_name_box[0].bind("<Tab>", self.focus_next_window)
            new_height_box[0].bind("<Tab>", self.focus_next_window)
            new_width_box[0].bind("<Tab>", self.focus_next_window)
            new_price_box[0].bind("<Tab>", self.focus_next_window)


            # add boxes to list
            self.stone_level_name_box.append(new_name_box)
            self.stone_level_height_box.append(new_height_box)
            self.stone_level_width_box.append(new_width_box)
            self.stone_level_price_box.append(new_price_box)

        input_parser = [
            "Name",
            "Height",
            "Width",
            "Price"
        ]  # used to parse through individual stone level data

        for i,label in enumerate(input_parser):
            tk.Label(self.edit_page_frame,text=label).grid(row=0,column=i)
        for y, list_of_tbox in enumerate(self.stone_level_textboxes):
            x = 1

            for tbox, input in list_of_tbox:
                # at this point json_data is the stone_levels
                # input is the level of stone
                # input parser give you either the name, color, or price for that level pending on the iterator "y"
                # and y is simultaneously used for the input parser and column since all Name boxes are column 1, Colors column 2, and Pricing Column 3

                if y in [1,2]:
                    tbox_label = str(json_data[input]['Size'][input_parser[y]])
                else:
                    tbox_label = str(json_data[input][input_parser[y]])

                print(tbox_label)
                tbox_label = (
                    tbox_label.replace("{", "")
                    .replace("}", "")
                    .replace("[", "")
                    .replace("]", "")
                    .replace("'", "")
                )
                
                tbox.insert(index=1.0, chars=tbox_label)
                tbox.grid(row=x, column=y)#+1 is for the label row
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
        btns.append(Nonstocked_Stone_Material_Level_Button(window, pricing_data, data, name='stone_levels'))

    # pack buttons onto window
    for n, btn in enumerate(btns):
        btn.grid(row=n, column=0, sticky="news")
    window.mainloop()
