# tools/build_faiss_civil.py
# -*- coding: utf-8 -*-

# ===== macOS(Apple Silicon) 안전가드: 세그폴트 방지 =====
import os as _os
_os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")   # Rust tokenizer 멀티스레딩 off
_os.environ.setdefault("OMP_NUM_THREADS", "1")              # OpenMP thread 억제
_os.environ.setdefault("PYTORCH_ENABLE_MPS_FALLBACK", "1")  # MPS 문제 시 CPU 폴백
# ======================================================

import json, argparse
from pathlib import Path
import numpy as np
import torch
from sentence_transformers import SentenceTransformer

def read_meta(meta_path: Path):
    rows=[]
    with open(meta_path, "r", encoding="utf-8") as f:
        for line in f:
            s=line.strip()
            if s: rows.append(json.loads(s))
    return rows

def make_embed_text(r: dict) -> str:
    # 검색 품질 향상: 조문/항 힌트 + 제목 + 경로 + 본문 결합
    head=[]
    if r.get("article_no"): head.append(f"제{r['article_no']}조")
    if r.get("title"):      head.append(r["title"])
    if r.get("path"):       head.append(r["path"])
    body = r.get("text","") or ""
    return " | ".join([*head, body])

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--meta",     required=True, help=".../rag/civil/data/civil_meta.jsonl")
    ap.add_argument("--out_dir",  required=True, help=".../index_mac/civil (또는 저장할 폴더)")
    ap.add_argument("--model",    default="BAAI/bge-m3")
    ap.add_argument("--device",   choices=["cpu","mps"], default="cpu",
                    help="M4에선 cpu 권장. mps는 드물게 충돌 가능")
    ap.add_argument("--batch_size", type=int, default=32)
    args = ap.parse_args()

    out_dir = Path(args.out_dir); out_dir.mkdir(parents=True, exist_ok=True)
    meta_path = Path(args.meta)
    if not meta_path.exists():
        raise FileNotFoundError(f"meta not found: {meta_path}")

    rows  = read_meta(meta_path)
    texts = [ make_embed_text(r) for r in rows ]

    print(f"[info] rows={len(rows)} | model={args.model} | device={args.device} | batch={args.batch_size}")

    # ---- 임베딩 (CPU 기본; MPS는 옵션) ----
    torch.set_num_threads(1)  # 추가 안전장치
    model = SentenceTransformer(args.model, device=args.device)
    try:
        model.max_seq_length = 512
    except Exception:
        pass

    embs = model.encode(
        texts,
        convert_to_numpy=True,
        normalize_embeddings=True,   # cosine ↔ IP 매칭
        batch_size=args.batch_size,
        show_progress_bar=True
    ).astype(np.float32)

    # ---- FAISS 인덱스 (지연 임포트로 초기 충돌 회피) ----
    import faiss
    index = faiss.IndexFlatIP(embs.shape[1])  # 정규화 임베딩엔 IP가 적합
    index.add(embs)

    faiss.write_index(index, str(out_dir / "faiss.index"))

    # 메타 파일도 인덱스 폴더에 복사
    meta_text = meta_path.read_text(encoding="utf-8")
    (out_dir / "meta.jsonl").write_text(meta_text, encoding="utf-8")

    print(f"[done] saved → {out_dir/'faiss.index'} | dims={embs.shape[1]} | ntotal={index.ntotal}")

if __name__ == "__main__":
    main()