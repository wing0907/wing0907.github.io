# rag/fetch_raw_only.py
import os, re, time, argparse, requests, json
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
OC = os.environ.get("LAW_OC")  # .env에 LAW_OC=네_OC
assert OC, "환경변수 LAW_OC가 없습니다 (.env에 LAW_OC=... 추가)."

def save_bytes(path: Path, content: bytes):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content)

def search_prec(query: str, page=1, display=100, search=2, sort="ddes", resp_type="XML"):
    """판례 목록 '원본 그대로' 가져와 bytes로 반환"""
    url = "http://www.law.go.kr/DRF/lawSearch.do"
    params = {
        "OC": OC,
        "target": "prec",
        "type": resp_type,     # XML/JSON/HTML 중 선택
        "query": query,
        "display": display,
        "page": page,
        "search": search,      # 1=사건명, 2=본문
        "sort": sort,
    }
    r = requests.get(url, params=params, timeout=30, headers={"User-Agent":"curl/8"})
    r.raise_for_status()
    return r.content, r.headers.get("Content-Type","")

def extract_ids_from_search(raw_bytes: bytes, resp_type: str):
    """상세 호출을 위해 ID만 최소한으로 뽑음. (원본 저장과 무관)"""
    ids = []
    if resp_type.upper() == "JSON":
        try:
            d = json.loads(raw_bytes.decode("utf-8"))
            items = d.get("PrecSearch", {}).get("prec", [])
            if isinstance(items, dict): items = [items]
            for it in items:
                pid = it.get("판례일련번호") or it.get("precSeq") or it.get("prec id")
                if pid: ids.append(str(pid))
        except Exception:
            pass
    else:  # XML/HTML일 때
        text = raw_bytes.decode("utf-8", errors="ignore")
        # 1) <판례일련번호>603539</판례일련번호>
        ids += re.findall(r"<\s*판례일련번호\s*>\s*([0-9]+)\s*<\s*/\s*판례일련번호\s*>", text)
        # 2) 판례상세링크에 ID=dddddd
        ids += re.findall(r"ID=([0-9]{3,})", text)
        ids = sorted({x for x in ids if x.isdigit()})
    return ids

def fetch_detail(prec_id: str, resp_type="XML"):
    """상세 원문 '그대로' 가져옴"""
    url = "http://www.law.go.kr/DRF/lawService.do"
    params = {"OC": OC, "target": "prec", "type": resp_type, "ID": prec_id}
    r = requests.get(url, params=params, timeout=60, headers={"User-Agent":"curl/8"})
    r.raise_for_status()
    return r.content, r.headers.get("Content-Type","")

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="라벨링 없이 원본 저장")
    ap.add_argument("--query", required=True, help="검색어 (예: 담보권)")
    ap.add_argument("--resp-type", default="XML", choices=["XML","JSON","HTML"], help="원본 저장 포맷")
    ap.add_argument("--search", type=int, default=2, help="검색범위 1=사건명, 2=본문")
    ap.add_argument("--display", type=int, default=50, help="페이지당 개수(<=100)")
    ap.add_argument("--pages", type=int, default=1, help="가져올 페이지 수")
    ap.add_argument("--limit", type=int, default=200, help="상세 최대 개수(총합)")
    ap.add_argument("--outdir", default="data/raw_only", help="저장 루트")
    ap.add_argument("--sleep", type=float, default=0.4, help="상세 호출 간 딜레이(초)")
    args = ap.parse_args()

    out_root = Path(args.outdir)
    qslug = args.query
    meta_dir = out_root / "meta"
    detail_dir = out_root / "detail" / args.resp_type.upper()

    total_ids = []
    for p in range(1, args.pages+1):
        raw, ctype = search_prec(args.query, page=p, display=args.display, search=args.search, resp_type=args.resp_type)
        # 검색 원본 저장
        save_bytes(meta_dir / f"prec_search_{qslug}_p{p}.{args.resp_type.lower()}", raw)
        ids = extract_ids_from_search(raw, args.resp_type)
        total_ids.extend(ids)
        print(f"[page {p}] saved search; found IDs: {len(ids)}")

    # 중복 제거 후 limit 적용
    seen = []
    for pid in total_ids:
        if pid not in seen:
            seen.append(pid)
    ids_final = seen[:args.limit]
    print(f"will fetch detail {len(ids_final)} items")

    # 상세 원본 그대로 저장
    for i, pid in enumerate(ids_final, 1):
        try:
            raw, ctype = fetch_detail(pid, resp_type=args.resp_type)
            save_bytes(detail_dir / f"{pid}.{args.resp_type.lower()}", raw)
            if i % 10 == 0:
                print(f"  fetched {i}/{len(ids_final)}")
            time.sleep(args.sleep)
        except Exception as e:
            print("  skip", pid, e)

    print(f"done. meta: {meta_dir} ; detail: {detail_dir}")