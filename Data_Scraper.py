import time
from selenium import webdriver 
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import csv 


# options = webdriver.ChromeOptions()
# options.add_argument('--headless') 
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
url = 'https://www.imdb.com/chart/top/'
data = driver.get("https://www.imdb.com/chart/top/")
try:
    driver.get(url)
    print(f"page '{url}' loaded")
    WebDriverWait(driver,10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR,".ipc-page-grid.ipc-page-grid--bias-left"))
    )
    page_source = driver.page_source
    soup = BeautifulSoup(page_source,"html.parser")
    # print(soup)

    all_info = soup.select("ul.ipc-metadata-list li.ipc-metadata-list-summary-item")
    with open ('Data_Scraper_output.csv',"w",newline="",encoding= "utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["TITLE","YEAR OF RELEASE","DURATION","IMDB RATING","VOTE COUNT"])
        for data in all_info:
            title = data.select_one(".ipc-title__text.ipc-title__text--reduced") 
            title = title.get_text(strip=True) if title else " "
            if "." in title:
                parts = title.split(".",1)
                if parts[0].isdigit():
                    title = parts[1].strip()

            yr = data.select(".sc-15ac7568-7.cCsint.cli-title-metadata-item")
            year = yr[0].get_text(strip =True) if yr else ""
            duration = yr[1].get_text(strip =True)  if yr else ""

            rate = data.select_one(".ipc-rating-star--rating")
            rating = rate.get_text(strip =True) if rate else " "

            count = data.select_one(".ipc-rating-star--voteCount")
            voteCount = count.get_text(strip =True)   if count else " "

            writer.writerow([title,year,duration,rating,voteCount])

    print("data saved")

    
except Exception as e :
    print("error: ",e)