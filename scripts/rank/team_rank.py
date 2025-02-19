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

def crawl_teams_rank(year):
    # URL 생성
    url = f"https://www.formula1.com/en/results/{year}/team"

    # 웹 페이지 요청
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve data for year {year}")
        return None

    # BeautifulSoup을 사용하여 HTML 파싱
    soup = BeautifulSoup(response.content, 'html.parser')

    # <table> 태그에서 <tbody> 내용 크롤링
    tbody = soup.find('table').find('tbody')
    teams_data = []
    for row in tbody.find_all('tr'):
        cols = row.find_all('td')
        team_name = cols[1].get_text(strip=True)

        # Supabase에서 team_id 가져오기
        response = supabase.table("teams").select("id").eq("name", team_name).execute()
        team_id = response.data[0]['id'] if response.data else None

        team_info = {
            'position': cols[0].get_text(strip=True),
            'team_id': team_id,
            'year': year,
            'points': cols[2].get_text(strip=True)
        }
        teams_data.append(team_info)

    return teams_data

def insert_teams_rank(year):
    teams_data = crawl_teams_rank(year)
    if teams_data:
        for team in teams_data:
            response = supabase.table("team_rankings").upsert(team, on_conflict=['team_id']).execute()
            if response.data:
                print("Data inserted or updated successfully:", team.get("team"))
            elif response.error:
                print("Failed to insert or update data:", team.get("team"), response.error.message)

# 연도 설정
year = 2024
insert_teams_rank(year)