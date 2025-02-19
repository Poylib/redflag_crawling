import requests
from bs4 import BeautifulSoup
import os
from supabase import create_client, Client
from dotenv import load_dotenv

# .env 파일에서 환경 변수 로드
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Supabase 클라이언트 생성
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

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

def insert_driver_info(driver_info,name):
    print(driver_info)
    # 드라이버 정보 삽입할 데이터 구조
    driver_data = {
        'name': name,
        'country': driver_info.get("Country"),
        'podiums': driver_info.get("Podiums"),
        'points': driver_info.get("Points"),
        'grands_prix_entered': driver_info.get("Grands Prix entered"),
        'world_championships': driver_info.get("World Championships"),
        'highest_race_finish': driver_info.get("Highest race finish"),
        'highest_grid_position': driver_info.get("Highest grid position"),
        'date_of_birth': driver_info.get("Date of birth"),
        'place_of_birth': driver_info.get("Place of birth")
    }

    # Supabase에 데이터 삽입 또는 업데이트
    response = supabase.table("drivers").upsert(driver_data, on_conflict=['name']).execute()

    # 응답 처리
    if response.data:
        print("Data inserted or updated successfully:", driver_data.get("name"))
    elif response.error:
        print("Failed to insert or update data:",driver_data.get("name"), response.error.message)

driver_name = [ "alexander-albon", "charles-leclerc", "carlos-sainz", "daniel-ricciardo", "esteban-ocon", "fernando-alonso", "george-russell", "lando-norris", "max-verstappen", "nico-hulkenberg", "kimi-antonelli", "pierre-gasly", "sebastian-vettel", "valtteri-bottas", "yuki-tsunoda","liam-lawson","gabriel-bortoleto","nico-hulkenberg","oliver-bearman","isack-hadjar","jack-doohan","lance-stroll","lewis-hamilton","oscar-piastri"]
for name in driver_name:
    info = crawl_driver_info(name)
    if info:
        insert_driver_info(info,name)
