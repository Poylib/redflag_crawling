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

def crawl_team_info(team_name):
    # URL 생성
    base_url = "https://www.formula1.com/en/teams/"
    url = f"{base_url}{team_name}"

    # 웹 페이지 요청
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve data for {team_name}")
        return None

    # BeautifulSoup을 사용하여 HTML 파싱
    soup = BeautifulSoup(response.content, 'html.parser')

    # <dl> 태그 찾기
    dl_tag = soup.find('dl')
    if not dl_tag:
        print(f"No <dl> tag found for {team_name}")
        return None

    # <dt>와 <dd> 쌍을 딕셔너리로 변환
    team_info = {}
    for dt, dd in zip(dl_tag.find_all('dt'), dl_tag.find_all('dd')):
        key = dt.get_text(strip=True)
        value = dd.get_text(strip=True)
        team_info[key] = value

    return team_info

def insert_team_info(team_info):
    print(team_info)
    # 팀 정보 삽입할 데이터 구조
    team_data = {
        'full_team_name': team_info.get("Full Team Name"),
        'base': team_info.get("Base"),
        'team_chief': team_info.get("Team Chief"),
        'technical_chief': team_info.get("Technical Chief"),
        'chassis': team_info.get("Chassis"),
        'power_unit': team_info.get("Power Unit"),
        'first_team_entry': team_info.get("First Team Entry"),
        'world_championships': team_info.get("World Championships"),
        'highest_race_finish': team_info.get("Highest Race Finish"),
        'pole_positions': team_info.get("Pole Positions"),
        'fastest_laps': team_info.get("Fastest Laps")
    }


    # Supabase에 데이터 삽입 또는 업데이트
    response = supabase.table("teams").upsert(team_data, on_conflict=['full_team_name']).execute()

    # 응답 처리
    if response.data:
        print("Data inserted or updated successfully:", team_data.get("full_team_name"))
    elif response.error:
        print("Failed to insert or update data:", team_data.get("full_team_name"), response.error.message)

# 팀 정보를 크롤링할 팀 이름
team_name = ["alpine","alphatauri","ferrari","aston-martin","mclaren","mercedes","red-bull-racing","williams","haas","kick-sauber","racing-bulls"]
for name in team_name:
    info = crawl_team_info(name)
    if info:
        insert_team_info(info)
