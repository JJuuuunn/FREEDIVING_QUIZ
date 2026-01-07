import pandas as pd
import json
import os

# 1. CSV 파일들이 들어있는 폴더 이름
DATA_FOLDER = "csv_data"

all_data = {}

print(f"📂 '{DATA_FOLDER}' 폴더에서 파일을 동적으로 읽어옵니다...")

# 줄바꿈 문자 변환 헬퍼 함수
def clean_text(text):
    if pd.isna(text):
        return ""
    # 텍스트 내의 '\\n' (글자)을 '\n' (실제 줄바꿈)으로 변환
    return str(text).replace('\\n', '\n').strip()

# 데이터 폴더가 없으면 생성
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

# 2. csv_data 폴더 내의 모든 .csv 파일 목록을 가져옴
try:
    # Get all files and sort them alphabetically
    csv_files = sorted([f for f in os.listdir(DATA_FOLDER) if f.lower().endswith('.csv')])
except FileNotFoundError:
    print(f"🚨 '{DATA_FOLDER}' 폴더를 찾을 수 없습니다. 폴더를 생성하고 CSV 파일을 넣어주세요.")
    csv_files = []

if not csv_files:
    print("⚠️ 처리할 CSV 파일이 없습니다.")
else:
    for filename in csv_files:
        # 파일명에서 레벨 이름 추출 (예: "AIDA 문제 - AIDA 1.csv" -> "AIDA 1")
        level_name = filename.replace('.csv', '').replace('AIDA 문제 - ', '').strip()
        
        file_path = os.path.join(DATA_FOLDER, filename)
        
        try:
            # engine='python'과 on_bad_lines='skip' 사용
            df = pd.read_csv(file_path, engine='python', on_bad_lines='skip')
            
            questions = []
            
            for _, row in df.iterrows():
                # 1. 행 데이터를 딕셔너리로 변환
                row_dict = row.to_dict()
                
                # 2. 필수 컬럼들을 '꺼내서(pop)' 변수에 저장 및 줄바꿈 처리
                q_id = row_dict.pop('question_id', '')
                q_text = clean_text(row_dict.pop('question', '')) # 수정됨
                
                img_val = row_dict.pop('image', '')
                img = "" if pd.isna(img_val) else str(img_val).strip()
                
                # 보기들도 줄바꿈 처리 적용
                opt1 = clean_text(row_dict.pop('option_1', ''))
                opt2 = clean_text(row_dict.pop('option_2', ''))
                opt3 = clean_text(row_dict.pop('option_3', ''))
                opt4 = clean_text(row_dict.pop('option_4', ''))
                
                ans = row_dict.pop('answer', 1)
                expl = clean_text(row_dict.pop('explanation', '')) # 수정됨
                topic = clean_text(row_dict.pop('topic', ''))      # 수정됨

                # 3. 필수 데이터로 기본 구조 생성
                q_data = {
                    "id": str(q_id),
                    "q": q_text,
                    "img": img,
                    "options": [
                        opt1, opt2, opt3, opt4
                    ],
                    "a": int(ans) if pd.notna(ans) else 1,
                    "expl": expl,
                    "topic": topic
                }
                
                # 4. 남은 컬럼들 자동 추가 (여기에도 줄바꿈 처리 적용)
                for key, val in row_dict.items():
                    q_data[key] = clean_text(val)

                questions.append(q_data)
            
            all_data[level_name] = questions
            print(f"✅ {level_name}: {len(questions)}문제 변환 성공")
            
        except Exception as e:
            print(f"❌ {filename} 읽기 실패: {e}")

# 3. JSON 파일 저장
output_file = "quiz_data.json"
with open(output_file, "w", encoding="utf-8") as f:
    # ensure_ascii=False: 한글 깨짐 방지
    # indent=2: 들여쓰기해서 보기 좋게 저장
    json.dump(all_data, f, ensure_ascii=False, indent=2)

print(f"\n🎉 변환 완료! '{output_file}' 파일이 생성되었습니다.")