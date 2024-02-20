import PyPDF2
import re

def extractDataFromPdf(file_path: str) -> dict :
    """Takes file_path to pdf file and returns the last instance of the float found on a line starting with
    'Total Area', 'Wall', 'Finished Lnft', and 'Flat Finished Lnft' in a dictionary with keys of the same
    Output: {
        "Total Area": float(final_total_area),
        "Wall Lnft": float(final_wall_lnft),
        "Finished Lnft": float(final_finished_lnft),
        "Flat Finished Lnft": float(final_flat_finished_lnft)
    }
"""
    with open(file_path, 'rb') as file:
        final_total_area = float()
        final_wall_lnft = float()
        final_finished_lnft = float()
        final_flat_finish_lnft = float()
        final_KD_lnft = float()
        final_KDDeck_lnft = float()
        final_VD_lnft = float()
        final_VDDeck_lnft = float()
        final_twelve_bar_lnft = float()
        final_fifteen_bar_lnft = float()
        final_eighteen_bar_lnft = float()
        final_twenty_six_bar_lnft = float()
        final_twenty_seven_bar_lnft = float()
        final_thirty_two_bar_lnft = float()
        final_thirty_six_bar_lnft = float()
        final_forty_two_bar_lnft = float()
        final_forty_five_bar_lnft = float()





        #remember to put a post-form check to avoid pricing issues later
        
        
        pdf_reader = PyPDF2.PdfReader(file)



        for page in range(len(pdf_reader.pages)):
            page_obj = pdf_reader.pages[page]
            text = page_obj.extract_text()


            #get job name 
            job_name = text.split('Job Name:\n')[1].split('Customer Name:')[0]
            customer_name = text.split('Customer Name:\n')[1].split('Customer Phone:')[0]



            lines = text.split('\n') #convert to list
            lines.reverse() #lines is reversed to speed up large files because the key is last in the text files


    def extract_and_accumulate(line, keyword):
        pattern = r'{}:\s*(\d+(?:\.\d+)?)'.format(re.escape(keyword))
        match = re.search(pattern, line)
        if keyword in line and match:
            value = float(match.group(1))
            return value
        else:
            return 0

    for line in lines:
        
        final_total_area += extract_and_accumulate(line, 'Total Area')
        final_wall_lnft += extract_and_accumulate(line, 'Wall')
        final_finished_lnft += extract_and_accumulate(line, "Finished")
        final_flat_finish_lnft += extract_and_accumulate(line, "Flat Finish")
        final_KD_lnft += extract_and_accumulate(line, "Kitchen Depth")
        final_KDDeck_lnft += extract_and_accumulate(line, "Kitchen Depth Deck")
        final_VD_lnft += extract_and_accumulate(line, "Vanity Depth")
        final_VDDeck_lnft += extract_and_accumulate(line, "Vanity Depth Deck")
        final_twelve_bar_lnft += extract_and_accumulate(line, '12" Bar')
        final_fifteen_bar_lnft += extract_and_accumulate(line, '15" Bar')
        final_eighteen_bar_lnft += extract_and_accumulate(line, '18" Bar')
        final_twenty_six_bar_lnft += extract_and_accumulate(line, '26" Bar')
        final_twenty_seven_bar_lnft += extract_and_accumulate(line, '27" Bar')
        final_thirty_two_bar_lnft += extract_and_accumulate(line, '32" Bar')
        final_thirty_six_bar_lnft += extract_and_accumulate(line, '36" Bar')
        final_forty_two_bar_lnft += extract_and_accumulate(line, '42" Bar')
        final_forty_five_bar_lnft += extract_and_accumulate(line, '45" Bar')


    if final_wall_lnft or final_finished_lnft or final_flat_finish_lnft:
        data = {
            "Customer Name": customer_name.replace('\n',' '),
            "Job Name": job_name.replace('\n',' '),
            "Total Area": final_total_area,
            "Wall Lnft": final_wall_lnft,
            "Finished Lnft": final_finished_lnft,
            "Flat Finished Lnft": final_flat_finish_lnft
        }
    else:
        data = {
            "Customer Name": customer_name.replace('\n',' '),
            "Job Name": job_name.replace('\n',' '),
            "Kitchen Depth": final_KD_lnft,
            "Kitchen Depth Deck": final_KDDeck_lnft,
            "Vanity Depth": final_VD_lnft,
            "Vanity Depth Deck": final_VDDeck_lnft,
            '12" Bar': final_twelve_bar_lnft,
            '15" Bar': final_fifteen_bar_lnft,
            '18" Bar': final_eighteen_bar_lnft,
            '26" Bar': final_twenty_six_bar_lnft,
            '27" Bar': final_twenty_seven_bar_lnft,
            '32" Bar': final_thirty_two_bar_lnft,
            '36" Bar': final_thirty_six_bar_lnft,
            '42" Bar': final_forty_two_bar_lnft,
            '45" Bar': final_forty_five_bar_lnft
        }

    return data


if __name__ == "__main__":
    # Usage example
    single_page = 'Pricing_Testing_P1.pdf'
    multi_page = 'Pricing_Testing_Job.pdf'
    post_form_page = 'Testing_Post-form_Stuff_P1.pdf'
    # extracted_data = extractDataFromPdf(single_page)
    extracted_data2 = extractDataFromPdf(multi_page)
    extracted_data3 = extractDataFromPdf(post_form_page)

    # print(extracted_data)
    print(extracted_data2)
    print(extracted_data3)

