# -*- coding: utf-8 -*-

"""
판례 청크(JSONL) -> 임베딩 -> FAISS(IndexFlatIP) 저장
- 입력: JSONL (각 행 예시)
  {
    "사건번호": "84누135",
    "사건명": "부당노동행위구제재심판정취소",
    "선고일자": "19841226",
    "법원명": "대법원",
    "판결유형": "판결",
    "chunk_index": 0,
    "chunk_total": 2,
    "chunk_id": "84누135-001",
    "전문": "......"
  }
- 출력:
  out_dir/faiss.index
  out_dir/meta.jsonl        (입력 row 그대로 복사; 재현/추적용)
  out_dir/index_meta.json   (인덱스 메타 정보)

사용 예:
python rag/cases/src/tools/build_faiss_cases_from_jsonl.py \
  --chunks /path/to/chunks.jsonl \
  --out_dir /path/to/index_cases \
  --model BAAI/bge-m3 --device mps --batch 32
"""

# ===== macOS(Apple Silicon) 안전가드: 세그폴트/과도한 스레드 방지 =====
import os as _os
_os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
_os.environ.setdefault("OMP_NUM_THREADS", "1")
_os.environ.setdefault("PYTORCH_ENABLE_MPS_FALLBACK", "1")
# ===============================================================

import json
import argparse
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
    메타를 앞쪽에 요약 헤더로 구성 + 전문 본문 뒤에 배치
    → 검색 품질 개선 (코사인/IP 매칭)
    """
    case_no = row.get("사건번호") or ""
    case_nm = row.get("사건명") or ""
    date    = row.get("선고일자") or ""
    court   = row.get("법원명") or ""
    kind    = row.get("판결유형") or ""
    section = f"chunk {row.get('chunk_index',0)+1}/{row.get('chunk_total',1)}"
    head = " ".join([x for x in [f"[{kind}]", court, date, case_no, case_nm, section] if x])
    body = row.get("전문","") or ""
    return f"{head} | {body}"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--chunks", required=True, help="판례 청크 JSONL 경로")
    ap.add_argument("--out_dir", required=True, help="결과 저장 폴더")
    ap.add_argument("--model", default="BAAI/bge-m3")
    ap.add_argument("--device", choices=["cpu","mps","cuda"], default="cpu")
    ap.add_argument("--batch", type=int, default=32)
    args = ap.parse_args()

    chunks_path = Path(args.chunks)
    out_dir = Path(args.out_dir); out_dir.mkdir(parents=True, exist_ok=True)

    # 1) 로드
    rows = list(read_jsonl(chunks_path))
    if not rows:
        raise RuntimeError(f"empty input: {chunks_path}")

    texts = [make_embed_text(r) for r in rows]

    # 2) 임베딩 (정규화 → IP 인덱스와 코사인 동일)
    print(f"[info] rows={len(rows)} | model={args.model} | device={args.device} | batch={args.batch}")
    model = SentenceTransformer(args.model, device=args.device)
    try:
        model.max_seq_length = 512
    except Exception:
        pass

    embs = model.encode(
        texts,
        convert_to_numpy=True,
        normalize_embeddings=True,
        batch_size=args.batch,
        show_progress_bar=True
    ).astype(np.float32)

    # 3) 인덱스 빌드 & 저장
    index = faiss.IndexFlatIP(embs.shape[1])
    index.add(embs)
    faiss.write_index(index, str(out_dir / "faiss.index"))

    # 4) 매핑 파일(meta.jsonl): 입력을 그대로 복사(재현/추적용)
    (out_dir / "meta.jsonl").write_text(
        "\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n",
        encoding="utf-8"
    )

    # 5) 인덱스 메타 정보
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