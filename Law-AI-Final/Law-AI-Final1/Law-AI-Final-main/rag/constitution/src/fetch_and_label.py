# -*- coding: utf-8 -*-
# rag/fetch_and_label.py
import os, time, json, requests, xmltodict
from pathlib import Path
from urllib.parse import urlencode
from dotenv import load_dotenv

from parse_prec_detail import parse_prec_xml_to_labeled, parse_prec_json_to_labeled

load_dotenv()

OC            = os.environ.get("LAW_OC")  # 반드시 설정
RESP_TYPE     = os.environ.get("LAW_RESP_TYPE", "XML").upper()  # XML | JSON
COURT         = os.environ.get("LAW_COURT", "대법원")
SEARCH_MODE   = int(os.environ.get("LAW_SEARCH", "2"))  # 1: 사건명, 2: 본문
PERIOD        = os.environ.get("LAW_PERIOD", "20100101~20251231")
LIMIT_PER_KEY = int(os.environ.get("LAW_LIMIT", "200"))

# 키워드: 환경변수 -> 파일(rag/keywords.txt) -> 기본 세트
DEFAULT_KEYWORDS = ["담보권", "불법행위", "손해배상", "채무자회생", "계약해지", "하자담보", "소멸시효", "가압류"]
KEYWORDS = [k.strip() for k in os.environ.get("LAW_KEYWORDS","").split(",") if k.strip()]
if not KEYWORDS:
    kfile = Path(__file__).with_name("keywords.txt")
    if kfile.exists():
        KEYWORDS = [ln.strip() for ln in kfile.read_text(encoding="utf-8").splitlines() if ln.strip()]
if not KEYWORDS:
    KEYWORDS = DEFAULT_KEYWORDS

RAW_DIR = Path("data/raw/case"); RAW_DIR.mkdir(parents=True, exist_ok=True)

def _fail_if_no_oc():
    if not OC or OC.strip()=="":
        raise RuntimeError("LAW_OC 가 비어있다. .env에 LAW_OC=네_OC 이메일ID 를 넣어라.")

def _parse_search_items_xml(text: str):
    d = xmltodict.parse(text)
    items = d.get("PrecSearch",{}).get("prec",[])
    if isinstance(items, dict): items = [items]
    out=[]
    for it in items:
        out.append({
            "prec_id": it.get("판례일련번호") or it.get("prec id"),
            "case_no": it.get("사건번호"),
            "case_name": it.get("사건명"),
            "court": it.get("법원명"),
            "judgement_date": it.get("선고일자"),
        })
    return out

def _parse_search_items_json(text: str):
    data = json.loads(text)
    items = data.get("PrecSearch",{}).get("prec",[])
    if isinstance(items, dict): items=[items]
    out=[]
    for it in items:
        out.append({
            "prec_id": it.get("판례일련번호") or it.get("prec id"),
            "case_no": it.get("사건번호"),
            "case_name": it.get("사건명"),
            "court": it.get("법원명"),
            "judgement_date": it.get("선고일자"),
        })
    return out

def prec_search(query: str, page=1, display=100):
    base = "http://www.law.go.kr/DRF/lawSearch.do"
    params = {
        "OC": OC, "target": "prec", "type": RESP_TYPE,
        "query": query, "display": display, "page": page,
        "search": SEARCH_MODE, "sort": "ddes"
    }
    if PERIOD: params["prncYd"] = PERIOD
    if COURT:  params["curt"]   = COURT
    r = requests.get(base, params=params, timeout=30, headers={"User-Agent":"curl/8"})
    r.raise_for_status()
    ct = r.headers.get("Content-Type","")
    if "text/html" in ct:
        raise RuntimeError("HTML 오류 페이지 수신(OC 또는 파라미터 점검).")
    if RESP_TYPE == "JSON":
        return _parse_search_items_json(r.text)
    else:
        return _parse_search_items_xml(r.text)

def fetch_detail(prec_id: str) -> dict:
    base = "http://www.law.go.kr/DRF/lawService.do"
    params = {"OC": OC, "target": "prec", "type": RESP_TYPE, "ID": prec_id}
    url = f"{base}?{urlencode(params)}"
    r = requests.get(url, timeout=60, headers={"User-Agent":"curl/8"})
    r.raise_for_status()
    ct = r.headers.get("Content-Type","")
    if "text/html" in ct:
        raise RuntimeError("HTML 오류 페이지 수신")
    if RESP_TYPE == "JSON":
        return parse_prec_json_to_labeled(r.text)
    else:
        return parse_prec_xml_to_labeled(r.text)

def save_jsonl(path: Path, rows):
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False)+"\n")

if __name__ == "__main__":
    _fail_if_no_oc()
    print(f"[RUN] RESP_TYPE={RESP_TYPE}  COURT={COURT}  SEARCH={SEARCH_MODE}  PERIOD={PERIOD}  LIMIT_PER_KEY={LIMIT_PER_KEY}")
    print(f"[RUN] KEYWORDS={KEYWORDS}")

    for Q in KEYWORDS:
        out_rows=[]
        page, got = 1, 0
        while got < LIMIT_PER_KEY:
            lst = prec_search(Q, page=page, display=100)
            if not lst: break
            for it in lst:
                if got>=LIMIT_PER_KEY: break
                pid = it.get("prec_id") or it.get("case_no")
                if not pid: continue
                try:
                    labeled = fetch_detail(pid)
                    out_rows.append(labeled)
                    got += 1
                    time.sleep(0.3)  # DRF 배려
                except Exception as e:
                    print("skip", it, e)
            page += 1
        out_path = RAW_DIR / f"prec_{Q}_s{SEARCH_MODE}_labeled.jsonl"
        save_jsonl(out_path, out_rows)
        print(f"[OK] saved {out_path} ({len(out_rows)} docs)")