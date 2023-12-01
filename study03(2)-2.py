from flask import Flask, render_template
import datetime
from bs4 import BeautifulSoup as bs
import urllib.request as req
import urllib
# index3.html

app = Flask(__name__)

def get_today_date():
    today = datetime.datetime.today()
    return today.strftime("%Y-%m\\%d.")

def today_main_post():
    today_date = get_today_date()
    today_date = str(today_date).replace("-", "년").replace("\\", "월").replace(".", "일")
    dates = []
    titles = []
    try:
        url = "https://www.boannews.com/media/t_list.asp"
        res = req.urlopen(url)
        soup = bs(res, "html.parser")
        today_main_posts_title = soup.find_all("span", class_="news_txt")
        today_main_posts_dates = soup.select("div.news_list > span.news_writer")
        tmp = today_main_posts_dates
        for ls in tmp:
            today_main_posts_dates = ls.string
            dates.append(today_main_posts_dates.split("|")[1])
        tmp = today_main_posts_title
        for ls in tmp:
            today_main_posts_title = ls.string
            titles.append(today_main_posts_title)
        i = 0
        for ls in dates:
            dates[i] = dates[i].replace(" ", "")
            i += 1
        i = 0
        result = []
        for i, date in enumerate(dates):
            if str(date[0:11]) == today_date:
                result.append(f"#{i + 1} >> {titles[i]}")
        return result
    except urllib.error.URLError as e:
        return f"오류 발생: {e}"

def week_hit_news():
    try:
        url = "https://www.boannews.com/media/o_list.asp"
        res = req.urlopen(url)
        soup = bs(res, "html.parser")
        hit_news_list = soup.select("#main_HitNews > ul > li > a ")
        result = [f"#{i + 1} >> {hit.text}" for i, hit in enumerate(hit_news_list)]
        return result
    except urllib.error.URLError as e:
        return f"오류 발생: {e}"

def search_article(name_article):
    try:
        name_article_euc = name_article.encode("euc-kr")
        name_article_euc_kr = str(name_article_euc)
        name_article_euc_kr = name_article_euc_kr.replace("\\x", "%").replace("b", "").replace("\'", "")
        name_article_euc = urllib.parse.quote(name_article_euc)
        url = "https://www.boannews.com/search/news_list.asp?search=key_word&find=" + name_article_euc
        res = req.urlopen(url)
        soup = bs(res, "html.parser")
        searching_news_title = soup.select("#news_area > div > a")
        result = [f"#{i + 1} >> {title.text}" for i, title in enumerate(searching_news_title) if i < 10 and title is not None]
        return result
    except urllib.error.URLError as e:
        return f"오류 발생: {e}"

@app.route('/')
def index():
    return render_template('index3.html')

@app.route('/today_main_post')
def today_main_post_route():
    result = today_main_post()
    return render_template('result.html', result=result)

@app.route('/week_hit_news')
def week_hit_news_route():
    result = week_hit_news()
    return render_template('result.html', result=result)

@app.route('/search_article/<name_article>')
def search_article_route(name_article):
    result = search_article(name_article)
    return render_template('result.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)