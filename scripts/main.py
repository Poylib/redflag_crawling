from crawl_data import fetch_table_data
from insert_data import insert_race_data

if __name__ == "__main__":
    url = 'https://www.formula1.com/en/results/2024/drivers'  # 실제 URL로 변경
    table_data = fetch_table_data(url)
    if table_data:
        insert_race_data(table_data)
    else:
        print("No data to insert.")