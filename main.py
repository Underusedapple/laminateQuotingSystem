# TODO:add option for job name, auto pull from pdf file but allow person to overwrite the job name
# TODO: create a Focus out ont he entries that if left empty they revert to '0' (around line 365)



import json
import os
import re
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox,ttk
import math
import bcrypt
from Material_Level_Button import Material_Level_Button
from FabCostAndMarkUpButton import Fab_Cost_Mark_Up_button
from EdgesAndAddOnButton import Edge_and_Add_On_Button
from ExtractDataFromPdf import extractDataFromPdf
from createQuoteFromData import createQuoteFromData



class QuoteGenerator:
    def __init__(self, master):
        """Application used for quoting stocked materials from drawings """
        

        # self.main = main
        self.import_pricing_data()  # pull pricing data
        
        self.material = 'Self Edge'
        
        # lists of entries and labels for later use
        self.entries = {'Self Edge':[],'Stone':[]}
        self.labels = {'Self Edge':[],'Stone':[]}
        #create master frame
        self.master = master

        self.master.rowconfigure(0, weight=2)
        self.master.rowconfigure(1, weight=1)
        self.master.rowconfigure(2, weight=5)
        self.master.rowconfigure(3, weight=1)
        self.master.columnconfigure(0, weight=1)
        self.master.geometry("700x600")
        self.master.resizable(False, False)


        #create directory frame (where you pick the file)
        self.directory_frm = tk.Frame(master=self.master, relief=tk.SUNKEN, borderwidth=2)
        self.directory_frm.grid(
            row=0, column=0, sticky="news"
        )  # this is the frame for the directory
        self.directory_frm.rowconfigure(index=0, weight=1)
        self.directory_frm.columnconfigure(index=0, weight=1)
        self.directory_frm.columnconfigure(index=1, weight=1)




        #create multiplier frame
        self.multiplier_frm = tk.Frame(master=self.master, relief=tk.FLAT, borderwidth=2)
        self.multiplier_frm.grid(row=1, column=0, sticky="news")
        self.multiplier_frm.rowconfigure(index=0, weight=1)
        self.multiplier_frm.rowconfigure(index=1, weight=1)
        self.multiplier_frm.columnconfigure(index=0, weight=1)
        self.multiplier_frm.columnconfigure(index=1, weight=1)
        




        #create add-ons frame
        self.add_on_frm = tk.Frame(master=self.master, relief=tk.SUNKEN, borderwidth=2)
        
        self.pricingTabControl = ttk.Notebook(self.add_on_frm)

        #create self edge tab for add-on frame and non stock frame
        self.self_edge_tab = ttk.Frame(self.pricingTabControl)
        self.self_edge_tab.rowconfigure(0,weight=2)
        self.self_edge_tab.rowconfigure(1,weight=1)
        self.self_edge_tab.columnconfigure(0,weight=1)

        #add on frame
        self.self_edge_add_on_frm = ttk.Frame(self.self_edge_tab,relief=tk.RAISED)
        self.self_edge_add_on_frm.grid(row=0,column=0, sticky='nsew',pady=3,padx=2)
        #non-stocked frame
        self.self_edge_non_stocked_frm = ttk.Frame(self.self_edge_tab)
        self.self_edge_non_stocked_frm.grid(row=1,column=0, sticky='nsew')

        non_stock_lam_btn = ttk.Button(self.self_edge_non_stocked_frm,text='Add Non-Stocked Laminate Selection',).pack() 


        #create stone tab for add-on frame and non-stocked frame 
        self.stone_tab = ttk.Frame(self.pricingTabControl)
        self.stone_tab.rowconfigure(0,weight=2)
        self.stone_tab.rowconfigure(1,weight=1)
        self.stone_tab.columnconfigure(0,weight=1)

        #add on frame
        self.stone_add_on_frm = ttk.Frame(self.stone_tab,relief=tk.RAISED)
        self.stone_add_on_frm.grid(row=0,column=0, sticky='nsew',pady=3,padx=2)
        #non-stocked frame
        self.stone_non_stocked_frm = ttk.Frame(self.stone_tab)
        self.stone_non_stocked_frm.grid(row=1,column=0, sticky='nsew')


        non_stock_stone_btn = ttk.Button(self.stone_non_stocked_frm,text='Add Non-Stocked Stone Selection',command=self.add_non_stocked_stone_cmd).pack() 



        self.pricingTabs = { 'Self Edge':self.self_edge_add_on_frm, 'Stone': self.stone_add_on_frm }

        self.pricingTabControl.bind("<ButtonRelease-1>", self.set_material)



        


        self.pricingTabControl.add(self.self_edge_tab,text= "Self-Edge")
        self.pricingTabControl.add(self.stone_tab,text= "Stone")
    
        self.pricingTabControl.pack(expand=1,fill= 'both')

        self.load_add_on_frame(self.stone_add_on_frm,'Stone')

        self.load_add_on_frame(self.self_edge_add_on_frm,'Self Edge')
        

        self.add_on_frm.grid(
            row=2, column=0, sticky="news"
        ) 


        #create buttons frame
        self.button_frm = tk.Frame(master=self.master, relief=tk.RAISED, borderwidth=2)
        self.button_frm.grid(row=3, column=0, sticky="news") 
        for x in range(3):
            self.button_frm.columnconfigure(index=x, weight=2)
        self.button_frm.rowconfigure(index=0, weight=1)



        #load all buttons and widgets into frames
        self.load_directory_frame()
        self.load_multiplier_frame()
        self.load_button_frame()



        # self.master.protocol("WM_DELETE_WINDOW", self.on_closing)
        # # TODO: uncomment for testing
        # self.submit_button()




    # def on_closing(self):
    #     self.main.root.destroy()
    #     self.master.destroy()



    def add_non_stocked_stone_cmd(self):
        ns_stone_data_json = r"jsons\non_stock_stone.json"
        """This imports the pricing structures saved under 'data_json' and saves them as 'self.pricing_data' """
        with open(ns_stone_data_json,"r") as ns_stone_info:
            self.nonstocked_stone_data = json.load(ns_stone_info)



            
        self.non_stocked_stone_selector = tk.Toplevel()







        self.ns_stone_brand_frm = tk.Frame(self.non_stocked_stone_selector)
        self.ns_stone_brand_frm.pack()
    


        # Brand and Color Dropdown menu options
        brand_options = [brand for brand in self.nonstocked_stone_data.keys()]
        self.color_options = []
        
        # datatype of menu text
        self.stone_brand = tk.StringVar()
        # initial menu text
        self.stone_brand.set( brand_options[0] )
        
        # Create Dropdown menu
        brand_dropdown = tk.OptionMenu( self.ns_stone_brand_frm , self.stone_brand , *brand_options )
        brand_dropdown.grid(row=0,column=0)









        self.ns_stone_color_frm =  tk.Frame(self.non_stocked_stone_selector)
        self.ns_stone_color_frm.pack()

        self.ns_stone_color = tk.StringVar()
        self.stone_brand.trace("w",lambda name,index,mode, brand = self.stone_brand:self.load_colors(brand))


        color_dropdown = tk.OptionMenu( self.ns_stone_color_frm , self.ns_stone_color ,"i'm a formality", *self.color_options )
        color_dropdown.grid(row=0,column=0)
        self.load_colors(self.stone_brand)

        # self.stone_brand.trace("w",)



    def load_colors(self,brand):
        #find brand in json and load names
        brand = brand.get()
        self.color_options = [color for color in self.nonstocked_stone_data[brand].keys()]
        self.ns_stone_color.set(self.color_options[0])
        print(brand)
    

    def set_material(self,event):
        index = self.pricingTabControl.index('current')
        if index == 0:
            self.material = 'Self Edge'
        elif index == 1:
            self.material = 'Stone'
        print(self.material)




    def import_pricing_data(self):
        self_edge_data_json = r"jsons\lam_pricing_data.json"
        stone_data_json = r"jsons\stone_pricing_data.json"
        self.data_jsons = {'Self Edge': self_edge_data_json, 'Stone': stone_data_json}
        self.pricing_data = {}
        """This imports the pricing structures saved under 'data_json' and saves them as 'self.pricing_data' """
        with open(self_edge_data_json,"r") as se_pricing_data:
            self.pricing_data['Self Edge'] = json.load(se_pricing_data)
        with open(stone_data_json,"r") as stone_pricing_data:
            self.pricing_data['Stone'] = json.load(stone_pricing_data)
    def lam_quote(self,sqft,multiplier):
        


        # info for pricing structures on stones

        lam_levels = self.pricing_data['Self Edge']["lam_levels"]

        # pricing on add-ons
        add_ons = self.pricing_data['Self Edge']["add_ons"]


        

        #lambda for getting final price of laminate by multiplying level price by sqft, adding in add-ons
        #multiplying by 2 and then multiply by customer multiplier
        get_final_lam_price = lambda material_sqft_cost: math.ceil(
                (((material_sqft_cost * sqft) + sum(add_on_price.values())) * 2) * multiplier)
        

        # takes the entries for the quantities of add-ons and multiplies it by the preset values to get costs of add-ons
        add_on_price = {key: add_ons[key] * self.add_on_quants[key] for key in add_ons}

        #change dictionary of levels to also have a price?

        for level in lam_levels:
            sqft_cost = lam_levels[level]['Price'] #prettify the get final price

            lam_levels[level]['Price'] = get_final_lam_price(sqft_cost)

            #laminate minumum $250 check
            if lam_levels[level]['Price'] < 250:
                full_charge = self.pricing_data['Self Edge']['add_ons']['trip_charge']* multiplier
                current_level_price = lam_levels[level]['Price']
                increase_options = [250 - current_level_price,full_charge] #price is the lower of either the difference or half a trip charge
                price_increase = min(increase_options)
                print(price_increase, 'options where', increase_options)
                lam_levels[level]['Price'] = math.ceil(current_level_price + price_increase)



        # TODO: add in check for prices under $250
        return lam_levels
    def stone_quote(self,sqft,multiplier):
    
        # pre-set values
        fabrication_cost = self.pricing_data['Stone']["fabrication_cost"]
        mark_up = self.pricing_data['Stone']["mark_up"]


        # info for pricing structures on stones

        stone_levels = self.pricing_data['Stone']["stone_levels"]

        # pricing on add-ons
        add_ons = self.pricing_data['Stone']["add_ons"]


        
        # lambda for getting our list price of stone without add-ons
        get_stone_cost = lambda material_sqft_cost: math.ceil(
            (sqft * fabrication_cost) + (((sqft * 1.25) * material_sqft_cost) / mark_up)
        )
        #lambda for getting final price of stone by getting stone cost, adding in add-ons
        #multiplying by 2 and then multiply by customer multiplier
        get_final_stone_price = lambda material_sqft_cost: math.ceil(
                ((get_stone_cost(material_sqft_cost) + sum(add_on_price.values())) * 2) * multiplier)
        

        # takes the entries for the quantities of add-ons and multiplies it by the preset values to get costs of add-ons
        add_on_price = {key: add_ons[key] * self.add_on_quants[key] for key in add_ons}

        #change dictionary of levels to also have a price?

        for stone_level in stone_levels:
            sqft_cost = stone_levels[stone_level]['Price'] #prettify the get final price

            stone_levels[stone_level]['Price'] = get_final_stone_price(sqft_cost)
        return stone_levels



    def print_quote(self):

        
        """Updates and then creates a PDF from a premade excel form used as a template"""
        #TODO: Turn self edge print quote and stone print quote into seperate fucntions for legibility
        if not self.multiplier_ent.get():
            return
        # get entered multiplier
        multiplier = float(self.multiplier_ent.get())

        # load pricing data for quote
        self.import_pricing_data()

        #load edging
        print(self.material)
        if self.material == 'Self Edge':
            
            edge_pricing = self.pricing_data['Self Edge']["edge_pricing"]
        elif self.material == 'Stone':
            edge_pricing = self.pricing_data['Stone']["edge_pricing"]

        print(edge_pricing)


        # get the sqft from the pdf data

        sqft = self.jobData["Total Area"]
        if self.material == 'Self Edge':
            pricing_levels = self.lam_quote(sqft,multiplier)
            #This is to make the linear edging in multiplicatives of 12 as that's what we order the material lengths in
            self.jobData["Finished Lnft"] = math.ceil(self.jobData["Finished Lnft"]*1.333 /12) *12
        elif self.material == 'Stone':
            pricing_levels = self.stone_quote(sqft,multiplier)



        # create pricing for edging
        upgrade_edge_pricing = {
            edge.replace('/', ' or ').replace('_',' ').title()#edge name revised for legibility and formating
                :math.ceil(edge_pricing[edge] * self.jobData["Finished Lnft"]) 
                for edge in edge_pricing
        }

        if self.material == 'Self Edge':
            for edge in upgrade_edge_pricing:
                upgrade_edge_pricing[edge] = math.ceil(upgrade_edge_pricing[edge] * multiplier)
        elif self.material == 'Stone':
            for edge in upgrade_edge_pricing:
                upgrade_edge_pricing[edge] = math.ceil(upgrade_edge_pricing[edge] * 2 * multiplier)
                

        createQuoteFromData(self.jobData,pricing_levels,upgrade_edge_pricing,self.folderpath,self.filepath,self.add_on_quants,self.material)

    def validate_ent(self, input, char):
        """Checks for numerical inputs only"""

        if char in input:
            return True
        elif re.fullmatch(r"^[0-9]$", char):
            return True

        return False

    def validate_multiplier(self, input, char):
        """Regex validaiton for only numeric and . in multiplier entry"""

        if char in input:
            return True
        # check that entered character is only a number or period and return true
        elif re.fullmatch(r"[0-9.]$", char):
            return True

        return False

    def check_multiplier(self, event):
        """Regex check for a valid multiplier"""
        input = self.multiplier_ent.get()

        if input == "":
            return True

        try:
            input = float(input)
        except:
            messagebox.showerror(
                "Invalid Multiplier",
                "Multiplier must be between .5 and .8 and no more than 3 characters after the period (#.###)",
            )
            self.multiplier_ent.focus_set()
        if (
            re.fullmatch(r"^[0]?[.][0-9][0-9]?[0-9]?$", str(input))
            and 0.5 < input < 0.8
        ):
            return True
        messagebox.showerror(
            "Invalid Multiplier",
            "Multiplier must be between .5 and .8 and no more than 3 characters after the period (#.###)",
        )
        self.multiplier_ent.focus_set()

    def select_all_entry(self, event):
        """Selects entire entry in widget"""
        event.widget.select_range(0, tk.END)

    def search_file(self,*args):

        # TODO: Delete args, just for ease of practice use
        if args:
            if os.environ['COMPUTERNAME'] == 'GREGORYLEE':
                self.filepath = r"W:\Ashton\Daniel_Tusing_Job\Pages\Daniel_Tusing_Job_P1.pdf"
                self.folderpath = r"W:\Ashton\Daniel_Tusing_Job\Pages"
            else:
                self.filepath = r"C:\Users\hump_\OneDrive\Documents\GitHub\laminateQuotingSystem\Pricing_Testing_Job.pdf"
                self.folderpath = r"C:\Users\hump_\OneDrive\Documents\GitHub\laminateQuotingSystem"

            self.jobData = extractDataFromPdf(self.filepath)
            self.file_select_text["text"
            ] = f"{self.jobData['Job Name']} for {self.jobData['Customer Name']} is currently selected"
        else:


            """Parses PDF file after selection and calls get_pdf_data to parse and save the data"""
            file = fd.askopenfile(mode="r", filetypes=[("PDF Files", "*.pdf")])
            if file:
                self.filepath = os.path.abspath(file.name)
                self.folderpath = "\\".join(self.filepath.split("\\")[0:-1])

                self.jobData = extractDataFromPdf(self.filepath)
                self.file_select_text["text"
                ] = f"{self.jobData['Job Name']} for {self.jobData['Customer Name']} is currently selected"
            


    def load_directory_frame(self):
        """Creats and grids all objects for directory frame"""
        file_select_btn = tk.Button(
            master=self.directory_frm, text="Select a file", command=self.search_file
        )
        file_select_btn.grid(column=0, row=0, sticky="e")
        self.file_select_text = tk.Label(
            master=self.directory_frm, text="No File Selected"
        )
        self.file_select_text.grid(column=1, row=0, sticky="w")

        
        # TODO: uncomment for testing
        # self.search_file(True)

    def load_multiplier_frame(self):
        """Creats and grids all objects for mutliplier frame"""

        mult_vcmd = (self.master.register(self.validate_multiplier), "%s", "%S")

        self.multiplier_lbl = tk.Label(master=self.multiplier_frm, text="Multiplier")
        self.multiplier_lbl.grid(column=0, row=0, sticky="e")

        self.multiplier_ent = tk.Entry(
            master=self.multiplier_frm, validate="key", validatecommand=mult_vcmd
        )
        self.multiplier_ent.grid(column=1, row=0, sticky="w")
        self.multiplier_ent.bind("<FocusOut>", self.check_multiplier)
        self.multiplier_ent.bind("<FocusIn>", self.select_all_entry)
        
        #enter for ease of running
        # TODO: uncomment for testing
        # self.multiplier_ent.insert(0,'6')
        # self.multiplier_ent.insert(0,'.')
        # self.multiplier_ent.insert(0,'0')

        self.stnd_multipliers_lbl = tk.Label(
            master=self.multiplier_frm,
            text="Standard Multipliers \n"
            + "Wholesale: .525  |  Large K&B: .55  |  Small K&B: .575  |  Builders: .625  |  Local Contractors: .645  |  Retail: .7",
        )
        self.stnd_multipliers_lbl.grid(row=1, column=0, columnspan=2)

    def load_add_on_frame(self,tab,material):
        """Creats and grids all objects for add on frame"""

        vcmd = (
            self.master.register(self.validate_ent),
            "%s",
            "%S",
        )  # validate command for entries


        add_on_data = self.pricing_data[f'{material}']["add_ons"]

        # half point is used to create two columns putting half(+1)in the first column and the rest in the second
        half_point = (math.floor(len(add_on_data) / 2)) + (len(add_on_data) % 2)

        # configure the rows based on half point
        for x in range(half_point):
            tab.rowconfigure(x, weight=1)
        for x in range(4):
            tab.columnconfigure(x, weight=1)

        #reload entries and labels if there are already entries
        if len(self.entries[material]) != 0 or len(self.labels[material]) != 0:
            self.entries[material] = []
            self.labels[material] = []
        # create entries and labels and add to lists
        for data in add_on_data:
            new_entry = tk.Entry(
                master=tab,
                validate="key",
                validatecommand=vcmd,
                name=data,
            )
            self.entries[material].append(new_entry)
            new_entry.insert(0, 0)
            new_entry.bind("<FocusIn>", self.select_all_entry)

            new_label = tk.Label(
                master=tab, text=data.title().replace("_", " ")
            )
            self.labels[material].append(new_label)

        x, z = 0, 0

        # grid the objects
        for n, entry_object in enumerate(self.entries[material]):
            if n >= half_point and n == x:
                x = 0
                z = 2
            self.labels[material][n].grid(column=z, row=x,pady = 3)
            entry_object.grid(column=z + 1, row=x, pady = 3)

            x += 1

    def load_button_frame(self):

        # create and load buttons
        submit_btn = tk.Button(
            master=self.button_frm, text="Submit", command=self.submit_button, width=15
        )
        submit_btn.grid(column=0, row=0, padx=5, sticky="e")
        clear_btn = tk.Button(
            master=self.button_frm, text="Clear", command=self.clear_button_cmd, width=15
        )
        clear_btn.grid(column=1, row=0, padx=5)
        advanced_btn = tk.Button(
            master=self.button_frm,
            text="Advanced",
            command=self.advanced_button_cmd,
            width=15,
        )
        advanced_btn.grid(column=2, row=0, padx=5, sticky="w")

    def clear_button_cmd(self):
        """This clears all entries on click"""
        for list in self.entries:
            for entry in list:
                entry.delete(0, tk.END)
                entry.insert(0, "0")

    def submit_button(self):
        """Updates self.add_on_quants from the entry widgets and calls self.print_quote()"""
        # create a dictionary of the entries with the corresponding names
        self.add_on_quants = {v._name: int(v.get()) for v in self.entries[self.material]}

        ##print the quote out
        self.print_quote()




    def check_password(self, entered_password_bytes):
        """Checks entered password with json file"""
        # load correct password
        with open(r"jsons\password.json", "r") as pricing_data_json:
            pswrd = json.load(pricing_data_json)

        # password saved and string and then converted to bytes
        pswrd = bytes(pswrd["password"], encoding="utf8")

        # make entered password into bytes
        return bcrypt.checkpw(entered_password_bytes, pswrd)
    
    def advanced_button_cmd(self):
        """Opens window for advanced options""" 
            


        #password check
        passwordbytes = bytes()
        salt = bcrypt.gensalt()

        while not self.check_password(passwordbytes):

            password = tk.simpledialog.askstring("", "Enter password:", show="*")
            
            
            passwordbytes = password.encode("utf-8")

            if password == None:
                break
            elif not self.check_password(passwordbytes):
                messagebox.showerror("Incorrect Password", "Please enter your password")





        self.advanced_window = tk.Toplevel()   
        self.advanced_window.resizable(False,False)
        self.advanced_window.rowconfigure(0,weight=1,pad=10)
        self.advanced_window.rowconfigure(1,weight=1,pad=10)
        self.advanced_window.columnconfigure(0,weight=1,pad=10)
        edit_price_btn = tk.Button(
            self.advanced_window, text="Edit Pricing", command=self.select_material_to_edit
        ).grid(column=0,row=0, sticky='nsew', padx=5, pady=3)
        chnge_pssword_btn = tk.Button(
            self.advanced_window, text="Change Password", command=self.change_password_cmd
        ).grid(column=0,row=1, sticky='nsew', padx=5, pady=3)
    def change_password_cmd(self):
        """Opens frame to update password and save"""
        def submit_password(*args):
            old_pass_txt = old_password_ent.get().strip()
            pass1_txt = new_password_1_ent.get().strip()
            pass2_txt = new_password_2_ent.get().strip()

            # turn entered old password into bytes
            old_pass_bytes = old_pass_txt.encode("utf-8")

            # generate salt
            salt = bcrypt.gensalt()

            # check old password
            if not self.check_password(old_pass_bytes):
                messagebox.showerror(
                    "Incorrect Old Password", "Please enter your most recent password."
                )
                old_password_ent.focus_set()
                old_password_ent.select_range(0, "end")

            # check that new passwords match
            elif pass1_txt != pass2_txt:
                messagebox.showerror(
                    "Passwords did not match",
                    "Please make sure both passwords are entered correctly",
                )
                new_password_1_ent.focus_set()
                new_password_1_ent.select_range(0, "end")

            # if both pass the check, save new password
            else:
                # creates bytes
                new_pswrd_bytes = pass1_txt.encode("utf-8")
                # create hash
                new_hash_pswrd = bcrypt.hashpw(new_pswrd_bytes, salt)
                # convert hash to string for json
                new_hash_pswrd_str = new_hash_pswrd.decode()

                # update json (i currently have it rewriting all data just for simplicity, could only update the pricing data for effeciency)

                # create dicitonary with new password
                json_dict = dict(password=new_hash_pswrd_str)

                # create json item
                json_dict = json.dumps(json_dict, indent=4)

                # rewrite json
                with open(r"jsons\password.json", "w") as pricing_data_json:
                    pricing_data_json.write(json_dict)

                # this is a verification that the password saved correctly
                if self.check_password(new_pswrd_bytes):
                    messagebox.showinfo(
                        "Password Saved", "Password saved successfully."
                    )
                else:
                    messagebox.showinfo(
                        "Password Error", "Unable to save password. Please try again."
                    )

                self.edit_pswrd_frame.destroy()
                self.advanced_window.focus_set()

        def cancel_button():
            self.edit_pswrd_frame.destroy()


        self.edit_pswrd_frame = tk.Toplevel()
        self.edit_pswrd_frame.resizable(False,False)
        old_password_lbl = tk.Label(
            self.edit_pswrd_frame, text="Enter your old password:"
        ).grid(row=0, column=0)
        old_password_ent = tk.Entry(self.edit_pswrd_frame, show="*")
        old_password_ent.grid(row=0, column=1)

        new_password_1_lbl = tk.Label(
            self.edit_pswrd_frame, text="Please enter your new password:"
        ).grid(row=1, column=0)
        new_password_1_ent = tk.Entry(self.edit_pswrd_frame, show="*")
        new_password_1_ent.grid(row=1, column=1)

        new_password_2_lbl = tk.Label(
            self.edit_pswrd_frame, text="Please enter your new password again:"
        ).grid(row=2, column=0)
        new_password_2_ent = tk.Entry(self.edit_pswrd_frame, show="*")
        new_password_2_ent.grid(row=2, column=1)
        new_password_2_ent.bind('<Return>',submit_password)

        

        submit_password_btn = tk.Button(
            self.edit_pswrd_frame, text="Submit Password", command=submit_password
        ).grid(row=3, column=0)
        cancel_password_btn = tk.Button(
            self.edit_pswrd_frame, text="Cancel", command=cancel_button
        ).grid(row=3, column=1)



    def select_material_to_edit(self):
        self.advanced_window.destroy()
        self.import_pricing_data()
        self.material_price_select_frm = tk.Toplevel()
        self.material_price_select_frm.resizable(False,False)
        self.material_price_select_frm.columnconfigure(0,weight=1)
        for n,material in enumerate(self.pricing_data):
            self.material_price_select_frm.rowconfigure(n, weight=1)
            btn = tk.Button(self.material_price_select_frm, text=material, command= lambda material = material: self.open_info_edit(material),height=2,width=15)
            btn.grid(row=n,column=0, sticky ='nsew',padx = 5, pady = 1.5)

        

        


    def open_info_edit(self,material):
        """Opens window to buttons that updates pricing structure """
        self.material_price_select_frm.destroy()
        



        # window no frame
        self.edit_info_btn_page = tk.Toplevel()
        self.edit_info_btn_page.resizable(False,False)
        for z, data in enumerate(self.pricing_data):
            self.edit_info_btn_page.rowconfigure(z, weight=1,pad=10)
        self.edit_info_btn_page.columnconfigure(0, weight=1)
        self.edit_info_btn_page.columnconfigure(1, weight=1)


        # lsit of buttons for later?
        btns = []

        if material == 'Self Edge':
            button_organizer = [
                    Material_Level_Button,
                    Edge_and_Add_On_Button,
                    Edge_and_Add_On_Button
                ]
        elif material == 'Stone':

            button_organizer = [
                    Fab_Cost_Mark_Up_button,
                    Fab_Cost_Mark_Up_button,
                    Material_Level_Button,
                    Edge_and_Add_On_Button,
                    Edge_and_Add_On_Button
                ]
        # make and add buttons to list
        for z, data in enumerate(self.pricing_data[material]):

            crnt_btn = button_organizer[z]

            btns.append(crnt_btn(
                    self.edit_info_btn_page, self.pricing_data,material, self, data
                ))

        # pack buttons onto window


        half_point = math.ceil(len(btns)/2)
        rw = 0
        col = 0

        for n, btn in enumerate(btns):
            if n >= half_point:
                col = 1
                rw = n - half_point
            else:
                rw = n
            
            
            btn.grid(row=rw, column=col, sticky ='nsew',padx = 5, pady = 1.5)



if __name__ == '__main__':
    my_window = tk.Tk()

    new_quote = QuoteGenerator(my_window)
    my_window.mainloop()
