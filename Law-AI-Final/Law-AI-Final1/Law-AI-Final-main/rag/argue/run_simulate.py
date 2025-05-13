# rag/argue/run_simulate.py
# -*- coding: utf-8 -*-
import json
import argparse
from pathlib import Path
from rag.argue.simulator import simulate_counter

def run_one(query: str, args):
    return simulate_counter(
        opponent_text=query.strip(),
        index_root=Path(args.index_root),
        embed_model=args.embed_model,
        device=args.device,
        pre_k=args.pre_k,
        final_k=args.final_k,
        llm_path=Path(args.llm),
        max_new_tokens=args.max_new_tokens,
        alpha=args.alpha,
    )

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--index_root", required=True,
                    help="FAISS 인덱스 루트 (예: rag/cases/data/index_cases)")
    ap.add_argument("--embed_model", default="BAAI/bge-m3")
    ap.add_argument("--device", default="cuda")
    ap.add_argument("--llm", default="models/Meta-Llama-3-8B")
    ap.add_argument("--max_new_tokens", type=int, default=400)
    ap.add_argument("--pre_k", type=int, default=60)
    ap.add_argument("--final_k", type=int, default=8)
    ap.add_argument("--alpha", type=float, default=0.75)  # 리랭커 혼합가중치

    # 입력 소스: -q / --query_file / STDIN
    ap.add_argument("-q", "--query", help="단일 질문/주장 텍스트")
    ap.add_argument("--query_file", help="여러 질문이 담긴 txt (줄마다 1개)")
    args = ap.parse_args()

    queries = []
    if args.query:
        queries = [args.query]
    elif args.query_file:
        p = Path(args.query_file)
        queries = [ln.strip() for ln in p.read_text(encoding="utf-8").splitlines() if ln.strip()]
    else:
        import sys
        buf = sys.stdin.read().strip()
        if buf:
            queries = [buf]

    if not queries:
        print("입력이 없습니다. -q 또는 --query_file 또는 STDIN을 사용하세요.")
        return

    outs = []
    for q in queries:
        res = run_one(q, args)
        outs.append({"query": q, "result": res})

    print(json.dumps(outs if len(outs) > 1 else outs[0], ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()