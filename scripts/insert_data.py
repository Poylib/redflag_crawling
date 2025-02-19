import os
from supabase import create_client, Client
from dotenv import load_dotenv

# .env 파일에서 환경 변수 로드
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Supabase 클라이언트 생성
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def insert_race_data(data):
    for row in data:
        # 데이터베이스에 삽입할 데이터 구조
        race_data = {
            'position': row[0],
            'name': row[1],
            'nationality': row[2],
            'team': row[3],
            'points': row[4]
        }

        # Supabase에 데이터 삽입 또는 업데이트
        response = supabase.table("drivers").upsert(race_data, on_conflict=['name']).execute()

        # 응답 처리
        if response.data:
            print("Data inserted or updated successfully:", race_data)
        elif response.error:
            print("Failed to insert or update data:", response.error.message)
