from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from time import sleep
from selenium.common.exceptions import NoSuchElementException

# ссылка на первую страницу книгу
url = "https://readli.net/chitat-online/?b=1273136&pg=1"
# login = ''
# password = ''

options = webdriver.ChromeOptions()
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument("--lang=ru-RU")
options.add_argument('--no-sandbox')
#options.add_argument('--headless')
options.add_argument("--window-size=1200,700")
options.page_load_strategy = 'eager'
options.add_argument('--disable-dev-shm-usage')
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.set_capability("goog:loggingPrefs", {"performance": "ALL", "browser": "ALL"})
service = Service(executable_path='chromedriver.exe')
driver = webdriver.Chrome(service=service, options=options)

driver.get(url) # открываем сайт

# # ищем кнопка для открытия окна входа
# auth_form = driver.find_element(By.XPATH, '//a[@data-popup="#popup-login"]')
# auth_form.click()
# sleep(1)

# # ищем поля ввода логина и пароля
# login_input = driver.find_element(By.XPATH, '//input[@id="loginform-email"]')
# password_input = driver.find_element(By.XPATH, '//input[@id="loginform-password"]')

# login_input.clear()
# password_input.clear()

# login_input.send_keys(login)
# password_input.send_keys(password)
# sleep(1)

# # непосредственно кнопка входа
# auth_button = driver.find_element(By.XPATH, '//button[@class="popup-form__button button"]')
# auth_button.click()
# sleep(1)

# открываем скелет fb2
with open('fish.fb2', 'r', encoding='utf-8') as file:
    fish = file.read()

head = driver.find_element(By.XPATH, '//div[@class="reading__left"]').text
head_list = head.split('\n')
title = head_list[0]
author = head_list[1]

# открываем книгу
with open(f'{title} - {author}.fb2', 'w', encoding='utf-8') as book:

    # добавляем скелет в начало
    book.write(fish)
    check = 0
    while check == 0:
        # берем элемент текущей страницы
        page_element = driver.find_element(By.XPATH, '//div[@class="reading__text"]')

        try:
            # парсим главу
            chapter = page_element.find_element(By.XPATH, './h3')

            book.write(f'''
</section>\n
<section>\n
<title>\n
<p>{chapter.text}</p>\n
</title>\n
<empty-line/>\n
''')
        except NoSuchElementException as ex:
            pass

        try:
            # парсим все параграфы на странице
            p_elements = page_element.find_elements(By.XPATH, './p')

            p_text = []
            for paragraph in p_elements:
                p_text.append(paragraph.text)

            for paragraph in p_text:
                book.write(f'<p>{paragraph}</p>\n')
            
        except NoSuchElementException as ex:
            raise(ex)
        
        try:
            next_button = driver.find_element(By.XPATH, '//a[@class="page-nav-1__button button"][text()="Следующая"]')
            if next_button.is_enabled(): # тыкаем переход только если кнопка активна
                next_button.click()
                print('переход на следующую страницу')
                sleep(1)
        except NoSuchElementException:
            check = 1

    book.write('</section>\n</body>\n</FictionBook>\n')
