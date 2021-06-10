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

def sign_in():
    driver.get('https://mail.ru/')

    elem = driver.find_element_by_xpath("//input[@data-testid='login-input']")
    elem.send_keys('zero-9495@mail.ru')
    elem.send_keys(Keys.ENTER)

    elem = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//input[@data-testid='password-input']"))
    )
    elem.send_keys('Ekaterinburg*88!')
    elem.send_keys(Keys.ENTER)

    letter = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//a[@class='llc js-tooltip-direction_letter-bottom js-letter-list-item llc_pony-mode llc_normal']"))
    )

def get_urls():
    sign_in()

    urls = set()
    for i in range(5):
        letters = driver.find_elements_by_xpath("//a[@class='llc js-tooltip-direction_letter-bottom js-letter-list-item llc_pony-mode llc_normal']")

        for letter in letters:
            urls.add(letter.get_attribute('href'))

        actions = ActionChains(driver)
        actions.move_to_element(letters[-1])
        actions.perform()

    urls_list = []
    for url in urls:
        urls_list.append({'url': url})
    return urls_list


sign_in()

urls = get_urls()

# Запись собранных вакансий в БД
db.letters.insert_many(urls)

for letter in db.letters.find({}):
    driver.get(letter['url'])

    x = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//div[@class='letter-body__body-content']"))
    )

    letter_dict = {
        'letter_author': driver.find_element_by_xpath("//div[@class='letter__author']/span").get_attribute('title'),
        'letter_date': driver.find_element_by_xpath("//div[@class='letter__date']").text,
        'letter_subject': driver.find_element_by_xpath("//h2").text,
        'letter_body': driver.find_element_by_xpath("//div[@class='letter-body__body-content']").text
    }

    db.letters.update({'_id': letter['_id']}, {'$set': letter_dict})

driver.close()
