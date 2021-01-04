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


def compare_date(planString, moPlanString, regExpDate):
    idx = get_startEndIndex_withRegExp(planString, regExpDate)
    #print(idx)
    #n = range(idx[0], idx[1])
    mp_date = get_regExp_fromStringList(planString, idx[0]+2, idx[1])
    mo_date = get_regExp_fromStringList(moPlanString, idx[0]+2, idx[1])
    #mp_date_msg = get_regExp_fromStringList(planString, idx[0], idx[1])
    #mo_date_msg = get_regExp_fromStringList(planString, idx[0], idx[1])
    #print(mp_date)
    #print(mo_date)
    boolean = True
    if mp_date == mo_date:
        writableOutput = ['Date sauvegarde du plan identiques ? : ' + str(
            boolean), 'Date du pdf de Multiplan : ' + str(mp_date), 'Date du pdf Mosaiq :       ' + str(mo_date)]
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
    idx_frac = get_startEndIndex_withRegExp(planString, regExpPlan[0])
    path_fraction_colli = get_stringList(
        planString, idx_frac[0], idx_frac[1])
    fraction = extract_namedValue(path_fraction_colli, [0, 1, 6])
    path = extract_namedValue(path_fraction_colli, list(
        range(len(path_fraction_colli)-3, len(path_fraction_colli))))
    collimator = extract_namedValue(path_fraction_colli, [2, 3, 7, 8])
    '''print(fraction, '\n', path, '\n', collimator)
        print(path_fraction_colli)'''

    idx_tracking = get_startEndIndex_withRegExp(
        planString, regExpPlan[1])
    tracking_ = get_stringList(
        planString, idx_tracking[0], idx_tracking[1])
    tracking = extract_namedValue(
        tracking_, list(range(0, len(tracking_))))
    # print(tracking)

    idx_dose_isodose = get_startEndIndex_withRegExp(
        planString, regExpPlan[2])
    dose_isodose = get_stringList(
        planString, idx_dose_isodose[0], idx_dose_isodose[1])
    dose = extract_namedValue(dose_isodose, [0, 7, 4, 2])
    isodose = extract_namedValue(dose_isodose, [6, 7, 8, 5])
    '''print(dose, '\n', isodose)
        print(dose_isodose)'''

    idx_time_beam = get_startEndIndex_withRegExp(planString, regExpPlan[4])
    time_beam = get_stringList(
        planString, idx_time_beam[0], idx_time_beam[1])
    resolution = extract_namedValue(time_beam, list(range(0, 3)))
    time = extract_namedValue(time_beam, [11, 1, 15, 13])
    beam = extract_namedValue(time_beam, [9, 1, 8])
    '''print(resolution, '\n', time, '\n', beam)
        print(time_beam)'''

    idx_algo_segment = get_startEndIndex_withRegExp(
        planString, regExpPlan[3])
    algo_segment = get_stringList(
        planString, idx_algo_segment[0], idx_algo_segment[1])
    algorithm = extract_namedValue(algo_segment, list(range(0, 3)))
    scaling = extract_namedValue(algo_segment, list(range(3, 6)))
    r = re.compile(".*MLC")
    isMLC = list(filter(r.match, planString))
    if not isMLC:  # empty list, i.e. fixed collimator
        minorPagePlan = [collimator, path, algorithm,
                         resolution, time, beam]
    else:  # MLC collimator
        segment = extract_namedValue(algo_segment, list(range(6, 9)))
        minorPagePlan = [collimator, path, algorithm,
                         resolution, time, beam, segment]
    '''print(algorithm, '\n', scaling, '\n', segment)
        print(algo_segment)'''
    majorPagePlan = [fraction, dose, isodose, tracking, scaling]
    # print(majorPagePlan)
    # print(minorPagePlan)
    return majorPagePlan, minorPagePlan


def extractPatientData(patientString, regExpList):
    idx_patient = get_startEndIndex_withRegExp(
        patientString, regExpList[0])
    patient_data = get_stringList(
        patientString, idx_patient[0], idx_patient[1])
    # print(patient_data)
    name = extract_namedValue(patient_data, [0, 1, 2, 3, 4, 8])
    nameForOutputFile = extract_namedValue(patient_data, [2])
    # print(nameForOutputFile)
    id_ = extract_namedValue(patient_data, list(
        range(len(patient_data)-4, len(patient_data)-1)))
    plan_name = extract_namedValue(patient_data, [5, 6, 7])

    idx_status = get_startEndIndex_withRegExp(patientString, regExpList[1])
    plan_status = get_stringList(
        patientString, idx_status[0], idx_status[1]+1)
    idx_position = [0, 1]
    idx_position.extend(list(range(4, len(plan_status)-1)))
    plan_name = extract_namedValue(plan_status, idx_position)
    # print(plan_status)
    status = extract_namedValue(plan_status, [2, 3, len(plan_status)-1])
    #print(name, '\n', id_, '\n', plan_name, '\n', status)
    majorCheck = [name, id_, plan_name, status]
    # print(majorCheck)
    return majorCheck, nameForOutputFile


def extractCTData(CTString, regExpList):
    idx_CT_date = get_startEndIndex_withRegExp(CTString, regExpList[0])
    CT_date = get_stringList(CTString, idx_CT_date[0], idx_CT_date[1])
    # print(CT_date)
    idx_position = [0, 1]
    idx_position.extend(list(range(6, len(CT_date)-1)))
    date = extract_namedValue(CT_date, idx_position)
    # print(date)
    idx_CT_protocol = get_startEndIndex_withRegExp(CTString, regExpList[1])
    CT_protocol = get_stringList(
        CTString, idx_CT_protocol[0], idx_CT_protocol[1])
    # print(CT_protocol)
    idx_position = [2, 3]
    idx_position.extend(list(range(6, len(CT_protocol)-2)))
    protocol = extract_namedValue(CT_protocol, idx_position)
    # print(protocol)
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
        #firstPage = ['Plan Overview', 'not']
        self.chapter1 = ['Chapter ', 'Overview']
        self.chapter2 = ['DICOM Series', '2: ']
        self.chapter3 = ['Chapter ', 'Plan']
        self.list_forDate = ['Date Plan Saved', 'Created in Version']
        self.list_data_plan = [['Planned Fractions', 'HFS'], ['Tracking Method', 'Alignment Center '], [
            'Prescribed Plan Dose ', 'Reference Point '], ['Optimization Algorithm', 'Page'], ['Dose Calculation Resolution', 'dose Beams']]
        self.regExp_CT = [['Scan Date', 'hr'], ['Study UID', 'Plan Overview']]
        self.regExp_patient = [['Last Name', 'Plan Summary'],
                               ['Plan Name', 'Deliverable']]
        self.all_major_messages = []
        self.all_minor_messages = []
        self.patient_name = ''

    def writeReport(self):
        majorChecks = '\n'+'VERIFICATIONS MAJEURES : '
        minChecks = '\n'+'VERIFICATIONS MINEURES : '
        self.all_major_messages.insert(0, majorChecks)
        self.all_minor_messages .insert(0, minChecks)
        finalList = self.all_major_messages + self.all_minor_messages 
        finalString = '\n\n'.join([str(i) for i in finalList])
        fileName = self.outputDirectory+'ExportCK-' + str(self.patient_name)+'.txt'
        MyFile = open(fileName, 'w')
        MyFile.writelines(finalString)
        MyFile.close()
        # print(finalString)

    def mainExportFunction(self):
        i_patient_data = get_pageIndex_withRegExp(self.moPDF, self.chapter1)
        list_patient_data = convert_PDFpage_ToStringList(
            self.moPDF, i_patient_data)

        i_CT_data = get_pageIndex_withRegExp(self.moPDF, self.chapter2)
        list_CT_data_protocol = convert_PDFpage_ToStringList(
            self.moPDF, i_CT_data)
        # print(list_CT_data_protocol)

        # Get Page index of pdf using regular express
        #i0_mosaiq = get_pageIndex_withRegExp(self.moPDF, firstPage)
        #i0_mp = get_pageIndex_withRegExp(self.mpPDF, firstPage)

        i_plan_mosaiq = get_pageIndex_withRegExp(self.moPDF, self.chapter3)
        i_plan_mp = get_pageIndex_withRegExp(self.mpPDF, self.chapter3)

        # extract and convert the wanted page of the pdf
        mp_plan_string = convert_PDFpage_ToStringList(self.mpPDF, i_plan_mp)
        mo_plan_string = convert_PDFpage_ToStringList(
            self.moPDF, i_plan_mosaiq)
        #mo_patient_string = convert_PDFpage_ToStringList(self.moPDF, i0_mosaiq)
        #print(mo_plan_string)

        # print(i0_mosaiq,i0_mp,i_plan_mosaiq,i_plan_mp)
        major_CT_data = extractCTData(list_CT_data_protocol, self.regExp_CT)
        major_patient_data, self.patient_name = extractPatientData(
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
        #writeFile(self.all_major_messages, self.all_minor_messages,
        #          self.patient_name)
        # print(date_output)
        # print(mp_plan_string)
