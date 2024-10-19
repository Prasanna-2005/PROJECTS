from bs4 import BeautifulSoup
from time import sleep
import re
import tkinter as tk
skip_words =['cloth','glass','cover']
############################################################################################
def verify_product_details(inp):
    global saved_data
    global query
    input_str = inp.strip()
    
    def is_alpha_string(s):
        return s.isalnum()

    def validate_storage(storage_str):
        if storage_str[-2:].lower()=='gb':
            storage_str = storage_str[:-2]
        if storage_str.isdigit() and int(storage_str) in [64 ,128, 256, 512]:
            return True
        return False

    if (input_str.count(',') == 3 and 
        not re.match(r'^[,.;!?@#$%^&*()-+=]', input_str[0]) and 
        not re.match(r'[,.;!?@#$%^&*()-+=]$', input_str[-1])):
        
        parts = [part.strip() for part in input_str.split(',')]
        brand, model,storage, color = parts
        
        storage= storage.lower().replace(' ','')
        brand = brand.lower().replace(' ','')
        color = color.lower().replace(' ','')
        model = model.lower().replace(' ','')
        
        if (color.isalpha() and model.isalnum() and 
            validate_storage(storage)):
            query = brand+' '+model+' '+(storage if storage.endswith('gb') else storage+'gb')+' '+color
            saved_data = [brand,model,(storage if not storage.endswith('gb') else storage[:-2]),color]

            return(1,[f"Brand: {brand}",
                       f"Model: {model}",
            f"Storage: {storage}",
            f"Color: {color}",]
           )
        else:
            return(0,"Invalid input format. Please ensure storage is a valid.")
    else:
        return(0,"Invalid input format. Please ensure there are exactly 3 commas and no special characters at the start or end.")
############################ INPUT ############################################################################
def io():
    while 1:
        user_input =input("What is the product that you want to buy? (Brandname,model, Storage in gb, color)")
        signal , user_input = verify_product_details(user_input)
        if signal==1:
            message = f"You entered: {user_input} \n\n FINDING BEST PRICE...."
            print(message)
            break
        else:
            message = f" {user_input}"
            print(message)
io()
#----------------------------  SELENIUM   --------------------------------------------#
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
opt = webdriver.ChromeOptions()
opt.binary_location = r"C:\Users\Windows\VS\PY\PROJECTS\DATA-SCIENCE\DS-1\bin\chrome-win64\chrome.exe"
opt.add_argument('--start-maximized') 
opt.add_argument("--disable-infobars")
opt.add_argument("--disable-dev-shm-usage")
opt.add_argument("--no-sandbox")
opt.add_experimental_option('excludeSwitches', ['enable-logging'])
# opt.add_argument('--headless') 
# opt.add_argument('--disable-gpu')    
driver = webdriver.Chrome(service=Service(r'C:\Users\Windows\VS\PY\PROJECTS\DATA-SCIENCE\DS-1\bin\chromedriver-win64\chromedriver.exe'),options=opt)
####################   SCRAP  ########################################################
def amazon():
    def check_color_below(centre_tag):
        colors=[]
        c_variation_tag = centre_tag.find('div',{'id':'variation_color_name'})
        if c_variation_tag:
            c_variations = c_variation_tag.find_all('li')
            for i in c_variations:
                if i.find('img')['alt'] :
                    colors.append(i.find('img')['alt'].lower())
            
            if colors:
                for i in colors:
                    if splitted_data[3] in i :
                        return True 
        return False
    def check_size_below(centre_tag):
        sizes=[]
        s_variation_tag = centre_tag.find('div',{'id':'variation_size_name'})
        if s_variation_tag:
            s_variations = s_variation_tag.find_all('li')
            for i in s_variations:
                if i.find('p'):
                    sizes.append((i.find('p').text,i.find('span',{'class':'a-declarative'}).find('span',{'class':'a-button'}).attrs['id']))
            if sizes :
                for color_,prefix_tag in sizes:
                    if splitted_data[2] in color_.lower().replace(' ',""):
                        butt_on = driver.find_element(By.ID,prefix_tag+'-announce')
                        if butt_on:
                            butt_on.click()
                            return True
        return False

    driver.get('https://www.amazon.in')
    search_box = driver.find_element(By.ID, 'twotabsearchtextbox')
    search_box.send_keys(query_)
    search_box.send_keys(Keys.ENTER)  #moving to next page contains--->list of target phones
    sleep(3)
    soup = BeautifulSoup(driver.page_source,'html.parser')
    all_res = soup.find('span',attrs={'data-component-type':"s-search-results"})
    for attempt in range(5):
            con = False 
            size = False
            color = False
            try:  
                indi_from_all= all_res.find('div',attrs={"data-index":str(attempt+2)})   #div pointing the single phone from all-results page
                if indi_from_all:
                    mobile_data = indi_from_all.find('span',{'class':'a-size-medium a-color-base a-text-normal'}).text.replace(" ",'').lower()
                    price_a = indi_from_all.find('span',{'class':'a-price-whole'}).text
                    cont = 1
                    for word in skip_words:
                        if word in mobile_data:
                            cont = 0
                            break
                    if cont == 0:
                        continue
                    if ((splitted_data[0] in mobile_data) and (splitted_data[1] in mobile_data)):
                        con = True
                        if((splitted_data[2] in mobile_data) and (splitted_data[3] in mobile_data)):
                            size = True
                            color = True    
                        else:
                            if not splitted_data[2] in mobile_data:
                                phonelink = indi_from_all.find('a').attrs['href']
                                driver.get("https://www.amazon.in"+phonelink)
                                sleep(1.5)
                                eachphone = BeautifulSoup(driver.page_source,'html.parser')
                                centre_tag =eachphone.find('div',{'id':"centerCol"})
                                color = check_color_below(centre_tag)
                                size = check_size_below(centre_tag)
                                if size == True:
                                    sleep(2.5)
                                    eachph = BeautifulSoup(driver.page_source,'html.parser')
                                    centre_ta =eachph.find('div',{'id':"centerCol"})
                                    price_a = centre_ta.find('span',{'class':'a-price-whole'}).text
                            if not color:
                                phonelink = indi_from_all.find('a').attrs['href']
                                driver.get("https://www.amazon.in"+phonelink)
                                sleep(1.5)
                                eachphone = BeautifulSoup(driver.page_source,'html.parser')
                                centre_tag =eachphone.find('div',{'id':"centerCol"})
                                color = check_color_below(centre_tag)

                            

                        pricelist['amazon']=[price_a,(1 if color else 0)]
                        break
                    con = False 
                    size = False
                    color = False
                    driver.back()
            except Exception as E:
              pass
def flipkart():
    def checkcolor(soupobj):
        colorlist=[]
        p = soupobj.find('span',{'id':'Color'})
        if p:
            par = p.parent
            if par:
                col = par.find_all('li',{'class':'aJWdJI'})
                for i in col:
                    data = i.find('div',{'class':'V3Zflw QX54-Q E1E-3Z'})
                    colorlist.append(data.text.lower().replace(' ',''))
                if colorlist:
                    for i in colorlist:
                        if splitted_data[3] in i :
                            return True
        return False
    def checksize(soupobj):
        sizelist=[]
        p= soupobj.find('span',{'id':'Storage'})
        if p:
            par = p.parent
            if par:
                sizetags = par.find_all('li',{'class':'aJWdJI'})
                for i in sizetags:
                    data = i.find('div',{'class':'V3Zflw QX54-Q E1E-3Z'})
                    sizelist.append((data.text,i.find('a').attrs['href']))
                if sizelist :
                    for size_,href_for_size in sizelist:
                        if splitted_data[2] in (size_.lower().replace(' ','')):
                            driver.get('https://www.flipkart.com'+href_for_size)
                            sleep(0.5)
                            return True
        return False
    driver.get('https://www.flipkart.com')
    search_box = driver.find_element(By.CLASS_NAME,'Pke_EE')
    search_box.send_keys(query_)
    search_box.send_keys(Keys.ENTER)  #moving to next page contains--->list of target phones
    sleep(1.5)
    soup = BeautifulSoup(driver.page_source,'html.parser')
    all_result_div = soup.find('div',attrs={'class':"DOjaWF gdgoEp"})
    indi_div = all_result_div.find_all('div',attrs={'class':'cPHDOP col-12-12'})[:4]
    for attempt in range(4):
        con = False ; size = False; color = False
        try:
            ind_phone = indi_div[attempt]
            mob_detail_tag = ind_phone.find('div',{'class':'KzDlHZ'})
            mob_details = mob_detail_tag.text.replace(' ',"").lower()
            price_f = ind_phone.find('div',{'class':'Nx9bqj _4b5DiR'}).text
            cont = 1
            for word in skip_words:
                    if word in mob_details:
                        cont = 0
                        break
            if cont == 0:
                        continue   
            if splitted_data[0] in mob_details and splitted_data[1] in mob_details:
                con = True
                             
                if splitted_data[3] in mob_details and splitted_data[2] in mob_details:
                    size = True
                    color = True
                else:
                    if not size:
                        link = ind_phone.find('a')['href']
                        driver.get('https://www.flipkart.com'+link)
                        soup = BeautifulSoup(driver.page_source,'html.parser')
                        size = checksize(soup)
                        color = checkcolor(soup)
                        if size:
                            soup1 = BeautifulSoup(driver.page_source,'html.parser')
                            ptag = soup1.find('div',{'class':'hl05eU'})
                            price_f = ptag.find('div').text  #newPrice
                    if not color:
                        link = ind_phone.find('a')['href']
                        driver.get('https://www.flipkart.com'+link)
                        soup_ = BeautifulSoup(driver.page_source,'html.parser')
                        color = checkcolor(soup_)
                pricelist['flipkart']=[price_f,(1 if color else 0)]
                break
            con = False
            size =False
            color =False    
        except Exception as e:
            print(e)
            pass
def poorvika():
    def checkcolor(soupobj):
        colorlist=[]
        p= soupobj.find('h3',string="Color").parent
        if p:
            par = p.parent
            if par:
                clr = par.find_all('div',{'class':'new-variants_space_margin__atojQ text-center'})
                for i in clr:
                    data = i.find('label',{'class':'new-variants_variant_label__JXnrg'})
                    colorlist.append(data.text.lower().replace(' ',''))
                if colorlist:
                    for i in colorlist:
                        if splitted_data[3] in i :
                            return 1    
        return 0
    def checksize(soupobj):
        sizelist=[]
        p= soupobj.find('h3',string="Storage")
        if p:
            par = par.parent
            if par:
                size = par.find_all('div',{'class':'false text-center'})
                for ref,i in enumerate(size):
                    data = i.find('label',{'class':'new-variants_variant_label__JXnrg'})
                    sizelist.append((data,ref))
        
                if sizelist :
                    for r,i in sizelist:
                        if splitted_data[2] in r.text.lower().replace(' ',"") :
                            driver.execute_script(f'''if(document.querySelectorAll('h3')[1].textContent === 'Storage')
                                                    document.querySelectorAll('h3')[1].parentElement.getElementsByTagName('label')[{r}].parentElement.click();
                                                
                                                else if(document.querySelectorAll('h3')[2].textContent === 'Storage')
                                                    document.querySelectorAll('h3')[2].parentElement.getElementsByTagName('label')[{r}].parentElement.click();
                                                ''')
                            return 1 
        return 0
    driver.get('https://www.poorvika.com')
    wait = WebDriverWait(driver, 10)
    search_box = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'text-black')))
    search_box.send_keys(query_)
    search_box.send_keys(Keys.ENTER)  #moving to next page contains--->list of target phones
    sleep(10)
    soup = BeautifulSoup(driver.page_source,'html.parser')
    all_result_div = soup.find('div',attrs={'class':"search-list_search_grid_four__aa4uY mt-2"})
    indi_div = list(all_result_div.children)   #as it is iterable
    
    for attempt in range(12):
        con = False ; size = False; color = False
        try:
            ind_phone = indi_div[attempt]
            mob_detail_tag = ind_phone.find('div',{'class':'product-cardlist_card__description__eduH5'}).find('a',{'target':'_blank'})
            mob_details = mob_detail_tag.text.replace(' ',"").lower()
            price_p = ind_phone.find('span',{'class':'whitespace-nowrap'}).text
            
            cont = 1
            for word in skip_words:
                    if word in mob_details:
                        cont = 0
                        break
            if cont == 0:
                        continue
            
            if splitted_data[0] in mob_details and splitted_data[1] in mob_details:
                con = True
                if splitted_data[3] in mob_details and splitted_data[2] in mob_details:
                    size = True
                    color = True

                else:
                    if not splitted_data[2] in mob_details:
                        link = ind_phone.find('div',{'class':'product-cardlist_card__description__eduH5'}).find('a',{'target':'_blank'})['href']
                        driver.get('https://www.poorvika.com'+link)
                        sleep(4)
                        soup = BeautifulSoup(driver.page_source,'html.parser')
                        size = checksize(soup)
                        color = checkcolor(soup)
                        if size:
                            sleep(5)
                            soup1 = BeautifulSoup(driver.page_source,'html.parser')
                            price_p = soup1.find('div',{'class':'center-content_price_special__LGEjP'}).find('b').text
                    if not color:
                        link = ind_phone.find('div',{'class':'product-cardlist_card__description__eduH5'}).find('a',{'target':'_blank'})['href']
                        driver.get('https://www.poorvika.com'+link)
                        sleep(4)
                        soup = BeautifulSoup(driver.page_source,'html.parser')
                        color = checkcolor(soup)
            
                pricelist['poorvika']=[price_p,(1 if color else 0)]
                break
    
            con = False
            size =False
            color =False    
        except Exception as e :

            pass
def final_price_list(sdata):
    best = ['',float('inf')]
    l=[]
    if not pricelist:
        print('Error Retriving data/Mobile not found')
        exit()
    for site in pricelist:
        price , c_avail = pricelist[site]
        price = price.replace(',','').replace(' ','')

        if not price[0].isnumeric():
            price = price[1:]
        
        if int(price) < best[1]:
            best = [site,int(price)]
        s = site + ": RS " + f"{price}" 
        if not c_avail:
            s += " (Other color)"
        l.append((site,s))
    print(f"You can buy {sdata} at {best[0]} for RS{best[1]}.)")
    if len(pricelist) > 1:
        print('Other Competitive prices:::')
        for site_,data in l:
            if site_ not in best[0]:
                print(data)
#************************************ MAIN ************************************************
sites = ['https://www.amazon.in',
         'https://www.flipkart.com',
         'https://www.poorvika.com'         
         ]

query_ = query.replace(','," ").lower()              
splitted_data = saved_data
pricelist={}
try:
    amazon()
    flipkart()
    poorvika()
except:
    pass
final_price_list(query)
driver.quit()