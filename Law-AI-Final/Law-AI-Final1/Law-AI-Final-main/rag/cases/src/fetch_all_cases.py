# # -*- coding: utf-8 -*-
# """
# law.go.kr DRF - 판례 전체 수집기
# - 월별(prncYd)로 페이지 끝까지 탐색 (query 없이도 동작)
# - org/curt/datSrcNm/검색범위(search) 선택 가능 (기본: 전체 법원, 판례명 검색)
# - 목록 -> 상세(본문)까지 수집, JSONL로 저장, 재시작 내결합(resume/dedup)

# 사용법 예)
# python fetch_all_prec.py --oc YOUR_OC --start 195001 --end 202512 --out_dir ./prec_all
# """
# import argparse, time, json
# from pathlib import Path
# from datetime import date, timedelta
# import requests

# SEARCH_URL = "http://www.law.go.kr/DRF/lawSearch.do"
# DETAIL_URL = "http://www.law.go.kr/DRF/lawService.do"

# def month_iter(start_yyyymm: int, end_yyyymm: int):
#     sy, sm = divmod(start_yyyymm, 100); sm = sm or 1
#     ey, em = divmod(end_yyyymm, 100);   em = em or 12
#     d = date(sy, sm, 1)
#     last = date(ey, em, 1)
#     while d <= last:
#         n = date(d.year + (1 if d.month == 12 else 0), 1 if d.month == 12 else d.month+1, 1)
#         yield d, (n - timedelta(days=1))
#         d = n

# def http_get(url, params, retry=3, delay=0.6):
#     for i in range(retry):
#         try:
#             r = requests.get(url, params=params, timeout=30)
#             r.raise_for_status()
#             return r
#         except Exception:
#             if i == retry - 1:
#                 raise
#             time.sleep(delay * (i + 1))

# def main():
#     ap = argparse.ArgumentParser()
#     ap.add_argument("--oc", required=True, help="peter.jaewoochang")
#     ap.add_argument("--start", type=int, default=195001, help="시작 YYYYMM")
#     ap.add_argument("--end",   type=int, default=203012, help="끝 YYYYMM")
#     ap.add_argument("--out_dir", default="/workspace/TensorJae/Study25/Kings_final_project/rag/cases/data")

#     # 필터 옵션
#     ap.add_argument("--org", help="법원종류 코드 (대법원:400201, 하위법원:400202)")
#     ap.add_argument("--curt", help="법원명(대법원, 서울고등법원 등)")
#     ap.add_argument("--datSrcNm", help="데이터출처명(국세법령정보시스템, 근로복지공단산재판례, 대법원)")
#     ap.add_argument("--search", type=int, default=1, help="검색범위 1:판례명(기본), 2:본문검색")
#     ap.add_argument("--sort", default="ddes", help="정렬옵션(dasc/ddes/lasc/ldes/nasc/ndes)")

#     # 수집 파라미터
#     ap.add_argument("--delay", type=float, default=0.5, help="요청 사이 딜레이(초)")
#     ap.add_argument("--display", type=int, default=100, help="페이지 당 개수(최대 100)")
#     ap.add_argument("--max_pages", type=int, default=5000, help="월별 안전장치: 최대 페이지")
#     args = ap.parse_args()

#     out = Path(args.out_dir); out.mkdir(parents=True, exist_ok=True)
#     list_fp   = out / "prec_list.jsonl"
#     detail_fp = out / "prec_detail.jsonl"

#     # 상세 dedup (resume)
#     seen = set()
#     if detail_fp.exists():
#         for line in detail_fp.open(encoding="utf-8"):
#             try:
#                 j = json.loads(line)
#                 pid = str(j.get("판례정보일련번호") or j.get("판례일련번호") or "")
#                 if pid: seen.add(pid)
#             except: pass
#     print(f"[resume] existing detail: {len(seen)}")

#     with list_fp.open("a", encoding="utf-8") as fo_list, \
#          detail_fp.open("a", encoding="utf-8") as fo_det:

#         for s, e in month_iter(args.start, args.end):
#             ym = f"{s:%Y-%m}"
#             page = 1
#             while page <= args.max_pages:
#                 params = {
#                     "OC": args.oc,
#                     "target": "prec",
#                     "type": "JSON",
#                     "display": args.display,
#                     "page": page,
#                     "search": args.search,
#                     "prncYd": f"{s:%Y%m%d}~{e:%Y%m%d}",
#                     "sort": args.sort
#                 }
#                 if args.org: params["org"] = args.org
#                 if args.curt: params["curt"] = args.curt
#                 if args.datSrcNm: params["datSrcNm"] = args.datSrcNm
#                 # query 없이 월 전체 긁기

#                 r = http_get(SEARCH_URL, params, delay=args.delay)
#                 data = r.json()

#                 items = data.get("prec")
#                 if not items:
#                     if page == 1:
#                         print(f"[{ym}] no results")
#                     break
#                 if isinstance(items, dict):
#                     items = [items]

#                 # 목록 저장
#                 for it in items:
#                     fo_list.write(json.dumps(it, ensure_ascii=False) + "\n")

#                 # 상세
#                 got = 0
#                 for it in items:
#                     pid = str(it.get("판례일련번호") or it.get("prec id") or "").strip()
#                     if not pid or pid in seen: continue

#                     dparams = {"OC": args.oc, "target": "prec", "ID": pid, "type": "JSON"}
#                     try:
#                         dr = http_get(DETAIL_URL, dparams, delay=args.delay)
#                         dj = dr.json()
#                     except Exception as ex:
#                         print(f"[warn] detail fail id={pid}: {ex}"); continue

#                     dj["_meta"] = {"월": ym, "목록": it}
#                     fo_det.write(json.dumps(dj, ensure_ascii=False) + "\n")
#                     seen.add(pid); got += 1
#                     time.sleep(args.delay)

#                 print(f"[{ym}] page {page}: list={len(items)} detail_new={got}")
#                 page += 1
#                 time.sleep(args.delay)

#     print("[done] 목록:", list_fp)
#     print("[done] 상세:", detail_fp)
#     print(f"[done] 상세 총 {len(seen)} 건 수집(파일 누적 기준)")
# if __name__ == "__main__":
#     main()










# save as: fetch_prec_smart.py
# -*- coding: utf-8 -*-
import os, json, time, math, argparse
import requests
from datetime import datetime
from calendar import monthrange

LIST_URL = "https://www.law.go.kr/DRF/lawSearch.do"
DETAIL_URL = "https://www.law.go.kr/DRF/lawService.do"

GANA_BUCKETS = ["ga","na","da","ra","ma","ba","sa","a","ja","cha","ka","ta","pa","ha"]

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
    "Referer": "https://www.law.go.kr/",
}

CASE_TYPES = {  # 필요시 추가
    "민사": "400101",
    "형사": "400102",
    "가사": "400105",
    "특허": "400106",
    "일반행정": "400107",
}

def month_range_str(y, m):
    last = monthrange(y, m)[1]
    return f"{y:04d}{m:02d}01~{y:04d}{m:02d}{last:02d}"

def year_range_str(y):
    return f"{y}0101~{y}1231"

def get_json(url, params, delay, retries=4):
    backoff = delay
    last_txt = ""
    for attempt in range(retries):
        r = requests.get(url, params=params, headers=HEADERS, timeout=30, allow_redirects=True)
        ct = (r.headers.get("Content-Type") or "").lower()
        txt = (r.text or "").strip()
        if ("json" in ct) or txt.startswith("{") or txt.startswith("["):
            try:
                return r.json()
            except Exception:
                last_txt = txt[:200]
        # HTML/차단 등 → 백오프
        time.sleep(backoff)
        backoff *= 1.8
    raise RuntimeError(f"Non-JSON response: {last_txt!r} params={params}")

def iter_periods(mode, start, end):
    if mode == "year":
        ys, ye = int(start[:4]), int(end[:4])
        for y in range(ys, ye+1):
            yield ("Y", y, None, year_range_str(y))
    else:  # month
        ys, ms = int(start[:4]), int(start[4:])
        ye, me = int(end[:4]), int(end[4:])
        y, m = ys, ms
        while (y < ye) or (y == ye and m <= me):
            yield ("M", y, m, month_range_str(y,m))
            if m == 12: y, m = y+1, 1
            else: m += 1

def save_state(path, state):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

def load_state(path):
    if os.path.exists(path):
        try:
            return json.load(open(path, encoding="utf-8"))
        except Exception:
            return {}
    return {}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--oc", required=True)
    ap.add_argument("--out_dir", default="./prec_out")
    ap.add_argument("--start", default="200001", help="YYYYMM (month mode) or YYYY000 (year mode ignored)")
    ap.add_argument("--end", default=datetime.now().strftime("%Y%m"))
    ap.add_argument("--mode", choices=["month","year"], default="month")
    ap.add_argument("--display", type=int, default=100)  # 1~100
    ap.add_argument("--delay", type=float, default=0.9)
    ap.add_argument("--court", choices=["all","sc","lower"], default="all")
    ap.add_argument("--types", default="all", help="comma names or 'all' (예: 민사,형사,특허)")
    ap.add_argument("--with_body", action="store_true")
    ap.add_argument("--resume", action="store_true")
    args = ap.parse_args()

    os.makedirs(args.out_dir, exist_ok=True)
    f_list = open(os.path.join(args.out_dir, "prec_list.jsonl"), "a", encoding="utf-8")
    f_det  = open(os.path.join(args.out_dir, "prec_detail.jsonl"), "a", encoding="utf-8")
    seen_ids_path = os.path.join(args.out_dir, ".seen_ids.json")
    state_path = os.path.join(args.out_dir, ".state.json")

    # court param
    court_param = {}
    if args.court == "sc":
        court_param["org"] = "400201"
    elif args.court == "lower":
        court_param["org"] = "400202"

    # types parse
    type_map = {}
    if args.types == "all":
        type_map = CASE_TYPES.copy()
    else:
        for name in [x.strip() for x in args.types.split(",") if x.strip()]:
            if name not in CASE_TYPES:
                print(f"[warn] unknown 사건종류명: {name} (스킵)")
                continue
            type_map[name] = CASE_TYPES[name]
        if not type_map:
            type_map = CASE_TYPES.copy()

    # seen ids
    if os.path.exists(seen_ids_path):
        seen_ids = set(json.load(open(seen_ids_path, encoding="utf-8")))
    else:
        seen_ids = set()

    state = load_state(state_path) if args.resume else {}

    for (mode_tag, y, m, pr) in iter_periods(args.mode, args.start, args.end):
        for type_name, type_code in type_map.items():
            for gana in GANA_BUCKETS:
                page = 1
                # resume support
                key = f"{mode_tag}:{y}:{m or 0}:{type_code}:{gana}"
                if args.resume and state.get("key") == key:
                    page = int(state.get("page", 1))

                while True:
                    params = {
                        "OC": args.oc,
                        "target": "prec",
                        "type": "JSON",
                        "display": str(args.display),
                        "page": str(page),
                        "gana": gana,
                        "prncYd": pr,
                        "사건종류코드": type_code,  # 필터 추가
                        **court_param,
                    }
                    try:
                        data = get_json(LIST_URL, params, delay=args.delay)
                    except Exception as e:
                        print(f"[warn] list fail {y}-{m or 0} type={type_name} gana={gana} page={page}: {e}")
                        break

                    root = data.get("PrecSearch") or {}
                    arr = root.get("prec") or []
                    total_cnt = None
                    try:
                        total_cnt = int(root.get("totalCnt")) if root.get("totalCnt") is not None else None
                    except Exception:
                        total_cnt = None

                    if not arr:
                        if page == 1:
                            print(f"[{mode_tag}-{y}-{m or 0} {type_name} gana={gana}] no results")
                        break

                    # 기록 + 상세 큐
                    ids=[]
                    for row in arr:
                        f_list.write(json.dumps(row, ensure_ascii=False) + "\n")
                        pid = str(row.get("판례일련번호") or row.get("id") or "").strip()
                        if pid:
                            ids.append(pid)
                    f_list.flush()

                    if args.with_body:
                        for pid in ids:
                            if pid in seen_ids:
                                continue
                            dparams = {"OC": args.oc, "target": "prec", "ID": pid, "type":"JSON"}
                            try:
                                det = get_json(DETAIL_URL, dparams, delay=args.delay)
                                det["_id"] = pid
                                f_det.write(json.dumps(det, ensure_ascii=False) + "\n")
                                f_det.flush()
                                seen_ids.add(pid)
                                # 주기적 체크포인트
                                if len(seen_ids) % 200 == 0:
                                    json.dump(list(seen_ids), open(seen_ids_path, "w", encoding="utf-8"), ensure_ascii=False)
                            except Exception as e:
                                print(f"[warn] detail fail id={pid}: {e}")
                            time.sleep(args.delay)

                    # 페이지 계속?
                    if total_cnt:
                        max_pages = math.ceil(total_cnt / args.display)
                        if page >= max_pages:
                            break
                    else:
                        # totalCnt가 없으면, 빈 페이지 만날 때까지 진행
                        pass

                    page += 1
                    if args.resume:
                        state = {"key": key, "page": page}
                        save_state(state_path, state)
                    time.sleep(args.delay)

    # save seen
    json.dump(list(seen_ids), open(seen_ids_path, "w", encoding="utf-8"), ensure_ascii=False)
    f_list.close(); f_det.close()
    print(f"[done] 목록: {f_list.name}")
    print(f"[done] 상세: {f_det.name}")
    if os.path.exists(state_path):
        os.remove(state_path)

if __name__ == "__main__":
    main()