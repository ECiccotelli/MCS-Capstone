import pdfrw
import random
import os
from datetime import date
import time
import copy

# ***** MUST pip install pdfrw *****
os.environ["PATH4PDF"] = 'website/static/pdf/undergraduate_registration_form.pdf'
# Map of PDF tags to the corresponding field name and data
# x = {PDF_TAG: [FIELD_NAME, DATASTORE_VALUE]}
x = {
    "'(Name)'" : ['FULL_NAME', ""],
    "'(Campus ID)'" : ['CAMPUS_ID', ""],
    "'(1)'" : ['MAJOR_1', ""],
    "'(2)'" : ['MAJOR_2', ""],
    "'(1_2)'" : ['MINOR_1', ""],
    "'(2_2)'" : ['MINOR_2', ""],
    "'(Month  Year)'" : ['GRADMONTH_YEAR',""],
    "'(Check Box1)'": ["FRESHMAN_CHECKBOX", "1"],
    "'(Check Box2)'": ["SOPHOMORE_CHECKBOX", "1"],
    "'(Check Box3)'": ["JUNIOR_CHECKBOX", "1"],
    "'(Check Box4)'": ["SENIOR_CHECKBOX", "1"],
    "'(Check Box5)'": ["NONMAT_CHECKBOX", "1"],
    "'(Check Box6)'": ["SPRING_CHECKBOX", "1"],
    "'(Check Box7)'": ["FALL_CHECKBOX", "1"],
    "'(Text8)'": ["FALL_SEMESTER_YEAR", ""],
    "'(Text9)'": ["SPRING_SEMESTER_YEAR", ""],
    "'(Check Box10)'": ["ARTS_CHECKBOX", "1"],
    "'(Check Box11)'": ["BUSINESS_CHECKBOX", "1"],
    "'(Check Box12)'": ["EDUCATION_CHECKBOX", "1"],
    "'(Check Box13)'": ["ENGINEERING_CHECKBOX", "1"],
    "'(Check Box14)'": ["SCIENCE_CHECKBOX", "1"],
    "'(Check Box15)'": ["SCPS_CHECKBOX", "1"],
    "'(CRN)'" : ['CRN_1', ""],
    "'(undefined)'" : ['CRN_2', ""],
    "'(undefined_5)'" : ['CRN_3', ""],
    "'(undefined_9)'" : ['CRN_4', ""],
    "'(undefined_13)'" : ['CRN_5', ""],
    "'(undefined_17)'" : ['CRN_6', ""],
    "'(undefined_21)'" : ['CRN_7', ""],
    "'(Dept)'" : ['DEPT_1', ""],
    "'(undefined_2)'" : ['DEPT_2', ""],
    "'(undefined_6)'" : ['DEPT_3', ""],
    "'(undefined_10)'" : ['DEPT_4', ""],
    "'(undefined_14)'" : ['DEPT_5', ""],
    "'(undefined_18)'" : ['DEPT_6', ""],
    "'(undefined_22)'" : ['DEPT_7', ""],
    "'(Crs)'" : ['CRS_1', ""],
    "'(undefined_3)'" : ['CRS_2', ""],
    "'(undefined_7)'" : ['CRS_3', ""],
    "'(undefined_11)'" : ['CRS_4', ""],
    "'(undefined_15)'" : ['CRS_5', ""],
    "'(undefined_19)'" : ['CRS_6', ""],
    "'(undefined_23)'" : ['CRS_7', ""],
    "'(Sec)'" : ['SEC_1', ""],
    "'(undefined_4)'" : ['SEC_2', ""],
    "'(undefined_8)'" : ['SEC_3', ""],
    "'(undefined_12)'" : ['SEC_4', ""],
    "'(undefined_16)'" : ['SEC_5', ""],
    "'(undefined_20)'" : ['SEC_6', ""],
    "'(undefined_24)'" : ['SEC_7', ""],
    "'(TitleRow1)'" : ['TITLE_1', ""],
    "'(TitleRow2)'" : ['TITLE_2', ""],
    "'(TitleRow3)'" : ['TITLE_3', ""],
    "'(TitleRow4)'" : ['TITLE_4', ""],
    "'(TitleRow5)'" : ['TITLE_5', ""],
    "'(TitleRow6)'" : ['TITLE_6', ""],
    "'(TitleRow7)'" : ['TITLE_7', ""],
    "'(CrRow1)'" : ['CREDIT_1', ""],
    "'(CrRow2)'" : ['CREDIT_2', ""],
    "'(CrRow3)'" : ['CREDIT_3', ""],
    "'(CrRow4)'" : ['CREDIT_4', ""],
    "'(CrRow5)'" : ['CREDIT_5', ""],
    "'(CrRow6)'" : ['CREDIT_6', ""],
    "'(CrRow7)'" : ['CREDIT_7', ""],
    "'(Total Credits)'" : ['TOTAL_CREDITS', ""],
    "'(Student Signature)'" : 'STUDENT_SIGNATURE',
    "'(Date)'": ['DATE', ""]
}


def fillPDF(p_data, userInfoDict):
    num = random.randint(1000, 9999999999)
    exportname = 'website/static/pdf/undergraduate_reg_export-'+str(num)+str(time.time())+'.pdf'
    template_pdf = pdfrw.PdfReader(os.getenv("PATH4PDF")) # Path to PDF form (local)
    annotations = template_pdf.pages[0]['/Annots']
    i = 0
    totalCreditCount = 0
    today = date.today()
    d1 = today.strftime("%m/%d/%Y")
    #Text Data for Personal AutoFill
    userInfoDict["'(Name)'"][1] = p_data[0]+' '+p_data[1]
    userInfoDict["'(Campus ID)'"][1] = p_data[2]
    userInfoDict["'(1)'"][1] = p_data[10]
    userInfoDict["'(2)'"][1] = p_data[11]
    userInfoDict["'(1_2)'"][1] = p_data[12]
    userInfoDict["'(2_2)'"][1] = p_data[13]
    if p_data[14] == 'Fall':
        userInfoDict["'(Text8)'"][1] = p_data[15]
    else:
        userInfoDict["'(Text9)'"][1] = p_data[15]
    userInfoDict["'(Month  Year)'"][1] = p_data[17]+' '+p_data[18]
    userInfoDict["'(Date)'"][1] = d1
    checkthisStudy = []
    for i in range(4, 11):
        if p_data[i] is not None:
            num = i + 6
            checkthisStudy.append(num)
    for annotation in annotations:

        pdfTag = repr(annotation['/T'])
        if pdfTag in x:
            if "Check Box" in pdfTag:
                #Check box for grade
                tempTag = "'(Check Box"+p_data[3]+")'"
                if pdfTag == tempTag:
                    annotation.update(pdfrw.PdfDict(AS=pdfrw.PdfName('Yes')))
                    continue

                newtag = pdfTag.replace("Check Box", "")
                if int(newtag.replace("'(","").replace(")'","")) in checkthisStudy:
                    annotation.update(pdfrw.PdfDict(AS=pdfrw.PdfName('Yes')))
                    continue
                if not userInfoDict["'(Text8)'"][1] and pdfTag == "'(Check Box6)'":
                    annotation.update(pdfrw.PdfDict(AS=pdfrw.PdfName('Yes')))
                    continue
                if not userInfoDict["'(Text9)'"][1] and pdfTag == "'(Check Box7)'":
                    annotation.update(pdfrw.PdfDict(AS=pdfrw.PdfName('Yes')))
                    continue


            else:
                if "Total Credits" in pdfTag:
                    entry = str(totalCreditCount)
                    annotation.update(pdfrw.PdfDict(AP=" ", V=entry))
                    continue
                elif 'CrRow' in pdfTag and len(userInfoDict[pdfTag][1]) > 0:
                    creditValue = int(userInfoDict[repr(annotation['/T'])][1])
                    totalCreditCount += creditValue

                entry = userInfoDict[repr(annotation['/T'])][1]
                annotation.update(pdfrw.PdfDict(AP=" ", V=entry))

    pdfrw.PdfWriter().write(exportname, template_pdf)
    return exportname, totalCreditCount

def fillPDFsession(userInfoDict):
    num = random.randint(1000, 9999999999)
    exportname = 'website/static/pdf/undergraduate_reg_export-'+str(num)+str(time.time())+'.pdf'
    template_pdf = pdfrw.PdfReader(os.getenv("PATH4PDF")) # Path to PDF form (local)
    annotations = template_pdf.pages[0]['/Annots']
    i = 0
    totalCreditCount = 0

    for annotation in annotations:

        pdfTag = repr(annotation['/T'])
        if pdfTag in x:
            if "Check Box" in pdfTag:
                pass
            else:
                if "Total Credits" in pdfTag:
                    entry = str(totalCreditCount)
                    annotation.update(pdfrw.PdfDict(AP=" ", V=entry))
                    continue
                elif 'CrRow' in pdfTag and len(userInfoDict[pdfTag][1]) > 0:
                    creditValue = int(userInfoDict[repr(annotation['/T'])][1])
                    totalCreditCount += creditValue

                entry = userInfoDict[repr(annotation['/T'])][1]
                annotation.update(pdfrw.PdfDict(AP=" ", V=entry))

    pdfrw.PdfWriter().write(exportname, template_pdf)
    return exportname, totalCreditCount

def updateX(mylist, userInfoDict):
    tempArr = []
    count = 0
    startIndex = 22
    for entry in mylist:
        print(entry)
        info = mylist[entry]
        print(info)
        if int(info[2]) == 0:
            continue
        count += 1
        ndcs = info[0].split('-')
        tempArr.append(entry)
        name = ndcs[0].strip()
        dc = ndcs[1].strip()
        dept = dc.split()[0]
        tempArr.append(dept)
        crs = dc.split()[1]
        tempArr.append(crs)
        section = ndcs[2].strip()
        tempArr.append(section)
        tempArr.append(name)
        credit = info[3]
        tempArr.append(credit)
        for y in range(0,6):
            currentval = userInfoDict[list(userInfoDict)[startIndex]]
            currentval[1] = tempArr[y]
            if startIndex >= 57:
                startIndex-=34
            else:
                startIndex+=7
        tempArr = []
    return count


def run(mylist):
    userInfoDict = copy.deepcopy(x)
    print('Creation')
    print(userInfoDict)
    courses = updateX(mylist, userInfoDict)
    exportdelname, cred = fillPDFsession(userInfoDict)
    print('Modified')
    print(userInfoDict)
    return exportdelname, cred, courses

def runfull(mylist, p_data):
    userInfoDict = copy.deepcopy(x)
    courses = updateX(mylist, userInfoDict)
    if p_data == []:
        exportdelname, cred = fillPDFsession(userInfoDict)
    else:
        exportdelname, cred = fillPDF(p_data, userInfoDict)
    return exportdelname, cred, courses