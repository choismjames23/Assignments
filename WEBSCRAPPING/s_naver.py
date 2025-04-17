from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

keyword = input("겁색 키워드 입력: ")
url = "https://search.naver.com/search.naver?ssc=tab.blog.all&sm=tab_jum&query=" + keyword

header_user = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
option__ = Options()
option__.add_argument(f"User-Agent={header_user}")
option__.add_experimental_option("detach", True)
option__.add_experimental_option('excludeSwitches',["enable-logging"])

driver = webdriver.Chrome(options=option__)
driver.get(url)

for i in range(5):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(1)

html = driver.page_source
soup = BeautifulSoup(html, "html.parser")

result = soup.select(".view_wrap")
rank = 1
for i in result: 
    ad = i.select_one(".link_ad") #값이 있어 -> True / False / 챌린지 힌트
    
    if not ad :
        title = i.select_one(".title_link").text
        link = i.select_one(".title_link")["href"]
        writer = i.select_one(".name").text #작성자
        dsc = i.select_one(".dsc_link").text #요약 내용
        print(f"번호 : {rank}")
        print(f"제목 : {title}")
        print(f"링크 : {link}")
        print(f"작성자 : {writer}")
        print(f"글요약 : {dsc}")
        print('---------------')
        rank += 1