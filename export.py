from PyPDF2 import PdfFileReader, PdfFileWriter
import csv
import re


def convert_PDFpage_ToStringList(myfile, pageIndex):
    reader = PdfFileReader(myfile)
    num_of_pages = reader.numPages
    pages = list(range(0, reader.numPages))
    txt = reader.getPage(pages[pageIndex]).extractText()
    return txt.splitlines()


def get_startEndIndex_withRegExp(stringList, regExp):
    start_idx = [i for i, item in enumerate(
        stringList) if re.search(regExp[0], item)]
    end_idx = [i for i, item in enumerate(
        stringList) if re.search(regExp[1], item)]
    return [start_idx[0], end_idx[0]]


def get_pageIndex_withRegExp(myfile, regExp):
    reader = PdfFileReader(myfile)
    num_of_pages = reader.numPages
    pages = list(range(0, reader.numPages))
    # print(pages)
    n = 0
    while True:
        txt = reader.getPage(pages[n]).extractText()
        txt_lineList = txt.splitlines()
        # print(txt_lineList)
        try:
            # print(txt_lineList[0],'--',txt_lineList[1],'--',txt_lineList[2])
            if regExp[1] == 'not':
                if txt_lineList[0] == regExp[0]:
                    break
            if (txt_lineList[0] == regExp[0] and txt_lineList[2] == regExp[1]):
                break
        except IndexError:
            pass
        if n == num_of_pages-1:
            break
        n += 1
    return n


def get_regExp_fromStringList(stringList, startIdx, endIdx):
    n = range(startIdx, endIdx)
    listOfInterest = [stringList[i] for i in n]
    return ''.join(listOfInterest)
    
def get_stringList(stringList, startIdx, endIdx):
    n = range(startIdx, endIdx)
    return [stringList[i] for i in n]

def compare_date(mpPlanString, moPlanString, regExpDate):
    idx = get_startEndIndex_withRegExp(mpPlanString, regExpDate)
    # print(idx)
    n = range(idx[0], idx[1])
    mp_date = get_regExp_fromStringList(mpPlanString, idx[0],idx[1])
    mo_date = get_regExp_fromStringList(moPlanString, idx[0],idx[1])
    #print(mp_date)
    # print(mo_date)
    boolean = True
    if mp_date == mo_date:
        pass
    else:
        boolean = False
    return boolean, mp_date, mo_date


firstPage = ['Plan Overview', 'not']
chapter3 = ['Chapter ', 'Plan']
moPDF = 'Mosaiq.pdf'
mpPDF = 'PlanOverview.pdf'
list_forDate = ['Date Plan Saved', 'Created in Version']
list_prescription_mp = [['Planned Fractions', 'HFS'], ['Tracking Method', 'Alignment Center '], ['Prescribed Plan Dose ', 'Reference Point '], ['Sequential', 'Number of Segments']]

# Get Page index of pdf using regular express
i0_mosaiq = get_pageIndex_withRegExp(moPDF, firstPage)
i0_mp = get_pageIndex_withRegExp(mpPDF, firstPage)
i_plan_mosaiq = get_pageIndex_withRegExp(moPDF, chapter3)
i_plan_mp = get_pageIndex_withRegExp(mpPDF, chapter3)

# extract and convert the wanted page of the pdf
mp_plan_string = convert_PDFpage_ToStringList(mpPDF, i_plan_mp)
mo_plan_string = convert_PDFpage_ToStringList(moPDF, i_plan_mosaiq)
# print(i0_mosaiq,i0_mp,i_plan_mosaiq,i_plan_mp)

idx_frac = get_startEndIndex_withRegExp(mp_plan_string,list_prescription_mp[0])
a = get_stringList(mp_plan_string,idx_frac[0],idx_frac[1])
fraction = ' '.join([a[0],a[1],a[6]])
path = ' '.join(get_stringList(a,7,len(a)))
print(path, fraction)
print(a)
# identical date plan saved between multiplan and mosaiq ? date_output [True/False, mp_datePlan, mo_datePlan]
date_output = compare_date(mp_plan_string, mo_plan_string, list_forDate)
print(date_output)
#print(mp_plan_string)


def Extract_MainPage_toStringList(myfile, initialPage):
    reader = PdfFileReader(myfile)
    num_of_pages = reader.numPages
    mainPageIndex = 3
    indexMainPage = initialPage + mainPageIndex
    txt = reader.getPage(actualMainPageIndex).extractText()
    return txt.splitlines()


def Fitted_MosaiqPDF_toMultiplanPDF(myfile, numberOfPages, start):
    file_base_name = myfile.replace('.pdf', '')
    mosaiq_subset = '{0}_subset.pdf'.format(file_base_name)
    reader = PdfFileReader(myfile)
    pages = list(range(start, start+numberOfPages))
    pdf_writer = PdfFileWriter()
    for page_num in pages:
        pdf_writer.addPage(reader.getPage(page_num))
    with open(mosaiq_subset, 'wb') as f:
        pdf_writer.write(f)
        f.close()
    return mosaiq_subset


def Get_MultiplanPDF_NumberOfPages(myfile):

    reader = PdfFileReader(myfile)
    num_of_pages = reader.numPages
    print(reader.documentInfo)
    # txt=reader.getPage(0-3).extractText()
    return num_of_pages


'''
nPages = Get_MultiplanPDF_NumberOfPages('PlanOverview.pdf')

print('Number of pages: ' + str(nPages))
Mosaiq_file= Fitted_MosaiqPDF_toMultiplanPDF('Mosaiq.pdf',nPages,1)
nPages = Get_MultiplanPDF_NumberOfPages(Mosaiq_file)
print('Number of pages: ' + str(nPages))
'''
