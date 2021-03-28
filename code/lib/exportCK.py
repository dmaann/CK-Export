from PyPDF2 import PdfFileReader, PdfFileWriter
import re
from fpdf import FPDF


def convert_PDFpage_ToStringList(myfile, pageIndex):
    reader = PdfFileReader(myfile)
    # num_of_pages = reader.numPages
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
    #print(pages)
    n = 0
    while True:
        txt = reader.getPage(pages[n]).extractText()
        txt_lineList = txt.splitlines()
        #print(txt_lineList)
        try:
          #  print(txt_lineList[0],'--',txt_lineList[1],'--',txt_lineList[2])
            if regExp[1] == 'not':
                if txt_lineList[1] == regExp[0]:
                    break
            if (txt_lineList[1] == regExp[0] and txt_lineList[3] == regExp[1]):
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


def compare_date(planString, moPlanString, regExpDate):
    idx = get_startEndIndex_withRegExp(planString, regExpDate)
    # print(idx)
    # n = range(idx[0], idx[1])
    mp_date = get_regExp_fromStringList(planString, idx[0]+1, idx[1])
    mo_date = get_regExp_fromStringList(moPlanString, idx[0]+1, idx[1])
    # mp_date_msg = get_regExp_fromStringList(planString, idx[0], idx[1])
    # mo_date_msg = get_regExp_fromStringList(planString, idx[0], idx[1])
    # print(mp_date)
    # print(mo_date)
    boolean = True
    if mp_date == mo_date:
        writableOutput = ['Date sauvegarde du plan identiques ? : ' + str(
            boolean), 'Date du pdf de Multiplan : ' + str(mp_date), 'Date du pdf Mosaiq :        ' + str(mo_date)]
    else:
        boolean = False
        writableOutput = ['PROBLEME : VERIFIER LA CONCORDANCE DU PLAN ET DES PDF', '', 'Date sauvegarde du plan identiques ? : ' + str(boolean),
                          'Date du pdf de Multiplan : ' + str(mp_date), 'Date du pdf Mosaiq :       ' + str(mo_date)]
    return [boolean, mp_date, mo_date], writableOutput


def extract_namedValue(stringList, listIndex):
    # ' '.join(get_stringList(a,7,len(a)))
    value = ' '.join([stringList[i] for i in listIndex])
    return value


def extract_dataPlan(planString, regExpPlan):
    idx_ = get_startEndIndex_withRegExp(planString, regExpPlan[0])
    path_ = get_stringList(planString, idx_[0], idx_[1])
  
    path = extract_namedValue(path_, [6,7,5])
    #print(path)
    collimator = extract_namedValue(path_, [0, 1, 2, 3])
    #print(collimator)
    tracking = extract_namedValue(path_, [len(path_)-1,len(path_)-2])
    #print(tracking)
    idx_ = get_startEndIndex_withRegExp(planString, regExpPlan[1])
    path_ = get_stringList(planString, idx_[0], idx_[1])
    algorithm = extract_namedValue(path_, [0,1])
    #print(algorithm)
    resolution = extract_namedValue(path_, [len(path_)-2,len(path_)-1])
    #print(resolution)
    scaling = extract_namedValue(path_, [2,3])
    #print(scaling)
    idx_ = get_startEndIndex_withRegExp(planString, regExpPlan[2])
    path_ = get_stringList(planString, idx_[0], idx_[1])
    optimizer= extract_namedValue(path_, [0,1])
    #print(optimizer)
    idx_ = get_startEndIndex_withRegExp(planString, regExpPlan[3])
    path_ = get_stringList(planString, idx_[0], idx_[1])
    fraction = extract_namedValue(path_, [2, 7])    
    dose = extract_namedValue(path_, [1,6])
    prescription = extract_namedValue(path_,[0,5])
    MUs= extract_namedValue(path_,[4,9])
    #print(fraction, '\n', dose, '\n', prescription, '\n', MUs)
    time = extract_namedValue(path_, [len(path_)-2,len(path_)-1])

    idx_ = get_startEndIndex_withRegExp(planString, regExpPlan[4])
    path_ = get_stringList(planString, idx_[0], idx_[1])
    beam = extract_namedValue(path_, list(range(0, len(path_))))
    print(resolution, '\n', time, '\n', beam)

    idx_algo_segment = get_startEndIndex_withRegExp(
        planString, regExpPlan[3])
    algo_segment = get_stringList(
        planString, idx_algo_segment[0], idx_algo_segment[1])
    r = re.compile(".*MLC")
    isMLC = list(filter(r.match, planString))
    if not isMLC:  # empty list, i.e. fixed collimator
        minorPagePlan = [collimator, path, algorithm,optimizer,
                         resolution, MUs,time, beam]
    else:  # MLC collimator
        segment = extract_namedValue(algo_segment, list(range(6, 9)))
        minorPagePlan = [collimator, path, algorithm,optimizer,
                         resolution, MUs, time, beam, segment]
    '''print(algorithm, '\n', scaling, '\n', segment)
        print(algo_segment)'''
    majorPagePlan = [fraction, dose, prescription, tracking, scaling]
    # print(majorPagePlan)
    # print(minorPagePlan)
    return majorPagePlan, minorPagePlan


def extractPatientData(patientString, regExpList):
    idx_patient = get_startEndIndex_withRegExp(
        patientString, regExpList[0])
    patient_data = get_stringList(
        patientString, idx_patient[0], idx_patient[1])
    #print(patient_data)
    name = extract_namedValue(patient_data, [0, 1])
    #print(name)
    nameForOutputFile = extract_namedValue(patient_data, [1])
    #print(nameForOutputFile)
    id_ = extract_namedValue(patient_data, list(
        range(len(patient_data)-2, len(patient_data))))

    idx_status = get_startEndIndex_withRegExp(patientString, regExpList[1])
    plan_status = get_stringList(
        patientString, idx_status[0], idx_status[1]+1)
    plan_name = extract_namedValue(plan_status, [0,len(plan_status)-4])
    # print(plan_status)
    plan_nameForOutputFile = extract_namedValue(plan_status, [len(plan_status)-4])
    status = extract_namedValue(plan_status, [1, len(plan_status)-3])
    #print(name, '\n', id_, '\n', plan_name, '\n', status)
    majorCheck = [name, id_, plan_name, status]
    # print(majorCheck)
    return majorCheck, nameForOutputFile, plan_nameForOutputFile


def extractCTData(CTString, regExpList):
    idx_CT_date = get_startEndIndex_withRegExp(CTString, regExpList[0])
    CT_date = get_stringList(CTString, idx_CT_date[0], idx_CT_date[1])
    # print(CT_date)
    idx_position = [0]
    idx_position.extend(list(range(4, len(CT_date)-1)))
    #print(idx_position)
    date = extract_namedValue(CT_date, idx_position)
    #print(date)
    idx_CT_protocol = get_startEndIndex_withRegExp(CTString, regExpList[1])
    CT_protocol = get_stringList(
        CTString, idx_CT_protocol[0], idx_CT_protocol[1])
    # print(CT_protocol)
    idx_position = [0,4,1,5]
    #idx_position.extend(list(range(6, len(CT_protocol)-2)))
    protocol = extract_namedValue(CT_protocol, idx_position)
    #print(protocol)
    majorCheck = [date, protocol]
    # print(majorCheck)
    return majorCheck


def makeReadableMessage(myList):
    msg = '\n'.join([str(i) for i in myList])
    # print(msg)
    return msg


class ExportCyberknife:

    def __init__(self, moPDF, mpPDF, outputDirectory):
        self.moPDF = moPDF
        self.mpPDF = mpPDF
        self.outputDirectory = outputDirectory
        # firstPage = ['Plan Overview', 'not']
        self.chapter1 = ['Patient Name:', 'Medical ID:']
        self.chapter2 = ['X','Z']
        #self.chapter2 = ['DICOM Series', '2: ']
        #self.chapter3 = ['Chapter ', 'Plan']
        self.list_forDate = ['C0410 / C0410','Prescription:']
        #self.list_forDate = ['Date Plan Saved', 'Created in Version']
        self.list_data_plan = [['Collimator Type:', 'InTempo Imaging:'],['Dose Calculation Algorithm:','Spacing'],['Optimization Algorithm:', 'Plan Name:'],['Prescription:','Reference'],['Number of Non-zero Beams:','Plan Overview']]
        #self.regExp_CT = [['Scan Date', 'hr'], ['Study UID', 'Plan Overview']]
        self.regExp_CT = [['Scan Date', 'Scanner Model:'], ['Series UID/Description', 'Plan Overview']]
        self.regExp_patient = [['Patient Name:', 'Date Of Birth:'],
                               ['Plan Name:', 'C0410 / C0410']]
        self.all_major_messages = []
        self.all_minor_messages = []
        self.patient_name = ''
        self.plan_name = ''
        self.finalString = ''
        self.finalList = ''
        self.fileName = ''

    def writePDF_Report(self):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        f = open(self.fileName, "r")
        for x in f:
            pdf.cell(100, 5, txt=x, ln=2, align='l')
        f.close()
        pdf.output(self.fileName)

    def configureWriteTxt_Report(self):
        majorChecks = '\n'+'VERIFICATIONS MAJEURES : '
        minChecks = '\n'+'VERIFICATIONS MINEURES : '
        self.all_major_messages.insert(0, majorChecks)
        # print(self.all_major_messages)
        self.all_minor_messages .insert(0, minChecks)
        self.finalList = self.all_major_messages + self.all_minor_messages
        self.finalString = '\n\n'.join([str(i) for i in self.finalList])
        self.fileName = self.outputDirectory + \
            'ExportCK-' + str(self.patient_name)+'-'+str(self.plan_name)+'.pdf'
        MyFile = open(self.fileName, 'w')
        MyFile.writelines(self.finalString)
        MyFile.close()
        # print(finalString)

    def mainExportFunction(self):
        i_patient_data = get_pageIndex_withRegExp(self.moPDF, self.chapter1)
        list_patient_data = convert_PDFpage_ToStringList(
            self.moPDF, i_patient_data)
        #print(list_patient_data)
        i_CT_data = get_pageIndex_withRegExp(self.moPDF, self.chapter2)
        list_CT_data_protocol = convert_PDFpage_ToStringList(
            self.moPDF, i_CT_data)
        #print(list_CT_data_protocol)

        # Get Page index of pdf using regular express
        # i0_mosaiq = get_pageIndex_withRegExp(self.moPDF, firstPage)
        # i0_mp = get_pageIndex_withRegExp(self.mpPDF, firstPage)

        i_plan_mosaiq = get_pageIndex_withRegExp(self.moPDF, self.chapter1)
        i_plan_mp = get_pageIndex_withRegExp(self.mpPDF, self.chapter1)

        # extract and convert the wanted page of the pdf
        mp_plan_string = convert_PDFpage_ToStringList(self.mpPDF, i_plan_mp)
        mo_plan_string = convert_PDFpage_ToStringList(
            self.moPDF, i_plan_mosaiq)
        # mo_patient_string = convert_PDFpage_ToStringList(self.moPDF, i0_mosaiq)
        # print(mo_plan_string)

        # print(i0_mosaiq,i0_mp,i_plan_mosaiq,i_plan_mp)
        major_CT_data = extractCTData(list_CT_data_protocol, self.regExp_CT)
        major_patient_data, self.patient_name, self.plan_name = extractPatientData(
            list_patient_data, self.regExp_patient)
        major_plan_data, minor_plan_data = extract_dataPlan(
            mo_plan_string, self.list_data_plan)
        # identical date plan saved between multiplan and mosaiq ? date_output [True/False, mp_datePlan, mo_datePlan]
        row_date_data, date_output = compare_date(
            mp_plan_string, mo_plan_string, self.list_forDate)

        message_CT_major = makeReadableMessage(major_CT_data)
        message_date_major = makeReadableMessage(date_output)
        message_patient_major = makeReadableMessage(major_patient_data)
        message_plan_minor = makeReadableMessage(minor_plan_data)
        message_plan_major = makeReadableMessage(major_plan_data)

        self.all_major_messages = [message_date_major, message_patient_major,
                                   message_plan_major, message_CT_major]
        self.all_minor_messages = [message_plan_minor]
        '''
        all_major_messages = [message_date_major, message_patient_major,
                            message_CT_major]
        all_minor_messages = []'''
        # writeFile(self.all_major_messages, self.all_minor_messages,
        #          self.patient_name)
        # print(date_output)
        # print(mp_plan_string)


# Debug world for the CK export class
'''import os
print(os.getcwd())
#os.chdir('/run/user/1001/gvfs/smb-share:server=sd00d35,share=dosimetrie/CyberKnife/06_CK-Export/code/lib/')
os.chdir('/home/daniel/Documents/CK-Export/code/lib')
mpPDF= "PlanOverview.pdf"
moPDF= "PlanOverview.pdf"
outputDirectory="PDF"
classExportCK = ExportCyberknife(moPDF, mpPDF, outputDirectory)
classExportCK.mainExportFunction()
'''