import bs4
import requests
import os
import yagmail
import time

WAIT = 15


def Email(newtext, myemail=None, password=None, sendemail=None):
    if myemail == None:
        myemail = str(open(“send.txt”, “r”).read()).partition(':')[0]
    if password == None:
        password = str(open(“send.txt”, “r”).read()).partition(':')[2]
    if sendemail == None:
        sendemail = list(str(open(“to.txt”, “r”).read()))
    yagmail.register(myemail, password)
    yag = yagmail.SMTP(myemail)
    text_file = open("status.txt", "w")
    text_file.write(newtext)
    text_file.close()
    yagmail.SMTP(myemail).send(sendemail, 'Change Detected {} Spots Now Available for 7/29'.format(newtext), 'Click here: https://www.recreation.gov/permitCalendar.do?page=calendar&calarvdate=07/16/2017&contractCode=NRSO&parkId=72201\nTo Purchase the tickets')
    print('sent email')

def resetFile():
    if os.path.isfile('status.txt') == True:
        os.remove('status.txt')
    os.system("touch status.txt")


def returnActionToken(page):
    for tag in page.find_all("input", type="hidden"):
        if 'actionToken' in str(tag):
            return str(str(tag).partition("value='")[2]).partition("' name='")[0]

def CheckChange():
    res = requests.session()

    data = {'permitTypeId':'1034702728',
    'targetUIID':'entrance',
    'contractCode':'NRSO',
    'facilityId':'72201',
    'titleText':'Any Trail/Zone'}

    a = res.post('https://www.recreation.gov/ajax/EntranceList', data=data)

    data = {'contractCode':'NRSO',
    'performSearch':'true',
    'pageOrigin':'permitCalendar',
    'permitTypeId':'1034702728',
    'searchType':'1',
    'trail':'1',
    'entrance':'315840|1065',
    'range':'1',
    'entryStartDate':'Fri Jul 28 2017',
    'entryEndDate': '',
    'groupSize':'2',
    'lengthOfStay': '',
    'stockSize': '',
    'watercraftSize':'',
    'cartItemId': '',
    'availStatus': '',
    'actionToken': returnActionToken(bs4.BeautifulSoup(res.get('https://www.recreation.gov/permitCalendar.do?page=calendar&calarvdate=07/16/2017&contractCode=NRSO&parkId=72201').text))}
    
    res.post('https://www.recreation.gov/permitCalendar.do?mode=submit', data=data)
    page = res.get('https://www.recreation.gov/permits/Mt_Whitney/r/permitCalendar.do?page=calendar&contractCode=NRSO&parkId=72201')
    page = bs4.BeautifulSoup(page.text, 'lxml')
    with open('status.txt') as f:
        if page.select('.permitStatus')[1].getText() not in f.readlines():
            return str(page.select('.permitStatus')[1].getText())
    return None

if __name__ == "__main__":
    resetFile()
    while True:
        A = CheckChange()
        if A != None:
            Email(A)
        time.sleep(60 * WAIT)