from bs4 import BeautifulSoup
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
opt = webdriver.ChromeOptions()
opt.binary_location = r"C:\Users\Windows\VS\PY\PROJECTS\DATA-SCIENCE\DS-1\bin\chrome-win64\chrome.exe"
opt.add_argument('--start-maximized') #or '--window-size=1920x1080'
# opt.add_argument('--headless') 
# opt.add_argument('--disable-gpu')    
driver = webdriver.Chrome(service=Service(r'C:\Users\Windows\VS\PY\PROJECTS\DATA-SCIENCE\DS-1\bin\chromedriver-win64\chromedriver.exe'),options=opt)
productList = []
priceList = []
discountList =[]
num_ratingList=[]
ratingList=[]
divindexList=[]
driver.get('https://www.amazon.in/deals?ref_=nav_cs_gb&discounts-widget=%2522%257B%255C%2522state%255C%2522%253A%257B%255C%2522refinementFilters%255C%2522%253A%257B%257D%257D%252C%255C%2522version%255C%2522%253A1%257D%2522')
# ---------------------------------------------------------------------------
def parse():
    responsePageSource = driver.page_source
    doc = BeautifulSoup(responsePageSource, "html.parser")
    
    dealPageTag = doc.find(attrs={'data-testid': "virtuoso-item-list"})
    divIndexTag = dealPageTag.find_all(attrs={'data-index':True})
    
    
    if divIndexTag:
        for eachTag in divIndexTag:
            indexVal = eachTag['data-index']
            print(indexVal)
            if indexVal in divindexList:
                continue
            divindexList.append(indexVal)
            aTags = eachTag.find_all('a', href=True, attrs={'data-testid': "product-card-link"})
            for aTag in aTags:
                href = aTag['href']
                driver.get(href)
                productPageSource = driver.page_source
                productDoc = BeautifulSoup(productPageSource, "html.parser")
                
                cTag = productDoc.find(attrs={'id': "centerCol"})
                
                name = cTag.find('span', attrs={'id': 'productTitle'})
                price = cTag.find('span', attrs={'class': 'a-price-whole'})
                deal = cTag.find('span', attrs={'class': 'a-size-large a-color-price savingPriceOverride aok-align-center reinventPriceSavingsPercentageMargin savingsPercentage'})
                num_ratings = cTag.find('span',attrs={'id':'acrCustomerReviewText'})
                ratings = cTag.find('span',attrs={'class':'a-size-base a-color-base'})

                productList.append(name.text.strip() if name else "*")
                priceList.append(price.text.strip() if price else "$")
                discountList.append(deal.text.strip() if deal else 'LIMITED TIME DEAL')
                num_ratingList.append(num_ratings.text.rstrip('ratings') if num_ratings else "-")
                ratingList.append(ratings.text.rstrip() if ratings else 2.5)
                driver.back()
                time.sleep(2)  

try:
    INCREMENT_SCROLL = 900
    parse()
    for i in range(2):        
        for count in range(3): #1 down --> 40 px
            driver.execute_script(f"window.scrollBy(0, {INCREMENT_SCROLL});")
            if i!=2:
                time.sleep(2)  
            else:
                time.sleep(8)
            parse()
        
        
    
except Exception as e:
    print(e)
finally:
    df = pd.DataFrame({'Product Name': productList, 'Price': priceList, 'Discount': discountList,'Num_Ratings':num_ratingList,'ratings':ratingList})
    df.to_csv('products.csv', index=False, encoding='utf-8')
    driver.quit()
