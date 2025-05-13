# -*- coding: utf-8 -*-
"""
법령해석례 청크(chunks.jsonl) -> 임베딩 -> FAISS(IndexFlatIP) 저장
- 입력: chunks.jsonl (각 행: {"전문", "회답?", "안건번호", "안건명", "해석기관명", "해석일자", "chunk_index?", "chunk_total?", "chunk_id?" ...})
- 출력: faiss.index, meta.jsonl(원본 매핑), index_meta.json
사용 예:
python rag/opinions/src/tools/build_faiss_opinions.py \
  --chunks rag/opinions/data/chunks.jsonl \
  --out_dir rag/opinions/data/index_opinions \
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

def get(meta: dict, *keys, default=""):
    for k in keys:
        if k in meta and meta[k]:
            return meta[k]
    return default

def make_embed_text(row: dict) -> str:
    """
    검색 품질을 위해 메타/요지를 앞쪽에, 전문 청크를 뒤쪽에 둔다.
    필드명이 없을 수 있으니 안전하게 꺼낸다.
    """
    # 메타
    case_no   = get(row, "안건번호")
    title     = get(row, "안건명")
    agency    = get(row, "해석기관명")
    date      = get(row, "해석일자")
    chunk_idx = row.get("chunk_index")
    chunk_tot = row.get("chunk_total")
    chunk_tag = f"(chunk {chunk_idx+1}/{chunk_tot})" if isinstance(chunk_idx, int) and isinstance(chunk_tot, int) else ""

    # 요지/회답(있으면 강하게 앞에)
    answer = (row.get("회답") or "").strip()
    head_bits = [ "[법령해석]", agency, date, case_no, title, chunk_tag ]
    head = " ".join([x for x in head_bits if x])

    body_main = row.get("전문","") or ""
    body = body_main if not answer else f"[회답요지] {answer}\n{body_main}"

    return f"{head} | {body}"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--chunks", required=True,
                    help="법령해석례 청크 jsonl 경로 (각 행은 dict)")
    ap.add_argument("--out_dir", required=True,
                    help="출력 디렉터리 (faiss.index, meta.jsonl, index_meta.json)")
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

    # 2) 임베딩 (코사인 유사도용 정규화=True) → IP 인덱스
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
            "kind": "legal_opinions",
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