# -*- coding: utf-8 -*-
"""
판례 청크(chunks.jsonl) -> 임베딩 -> FAISS(IndexFlatIP) 저장
- 입력: chunks.jsonl (각 행: {"text", "meta", "weight?", "chunk_id?"})
- 출력: faiss.index, meta.jsonl(매핑), index_meta.json
사용 예:
python rag/cases/src/tools/build_faiss_cases.py \
  --chunks rag/cases/data/chunks.jsonl \
  --out_dir rag/cases/data/index_cases \
  --model BAAI/bge-m3 --device cuda
"""
import json, argparse
from pathlib import Path
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

def read_jsonl(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            s = line.strip()
            if s:
                yield json.loads(s)

def make_embed_text(row: dict) -> str:
    """
    검색 품질을 위해 메타를 앞쪽에 요약 키로 붙이고, 본문 청크를 뒤에 둔다.
    """
    meta = row.get("meta", {}) or {}
    section = meta.get("section") or ""
    case_no = meta.get("사건번호") or ""
    case_nm = meta.get("사건명") or ""
    kind    = meta.get("사건종류명") or ""
    court   = meta.get("법원명") or ""
    date    = meta.get("선고일자") or ""
    head = " ".join([x for x in [f"[{kind}]", court, date, case_no, case_nm, section] if x])
    body = row.get("text","") or ""
    return f"{head} | {body}"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--chunks", required=True,
                    help="/Users/jaewoo000/Desktop/Law_AI/rag/cases/src/chunks.jsonl")
    ap.add_argument("--out_dir", required=True,
                    help="/Users/jaewoo000/Desktop/Law_AI/index_mac/cases")
    ap.add_argument("--model", default="BAAI/bge-m3")
    ap.add_argument("--device", default="cuda")
    ap.add_argument("--batch", type=int, default=16)
    args = ap.parse_args()

    chunks_path = Path(args.chunks)
    out_dir = Path(args.out_dir); out_dir.mkdir(parents=True, exist_ok=True)

    # 1) 로드
    rows = list(read_jsonl(chunks_path))
    if not rows:
        raise RuntimeError(f"empty input: {chunks_path}")

    texts = [make_embed_text(r) for r in rows]

    print(f"[info] rows={len(rows)} | model={args.model} | device={args.device}")
    model = SentenceTransformer(args.model, device=args.device)

    # 2) 임베딩 (코사인용 정규화=True) → IP 인덱스
    embs = model.encode(
        texts,
        convert_to_numpy=True,
        normalize_embeddings=True,   # cosine
        batch_size=args.batch,
        show_progress_bar=True
    ).astype(np.float32)

    # 3) 인덱스 빌드 & 저장
    index = faiss.IndexFlatIP(embs.shape[1])
    index.add(embs)
    faiss.write_index(index, str(out_dir / "faiss.index"))

    # 4) 매핑 파일(meta.jsonl) 저장: 입력을 그대로 복사(재현/추적용)
    (out_dir / "meta.jsonl").write_text(
        "\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n",
        encoding="utf-8"
    )

    # 5) 메타 정보
    (out_dir / "index_meta.json").write_text(
        json.dumps({
            "model": args.model,
            "device": args.device,
            "dim": int(embs.shape[1]),
            "size": int(index.ntotal),
            "normalize": True,
            "source": str(chunks_path.resolve())
        }, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print(f"[done] index  → {out_dir/'faiss.index'}")
    print(f"[done] meta   → {out_dir/'meta.jsonl'}")
    print(f"[done] detail → {out_dir/'index_meta.json'}")

if __name__ == "__main__":
    main()