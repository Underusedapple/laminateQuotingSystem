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
        final_flat_finished_lnft = float()

        
        
        
        pdf_reader = PyPDF2.PdfReader(file)



        for page in range(len(pdf_reader.pages)):
            page_obj = pdf_reader.pages[page]
            text = page_obj.extract_text()


            #get job name 
            job_name = text.split('Job Name:\n')[1].split('Customer Name:')[0]
            customer_name = text.split('Customer Name:\n')[1].split('Customer Phone:')[0]



            lines = text.split('\n') #convert to list
            lines.reverse() #lines is reversed to speed up large files because the key is last in the text files



            for line in lines:
                if "Total Area" in line and re.search(r'\b\d+(?:\.\d+)?\b', line):
                        total_area = re.search(r'\b\d+(?:\.\d+)?\b', line)
                        total_area = float(total_area[0])
                        final_total_area += total_area
                        break #"Total Area" is the first key and since order is reversed break skips to next page
                        
                elif "Wall" in line and re.search(r'\b\d+(?:\.\d+)?\b', line):
                        wall_lnft = re.search(r'\b\d+(?:\.\d+)?\b', line)
                        wall_lnft = float(wall_lnft[0])
                        final_wall_lnft += wall_lnft
                elif "Finished" in line and re.search(r'\b\d+(?:\.\d+)?\b', line):
                        finished_lnft = re.search(r'\b\d+(?:\.\d+)?\b', line)
                        finished_lnft = float(finished_lnft[0])
                        final_finished_lnft += finished_lnft
                elif "Flat Finish" in line and re.search(r'\b\d+(?:\.\d+)?\b', line):
                        flat_finished_lnft = re.search(r'\b\d+(?:\.\d+)?\b', line)
                        flat_finished_lnft = float(flat_finished_lnft[0])
                        final_flat_finished_lnft += flat_finished_lnft


    data = {
        "Customer Name": customer_name.replace('\n',''),
        "Job Name": job_name.replace('\n',''),
        "Total Area": final_total_area,
        "Wall Lnft": final_wall_lnft,
        "Finished Lnft": final_finished_lnft,
        "Flat Finished Lnft": final_flat_finished_lnft
    }

    return data


if __name__ == "__main__":
    # Usage example
    single_page = 'Pricing_Testing_P1.pdf'
    multi_page = 'Pricing_Testing_Job.pdf'
    extracted_data = extractDataFromPdf(single_page)
    extracted_data2 = extractDataFromPdf(multi_page)
    print(extracted_data)
    print(extracted_data2)
