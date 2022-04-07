from selenium import webdriver  
import time  
import urllib  
from slugify import slugify
import requests
import random
import os


conference = 'neurips'
conference_url = "https://papers.nips.cc/paper/2019" # the conference url to download papers from
chromedriver_path = './chromedriver' # the chromedriver.exe path
root = './out/' # file path to save the downloaded papers

os.makedirs(root, exist_ok=True)
print(root)


driver = webdriver.Chrome(chromedriver_path)  
driver.get(conference_url)

from retrieve_titles_urls_from_websites import *
retrieve = globals()['retrieve_from_'+conference]
print('Retrieving pdf urls. This could take some time...')
pdfurllist, pdfnamelist = retrieve(driver)

# check the retrieved urls
print('The first 5 pdf urls:\n')
for i in range(5):
    print(pdfurllist[i])
print('\nThe last 5 pdf urls:\n')
for i in range(5):
    print(pdfurllist[-(i+1)])
print('=======================================================')

# check the retrieved paper titles
print('The first 5 pdf titles:\n')
for i in range(5):
    print(pdfnamelist[i])
print('\nThe last 5 pdf titles:\n')
for i in range(5):
    print(pdfnamelist[-(i+1)])


print('The number of papers is ', len(pdfnamelist))
assert len(pdfnamelist)==len(pdfurllist), 'The number of titles and the number of urls are not matched. \
                                            You might solve the problem by checking the HTML code in the \
                                            website yourself or you could ask the author by raising an issue.'



print('Start downloading')
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:57.0) Gecko/20100101 Firefox/57.0'}
for i, url in enumerate(pdfurllist):
    if url != None :      
        pdfname = slugify(pdfnamelist[i])
        if os.path.isfile(root+'/'+pdfname+".pdf"):
            print('existed', i, '\t', pdfnamelist[i], '\t', pdfurllist[i])
        else:
            print(i, '\t', pdfnamelist[i], '\t', pdfurllist[i])
            data = requests.get(pdfurllist[i], timeout=80, headers=headers).content
            
            with open(root+'/'+pdfname+".pdf", 'wb')  as f:
                f.write(data)  
            _ = time.sleep(random.uniform(4,5)) 