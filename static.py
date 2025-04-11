import requests
from bs4 import BeautifulSoup
import json

# 定义请求头，模拟浏览器访问
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# 定义一个函数用于获取每一页的数据
def get_page_data(url):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        movie_list = []
        for item in soup.find_all('div', class_='item'):
            rank = item.find('em').text
            title = item.find('span', class_='title').text
            rating = item.find('span', class_='rating_num').text
            quote = item.find('span', class_='inq')
            quote = quote.text if quote else '无'
            movie = {
                '排名': rank,
                '电影名': title,
                '评分': rating,
                '简介': quote
            }
            movie_list.append(movie)
        return movie_list
    else:
        print(f'请求失败，状态码: {response.status_code}')
        return []

# 豆瓣电影Top250有多页，循环获取所有页数据
all_movies = []
base_url = 'https://movie.douban.com/top250?start={}&filter='
for start in range(0, 250, 25):
    url = base_url.format(start)
    page_data = get_page_data(url)
    all_movies.extend(page_data)

# 将数据输出到JSON文件
with open('static.json', 'w', encoding='utf-8') as f:
    json.dump(all_movies, f, ensure_ascii=False, indent=4)