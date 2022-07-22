import webbot_selenium
import analyzing_insider_trades
import consolidate_insider_weekly

import datetime
import sys

#dgd
import os
import sys
print(os.path.dirname(sys.executable))
print(os.path.dirname(__file__))
dir= os.path.dirname(__file__)
print(os.path.dirname(sys.executable))
# sys.exit()
# webbot_selenium.scrapedaily(dir)
# webbot_selenium.scrapeweekly(dir)

## run this every week day except monday at night?
if (datetime.datetime.today().weekday()>= 1) and (datetime.datetime.today().weekday()<=4):
    webbot_selenium.scrapedaily(dir)
    # consolidate_insider_weekly.consolidate_daily(dir)
    # analyzing_insider_trades.analyzing()

#now i need to scrape weekly insider buy information on every saturday -- scrapeweekly done
#Return the day of the week as an integer, where Monday is 0 and Sunday is 6.
if (datetime.datetime.today().weekday()==5): # or 4 on late friday
    webbot_selenium.scrapeweekly(dir)
    # consolidate_insider_weekly.consolidate(dir)


# and update their price the following days on every wednesday
# and then update the insider list accordingly


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
