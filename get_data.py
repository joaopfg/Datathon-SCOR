import time
import os
import re
import urllib.request
from bs4 import BeautifulSoup


url_demographics_base = 'https://wwwn.cdc.gov/nchs/nhanes/search/datapage.aspx?Component=Demographics&CycleBeginYear='
url_dietary_base = 'https://wwwn.cdc.gov/nchs/nhanes/search/datapage.aspx?Component=Dietary&CycleBeginYear='
url_examination_base = 'https://wwwn.cdc.gov/nchs/nhanes/search/datapage.aspx?Component=Examination&CycleBeginYear='
url_laboratory_base = 'https://wwwn.cdc.gov/nchs/nhanes/search/datapage.aspx?Component=Laboratory&CycleBeginYear='
url_questionnaire_base = 'https://wwwn.cdc.gov/nchs/nhanes/search/datapage.aspx?Component=Questionnaire&CycleBeginYear='

urls_demographics = [url_demographics_base + str(i) for i in range(1999, 2017, 2)]
urls_dietary = [url_dietary_base + str(i) for i in range(1999, 2017, 2)]
urls_examination = [url_examination_base + str(i) for i in range(1999, 2017, 2)]
urls_laboratory = [url_laboratory_base + str(i) for i in range(1999, 2017, 2)]
urls_questionnaire = [url_questionnaire_base + str(i) for i in range(1999, 2017, 2)]

base_dests = ['NHANES/NHANES' + str(i) + str(i+1) + '/' for i in range(1999, 2017, 2)]
dests_demographics = [dest + 'Demographics/' for dest in base_dests]
dests_dietary = [dest + 'Dietary/' for dest in base_dests]
dests_examination = [dest + 'Examination/' for dest in base_dests]
dests_laboratory = [dest + 'Laboratory/' for dest in base_dests]
dests_questionnaire = [dest + 'Questionnaire/' for  dest in base_dests]

html_demographics = []
html_dietary = []
html_examination  = []
html_laboratory = []
html_questionnaire = []

print('Connecting to the site and getting htmls of the pages...')

for url in urls_demographics:
	with urllib.request.urlopen(url) as page:
			html_demographics.append(page.read())

for url in urls_dietary:
	with urllib.request.urlopen(url) as page:
			html_dietary.append(page.read())

for url in urls_examination:
	with urllib.request.urlopen(url) as page:
			html_examination.append(page.read())

for url in urls_laboratory:
	with urllib.request.urlopen(url) as page:
			html_laboratory.append(page.read())

for url in urls_questionnaire:
	with urllib.request.urlopen(url) as page:
			html_questionnaire.append(page.read())

print('Processing the html of the pages...')

soup_demographics = [BeautifulSoup(html_doc, 'html.parser') for html_doc in html_demographics]
soup_dietary = [BeautifulSoup(html_doc, 'html.parser') for html_doc in html_dietary]
soup_examination = [BeautifulSoup(html_doc, 'html.parser') for html_doc in html_examination]
soup_laboratory = [BeautifulSoup(html_doc, 'html.parser') for html_doc in html_laboratory]
soup_questionnaire = [BeautifulSoup(html_doc, 'html.parser') for html_doc in html_questionnaire]

print('Getting url to download files...')
file_urls_demographics = [soup.find_all('a', href=re.compile('\.XPT$')) for soup in soup_demographics]
file_urls_dietary = [soup.find_all('a', href=re.compile('\.XPT$')) for soup in soup_dietary]
file_urls_examination = [soup.find_all('a', href=re.compile('\.XPT$')) for soup in soup_examination]
file_urls_laboratory = [soup.find_all('a', href=re.compile('\.XPT$')) for soup in soup_laboratory]
file_urls_questionnaire = [soup.find_all('a', href=re.compile('\.XPT$')) for soup in soup_questionnaire]

base_url = 'https://wwwn.cdc.gov'

cont = 0

for i in reversed(range(len(file_urls_demographics))):
	file_urls_demographics[i] = [base_url + url['href'] for url in file_urls_demographics[i]]

	for file_url in file_urls_demographics[i]:
		if not os.path.exists(dests_demographics[i]):
			os.makedirs(dests_demographics[i])

		file_dest = file_url.split('/')[-1]
		print('Getting file: %s' % file_dest)
		file_dest = dests_demographics[i] + file_dest
		urllib.request.urlretrieve(file_url, file_dest)
		cont += 1

		if cont == 200:
			print('Got 200 files, requests will stop for 10 min in order to avoid crashing...')
			time.sleep(600)
			cont = 0


	file_urls_dietary[i] = [base_url +  url['href'] for url in file_urls_dietary[i]]

	for file_url in file_urls_dietary[i]:
		if not os.path.exists(dests_dietary[i]):
			os.makedirs(dests_dietary[i])

		file_dest = file_url.split('/')[-1]
		print('Getting file: %s' % file_dest)
		file_dest = dests_dietary[i] + file_dest
		urllib.request.urlretrieve(file_url, file_dest)
		cont += 1

		if cont == 200:
			print('Got 200 files, requests will stop for 10 min in order to avoid crashing...')
			time.sleep(600)
			cont = 0

	file_urls_examination[i] = [base_url + url['href'] for url in file_urls_examination[i]]

	for file_url in file_urls_examination[i]:
		if not os.path.exists(dests_examination[i]):
			os.makedirs(dests_examination[i])

		file_dest = file_url.split('/')[-1]
		print('Getting file: %s' % file_dest)
		file_dest = dests_examination[i] + file_dest
		urllib.request.urlretrieve(file_url, file_dest)
		cont += 1

		if cont == 200:
			print('Got 200 files, requests will stop for 10 min in order to avoid crashing...')
			time.sleep(600)
			cont = 0

	file_urls_laboratory[i] = [base_url + url['href'] for url in file_urls_laboratory[i]]

	for file_url in file_urls_laboratory[i]:
		if not os.path.exists(dests_laboratory[i]):
			os.makedirs(dests_laboratory[i])

		file_dest = file_url.split('/')[-1]
		print('Getting file: %s' % file_dest)
		file_dest = dests_laboratory[i] + file_dest
		urllib.request.urlretrieve(file_url, file_dest)
		cont += 1

		if cont == 200:
			print('Got 200 files, requests will stop for 10 min in order to avoid crashing...')
			time.sleep(600)
			cont = 0


	file_urls_questionnaire[i] = [base_url + url['href'] for url in file_urls_questionnaire[i]]

	for file_url in file_urls_questionnaire[i]:
		if not os.path.exists(dests_questionnaire[i]):
			os.makedirs(dests_questionnaire[i])
			
		file_dest = file_url.split('/')[-1]
		print('Getting file: %s' % file_dest)
		file_dest = dests_questionnaire[i] + file_dest
		urllib.request.urlretrieve(file_url, file_dest)
		cont += 1

		if cont == 200:
			print('Got 200 files, requests will stop for 10 min in order to avoid crashing...')
			time.sleep(600)
			cont = 0