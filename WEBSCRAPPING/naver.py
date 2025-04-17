# ad = i.select_one(".link_ad") #값이 있어 -> True / False / 챌린지 힌트
import requests
from bs4 import BeautifulSoup

keyword = input("검색을 원하는 키워드를 입력해주세요 : ")
url = "https://search.naver.com/search.naver?ssc=tab.blog.all&sm=tab_jum&query=" + keyword # 문자열 + 문자열 합치는 방법
req = requests.get(url)

html = req.text

soup = BeautifulSoup(html, "html.parser") # 규칙이다 / 인스턴스화

result = soup.select(".view_wrap")  #select/find -> select로 찾아서 나오는 결과는 리스트와 동일한 형태다

rank = 1
for i in result: 
    ad = i.select_one(".link_ad") #값이 있어 -> True / False / 챌린지 힌트
    if not ad:
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

