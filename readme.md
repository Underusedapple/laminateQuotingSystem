# laminateQuotingSystem

As of 5-31-23 I still need to clean up the comments in the functions and create more legibility. 


laminateQuotingSystem is a program using html, css, and python.

Ironically this started for pricing laminate but it currently funcitons for quoting stone but will soon actually be converted for both.
The quotes are made from a pdf created by a outsdie program called LT3Raptor which is a CAD drawing software that Fenco uses.

Running main.py opens a QuoteForm tkinter window which is your main window.

There is a pdf in the main file called "Pricing_testing_Job.py" that can be used to test the program. 


# Usage
## Before using
!!
You will need to change pdfkit_config in createQuoteFromData.py to the file path for your wkhtmltopdf.exe for now. I have not yet moved it to a local folder!!

Here is a breakdown of the buttons and entries:


# Main Window Buttons (QuoteForm)


## Select a file (QuoteForm.file_select_btn) 
Opens a directory to select pdf file.
This is where you select the pdf for your quote to be generated from. A file must be selected to generate a quote
The data from the file is immediately added to the Class as QuoteForm.jobData
Additional QuoteForm.filepath is saved as the path to the file itself and QuoteForm.folderpath is the folder that contains the file path.

## Multiplier Entry (QuoteForm.multiplier_ent)
This is a multiplier for the type of customer requesting a quote. Running the file is not depending on this more than equations though the entry must be a float number that is ".5 <> .8".

## Add-ons Entries
All of the entries (and corresponding labels) are created in QuoteForm.load_multiplier_frame. They are dynamically created in correspondence with a json file that can be accessed through the main window (see "Advanced Button").
These are things that are "add-ons" to the base of the stone price.

## Submit Button (QuoteForm.submit_btn)
This button takes all the data from the entries on the main window, QuoteForm.jobData, and preset information from pricing_data.json to compile the pricing for a quote. 
This calls in createQuoteFromData.py which will takes the premade html and style sheet in the pages folder to create a quote. The quote has two pages and also add the drawing to to the end of the .pdf file.

## Clear Button (QuoteForm.clear_btn)
This clears all the entries in the add-ons frame. This does not affect the multiplier or file selection.

## Advanced Button (QuoteForm.advanced_btn)
!Please note all of the GUI side of anything behind the advanced button is not really touched so it is quite ugly at the moment!
This opens a tk.TopLevel() (QuoteForm.advanced_window) and is populated with two buttons "Edit Pricing" (QuoteForm.advanced_window.edit_price_btn) and "Change Password" (QuoteForm.advanced_window.chnge_pssword_btn).

# Advanced Window Buttons (QuoteForm.advanced_window)

## Edit Pricing (QuoteForm.advanced_window.edit_price_btn)
This opens a simple dialog for a password (currently defaulted to "password")
After entering the correct password a tk.TopLevel() (QuoteForm.edit_info_btn_page) which is then populated with 5 buttons. These buttons do not have python variable names and are never referenced other than being clicked. I have not had a reason to change them.

## Change Password (QuoteForm.advanced_window.chnge_pssword_btn)
This opens a simple dialog for a password (currently defaulted to "password")
After entering the correct password a tk.TopLevel (QuoteForm.edit_pswrd_frame) is created with 3 Entries. You need to first enter the old password and then a new password twice which must match. There is no check for using the same or similar passwords and there is currently no limitations set on the password.
!Please note! This password encryptiona and security is extremely crude. This form does not contain any high level importance information. Only pricing structure information. It is more of a formality to keep only those trusted from changing the data. I do need to add some security layers tot he .json files to help that which is not currently implemented.

# Edit Info Button Page (QuoteForm.edit_info_btn_page)
This page is extremely informal. There are 5 buttons with not variable names. The are created by a list:
    button_organizer = [
    Fab_Cost_Mark_Up_button(),
    Fab_Cost_Mark_Up_button(),
    Stone_Level_Button(),
    Edge_and_Add_On_Button(),
    Edge_and_Add_On_Button()]
That is looped and creates each button with paramaters necessary.

Fab_Cost_Mark_Up_button is from Fab_Cost_Mark_Up_button.py
Stone_Level_Button is from Stone_Level_Button.py
Edge_and_Add_On_Button is from Edge_and_Add_On_Button.py

Each button has a button class that creates a window commanded by "self.button_do()" You can see each individual class for the specifics on what they do, but generically each button opens a new window that displays one of 5 classifications of pricing;
Fabrication Cost, Mark Up, Stone Levels (pricing per stone tier), Edge Pricing (pricing per edge style tier), and Add-ons. 
The data is displayed in either entries or a text box that can be altered.
Stone_Level_Button and Edge_and_Add_On_Button have a button to add and row and delete a row. This deletes the bottom most row and adds to the bottom respectively. Please note that changing the add-on does reload the add-on frame and upon saving it will reload. 
!!All pricing changes are live after hitting submit and will appear upon submitting for a new quote.!!
The quote is also dynamic that adding more row will not run it off the edge of the page, however at some point the text does get to small to read. It does reach a limitation that does eventually run off the page but the text is too small to be legible by that point anyways and a restructuring would be necessary.


# Imports

    pip install bs4
    pip install pdfkit
    pip install os
    pip install PyPDF2
    pip install json
    pip install tkinter
    pip install re
    pip install math
    pip install bcrypt