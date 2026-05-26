import os
import requests
from datetime import datetime, timedelta

# 1. 날짜 계산 (어제 날짜 기준 데일리 박스오피스 가져오기)
yesterday = datetime.now() - timedelta(days=1)
target_dt = yesterday.strftime("%Y%m%d")  # YYYYMMDD 형식
display_date = yesterday.strftime("%Y년 %m월 %d일")

# 요일 계산 (한국어)
weekday_list = ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일']
weekday_str = weekday_list[yesterday.weekday()]

# 2. 영진위 API 호출
api_key = os.environ.get("KOBIS_API_KEY")
url = f"http://kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json?key={api_key}&targetDt={target_dt}"

try:
    response = requests.get(url).json()
    boxoffice_list = response['boxOfficeResult']['dailyBoxOfficeList']
    
    # 3. 마크다운 텍스트 생성
    md_content = f"### 📅 데일리 박스오피스 ({display_date} {weekday_str})\n\n"
    md_content += "| 순위 | 영화명 (개봉일) | 당일 관객수 | 누적 관객수 |\n"
    md_content += "| :---: | :--- | :---: | :---: |\n"
    
    for item in boxoffice_list:
        rank = item['rank']
        movie_nm = item['movieNm']
        open_dt = item['openDt']
        audi_cnt = int(item['audiCnt'])
        audi_acc = int(item['audiAcc'])
        
        # 숫자에 콤마(,) 넣기
        md_content += f"| **{rank}위** | {movie_nm} ({open_dt}) | {audi_cnt:,}명 | {audi_acc:,}명 |\n"
        
    # 4. 파일로 저장
    filename = f"{yesterday.strftime('%Y-%m-%d')}-boxoffice.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"성공적으로 {filename} 파일을 생성했습니다.")

except Exception as e:
    print(f"에러 발생: {e}")
