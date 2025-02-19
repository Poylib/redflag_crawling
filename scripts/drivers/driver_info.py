import requests
from bs4 import BeautifulSoup

def crawl_driver_info(driver_name):
    # URL 생성
    base_url = "https://www.formula1.com/en/drivers/"
    url = f"{base_url}{driver_name}"

    # 웹 페이지 요청
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve data for {driver_name}")
        return None

    # BeautifulSoup을 사용하여 HTML 파싱
    soup = BeautifulSoup(response.content, 'html.parser')

    # <dl> 태그 찾기
    dl_tag = soup.find('dl')
    if not dl_tag:
        print(f"No <dl> tag found for {driver_name}")
        return None

    # <dt>와 <dd> 쌍을 딕셔너리로 변환
    driver_info = {}
    for dt, dd in zip(dl_tag.find_all('dt'), dl_tag.find_all('dd')):
        key = dt.get_text(strip=True)
        value = dd.get_text(strip=True)
        driver_info[key] = value

    return driver_info

# 예시 사용
driver_name = "alexander-albon"
info = crawl_driver_info(driver_name)
if info:
    for key, value in info.items():
        print(f"{key}: {value}")
