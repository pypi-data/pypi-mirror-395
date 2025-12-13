import logging
import os
import sqlite3

from sayou.connector.pipeline import ConnectorPipeline

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")


# --- Helper: 더미 DB 생성 ---
def create_dummy_db(path="examples/user_demo.db"):
    if os.path.exists(path):
        os.remove(path)
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    cur.execute("CREATE TABLE users (id INTEGER, name TEXT, role TEXT)")
    # 25개 데이터 생성 (배치 테스트용)
    for i in range(25):
        role = "admin" if i % 5 == 0 else "user"
        cur.execute("INSERT INTO users VALUES (?, ?, ?)", (i, f"User_{i}", role))
    conn.commit()
    conn.close()
    return path


# --- Helper: 더미 파일 생성 ---
def create_dummy_files(root="test_docs"):
    if not os.path.exists(root):
        os.makedirs(root)
    with open(f"{root}/report_q1.txt", "w", encoding="utf-8") as f:
        f.write("2024 Q1 Financial Report...")
    with open(f"{root}/report_q2.txt", "w", encoding="utf-8") as f:
        f.write("2024 Q2 Financial Report...")
    return root


def run_demo():
    print(">>> Initializing Sayou Connector Brain...")
    pipeline = ConnectorPipeline()
    pipeline.initialize()

    # ---------------------------------------------------------
    # Scenario 1: Local File Scan
    # ---------------------------------------------------------
    print("\n=== [1] Local File Scan Demo ===")
    file_root = create_dummy_files()

    # strategy="file" 사용
    packets = pipeline.run(
        source=file_root, strategy="file", extensions=[".txt"], recursive=True
    )

    for i, packet in enumerate(packets):
        # SayouPacket 구조 활용
        if packet.success:
            # FileFetcher는 bytes를 반환하므로 decoding 필요
            content = packet.data.decode("utf-8")
            print(f"[{i}] File: {packet.task.meta['filename']}")
            print(f"    Content: {content[:20]}...")
        else:
            print(f"[{i}] Error: {packet.error}")

    # ---------------------------------------------------------
    # Scenario 2: SQLite DB Fetching (Pagination)
    # ---------------------------------------------------------
    print("\n=== [2] SQLite DB Demo ===")
    db_path = create_dummy_db()

    # strategy="sqlite" 사용
    # 배치 사이즈 10 -> 총 25개이므로 3번(10, 10, 5) Fetch 발생 예상
    db_packets = pipeline.run(
        source=db_path, strategy="sqlite", query="SELECT * FROM users", batch_size=10
    )

    for i, packet in enumerate(db_packets):
        if packet.success:
            rows = packet.data  # List[Dict]
            offset = packet.task.meta.get("offset")
            print(f"Batch {i+1} (Offset {offset}): Fetched {len(rows)} rows.")
            if rows:
                print(f"    Sample: {rows[0]}")
        else:
            print(f"Batch {i+1} Failed: {packet.error}")

    # ---------------------------------------------------------
    # Scenario 3: Web Crawling (Real World)
    # ---------------------------------------------------------
    print("\n=== [3] Web Crawling Demo ===")

    target_url = "https://news.daum.net/tech"
    # 예시: 다음 뉴스 패턴
    link_pattern = r"https://v\.daum\.net/v/\d+"

    try:
        web_packets = pipeline.run(
            source=target_url,
            strategy="requests",
            link_pattern=link_pattern,
            selectors={
                "title": ".head_view",
                "content": ".article_view",
            },  # 실제 선택자는 다를 수 있음
            max_depth=1,  # 1단계만 (메인 -> 기사)
        )

        count = 0
        for packet in web_packets:
            if not packet.success:
                continue

            data = packet.data  # Dict
            # 메타데이터 제외하고 본문 내용만 확인
            display_data = {
                k: v[:30] + "..." for k, v in data.items() if not k.startswith("__")
            }

            # 제목이 잡힌 경우만 출력 (메인 페이지 등은 선택자 매칭 안될 수 있음)
            if display_data.get("title"):
                print(f"[{count}] URL: {packet.task.uri}")
                print(f"    Data: {display_data}")
                count += 1
                if count >= 3:
                    print("    ... (Stopping demo after 3 articles)")
                    break

    except Exception as e:
        print(f"Skipping Web Demo: {e}")

    # Cleanup
    if os.path.exists("test_users.db"):
        os.remove("test_users.db")
    import shutil

    if os.path.exists("test_docs"):
        shutil.rmtree("test_docs")


if __name__ == "__main__":
    run_demo()
