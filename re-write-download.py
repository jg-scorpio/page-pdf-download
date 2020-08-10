from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import re
import os


#Creating driver object with a path to a webdriver for a desired browser
driver = webdriver.Firefox(executable_path=f"{os.getcwd()}/geckodriver")


#Providing a base url for the website and linking it to the webdriver
url = "http://edoc.sabor.hr/"

driver.get(url)

#Looping for a desired number of pages
for count in range (217,252):

    print (f" ---- Page no. - {count}  ----\n")
    #Changing current page to the number of the current iteration
    pageInput = driver.find_element_by_id("ctl00_ContentPlaceHolder_gvAkti_PagerBarB_GotoBox_I")
    pageInput.send_keys(Keys.CONTROL + "a")
    pageInput.send_keys(Keys.DELETE)
    pageInput.send_keys(count)
    pageInput.send_keys(Keys.ENTER)


    #Wait for the page to change
    try:
        myElem = WebDriverWait(driver, 25).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'Views/')]")))
    except:
        pass
    time.sleep(13)

    #Find all the links on the current page
    links = driver.find_elements_by_xpath("//a[contains(@href, 'Views/')]")

    #Create temporary lists
    pageUrls = []
    daty = []
    orderList = []
    names = []

    #Iterate thorugh links found
    for link in links[1::7]:
        #Click on one of the links 
        
        link.click()
        
        time.sleep(3)
        
        window_after = driver.window_handles
        driver.switch_to.window(window_after[1])
        
        time.sleep(1)

        #Check if the phonogram is avalible
        try:
            myElem = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.LINK_TEXT, "Fonogram rasprave")))
        except:
            print("nie znalazlem go")
            time.sleep(4)
            driver.close()
            window_after = driver.window_handles
            driver.switch_to.window(window_after[0])
            continue
        
        
        #Click the phonogram link
        phonLink = driver.find_element_by_link_text("Fonogram rasprave")
        phonLink.click()
        
        time.sleep(1)

        window_after = driver.window_handles
        driver.switch_to.window(window_after[2])

        time.sleep(4)

        #Take dates of the phonogram and number of the sitting
        try:
            myElem = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "dd.dateString")))
        except:
            pass
        date = driver.find_element_by_css_selector("dd.dateString")
        data = (date.text[:-1])
        daty.append(data)
        try:
            order = driver.find_element_by_id("ctl00_ContentPlaceHolder_lblSazivSjednicaDatum")
            order = order.text
            order = order.split(",")
            conv = order[0]
            session = order[1]
            conv = conv.replace("Saziv: ", "")
            session = session.replace(" sjednica: ", "")
            orderList.append(f"Kadencja_{conv}_Posiedzenie_{session}")
        except:
            orderList.append(f"Kadencja_IX_Posiedzenie_16")
        
        #Get page with url for download
        currentUrl = driver.current_url
        pageUrls.append(currentUrl)
        print(currentUrl)
        name = currentUrl.split("=")
        realName = (name[1].split("&"))[0]
        print (realName)
        names.append(realName)

        #Go back to the main page
        time.sleep(0.5)
        driver.close()
        time.sleep(0.5)
        window_after = driver.window_handles
        driver.switch_to.window(window_after[1])
        time.sleep(0.5)
        elems = driver.find_elements_by_name("pnlCitanje1")
        if not elems:
            pass
        else:
            time.sleep(2)
            second =  driver.find_element_by_name("pnlCitanje1")
            second.click()
            try:
                myElem = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.LINK_TEXT, "Fonogram rasprave")))
            except:
                print("nie znalazlem go")
                time.sleep(4)
                driver.close()
                window_after = driver.window_handles
                driver.switch_to.window(window_after[0])
                continue
            phonLink = driver.find_element_by_link_text("Fonogram rasprave")
            phonLink.click()
            
            time.sleep(1)

            window_after = driver.window_handles
            driver.switch_to.window(window_after[2])

            time.sleep(4)

            #Take dates of the phonogram and number of the sitting
            try:
                myElem = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "dd.dateString")))
            except:
                pass
            try:
                date = driver.find_element_by_css_selector("dd.dateString")
                data = (date.text[:-1])
                daty.append(data)
            except:
                daty.append("manual")
            
            try:
                order = driver.find_element_by_id("ctl00_ContentPlaceHolder_lblSazivSjednicaDatum")
                order = order.text
                order = order.split(",")
                conv = order[0]
                session = order[1]
                conv = conv.replace("Saziv: ", "")
                session = session.replace(" sjednica: ", "")
                orderList.append(f"Kadencja_{conv}_Posiedzenie_{session}")
            except:
                orderList.append(f"Kadencja_IX_Posiedzenie_16")
            
            #Get page with url for download
            currentUrl = driver.current_url
            pageUrls.append(currentUrl)
            print(currentUrl)
            name = currentUrl.split("=")
            realName = (name[1].split("&"))[0]
            print (realName)
            names.append(realName)

            driver.close()
            time.sleep(1)

            window_after = driver.window_handles
            driver.switch_to.window(window_after[1])

        driver.close()
        time.sleep(0.5)
        window_after = driver.window_handles
        driver.switch_to.window(window_after[0])
        time.sleep(0.5)


    #Download PDF file from each obtained link
    i = 0
    for url in pageUrls:
        page = "http://edoc.sabor.hr"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        links = soup.find_all('a', href=True)
        link = ""
        for a in links:
            txt = a['href']
            if ".." in txt:
                link = txt[2:]    
                break
        folder_location = f"{os.getcwd()}/Stenogramy/{orderList[i]}/"
        if not os.path.exists(folder_location):os.mkdir(folder_location)
        folder_location = f"{os.getcwd()}/Stenogramy/{orderList[i]}/{daty[i]}/"
        if not os.path.exists(folder_location):os.mkdir(folder_location)
        fileUrl = urljoin(page,link)
        filename = os.path.join(folder_location,f"{names[i]}.pdf")
        print (filename)
        with open(filename, 'wb') as f:
            f.write(requests.get(fileUrl).content)
        i += 1
                






    

driver.quit()