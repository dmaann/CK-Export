import os
import shutil as sh
from lib.exportCK import ExportCyberknife


def main():
    workedDirectory = "PDF"
    outputDirectory = "../Reports/"
    trashDirectory = "../Trash/"

    '''try:
        os.mkdir(workedDirectory)
    except(FileExistsError):
        pass
    '''
    try:
        os.chdir(workedDirectory)
        #print(os.getcwd())
    except FileNotFoundError:
        os.mkdir(workedDirectory)
        print('the pdf file is now created: create patient folder with the pdf of mosaiq and muliplan')
   
    try:
        os.mkdir(outputDirectory)
    except FileExistsError:
        pass

    try:
        os.mkdir(trashDirectory)
    except FileExistsError:
        pass

    full_dir = []
    patient_dir = []
    for root, dirs, files in os.walk('.', topdown=True):
        tup = (root[2:], files)
        patient_dir.append(dirs)
        #print(tup)
        full_dir.append(tup)
    # print(patient_dir[0])

    del full_dir[0]
    # print(full_dir)
    for path in full_dir:
        files = path[1]
        moPDF = 'Path to the mosaiq pdf file'
        mpPDF = 'Path to the multiplan pdf file'
        if len(files) == 2 or len(files) ==3:
            #print(files)
            for f in files:
                if f == "Thumbs.db":
                    #os.remove(f)
                    try:
                        os.remove(path[0]+'/'+f)
                    except:
                        pass
                    #print(f)
                    files.remove(f)
            if files[0] == 'PlanOverview.pdf':
                mpPDF = path[0]+'/'+files[0]
                moPDF = path[0]+'/'+files[1]
            else:
                if files[1] != 'PlanOverview.pdf':
                    print('Any multiplan pdf called PlanOverview.pdf')
                else:
                    mpPDF = path[0]+'/'+files[1]
                    moPDF = path[0]+'/'+files[0]
            classExportCK = ExportCyberknife(moPDF, mpPDF, outputDirectory)
            classExportCK.mainExportFunction()
            classExportCK.configureWriteTxt_Report()
            classExportCK.writePDF_Report()
            # print(moPDF, mpPDF)
            try:
                del classExportCK
            except:
                pass
            for d in patient_dir[0]:
                print(d)
                sh.move(d, trashDirectory+d)
        elif len(files) == 0 or len(files) == 1:
            pass
        else:
            print('Two pdf are required in the folder',
                  workedDirectory + path[0])
    os.chdir('..')
        


if __name__ == "__main__":
    main()