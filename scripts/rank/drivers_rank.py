import requests
from bs4 import BeautifulSoup
from supabase import create_client, Client
from dotenv import load_dotenv
import os

# .env 파일에서 환경 변수 로드
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Supabase 클라이언트 생성
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def crawl_drivers_rank(year):
    # URL 생성
    url = f"https://www.formula1.com/en/results/{year}/drivers"

    # 웹 페이지 요청
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve data for year {year}")
        return None

    # BeautifulSoup을 사용하여 HTML 파싱
    soup = BeautifulSoup(response.content, 'html.parser')

    # <table> 태그에서 <tbody> 내용 크롤링
    tbody = soup.find('table').find('tbody')
    drivers_data = []
    for row in tbody.find_all('tr'):
        cols = row.find_all('td')
        driver = '-'.join([span.get_text(strip=True).lower() for span in cols[1].find_all('span')[:2]])

        # driver_id 가져오기
        driver_id_response = supabase.table("drivers").select("id").eq("name", driver).execute()
        driver_id = driver_id_response.data[0]['id'] if driver_id_response.data else None

        # driver_id가 None이 아닐 경우에만 drivers_data에 추가
        if driver_id is not None:
            driver_info = {

                'position': cols[0].get_text(strip=True),
                'points': cols[4].get_text(strip=True),
                'driver_id': driver_id,  # driver_id 추가
                'year':year
            }
            drivers_data.append(driver_info)

    return drivers_data

def insert_drivers_rank(year):
    drivers_data = crawl_drivers_rank(year)
    if drivers_data:
        for driver in drivers_data:
            response = supabase.table("driver_rankings").upsert(driver, on_conflict=['driver_id']).execute()
            if response.data:
                print("Data inserted or updated successfully:", driver.get("driver"))
            elif response.error:
                print("Failed to insert or update data:", driver.get("driver"), response.error.message)
            else:
                # APIError 발생 시 오류 메시지 출력
                print("APIError occurred:", response.error)

if __name__ == "__main__":
    # 연도 설정
    year = 2024
    # 드라이버 순위 크롤링 및 데이터베이스에 삽입
    insert_drivers_rank(year)
