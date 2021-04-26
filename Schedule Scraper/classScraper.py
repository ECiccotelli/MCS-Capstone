

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from database import queryCRNs, insertData
import os
from bs4 import BeautifulSoup

#Returns the HTML of the dynamic scheduler page (which contains every classe's info)
#Parameters:
#Returns: soup
def initializeBrowser():
    chrome_options = Options()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage") #
    chrome_options.add_argument("--no-sandbox") #

    PATH = "C:\Program Files (x86)\chromedriver.exe"

    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options) #Path instead of executable path
    #driver = webdriver.Chrome(PATH)
    URL = "https://wlssb02.manhattan.edu/PROD/bwckschd.p_disp_dyn_sched"

    driver.get(URL)


    select = Select(driver.find_element_by_name("p_term"))

    select.select_by_index(1)

    submitButton = driver.find_element_by_xpath("/html/body/div[3]/form/input[2]")
    submitButton.send_keys(Keys.ENTER)


    subjectOptions = driver.find_element_by_xpath('//*[@id="subj_id"]')

    p = '//*[@id="subj_id"]/option[1]'
    myElemA = driver.find_element_by_xpath(p)

    ActionChains(driver).key_down(Keys.CONTROL).click(myElemA).send_keys('a').perform()



    classSearch = driver.find_element_by_xpath("/html/body/div[3]/form/input[12]").click()


    driver.switch_to.window(driver.window_handles[1])




    driver.implicitly_wait(15)
    time.sleep(15)

    
    html_doc = driver.page_source

    driver.quit()

    soup = BeautifulSoup(html_doc, 'html.parser')
    return soup

#Parameters:
#Returns: Array of credits
def getCredits(allCredits):


    creditList = []
    for credit in allCredits:
        #txt = str(tryingToFindCredits[0])
        #temp = allCredits[0].getText().split('\n')
        temp = credit.getText().split('\n')

        for ele in temp:
            if ".000 Credits" in ele:
                ele = ele.strip()
                tttt = ele.split('.')
                
                creditList.append(tttt[0])
    return creditList
    
#Parameters:
#Returns: crnList, titleList, classAbbr, classSection
def getClassInfo(allClassInfo):

    crnList = []
    titleList = []
    classAbbr = []
    classSection = []

    for y in allClassInfo:
        currentText = y.getText()
        #Index 0 is the course title
        #Index -1 is the section
        #Index -2 is the class abbreviation
        #Index -3 is the course numbers
        crnList.append(currentText.split("-")[-3])
        titleList.append(currentText.split("-")[0])
        classAbbr.append(currentText.split("-")[-2])
        classSection.append(currentText.split("-")[-1])
    
    return crnList, titleList, classAbbr, classSection

#Parameters:
#Returns:  count, classCounter, insertedCount, tbaCounter
def formatAndInsert(t2, creditList, crnList, titleList, classAbbr, classSection):
    count = 0
    classCounter = 0
    insertedCount=0
    tbaCounter=0

    for selectedClass in t2:

        if count == 0:
            count+=1
            continue


        info = selectedClass.findAll("td", {"class": "dddefault"})

        numberOfFields = 7
        length = len(info)

        #Calculates the number of times in the class (i.e. MR 10:30 - 11:30 would be 1 time, if it also has F: 2:00 - 3:00 that would be another time)
        numberOfTimes = int(length / numberOfFields)

        
        classInfo = []
        classTimes = []

        

        for p in info:
            classInfo.append(p.getText())
        '''
            0 - Type (Lecture, remote, etc)
            1 - Times
            2 - Days
            3 - Building
            4 - Dates
            5 - Schedule Type
            6 - Instructor
        '''

        exFound = False
        
        try:
            typeStr = classInfo[0]
            locationStr = classInfo[3]
            instStr = classInfo[6]
            daysAndTimes = ""
            scheduleType = classInfo[5]
        except Exception as e:

            print("Error!" + str(e))
            print("Current selected class info: " + str(classInfo))
            exFound = True
            pass

        if exFound:
            continue

        exFound = False
        #CHECK: IF TIME/DAYS TBA OR EMPTY, SKIP CLASS
        if classInfo[1].strip() == "TBA" or classInfo[1].strip() == "" or classInfo[2].strip() == "TBA" or classInfo[2].strip() == "":
            tbaCounter +=1
            classCounter+=1
            count+=1
            continue

        
        for i in range(0, length):

            current = i % 7
            
            #Type
            if current == 0 and classInfo[i] not in typeStr:
                s = ", " + classInfo[i]
                typeStr += s

            #Days and Times handling
            elif current == 2:
                for day in classInfo[i]:
                    s = day + ": " + classInfo[i-1] + ", "
                    daysAndTimes += s
            #Location
            elif current == 3 and classInfo[i] not in locationStr:
                s = ", " + classInfo[i]
                locationStr += s

            #Schedule type
            elif current == 5 and classInfo[i] not in scheduleType:
                s = ", " + classInfo[i]
                scheduleType += s

            #Instructor
            elif current == 6 and classInfo[i] not in instStr:
                s = ", " + classInfo[i]
                instStr += s
        
        if daysAndTimes.strip()[-1] == ",":
            daysAndTimes = daysAndTimes.strip()[:-1]
        
    
        insertData(crnList[classCounter], creditList[classCounter], instStr, locationStr, daysAndTimes, scheduleType, titleList[classCounter], typeStr, classAbbr[classCounter], classSection[classCounter])
        insertedCount+=1

        if insertedCount % 100 == 0:
            print("Inserted number " + str(insertedCount))


        classCounter+=1


        classInfo = []

        count+=1

    print("format and insert function complete")
    return count, classCounter, insertedCount, tbaCounter