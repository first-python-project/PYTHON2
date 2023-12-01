from flask import Flask, render_template
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

# 웹 서비스 주소
url = "https://www.malware-traffic-analysis.net/2023/index.html"

# Flask 애플리케이션 시작 시 크롤링 수행
crawl_results = []

def crawl_web_service():
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # 제목과 링크 정보 가져오기
    titles = soup.select('#main_content > div.content > ul > li > a.main_menu')
    links = [f"https://www.malware-traffic-analysis.net/2023/{title['href']}" for title in titles]

    # 결과 리스트 초기화 후 추가
    crawl_results.clear()
    crawl_results.extend({"title": title.text.strip(), "link": link} for title, link in zip(titles, links))

    # 결과를 txt 파일에 저장
    with open("result.txt", "w", encoding="utf-8") as file:
        for result in crawl_results:
            file.write(f"{result['title']} - {result['link']}\n")

# Flask 라우트 설정
@app.route('/')
def index():
    # 라우트 요청이 들어올 때마다 크롤링 수행
    crawl_web_service()

    # 템플릿 렌더링
    return render_template('index.html', crawl_results=crawl_results)

if __name__ == '__main__':
    app.run(debug=True)