from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains
import pandas as pd
import time

#### Loading URL ####
df1 = pd.read_csv("url.csv")
url = df1.url
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(
    options=options, executable_path=r'./chromedriver.exe')
driver.maximize_window()
shp = []
prc = []
crt = []
cut = []
col = []
clrt = []
report = []
diamond_list = []
for j in range(0, len(url)):
    if j==1 or j==4 or j==7:
        # j==0 ----- Round
        # j==1 ----- Oval
        # j==2 ----- Cushion
        # j==3 ----- Pear
        # j==4 ----- Princess
        # j==5 ----- Emarald
        # j==6 ----- Marquise
        # j==7 ----- Asscher
        # j==8 ----- Radiant
        # j==9 ----- Heart
        driver.get(url[j])
        #### LAB Diamond ####
        driver.find_element(By.XPATH, '//*[@id="diamond-category-switch-outside"]/li[2]').click()
        time.sleep(5)

        ##### Carat Option ######
        a = driver.find_element(By.XPATH, '//*[@id="max_carat_display"]')
        action = ActionChains(driver)
        action.double_click(a)
        action.send_keys('5.99')
        action.send_keys(Keys.ENTER)
        action.perform()

        #### Move to the next filter ####
        driver.find_element(By.XPATH, '//*[@id="collapseFilter"]/div/ul/li[2]').click()
        
        #### CutGrade Option ####
        Cut = driver.find_element(By.XPATH, '//*[@id="cuts"]')
        Cut_min = driver.find_element(By.XPATH, '//*[@id="cut_slider"]/div/div[1]')
        Cut_max = driver.find_element(By.XPATH, '//*[@id="cut_slider"]/div/div[2]')
        cut_left = driver.find_element(By.XPATH, '//*[@id="cut_slider"]/div/div[4]')
        cut_right = driver.find_element(By.XPATH, '//*[@id="cut_slider"]/div/div[3]')
        driver.execute_script(
            "arguments[0].setAttribute('value','Very Good')", Cut)
        driver.execute_script(
            "arguments[0].setAttribute('style','left: 40%;')", Cut_min)
        driver.execute_script(
            "arguments[0].setAttribute('style','left: 60%;')", Cut_max)
        driver.execute_script(
            "arguments[0].setAttribute('style','right: 60%;')", cut_right)
        driver.execute_script(
            "arguments[0].setAttribute('style','left: 60%;')", cut_left)
        action = ActionChains(driver)
        action.perform()
        time.sleep(5)
        driver.find_element(By.XPATH, '//*[@id="setting_morefilters"]/div/div[3]/div[1]').click()
        time.sleep(5)
        driver.find_element(By.XPATH, '//*[@id="setting_morefilters"]/div/div[3]/div[1]').click()

        #### MOve to the next filter ####
        driver.find_element(By.XPATH, '//*[@id="collapseFilter"]/div/ul/li[3]').click()
        time.sleep(5)

        #### Florescence Option ####
        Florescence = driver.find_element(By.XPATH, '//*[@id="fluorescences"]')
        Florescence_css = driver.find_element(By.XPATH, '//*[@id="fluorescence_slider"]/div/div[1]')
        Florescence_min = driver.find_element(By.XPATH, '//*[@id="fluorescence_slider"]/div/div[3]')
        driver.execute_script(
            "arguments[0].setAttribute('value','Faint,None')", Florescence)
        driver.execute_script(
            "arguments[0].setAttribute('style','left: 60%;')", Florescence_css)
        driver.execute_script(
            "arguments[0].setAttribute('style','right: 40%;')", Florescence_min)
        action.perform()
        time.sleep(2)

        #### Clicking GIA ####
        if j==1:    #### you need to change the j as the first loop number
            driver.find_element(By.XPATH, '//*[@id="report_div"]/div/ul/li[2]/div/label/i').click()
        time.sleep(2)
        
        #### Finding tables and scraping ####
        table_tr = driver.find_elements(By.XPATH, '//*[@id="diamonds_search_table"]/div/a/table/tbody/tr')

        for i in range(0, len(table_tr)):
            tr_td = table_tr[i].find_elements(By.TAG_NAME, 'td')
            new_data = {}
            Shape = tr_td[2].text
            shp.append(Shape)
            new_data["Shape"] = Shape

            Price = tr_td[3].text
            prc.append(Price)
            new_data["Price"] = Price

            Carat = tr_td[4].text
            crt.append(Carat)
            new_data["Carat"] = Carat

            CutGrade = tr_td[5].text
            cut.append(CutGrade)
            new_data["CutGrade"] = CutGrade

            Color = tr_td[6].text
            col.append(Color)
            new_data["Color"] = Color

            Clarity = tr_td[7].text
            clrt.append(Clarity)
            new_data["Clarity"] = Clarity

            Repo = tr_td[9].text
            report.append(Repo)
            new_data["report"] = Repo
            diamond_list.append(new_data)   
            dict = {'Shape': shp, 'Price': prc, 'Carat': crt, 'CutGrade': cut,
                'Color': col, 'Clarity': clrt, 'report': report}

            df = pd.DataFrame(dict)

            df.to_csv('Result_diamond.csv')  

print(diamond_list)
while True:
    pass
