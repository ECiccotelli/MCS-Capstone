

from discordSender import sendDiscordMessage, sendDiscordInitialize, deletionWarningMessenger
from database import queryCRNs, insertData, removeCRN
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

        #Queries all CRNs currently in database
        dbCRNS = queryCRNs()

        #Removes spaces from crns
        crnList = list(map(str.strip, crnList))

        removed = 0
        #toDelete = []
        for crn in dbCRNS:
            if crn not in crnList:
                #print("This CRN is in the database but NOT scraped - should remove! " + str(crn))
                #toDelete.append(crn)
                removeCRN(crn)
                removed+=1
                if removed > 50:
                    deletionWarningMessenger()
                    break

        
        
        #for deleteCRN in toDelete:
            #removeCRN(deleteCRN)
            #removed+=1

        endTime = time.time()
        if error:
            sendDiscordMessage(False, str(endTime - startTime), 0)
        else:
            sendDiscordMessage(True, str(endTime - startTime), removed, classCounter)
        
        print("Sleeping for 60 minutes")
        time.sleep(3600)
    



    

