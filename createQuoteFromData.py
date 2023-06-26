#TODO:add in pdf viewer to select pages. Allow user to select pages to quote, and to do multiple quotes doing multiple pages. Also create a button for quote all pages or all pages seperately.
# TODO: add dynamic naming for same file name, add space to enter add-ons into quote, edit 'fingerprint' page
# TODO: add in ability for a user to enter the file path for wkhtmltopdf.exe????
# TODO: make sure pricing is dynamic to include if price is under $250
from bs4 import BeautifulSoup
import pdfkit
import os
import math
from PyPDF2 import PdfMerger
from datetime import date

def createQuoteFromData(jobData, stone_dict, edging_dict,folder_path,file_path, add_on_dict, material):
    # Read the HTML file

    

    if jobData['Customer Name']:
        customerName = jobData['Customer Name']
    else:
        customerName = 'Customer Name'

    if jobData['Job Name']:
        jobName = jobData['Job Name']
    else:
        jobName = 'Job Name'

    with open(r"pages\pricing_rough.html", 'r') as file:
        pricing_page_content = file.read()

    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(pricing_page_content, 'html.parser')

    tier_label = soup.find(id='tier-label')

    tier_label.string = f'Stocked {material} Tiers'
    
    # Populate granite tiers
    customer_information = soup.find(id='customer-information')
    
    
    maxFontSize = 17


    # Get the font size
    def getFontSize(numberOfRows: int, maxFontSize):
        #if the number of rows is less than minRows the max row size will kick in
        minRows = 8 #number of row before the scaling kicks in
        if numberOfRows <= minRows:
            output = maxFontSize

        else:
            output = maxFontSize - ((numberOfRows - minRows) / minRows) * minRows
        return output

    font_size = getFontSize(len(stone_dict),maxFontSize)

    #populate pricing row
    infoRow = soup.new_tag('tr')
    customer_name = soup.new_tag('td')
    customer_name.string = customerName

    infoRow.append(customer_name)
    job_name = soup.new_tag('td')
    job_name.string = jobName

    infoRow.append(job_name)
    est_sqft = soup.new_tag('td')
    est_sqft.string = f"{math.floor(jobData['Total Area'])} sqft"
    infoRow.append(est_sqft)
    customer_information.append(infoRow)



    # Populate  tiers
    tiers = soup.find(id='stone-tiers')
    for tier in stone_dict:


        row = soup.new_tag('tr')
        customer_name = soup.new_tag('td')
        customer_name.string = stone_dict[tier]['Name']
        customer_name["style"] = f"font-size: {font_size}px;"





        row.append(customer_name)
        job_name = soup.new_tag('td')
        job_name.string = f"${stone_dict[tier]['Price']}"
        job_name["style"] = f"font-size: {font_size}px;"




        row.append(job_name)
        est_sqft = soup.new_tag('td')
        est_sqft.string = ', '.join(stone_dict[tier]['Color'])
        est_sqft["style"] = f"font-size: {font_size}px;"





        row.append(est_sqft)
        tiers.append(row)


    # Populate edge options
    edge_options = soup.find(id='edge-options')

    #Basic Edge always as included first

    easedEdgeRow = soup.new_tag('tr')
    eased_option_name = soup.new_tag('td')

    if material == 'Self Edge':
        eased_option_name.string = "Self Edge"
    elif material == 'Stone':
        eased_option_name.string = "Eased"
    easedEdgeRow.append(eased_option_name)



    eased_price = soup.new_tag('td')
    eased_price.string = "Included"
    easedEdgeRow.append(eased_price)


    #commit to table
    edge_options.append(easedEdgeRow)


    
    for option in edging_dict:



        row = soup.new_tag('tr')
        edging_name = soup.new_tag('td')
        edging_name.string = option
        row.append(edging_name)

        edging_price = soup.new_tag('td')
        edging_price.string = f"${edging_dict[option]}"
        row.append(edging_price)
        edge_options.append(row)



    fingerprint_section = soup.find(id= 'fingerprint')
    price_includes = "**Prices Incude: "
    price_excludes = "**Prices Exclude: "

    if material == 'Self Edge':
        included_text = '3/4" Particleboard Construction and Regular Route Warehouse Delivery'
        excluded_text = 'Site Delivery (unless noted on page 2), Distribution, Measuring, or Installation'
    elif material == 'Stone':
        included_text = 'Templating, Fabrication, Standard Finish, and Installation'
        excluded_text = '''Removal Of Existing Tops, Brackets, Supports, Carpentry Work, Appliance Placement, Plumbing & Electrical Hookup, Or Equipment & Operator To Lift 
                        Countertops For Upper Level Installations. Customer Must Advise If Area Of Installation Requires Access Via Stairs / Steps. Fenco'S Competitive Prices
                        Are Acheived Through A Balance Of Layout Design And Maximizing Material Yields. Customer Specified Seam Locations, Layout Design, And/Or Special Slab
                        Selections May Impact Material Yields And Increase Costs Resulting In Additional Charges.'''



    fp1 = soup.new_tag('p1')
    fp2 = soup.new_tag('p2')
    fp3 = soup.new_tag('p1')
    fp4 = soup.new_tag('p2')
    line1 = soup.new_tag('p')
    line2 = soup.new_tag('p')
    # fp_parts = [fp1,fp2,fp3,fp4]
    fp1.string, fp2.string,fp3.string,fp4.string = price_includes,included_text,price_excludes,excluded_text
    # fp1= price_includes
    # fp3= price_excludes
    

    line1.append(fp1)
    line1.append(fp2)
    line2.append(fp3)
    line2.append(fp4)

    fingerprint_section.append(line1)
    fingerprint_section.append(line2)
    # for section in fp_parts:
        # fingerprint_section.append(section)






    with open(r"pages\pricing_page.html", 'w') as file:
        file.write(str(soup))

    #clear soup
    
    soup.clear(decompose=True)



#create page 2
    with open(r"pages\add_ons_rough.html", 'r') as file:
        add_on_page_content = file.read()

    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(add_on_page_content, 'html.parser')
    # Populate  tiers
    add_on_table_1 = soup.find(id='add-ons1')
    add_on_table_2 = soup.find(id='add-ons2')
    

    getNumAddOnRows = lambda adDict: len(adDict) / 2 + len(add_on_dict)%2
    add_on_rows = getNumAddOnRows(add_on_dict)
    getFontSize(add_on_rows,18)


    for n,add_on in enumerate(add_on_dict):
        

        row = soup.new_tag('tr')
        add_on_name = soup.new_tag('td')
        add_on_name.string = add_on.title().replace("_", " ")
        add_on_name["style"] = f"font-size: {font_size}px;"





        row.append(add_on_name)
        add_on_quant = soup.new_tag('td')
        add_on_quant.string = str(add_on_dict[add_on])
        add_on_quant["style"] = f"font-size: {font_size}px;"


        row.append(add_on_quant)
        if n%2:
            add_on_table_1.append(row)
        else:
            add_on_table_2.append(row)



    with open(r"pages\add_on_page.html", 'w') as file:
        file.write(str(soup))

    #this is to bypass when i use my person computer vs using my work computer
    #the configuration is necessary regardless of using two different computers
    # TODO:replace pdfkit_config with the file path to your wkhtmltopdf.exe 
    if os.environ['COMPUTERNAME'] == 'GREGORYLEE':
        pdfkit_config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files (x86)\wkhtmltopdf\bin\wkhtmltopdf.exe')
    else:
        pdfkit_config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')

    #create pdf
    pages = [r"pages\pricing_page.html", r"pages\add_on_page.html" ]
    page_pdf_files = [] #this will be the file paths of the pdfs created
    for n,page in enumerate(pages):
        page_pdf_file = page.replace('.html','.pdf')
        page_pdf_files.append(page_pdf_file)
        pdfkit.from_file(f"{page}",
                        page_pdf_file, 
                        configuration=pdfkit_config, 
                        options={  "enable-local-file-access": "",
                                    "page-size": "A4",
                                    "margin-top": "1.25in",
                                    "margin-right": "0.00in",
                                    "margin-bottom": ".285in",
                                    "margin-left": "0.00in",
                                    "header-html": r"pages\header.html",
                                    "header-spacing" : "0",
                                    "footer-right": "[page] of [topage]",
                                    "footer-html": r"pages\footer.html",
                                    "footer-spacing": "0"})


    #merge outputted pdf and 
    merger = PdfMerger()
    for page_pdf in page_pdf_files:
        merger.append(f'{page_pdf}')##add quote to merger
    merger.append(file_path)##add orginal pdf drawing to merger


    #create date
    todaysDate = date.today().strftime('%m-%d-%Y')


    #new path name
    new_file_path = fr"{folder_path}\{customerName}_{jobName}_StoneQuote_{todaysDate}.pdf"

    #check for existing path
    quoteVersion = 1
    filePathCheck = new_file_path
    #if file path exists
    while os.path.exists(filePathCheck):
        filePathCheck = new_file_path.replace(".pdf",f"({quoteVersion}).pdf") #change create new file name
        quoteVersion += 1

    new_file_path = filePathCheck #after check passes we change the original


    #write final quote file
    merger.write(new_file_path)


    merger.close()


    os.remove(r"pages\pricing_page.html")

    os.remove(r"pages\add_on_page.html")



    for page_pdf in page_pdf_files:
        os.remove(f'{page_pdf}')
    

    os.startfile(new_file_path)

    
