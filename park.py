import bs4
import requests
import os
import yagmail
import time
import RandomHeaders

myemail = str(open(“send.txt”, “r”).read()).partition(':')[0]
password = str(open(“send.txt”, “r”).read()).partition(':')[2]
sendemail = list(str(open(“to.txt”, “r”).read()))

yagmail.register(myemail, password)
yag = yagmail.SMTP(myemail)


if os.path.isfile('status.txt') == False:
    os.system("touch status.txt")
def Changed(newtext, myemail=myemail, sendemail=sendemail):
    text_file = open("status.txt", "w")
    text_file.write(newtext)
    text_file.close()
    yagmail.SMTP(myemail).send(sendemail, 'Change Detected {} Spots Now Available for 7/29'.format(newtext), 'Click here: https://www.recreation.gov/permitCalendar.do?page=calendar&calarvdate=07/16/2017&contractCode=NRSO&parkId=72201\nTo Purchase the tickets')
    yagmail.SMTP(myemail).send(sendemailtwo, 'Change Detected {} Spots Now Available for 7/29'.format(newtext), 'Click here: https://www.recreation.gov/permitCalendar.do?page=calendar&calarvdate=07/16/2017&contractCode=NRSO&parkId=72201\nTo Purchase the tickets')
    print('sent email')


while True:
    res = requests.session()
    e = bs4.BeautifulSoup(res.get('https://www.recreation.gov/permitCalendar.do?page=calendar&calarvdate=07/16/2017&contractCode=NRSO&parkId=72201').text)

    data = {'permitTypeId':'1034702728',
    'targetUIID':'entrance',
    'contractCode':'NRSO',
    'facilityId':'72201',
    'titleText':'Any Trail/Zone'}
    a = res.post('https://www.recreation.gov/ajax/EntranceList', data=data)
    a = bs4.BeautifulSoup(a.text, 'lxml')
    hidden_tags = e.find_all("input", type="hidden")
    for tag in hidden_tags:
        print(tag)
        if 'actionToken' in str(tag):
            actionToken = str(str(tag).partition("value='")[2]).partition("' name='")[0]
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
    'actionToken': actionToken}
    a = res.post('https://www.recreation.gov/permitCalendar.do?mode=submit', data=data)
    a = res.get('https://www.recreation.gov/permits/Mt_Whitney/r/permitCalendar.do?page=calendar&contractCode=NRSO&parkId=72201')
    page = bs4.BeautifulSoup(a.text, 'lxml')
    with open('status.txt') as f:
        if page.select('.permitStatus')[1].getText() not in f.readlines():
            Changed(str(page.select('.permitStatus')[1].getText()))
    time.sleep(60 * 15)


