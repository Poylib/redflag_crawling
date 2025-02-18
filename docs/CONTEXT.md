# F1 정보 크롤링 프로그램

이 프로젝트는 F1 모바일 앱에 필요한 정보를 크롤링하고, Supabase에 저장을 목표로 합니다.

## 주요 기능

### 데이터 크롤링

- **레이스 정보 수집**: 다음 레이스의 이름, 서킷 정보, 날짜 및 시간을 포함한 정보를 수집합니다.
- **트랙 특성 수집**: 트랙 길이, 코너 수, DRS 존, 최고 속도, 랩 기록 등의 정보를 수집합니다.
- **일정 및 순위 정보 수집**: 레이스 캘린더와 드라이버 및 컨스트럭터 챔피언십 순위를 수집합니다.

### 데이터베이스 관리

- **Supabase 연동**: 수집된 데이터를 Supabase에 저장하고 관리합니다.
- **데이터 업데이트**: 정기적으로 데이터를 업데이트하여 최신 정보를 유지합니다.

## 프로젝트 목표

- F1 모바일 앱에 필요한 모든 정보를 자동으로 수집하고 관리할 수 있는 시스템을 구축합니다.

## 기술 스택

- **크롤링**: Python을 사용하여 데이터를 수집합니다.
- **자동화 및 스케줄링**: AWS Lambda와 AWS CloudWatch를 사용하여 일정 간격으로 크롤링 작업을 자동으로 실행합니다.
- **데이터베이스**: Supabase를 사용하여 데이터를 저장하고 관리합니다.
- **배포 및 호스팅**: AWS를 사용하여 서버리스 환경에서 애플리케이션을 배포합니다.
- use pip3 install requests
- use python3

## 데이터베이스 스키마

- **Races Table**: 레이스의 기본 정보를 저장합니다.

  - `id`: 고유 식별자
  - `name`: 레이스 이름
  - `circuit`: 서킷 이름
  - `date`: 레이스 날짜
  - `time`: 레이스 시간
  - `status`: 레이스 상태 (예: 완료, 예정)

- **Track Characteristics Table**: 트랙의 특성을 저장합니다.

  - `id`: 고유 식별자
  - `race_id`: 레이스 ID (Races Table 참조)
  - `track_length`: 트랙 길이
  - `number_of_corners`: 코너 수
  - `drs_zones`: DRS 존 수
  - `top_speed`: 최고 속도
  - `lap_record`: 랩 기록

- **Drivers Table**: 드라이버의 정보를 저장합니다.

  - `id`: 고유 식별자
  - `name`: 드라이버 이름
  - `nationality`: 소속 국가
  - `team`: 소속 팀
  - `points`: 포인트

- **Constructors Table**: 컨스트럭터의 정보를 저장합니다.

  - `id`: 고유 식별자
  - `name`: 컨스트럭터 이름
  - `points`: 포인트

- **Race Results Table**: 각 레이스의 결과를 저장합니다.
  - `id`: 고유 식별자
  - `race_id`: 레이스 ID (Races Table 참조)
  - `driver_id`: 드라이버 ID (Drivers Table 참조)
  - `position`: 순위
