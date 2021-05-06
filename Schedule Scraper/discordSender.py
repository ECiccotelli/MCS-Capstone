from dhooks import Webhook, Embed
import datetime
import os
def sendDiscordMessage(successOrFailure, timeTaken, deletedClasses, totalClasses=0):
    hook = Webhook(os.environ.get("DISC_HOOK"))

    if successOrFailure:
        now = datetime.datetime.now()
        #hook.send("[" + str(now) + "] Successfully updated database with " + str(totalClasses) + " classes in the database currently")
        embed = Embed(description="The scraper has successfully ran.", color=0x5CDBF0, timestamp='now')
        embed.set_author(name='Manhattan College Dynamic Schedule Class Scraper')
        embed.add_field(name="Classes Scraped from Dynamic Scheduler", value=str(totalClasses))
        embed.add_field(name="Deleted/Outdated Entries", value=str(deletedClasses))
        embed.add_field(name="Time taken to run (sec)", value=timeTaken)
        #embed.add_field(name="Availability", value=a)
        embed.set_footer(text="MCS")
        hook.send(embed=embed)
        

    else:
        now = datetime.datetime.now()
        hook.send("[" + str(now) + "] FAILED TO UPDATE DATABASE. PLEASE PANIC. @everyone \n " + " time taken is " + str(timeTaken))

def deletionWarningMessenger():
    hook = Webhook(os.environ.get("DISC_HOOK"))
    now = datetime.datetime.now()
    embed = Embed(description="The scraper wants to delete > 50 entries in the DB, so I automatically stopped!", color=0x5CDBF0, timestamp='now')
    embed.set_footer(text="MCS")
    hook.send(embed=embed)

def sendDiscordInitialize():
    now = datetime.datetime.now()
    hook = Webhook(os.environ.get("DISC_HOOK"))
    embed = Embed(description="The scraper has successfully booted up!", color=0x5CDBF0, timestamp='now')
    embed.set_footer(text="MCS")
    hook.send(embed=embed)
