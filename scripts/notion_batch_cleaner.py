import os
import re
import shutil
import glob
import argparse

def clean_notion_markdown(content):
    """
    1. 노션 토글(<details><summary>)을 마크다운 헤더(###) 기반으로 평탄화
    2. 과도한 빈 줄 여백 제거
    """
    # 1. Summary 태그를 헤더 3으로 변환
    content = re.sub(r'<summary>(.*?)</summary>', r'### \1', content)
    
    # 2. Details 태그 제거 (단순 줄바꿈으로 변경)
    content = content.replace('<details>', '\n').replace('</details>', '\n')
    
    # 3. 과도하게 연속된 빈 줄을 2줄로 정리
    content = re.sub(r'\n{3,}', '\n\n', content)
    
    return content.strip()

def process_batch(source_dir, staging_dir, trash_dir):
    # 하위 디렉토리를 포함한 모든 md 파일 순회
    md_files = glob.glob(os.path.join(source_dir, '**/*.md'), recursive=True)
    moved_count = 0
    trashed_count = 0
    
    print(f"발견된 마크다운 문서: {len(md_files)}개 -> 검수 및 정제 시작...")
    
    for md_path in md_files:
        with open(md_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 1. 유효성 평가 (가벼운 휴리스틱: 의미 있는 한글/영문 글자 수가 50자 이하인 경우 쓰레기로 간주)
        text_content = re.sub(r'[^A-Za-z0-9가-힣]', '', content)
        if len(text_content) < 50:
            shutil.move(md_path, os.path.join(trash_dir, os.path.basename(md_path)))
            trashed_count += 1
            continue
            
        # 2. 서식 평탄화 (토글 제거 등)
        cleaned_content = clean_notion_markdown(content)
        
        # 3. Frontmatter 에 승인 상태 및 출처 마커 삽입
        final_content = "---\nstatus: ready-for-raw\nsource: notion-batch-export\n---\n\n" + cleaned_content
        
        dest_path = os.path.join(staging_dir, os.path.basename(md_path))
        
        # 동일한 파일명이 있을 경우 덮어쓰기
        with open(dest_path, 'w', encoding='utf-8') as f:
            f.write(final_content)
            
        moved_count += 1

    print("\n✅ 배치 프로세스 완료")
    print(f"👉 합격 후 Staging 보관 완료(ready-for-raw): {moved_count}개")
    print(f"🗑️ 불합격 후 Trash 폐기: {trashed_count}개")
    print("이제 합격한 문서들을 00_Raw 폴더로 이동하여 P-Reinforce 를 트리거할 수 있습니다.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="노션 Export 일괄 마크다운 정제 스크립트")
    parser.add_argument("--source", required=True, help="노션에서 Export한 파일들 압축을 푼 폴더 경로")
    args = parser.parse_args()
    
    # 스크립트 실행 위치(WIKI/scripts/) 기준 상대 경로 계산
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    STAGING_DIR = os.path.join(BASE_DIR, "00_Staging")
    TRASH_DIR = os.path.join(STAGING_DIR, "Trash")
    
    os.makedirs(STAGING_DIR, exist_ok=True)
    os.makedirs(TRASH_DIR, exist_ok=True)
    
    if not os.path.exists(args.source):
        print(f"에러: 지정한 원본 폴더({args.source})를 찾을 수 없습니다.")
        exit(1)
        
    process_batch(args.source, STAGING_DIR, TRASH_DIR)
