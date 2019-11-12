#Написать программу, которая собирает «Хиты продаж» с сайта техники mvideo и складывает данные в БД.
# Магазины можно выбрать свои. Главный критерий выбора: динамически загружаемые товары

# Хотя кнопка пролистывания нажимается, остальные хиты все равно не подгружаются
# Также автоматически не нажимается кнопка закрытия всплывающего окна, если окно вовремя не закрыть, будет ошибка
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from pymongo import MongoClient
from selenium.webdriver.common.keys import Keys
chrome_options = Options()
chrome_options.add_argument('start-maximized')
#chrome_options.add_argument('--headless')

import time
# Mongo
client = MongoClient('localhost', 27017)
goods = client['mvideo']
mvideo = goods.hits

driver = webdriver.Chrome(options=chrome_options)
driver.get('https://www.mvideo.ru/')
assert "М.Видео - интернет-магазин цифровой и бытовой техники и электроники" in driver.title

try:
    push = WebDriverWait(driver, 10).until(
        # ec.presence_of_element_located((By.CLASS_NAME, 'catalog__pagination-button'))
        ec.element_to_be_clickable((By.CLASS_NAME, 'PushTip-button'))
    )
    push.send_keys(Keys.RETURN)

except Exception as e:
    print(e)


# time.sleep(2)
#driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

lasthit = WebDriverWait(driver, 10).until(ec.element_to_be_clickable(
    (By.XPATH, '(//div[@class="carousel-paging"])[3]/a[position()=last()]')))
lasthit.click()

#driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#driver.implicitly_wait(3)


''' 
# Другой способ - нажимая кнопку справа от хитов
end = 0
while end == 0:
    try:
        #button = driver.find_elements_by_class_name('sel-hits-button-next')[1]
        button = driver.find_elements_by_xpath('//div[@class="sel-hits-button-next"]//a[@class="sel-hits-button-next"]')
        button = driver.find_elements_by_xpath(f'/html[1]/body[1]/div[1]/div[1]/div[3]/div[4]/'
                                               f'div[1]/div[2]/div[1]/div[1]/div[1]/div[2]/a[{5}]')
        button.click()

        print('a')
    except:
        print('b')
        end = 1
'''
time.sleep(60)

hits = driver.find_elements_by_xpath('//div[4]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/ul/li')
print(len('hits'))

for i in range(len('hits')):
    i += 1
    mhit = {}
    link_to_li = \
        f'//div[4]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/ul/li[{i}]'

    title = driver.find_element_by_xpath(f'{link_to_li}//h4').get_attribute('title')

    price = driver.find_element_by_xpath(f'{link_to_li}//div[@class="c-pdp-price__current"]').get_attribute('innerHTML')
    price = int(''.join(filter(str.isdigit, price)))

    link = driver.find_element_by_xpath(f'{link_to_li}//h4/a').get_attribute('href')

    mhit['link'] = link
    mhit['title'] = title
    mhit['price'] = price
    mvideo.insert_one(mhit)


driver.quit()
