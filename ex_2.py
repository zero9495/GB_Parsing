from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['test_database']

chrome_options = Options()
# chrome_options.add_argument('start-maximized')
driver = webdriver.Chrome('/home/zero9495/Downloads/chromedriver', options=chrome_options)


def get_mvideo():
    driver.get('https://www.mvideo.ru/')

    goods_set = set()

    for x in range(5):
        print(x)
        goods = driver.find_elements_by_xpath("""//ul[contains(@data-init-param, '"title":"Хиты продаж"')]/li//h3/a""")

        for good in goods:
            goods_set.add(good.get_attribute('href'))

        button = driver.find_element_by_xpath("""//ul[contains(@data-init-param, '"title":"Хиты продаж"')]/../../a[contains(@class,'next-btn')]""")

        actions = ActionChains(driver)
        actions.move_to_element(button).click()
        actions.perform()

        button = WebDriverWait(driver, 10).until(
            EC.invisibility_of_element_located((By.XPATH, """//ul[contains(@data-init-param, '"title":"Хиты продаж"') and contains(@style, 'auto auto 0px')]"""))
        )

        button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, """//ul[contains(@data-init-param, '"title":"Хиты продаж"') and contains(@style, 'auto auto 0px')]"""))
        )

    goods_list = []
    for good in goods_set:
        goods_list.append({'url': good, 'site': 'mvideo'})
    return goods_list


def get_ot():
    driver.get('https://www.onlinetrade.ru/')

    goods_set = set()

    for x in range(1, 6):
        goods = driver.find_elements_by_xpath("""//div[@id='tabs_hits']//div[contains(@class, 'swiper-slide indexGoods__item')]//a[@class='indexGoods__item__image']""")

        for good in goods:
            goods_set.add(good.get_attribute('href'))

        button = driver.find_element_by_xpath("""//div[@id='tabs_hits']//span[contains(@class, 'swiper-button-next')]""")

        actions = ActionChains(driver)
        actions.move_to_element(button).click()
        actions.perform()

        button = WebDriverWait(driver, 10).until(
            EC.invisibility_of_element_located((By.XPATH, f"""//div[@id='tabs_hits']//div[contains(@style, 'transition-duration: 0ms;')]"""))
        )

        button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, """//div[@id='tabs_hits']//div[contains(@style, 'transition-duration: 0ms;')]"""))
        )

    goods_list = []
    for good in goods_set:
        goods_list.append({'url': good, 'site': 'ot'})
    return goods_list


goods_list = get_mvideo() + get_ot()
print(goods_list)

client = MongoClient('localhost', 27017)
db = client['test_database']

db.goods.insert_many(goods_list)