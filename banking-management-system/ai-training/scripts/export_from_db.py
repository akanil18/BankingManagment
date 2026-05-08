"""
Export training data from PostgreSQL → JSONL files (train + eval split).
Run: python scripts/export_from_db.py
"""
import os
import json
import random
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv("DATABASE_URL")
TRAIN_SPLIT = float(os.getenv("TRAIN_SPLIT", 0.9))
RAW_DIR = os.path.join(os.path.dirname(__file__), "../data/raw")
PROCESSED_DIR = os.path.join(os.path.dirname(__file__), "../data/processed")

os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)


def fetch_all():
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute("SELECT instruction, input, output FROM training_data ORDER BY created_at")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [{"instruction": r[0], "input": r[1] or "", "output": r[2]} for r in rows]


def format_prompt(item: dict) -> str:
    if item["input"].strip():
        return (
            f"### Instruction:\n{item['instruction']}\n\n"
            f"### Input:\n{item['input']}\n\n"
            f"### Response:\n{item['output']}"
        )
    return (
        f"### Instruction:\n{item['instruction']}\n\n"
        f"### Response:\n{item['output']}"
    )


def main():
    data = fetch_all()
    print(f"Total records: {len(data)}")

    # save raw
    with open(f"{RAW_DIR}/training_data.jsonl", "w") as f:
        for item in data:
            f.write(json.dumps(item) + "\n")

    # shuffle + split
    random.shuffle(data)
    split = int(len(data) * TRAIN_SPLIT)
    train, eval_ = data[:split], data[split:]

    for name, subset in [("train", train), ("eval", eval_)]:
        path = f"{PROCESSED_DIR}/{name}.jsonl"
        with open(path, "w") as f:
            for item in subset:
                f.write(json.dumps({"text": format_prompt(item)}) + "\n")
        print(f"Saved {len(subset)} records → {path}")


if __name__ == "__main__":
    main()
