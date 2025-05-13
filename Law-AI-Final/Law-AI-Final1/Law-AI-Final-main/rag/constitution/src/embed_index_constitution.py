# rag/embed_index_constitution.py
# -*- coding: utf-8 -*-

# ==== macOS (Apple Silicon) 안전 가드: 세그폴트 방지 ====
import os as _os
_os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")  # Rust tokenizer 멀티스레딩 off
_os.environ.setdefault("OMP_NUM_THREADS", "1")             # OpenMP 스레드 억제
_os.environ.setdefault("PYTORCH_ENABLE_MPS_FALLBACK", "1") # MPS 이슈시 CPU로 폴백

import json, argparse
from pathlib import Path
import numpy as np
import torch

from sentence_transformers import SentenceTransformer

# === 경로 기본값 (요청하신 구조) ===
ROOT = Path(__file__).resolve().parents[1]            # .../rag/constitution/
DEFAULT_INPUT  = ROOT / "data" / "constitution_chunks.jsonl"
DEFAULT_OUTDIR = ROOT / "index_mac" / "constitution"


def load_jsonl(p: Path):
    rows = []
    with open(p, "r", encoding="utf-8") as f:
        for line in f:
            s = line.strip()
            if s:
                rows.append(json.loads(s))
    return rows


def make_embed_text(r: dict) -> str:
    head = []
    art = r.get("article_no")
    if art:
        head.append(f"제{art}조")
    unit = r.get("unit")
    rid  = r.get("id", "")
    if unit in {"항", "호", "목"} and "::" in rid:
        # ①, ② 또는 '1','2' 등 세부 번호
        head.append(rid.split("::", 1)[1])
    head.append(r.get("text", "") or "")
    return " ".join([h for h in head if h])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input",   default=str(DEFAULT_INPUT))
    ap.add_argument("--model",   default="BAAI/bge-m3")
    ap.add_argument("--outdir",  default=str(DEFAULT_OUTDIR))
    ap.add_argument("--batch_size", type=int, default=32)      # 보수적 배치
    ap.add_argument("--device",  choices=["cpu", "mps"], default="cpu",
                    help="M4에서도 안정성 위해 기본은 cpu 권장 (mps는 드물게 충돌)")

    args = ap.parse_args()

    input_path = Path(args.input)
    outdir     = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    # 1) 데이터 로드
    rows  = load_jsonl(input_path)
    texts = [make_embed_text(r) for r in rows]

    # 2) 임베딩 (CPU 기본; MPS는 옵션)
    device = args.device
    torch.set_num_threads(1)  # 추가 안전장치
    model = SentenceTransformer(args.model, device=device)
    try:
        # 너무 긴 문장은 자르기 (안정성+일관성)
        model.max_seq_length = 512
    except Exception:
        pass

    vecs = model.encode(
        texts,
        batch_size=args.batch_size,
        convert_to_numpy=True,
        normalize_embeddings=True,  # cosine → inner product 대응
        show_progress_bar=True
    ).astype(np.float32)

    # 3) FAISS 인덱스 작성 (지연 임포트로 초기 충돌 회피)
    import faiss
    dim   = int(vecs.shape[1])
    index = faiss.IndexFlatIP(dim)   # 정규화 임베딩이면 IP가 적합
    index.add(vecs)

    # 4) 점검/저장
    print(f"[FAISS] added vectors: {index.ntotal} / expected: {len(rows)}")
    faiss.write_index(index, str(outdir / "faiss.index"))

    with open(outdir / "meta.jsonl", "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    print(f"✅ index saved to {outdir} | size={index.ntotal} | meta={len(rows)}")


if __name__ == "__main__":
    main()