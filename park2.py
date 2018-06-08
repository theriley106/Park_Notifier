import bs4
import requests
import os
import yagmail
import time

WAIT = 15


def Email(newtext, myemail=None, password=None, sendemail=None):
	if myemail == None:
		#myemail = str(open(“send.txt”, “r”).read()).partition(':')[0]
		print("error")
	if password == None:
		#password = str(open(“send.txt”, “r”).read()).partition(':')[2]
		print("error")
	if sendemail == None:
		#sendemail = list(str(open(“to.txt”, “r”).read()))
		print("error")
	yagmail.register(myemail, password)
	yag = yagmail.SMTP(myemail)
	text_file = open("status2.txt", "w")
	text_file.write(newtext)
	text_file.close()
	yagmail.SMTP(myemail).send(sendemail, 'Change Detected {} Spots Now Available for 6/13/2018'.format(newtext), 'Click here: https://www.recreation.gov/permitCalendar.do?page=calendar&calarvdate=06/13/2018&contractCode=NRSO&parkId=72201\nTo Purchase the tickets')
	print('sent email')

def resetFile():
	if os.path.isfile('status2.txt') == True:
		os.remove('status2.txt')
	os.system("echo.>status2.txt")


def returnActionToken(page):
	for tag in page.find_all("input", type="hidden"):
		if 'actionToken' in str(tag):
			return str(str(tag).partition("value='")[2]).partition("' name='")[0]

def CheckChange(facilityId):
	res = requests.session()

	data = {'permitTypeId':'1034702728',
	'targetUIID':'entrance',
	'contractCode':'NRSO',
	'facilityId':facilityId,
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
	'entryStartDate':'Wed Jun 13 2018',
	'entryEndDate': '',
	'groupSize':'1',
	'lengthOfStay': '',
	'stockSize': '',
	'watercraftSize':'',
	'cartItemId': '',
	'availStatus': '',
	'actionToken': returnActionToken(bs4.BeautifulSoup(res.get('https://www.recreation.gov/permitCalendar.do?page=calendar&calarvdate=06/13/2018&contractCode=NRSO&parkId=72201').text))}
	
	res.post('https://www.recreation.gov/permitCalendar.do?mode=submit', data=data)
	page = res.get('https://www.recreation.gov/permits/Mt_Whitney/r/permitCalendar.do?page=calendar&contractCode=NRSO&parkId=72201')
	page = bs4.BeautifulSoup(page.text, 'lxml')
	with open('status2.txt') as f:
		#if page.select('.permitStatus')[1].getText() not in f.readlines():
			#print(type(page.select('.status a')[0]))
			#print(page.select('.status a'))
			#return str(page.select('.permitStatus')[1].getText())
		numAvail = "R"
		for entry in page.select('.status a'):
			if 'arvdate=6/13/2018' in str(entry):
				numAvail = entry.select("small")[0].get_text()
		if numAvail not in f.readlines():
			return numAvail
	return None

if __name__ == "__main__":
	resetFile()
	while True:
		A = CheckChange('72201')
		if A != None:
			Email(A, myemail="", password="", sendemail="")
		time.sleep(60 * WAIT)