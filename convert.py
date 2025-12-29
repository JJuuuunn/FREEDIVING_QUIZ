import pandas as pd
import json
import os

# 1. CSV 파일들이 들어있는 폴더 이름
DATA_FOLDER = "csv_data"

# 2. 파일 목록 정의
file_map = {
    "AIDA 1": "AIDA 문제 - AIDA 1.csv",
    "AIDA 2": "AIDA 문제 - AIDA 2.csv",
    "AIDA 3": "AIDA 문제 - AIDA 3.csv",
    "AIDA 4": "AIDA 문제 - AIDA 4.csv"
}

all_data = {}

print(f"📂 '{DATA_FOLDER}' 폴더에서 파일을 읽어옵니다...")

for level, filename in file_map.items():
    # 경로 수정: 폴더명 + 파일명 결합
    file_path = os.path.join(DATA_FOLDER, filename)
    
    if not os.path.exists(file_path):
        print(f"⚠️ 파일 없음: {file_path}")
        continue
        
    try:
        df = pd.read_csv(file_path)
        questions = []
        
        for _, row in df.iterrows():
            # 데이터 정제
            img = row.get('image', '')
            if pd.isna(img): img = ""
            
            q_data = {
                "id": row.get('question_id', ''),
                "q": row.get('question', ''),
                "img": str(img).strip(),
                "options": [
                    str(row.get('option_1', '')),
                    str(row.get('option_2', '')),
                    str(row.get('option_3', '')),
                    str(row.get('option_4', ''))
                ],
                "a": int(row.get('answer', 1)),
                "expl": str(row.get('explanation', '')),
                "topic": str(row.get('topic', ''))
            }
            questions.append(q_data)
        
        all_data[level] = questions
        print(f"✅ {level}: {len(questions)}문제 변환 성공")
        
    except Exception as e:
        print(f"❌ {filename} 읽기 실패: {e}")

# 3. JSON 파일 저장 (프로젝트 루트 폴더에 저장됨)
output_file = "quiz_data.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(all_data, f, ensure_ascii=False, indent=2)

print(f"\n🎉 변환 완료! '{output_file}' 파일이 생성되었습니다.")