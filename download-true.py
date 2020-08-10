import os
import requests
import shutil
from urllib.parse import urljoin
from bs4 import BeautifulSoup

# url = input("Insert a download link:  ")
url = "https://www.bundestag.de/dokumente/protokolle"

folder_location = f"{os.getcwd()}/bunder/"

if not os.path.exists(folder_location):os.mkdir(folder_location)

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")     
for link in soup.select("a[href$='.pdf']"):
    filename = os.path.join(folder_location,link['href'].split('/')[-1])
    with open(filename, 'wb') as f:
        f.write(requests.get(urljoin(url,link['href'])).content)


'''
files = os.listdir(folder_location)

for f in files:
    name = f[:2]
    path = f"{os.getcwd()}/Stenogramy/{name}"   

    try:
        os.mkdir(path)
    except:
        pass
    shutil.move (f"{folder_location}/{f}", path)
'''


    


