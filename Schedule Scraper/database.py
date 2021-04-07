from google.cloud import datastore

import os
import sys

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(sys.path[0], "mc-scheduleMaker.json")

client = datastore.Client()

query = client.query(kind="Courses")



databaseCRN = []
def queryCRNs():
    query = client.query(kind='Courses')
    results = list(query.fetch())
    for entity in results:
        st = str(entity.key.id_or_name).strip()
        databaseCRN.append(st)


def insertData(crn, credits, instructor, location, meetingTimes, scheduleType, title, classType, abbr, section):

    key = client.key("Courses", crn)


    test = {
        "Credits": credits,
        "Instructor": instructor,
        "Location": location,
        "MeetingTimes": meetingTimes,
        "ScheduleType": scheduleType,
        "Title": title,
        "Type": classType,
        "Abbreviation": abbr,
        "Section": section

    }

    c = datastore.Entity(key)

    c.update(test)
    client.put(c)