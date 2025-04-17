from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
#class, id를 css_selector로 이용해서 컨트롤하기 위한 패키지
from selenium.webdriver.common.by import By
#키보드의 입력 형태를 코드로 작성해서 열려있는 크롬에게 전달하기 위한 패키지
from selenium.webdriver.common.keys import Keys
import pymysql

url = "https://kream.co.kr/"

header_user = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
option__ = Options()
option__.add_argument(f"User-Agent={header_user}")
option__.add_experimental_option("detach", True)
option__.add_experimental_option('excludeSwitches',["enable-logging"])

driver = webdriver.Chrome(options=option__)
driver.get(url)
time.sleep(1)
# for i in range(5):
#     driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
#     time.sleep(1)

driver.find_element(By.CSS_SELECTOR, ".btn_search.header-search-button.search-button-margin").click()
time.sleep(2)
keyword = input("원하는 제품, 브랜드 입력: ")
driver.find_element(By.CSS_SELECTOR, ".input_search.show_placeholder_on_focus").send_keys(keyword)
driver.find_element(By.CSS_SELECTOR, ".input_search.show_placeholder_on_focus").send_keys(Keys.ENTER)

for _ in range(10):
    driver.find_element(By.TAG_NAME, "body").send_keys(Keys.PAGE_DOWN)
    time.sleep(0.5)

html = driver.page_source
soup = BeautifulSoup(html, "html.parser")

items = soup.select(".item_inner")

product_list = []

for item in items:
    product_name = item.select_one(".translated_name").text
    if "후드" in product_name:
        #print(product_name)
        category = "상의"
        brand = item.select_one(".brand-name").text
        price = item.select_one(".amount").text
        product_info = [category, brand, product_name, price]
        product_list.append(product_info)

#         print(f"카테고리: {category}")
#         print(f"브랜드: {brand}")
#         print(f"제품명: {product_name}")
#         print(f"가격격 {price}")
# print(product_list)
driver.quit()

connection = pymysql.connect(
    host = '127.0.0.1',
    user = 'root',
    password = 'jssd23!!',
    db = 'kream',
    charset = 'utf8mb4'
)

def execute_query(connection, query, args=None):
    with connection.cursor() as cursor:
        cursor.execute(query, args or ())
        if query.strip().upper().startswith("SELECT"):
            return cursor.fetchall()
        else:
            connection.commit()

for i in product_list:
    execute_query(connection, "INSERT INTO kream (category, brand, product_name, price) VALUES (%s, %s, %s, %s)",(i[0],i[1],i[2],i[3]))

