

from discordSender import sendDiscordMessage, sendDiscordInitialize
from database import queryCRNs, insertData
from classScraper import *
import time


if __name__ == "__main__":
    sendDiscordInitialize()
    print("Scraper successfully booted up!")

    while True:
        #sendDiscordInitialize()
        #print("Scraper successfully booted up!")
        startTime = time.time() #Starting time
        error = False
        initializationError = False


        try:
            soup = initializeBrowser()
        except Exception as e:
            initializationError = True
            print("Exception caught:", str(e))
            pass

        if initializationError:
            print("Sleeping for 5 minutes")
            time.sleep(300)
            continue

        entirePageInfo = soup.findAll("table", {"class": "datadisplaytable"}) #gets passed into formatandinsert as t2


        allCredits = entirePageInfo[0].findAll("td", {"class": "dddefault"}) #pass into get credits function
        creditList = getCredits(allCredits)

        allClassInfo = entirePageInfo[0].findAll("th",{"class": "ddtitle"}) #pass into get class info
        crnList, titleList, classAbbr, classSection = getClassInfo(allClassInfo)

        #(t2, creditList, crnList, titleList, classAbbr, classSection):
        try:
            count, classCounter, insertedCount, tbaCounter = formatAndInsert(entirePageInfo, creditList, crnList, titleList, classAbbr, classSection)
        except Exception as e:
            print("Exception caught:", str(e))
            error = True
            pass

        endTime = time.time()
        if error:
            sendDiscordMessage(False, str(endTime - startTime), 0)
        else:
            sendDiscordMessage(True, str(endTime - startTime), classCounter)
        
        print("Sleeping for 60 minutes")
        time.sleep(3600)
    



    

