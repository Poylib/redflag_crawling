import requests
from bs4 import BeautifulSoup

def fetch_table_data(url):
    # 웹 페이지 요청
    response = requests.get(url)
    response.raise_for_status()

    # HTML 파싱
    soup = BeautifulSoup(response.text, 'html.parser')

    # 'f1-table' 클래스를 가진 테이블 찾기
    table = soup.find('table', class_='f1-table')

    # 테이블 데이터 추출
    data = []
    if table:
        # 테이블의 tbody에서 모든 행(tr) 찾기
        rows = table.find('tbody').find_all('tr')
        for row in rows:
            # 각 행의 열(td) 데이터 추출
            cols = row.find_all('td')
            cols = [col.text.strip() for col in cols]
            data.append(cols)
    else:
        print("Table with class 'f1-table' not found.")

    return data