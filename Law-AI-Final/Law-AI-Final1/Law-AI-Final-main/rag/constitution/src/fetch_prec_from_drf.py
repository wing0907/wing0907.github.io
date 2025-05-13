# rag/fetch_prec_from_drf.py
import os, time, re, json, requests, xmltodict
from urllib.parse import urlencode
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
OC = os.environ["LAW_OC"]  # .env에 LAW_OC=네_OC

RAW_DIR = Path("data/raw/case"); RAW_DIR.mkdir(parents=True, exist_ok=True)

def clean(s:str)->str:
    return re.sub(r"\s+"," ", s or "").strip()

def flatten_xml_text(obj):
    out=[]
    if isinstance(obj, dict):
        for k,v in obj.items(): out.append(flatten_xml_text(v))
    elif isinstance(obj, list):
        for v in obj: out.append(flatten_xml_text(v))
    else:
        if isinstance(obj, str): out.append(obj)
    return clean(" ".join(x for x in out if x))

def prec_search(query:str, page=1, display=100, search=1, curt=None, org=None, prncYd=None, sort="ddes"):
    base = "http://www.law.go.kr/DRF/lawSearch.do"
    params = {"OC":OC,"target":"prec","type":"XML","query":query,"display":display,"page":page,"search":search,"sort":sort}
    if curt: params["curt"]=curt
    if org:  params["org"]=org
    if prncYd: params["prncYd"]=prncYd
    r = requests.get(base, params=params, timeout=30, headers={"User-Agent":"curl/8"})
    r.raise_for_status()
    if "text/html" in r.headers.get("Content-Type",""):  # 에러 페이지 방지
        raise RuntimeError("HTML 에러 페이지 수신: OC/파라미터 확인")
    d = xmltodict.parse(r.text)
    items = d.get("PrecSearch",{}).get("prec",[])
    if isinstance(items, dict): items=[items]
    rows=[]
    for it in items:
        rows.append({
            "prec_id": it.get("판례일련번호") or it.get("precSeq") or it.get("prec id"),
            "case_no": it.get("사건번호") or it.get("caseNo"),
            "case_name": it.get("사건명") or it.get("caseName"),
            "court": it.get("법원명") or it.get("courtName"),
            "judgement_date": it.get("선고일자") or it.get("judgementDate"),
            "detail_link": it.get("판례상세링크"),
        })
    return rows

def extract_priority_sections(d:dict)->str:
    """
    상세 XML에서 핵심 섹션(판시사항/판결요지/참조조문/주문/이유 등)만 우선 결합.
    태그명이 환경에 따라 다를 수 있어, 후보 키들을 폭넓게 탐색한다.
    """
    key_candidates = [
        "판시사항","판결요지","참조조문","주문","이유",
        "holding","headnote","references","order","reason"
    ]
    buf=[]
    def walk(obj):
        if isinstance(obj, dict):
            for k,v in obj.items():
                if any(c in k for c in key_candidates):
                    txt = flatten_xml_text(v)
                    if txt: buf.append(f"[{k}]\n{txt}")
                walk(v)
        elif isinstance(obj, list):
            for v in obj: walk(v)
    walk(d)
    return "\n\n".join(buf)

def prec_detail(prec_id=None, case_no=None):
    # 1) 권장: 판례일련번호로 조회
    if prec_id:
        base = "http://www.law.go.kr/DRF/lawService.do"
        params = {"OC": OC, "target": "prec", "type": "XML", "ID": prec_id}
        r = requests.get(base, params=params, timeout=60, headers={"User-Agent":"curl/8"})
        r.raise_for_status()
        if "text/html" not in r.headers.get("Content-Type",""):
            d = xmltodict.parse(r.text)
            txt = extract_priority_sections(d) or flatten_xml_text(d)
            return clean(txt), d

    # 2) 예비: 사건번호로 조회(일부 케이스 대응)
    if case_no:
        base = "http://www.law.go.kr/DRF/lawService.do"
        params = {"OC": OC, "target": "prec", "type": "XML", "ID": case_no}
        r = requests.get(base, params=params, timeout=60, headers={"User-Agent":"curl/8"})
        r.raise_for_status()
        if "text/html" not in r.headers.get("Content-Type",""):
            d = xmltodict.parse(r.text)
            txt = extract_priority_sections(d) or flatten_xml_text(d)
            return clean(txt), d

    raise RuntimeError("상세 본문 조회 실패")

def save_jsonl(path:Path, rows):
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False)+"\n")

if __name__=="__main__":
    import argparse
    p=argparse.ArgumentParser()
    p.add_argument("--query", default="담보권")
    p.add_argument("--search", type=int, default=1)  # 1 사건명 / 2 본문
    p.add_argument("--limit", type=int, default=30)
    p.add_argument("--court", default="대법원")
    p.add_argument("--period", default=None)  # 예: 20150101~20251231
    args=p.parse_args()

    out_rows=[]
    page, got = 1, 0
    while got < args.limit:
        lst = prec_search(args.query, page=page, display=100, search=args.search, curt=args.court, prncYd=args.period, sort="ddes")
        if not lst: break
        for it in lst:
            if got>=args.limit: break
            pid = it["prec_id"] or it["case_no"]
            if not pid: continue
            try:
                text = prec_detail(pid)
                out_rows.append({
                    "source":"case",
                    "text": text,
                    "meta": {
                        "prec_id": it["prec_id"],
                        "case_no": it["case_no"],
                        "case_name": it["case_name"],
                        "court": it["court"],
                        "judgement_date": it["judgement_date"],
                    }
                })
                got += 1
                time.sleep(0.4)
            except Exception as e:
                print("skip", it, e)
        page += 1

    out_path = RAW_DIR / f"prec_{args.query}_s{args.search}.jsonl"
    save_jsonl(out_path, out_rows)
    print(f"saved {out_path} ({len(out_rows)} docs)")