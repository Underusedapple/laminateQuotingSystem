#TODO:add in pdf viewer to select pages. Allow user to select pages to quote, and to do multiple quotes doing multiple pages. Also create a button for quote all pages or all pages seperately.
# TODO: add dynamic naming for same file name, add space to enter add-ons into quote, edit 'fingerprint' page
# TODO: make sure pricing is dynamic to include if price is under $250
from bs4 import BeautifulSoup
import time
import asyncio
import pdfkit
import os
import math
from PyPDF2 import PdfMerger
from datetime import date

async def createQuoteFromData(jobData, stone_dict, edging_dict,folder_path,file_path, add_on_dict, material):
    # Read the HTML file

    startTime = time.time()
    asyncLock = asyncio.Lock()
    #add me to async list
    async def appendCustomerInformation():
        """Appends Customer information to page 1"""
        tier_label = pageOneSoup.find(id='tier-label')

        tier_label.string = f'Stocked {material} Tiers'
        
        # Populate granite tiers
        customer_information = pageOneSoup.find(id='customer-information')
    

        #populate pricing row #this needs to go before pricing
        infoRow = pageOneSoup.new_tag('tr')
        customer_name = pageOneSoup.new_tag('td')
        customer_name.string = customerName

        infoRow.append(customer_name)
        job_name = pageOneSoup.new_tag('td')
        job_name.string = jobName

        infoRow.append(job_name)
        est_sqft = pageOneSoup.new_tag('td')
        est_sqft.string = f"{math.floor(jobData['Total Area'])} sqft"
        infoRow.append(est_sqft)
        customer_information.append(infoRow)
        print('hello 1')


    async def appendPricing(tier):
        """Loops through pricing levels and append to soup"""


        row = pageOneSoup.new_tag('tr')
        customer_name = pageOneSoup.new_tag('td')
        customer_name.string = stone_dict[tier]['Name']
        customer_name["style"] = f"font-size: {pricingTableFontSize}px;"





        row.append(customer_name)
        job_name = pageOneSoup.new_tag('td')
        job_name.string = f"${stone_dict[tier]['Price']}"
        job_name["style"] = f"font-size: {pricingTableFontSize}px;"




        row.append(job_name)
        est_sqft = pageOneSoup.new_tag('td')
        est_sqft.string = ', '.join(stone_dict[tier]['Color'])
        est_sqft["style"] = f"font-size: {pricingTableFontSize}px;"





        row.append(est_sqft)
        async with asyncLock:
            tiers.append(row)
        print('hello 2')


    async def appendBaseEdgeRow():
        """Appends base edge option to edge pricing on page 2"""
        easedEdgeRow = pageOneSoup.new_tag('tr')
        eased_option_name = pageOneSoup.new_tag('td')

        if material == 'Self Edge':
            eased_option_name.string = "Self Edge"
        elif material == 'Stone':
            eased_option_name.string = "Eased"
        easedEdgeRow.append(eased_option_name)



        eased_price = pageOneSoup.new_tag('td')
        eased_price.string = "Included"
        easedEdgeRow.append(eased_price)

        async with asyncLock:
            edge_options.append(easedEdgeRow)
        print('hello 3')



    async def appendEdging(option):
        """Loops through edge levels and appends them to soup"""


        row = pageOneSoup.new_tag('tr')
        edging_name = pageOneSoup.new_tag('td')
        edging_name.string = option
        row.append(edging_name)

        edging_price = pageOneSoup.new_tag('td')
        edging_price.string = f"${edging_dict[option]}"
        row.append(edging_price)
        async with asyncLock:
            edge_options.append(row)
        print('hello 4')



    async def appendAddOn(add_on,n):
        

        row = pageTwoSoup.new_tag('tr')
        add_on_name = pageTwoSoup.new_tag('td')
        add_on_name.string = add_on.title().replace("_", " ")
        add_on_name["style"] = f"font-size: {addOnFontSize}px;"





        row.append(add_on_name)
        add_on_quant = pageTwoSoup.new_tag('td')
        add_on_quant.string = str(add_on_dict[add_on])
        add_on_quant["style"] = f"font-size: {addOnFontSize}px;"


        row.append(add_on_quant)
        if n == 1:
            async with asyncLock:
                add_on_table_1.append(row)
        elif n ==2:
            async with asyncLock:
                add_on_table_2.append(row)
        else: 
            print('table count beyond 2 at add-ons in createQuoteFromData')
        print('hello 5')



    async def appendFingerprint():
        fingerprint_section = pageOneSoup.find(id= 'fingerprint')
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

        field_veri_text = '**Price subject to change pending final field verification**'

        fp1 = pageOneSoup.new_tag('p1')
        fp2 = pageOneSoup.new_tag('p2')
        fp3 = pageOneSoup.new_tag('p1')
        fp4 = pageOneSoup.new_tag('p2')
        line1 = pageOneSoup.new_tag('p')
        line2 = pageOneSoup.new_tag('p')




        fp1.string, fp2.string,fp3.string,fp4.string = price_includes,included_text,price_excludes,excluded_text

        line1.append(fp1)
        line1.append(fp2)
        line2.append(fp3)
        line2.append(fp4)

        fingerprint_section.append(line1)
        fingerprint_section.append(line2)




        if material == 'Stone':
            field_ver_line = pageOneSoup.new_tag('p1')
            field_ver_line.string = field_veri_text
            fingerprint_section.append(field_ver_line)
        print('hello 6')
        

    # Get the font size
    def getFontSize(numberOfRows: int, maxFontSize):
        """Returns a px font size based on length of dicitonary with a max font size"""
        #if the number of rows is less than minRows the max row size will kick in
        minRows = 8 #number of row before the scaling kicks in
        if numberOfRows <= minRows:
            output = maxFontSize

        else:
            output = maxFontSize - ((numberOfRows - minRows) / minRows) * minRows
        return output


    #get customer and job informaiton
    if jobData['Customer Name']:
        customerName = jobData['Customer Name']
    else:
        customerName = 'Customer Name'

    if jobData['Job Name']:
        jobName = jobData['Job Name']
    else:
        jobName = 'Job Name'



    #get soups
    #open up pageOneSoup

    with open(r"pages\pricing_rough.html", 'r') as file:
        pricing_page_content = file.read()

    # Parse the HTML using BeautifulSoup
    pageOneSoup = BeautifulSoup(pricing_page_content, 'html.parser')


    #open up pageTwoSoup
    with open(r"pages\add_ons_rough.html", 'r') as file:
        add_on_page_content = file.read()

    # Parse the HTML using BeautifulSoup
    pageTwoSoup = BeautifulSoup(add_on_page_content, 'html.parser')


    #Get tables

    #Find stone-tiers table in soup
    tiers = pageOneSoup.find(id='stone-tiers')

    #Find Edge Options Table in soup
    edge_options = pageOneSoup.find(id='edge-options')

    #Find first column of add-on table in soup
    add_on_table_1 = pageTwoSoup.find(id='add-ons1')

    #Find second column of add-on table in soup
    add_on_table_2 = pageTwoSoup.find(id='add-ons2')
    
    #hard coded max font size
    maxFontSize = 17

    #Get font sizes
    pricingTableFontSize = getFontSize(len(stone_dict),maxFontSize)
    addOnFontSize = getFontSize(len(add_on_dict)//2,maxFontSize)



    appendCustomerInformationTask = asyncio.create_task(appendCustomerInformation())
    appendPricingTasks = [appendPricing(tier) for tier in stone_dict]
    appendBaseEdgeRowTast = asyncio.create_task(appendBaseEdgeRow())
    appendEdgingTasks =  [appendEdging(option) for option in edging_dict]
    appendAddOnTasks = []
    halfLength = len(add_on_dict)//2
    for i,add_on in enumerate(add_on_dict):
        if i <= halfLength:
            appendAddOnTasks.append(appendAddOn(add_on,1))
        else: 
            appendAddOnTasks.append(appendAddOn(add_on,2))
    appendFingerprintTast = asyncio.create_task(appendFingerprint())


    
    await asyncio.gather(appendCustomerInformationTask,*appendPricingTasks,appendBaseEdgeRowTast,*appendEdgingTasks,*appendAddOnTasks,appendFingerprintTast)
    
    async with asyncLock:
    #rewrite this into the code of createPDF and lock that function
        print('hi im starting')
        #write page 1
        with open(r"pages\pricing_page.html", 'w') as file:
            file.write(str(pageOneSoup))

        #write page 2
        with open(r"pages\add_on_page.html", 'w') as file:
            file.write(str(pageTwoSoup))


        #clear soup for cleanliness
        pageOneSoup.clear(decompose=True)
        pageTwoSoup.clear(decompose=True)

        #set pdf configuration
        pdfkit_config = pdfkit.configuration(wkhtmltopdf= r'wkhtmltopdf\bin\wkhtmltopdf.exe')
        
        #create pdfs from html
        htmlFilePaths = [r"pages\pricing_page.html", r"pages\add_on_page.html" ]
        pdfFilePaths = [] #this will be the file paths of the pdfs created

        for htmlPath in htmlFilePaths:  
            print('task started')
            """Takes Html Page after written and converts to pdf"""
            pdfPath = htmlPath.replace('.html','.pdf')
            pdfFilePaths.append(pdfPath)
            pdfkit.from_file(f"{htmlPath}",
                            pdfPath, 
                            configuration=pdfkit_config, 
                            options={  "enable-local-file-access": "",
                                        "page-size": "A4",
                                        "margin-top": "1.25in",
                                        "margin-right": "0.00in",
                                        "margin-bottom": ".55in",
                                        "margin-left": "0.00in",
                                        "header-html": r"pages\header.html",
                                        "header-spacing" : "0",
                                        "footer-right": "[page] of [topage]",
                                        "footer-html": r"pages\footer.html",
                                        "footer-spacing": "0"})
            print(f'made pdf page {pdfPath}')
            #had trouble running the following code outside of function so adding to create pdf function
            #runs when both lists are equal lengths
            if len(pdfFilePaths) == len(htmlFilePaths):
                #merge outputted pdf and 
                merger = PdfMerger()
                for pdfPath in pdfFilePaths:
                    merger.append(fr'{pdfPath}')##add quote to merger
                merger.append(file_path)##add orginal pdf drawing to merger


                #create date
                todaysDate = date.today().strftime('%m-%d-%Y')


                #new path name
                mergedPDFPath = fr"{folder_path}\{customerName}_{jobName}_{material.replace(' ','_')}_Quote_{todaysDate}.pdf"

                #check for existing path
                quoteVersion = 1
                #if file path exists
                while os.path.exists(mergedPDFPath):
                    if quoteVersion == 1:
                        mergedPDFPath = mergedPDFPath.replace(".pdf",f"({quoteVersion}).pdf") #change create new file name
                    else:
                        mergedPDFPath = mergedPDFPath.replace(f"({quoteVersion-1}).pdf",f"({quoteVersion}).pdf") #change create new file name

                    quoteVersion += 1



                #write final quote file
                merger.write(mergedPDFPath)

                endTime = time.time()
                executeTime = endTime-startTime
                print(f'code took {executeTime} to run')
                merger.close()
                for pdfPath in pdfFilePaths:
                    os.remove(f'{pdfPath}')


                for htmlPath in htmlFilePaths:
                    os.remove(f'{htmlPath}')
                
                print(f'starting file {mergedPDFPath}')
                os.startfile(mergedPDFPath)
