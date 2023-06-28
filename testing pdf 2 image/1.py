import os
from PyPDF2 import PdfReader
import pandas as pd
from pdf2image import convert_from_path
import warnings
import logging
import shutil

LARGE_SIZE = (1275, 1650)
PAGE_SIZE = (1148, 1485)
THUMB_SIZE = (77, 100)

#This is a scramble to replace 1.jpg across various folders 
#folders are in place 
#pdfs = pages containing a unique name that can be converted to jpgs
#folder = the folder containing the subfolders for fliphtml
#excel file = (csv in this case) containing the data a) their full name and b) the unique pdf name. 



def main(pdfs : str, folder : str, excel_file : str , large_size : tuple = LARGE_SIZE, page_size : tuple = PAGE_SIZE, thumb_size : tuple = THUMB_SIZE):
    
    #keep pypdf2 from writing stuff to output
    warnings.filterwarnings('ignore')
    logger = logging.getLogger("PyPDF2")
    logger.setLevel(logging.ERROR)
    
    #make paths absolute
    pdfs = os.path.abspath(pdfs)
    excel_file = os.path.abspath(excel_file)
    folder = os.path.abspath(folder)
    
    #Get Data (I know the variable name is excel file but you sent a csv. )
    dt = pd.read_csv(excel_file)
    
    #init dicts
    text_dict ={}
    check_list = {}
    
    #assign dictionary "FullName" : "Variable PDF Name"
    for idx, row in dt.iterrows():
        if check_list.get(row['First Name']) == None:
            check_list[row['First Name']] = row['Variable PDF Name'].replace(".pdf", ".htm")
            
        
    # creating a pdf reader object
    reader = PdfReader(os.path.join(pdfs))
    
   #for each page
    for i in range(0, len(reader.pages)):
        
        #extract text from page
        page = reader.pages[i]
    
        # add text to dictionary of the page number
        text_dict[i] = page.extract_text()
    
        
   #for each name
    for name in check_list.keys():
        #for each page
        for i in text_dict.keys():
            #if the name is in the text of the pdf page
            if name.lower() in text_dict[i].lower():    
                print(name, i)
                
                #make new thumbs
                large = convert_from_path(pdfs, size=LARGE_SIZE, first_page=i +1  , last_page=i +1 )
                pg = convert_from_path(pdfs, size=PAGE_SIZE, first_page=i + 1, last_page=i + 1)
                thumb = convert_from_path(pdfs, size=THUMB_SIZE, first_page=i + 1, last_page=i + 1)
                
                #save n log
                pth = os.path.join(folder, check_list[name], "Files\\large", "1.jpg")
                large[0].save(pth,'JPEG')
                print(f"Saved {name} to {pth}")
                #save n log
                pth = os.path.join(folder,check_list[name],  "Files\\page", "1.jpg")
                pg[0].save(pth,'JPEG')
                print(f"Saved {name} to {pth}")
                #save n log
                pth = os.path.join(folder, check_list[name], "Files\\thumb", "1.jpg")
                thumb[0].save(os.path.join(folder, check_list[name], "Files\\thumb", "1.jpg"),'JPEG')
                print(f"Saved {name} to {pth}")
                # #copy Default Folder to folder named after the Variable PDF section
                # files = os.listdir(folder)
                # try:
                #     shutil.copytree(folder, os.path.join(output_path, check_list[name]))
                # except FileExistsError:
                #     pass
                
if __name__ == "__main__":
    main(pdfs="252180_VariableData_Final.pdf", excel_file="252180-Final-PURLs.csv", folder="Test")