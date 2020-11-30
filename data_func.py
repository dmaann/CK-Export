from io import StringIO

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser


from pdfminer.high_level import extract_text
def extractpdf(file_path):
    with open(file_path, 'rb') as in_file:
        text = extract_text(file_path)
    file = open('sample.txt', 'w')
    # writing data using the write() method
    file.write(text)
    # closing the file
    file.close()
    return  text


def convert_pdf_to_string(file_path):

	output_string = StringIO()
	with open(file_path, 'rb') as in_file:
	    parser = PDFParser(in_file)
	    doc = PDFDocument(parser)
	    rsrcmgr = PDFResourceManager()
	    device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
	    interpreter = PDFPageInterpreter(rsrcmgr, device)
	    for page in PDFPage.create_pages(doc):
	        interpreter.process_page(page) 
	return(output_string.getvalue())

                
def convert_title_to_filename(title):
    filename = title.lower()
    filename = filename.replace(' ', '_')
    return filename


def split_to_title_and_pagenum(table_of_contents_entry):
    title_and_pagenum = table_of_contents_entry.strip()
    
    title = None
    pagenum = None
    
    if len(title_and_pagenum) > 0:
        if title_and_pagenum[-1].isdigit():
            i = -2
            while title_and_pagenum[i].isdigit():
                i -= 1

            title = title_and_pagenum[:i].strip()
            pagenum = int(title_and_pagenum[i:].strip())
        
    return title, pagenum

reader = convert_pdf_to_string('PlanOverview.pdf')
reader = convert_pdf_to_string('Mosaiq.pdf')
file = open('sample2.txt', 'w')
file.write(reader) 
file.close()  
#texte = extractpdf('PlanOverview.pdf')
#texte = extractpdf('Mosaiq.pdf')
#print(texte)