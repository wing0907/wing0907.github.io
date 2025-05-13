# -*- coding: utf-8 -*-
"""
형법 JSON(law.go.kr DRF) → 조문/항(필요시 호) 단위 chunking
민법 청킹 규격과 동일한 필드/로직으로 정렬

입력:  --infile  형법 전체 JSON (예: criminal_code_full.json)
출력:  --outfile 메타 jsonl (예: index/criminal/meta.jsonl)
옵션:  --include_supp  부칙도 chunking 포함
"""
import json, re, unicodedata, argparse
from pathlib import Path

# ---------- 공통 유틸 ----------
NFKC = lambda s: unicodedata.normalize("NFKC", s) if s else s

HEAD_PATTERNS = [
    (re.compile(r"^제\d+편\b"), "편"),
    (re.compile(r"^제\d+장\b"), "장"),
    (re.compile(r"^제\d+절\b"), "절"),
    (re.compile(r"^제\d+관\b"), "관"),
    (re.compile(r"^제\d+목\b"), "목"),
    (re.compile(r"^제\d+절의\d+\b"), "절의"),
]

# 제1004조의2(제목) 처럼 가지번호 포함
ART_HEADER_RE = re.compile(r"^제(?P<num>[\d]+(?:의\d+)?)조(?:\((?P<title>[^)]+)\))?")

def parse_headers_stack(item_text, stack):
    """'제1편 총칙', '제1장 …' 같은 헤더를 스택에 반영"""
    t = (item_text or "").strip()
    for pat, label in HEAD_PATTERNS:
        if pat.search(t):
            order = ["편","장","절","관","목","절의"]
            lvl = order.index(label)
            for k in order[lvl:]:
                stack.pop(k, None)
            stack[label] = t
            break

def current_path(stack):
    order = ["편","장","절","관","목","절의"]
    return " / ".join([stack[k] for k in order if k in stack])

# 항/호 본문 앞 카운터(①, 1., 1) 등) 제거
_LEAD_COUNTER = re.compile(r"^\s*(?:\d+|[①-⑳])(?:[\.\)\s\-]+)")

def clean_text_front_counter(s: str) -> str:
    if not s: return s
    t = NFKC(s).lstrip()
    return _LEAD_COUNTER.sub("", t, count=1).strip()

def article_key_from_content(content):
    """'제n조(제목)'에서 (article_no, title) 추출"""
    m = ART_HEADER_RE.match((content or "").strip())
    if not m:
        return "", ""
    return m.group("num") or "", m.group("title") or ""

# ---------- 부칙 분류(선택) ----------
TRIG_TYPES = [
    ("시행", "시행일"),
    ("적용례", "적용례"),
    ("경과조치", "경과조치"),
    ("다른 법률의 개정", "다른법개정"),
    ("다른 법령의 개정", "다른법개정"),
    ("제정", "제정"),
    ("삭제", "삭제/폐지"),
]
def classify_buchik(text: str) -> str:
    t = (text or "").replace(" ", "")
    for key, label in TRIG_TYPES:
        if key.replace(" ","") in t:
            return label
    return "부칙일반"

# ---------- 메인 처리 ----------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--infile", required=True, help="형법 DRF JSON 파일 경로")
    ap.add_argument("--outfile", required=True, help="출력 meta.jsonl 경로")
    ap.add_argument("--law_name", default="형법")
    ap.add_argument("--include_supp", action="store_true", help="부칙도 chunk로 포함")
    args = ap.parse_args()

    data = json.load(open(args.infile, encoding="utf-8"))
    outp = Path(args.outfile)
    outp.parent.mkdir(parents=True, exist_ok=True)
    out = open(outp, "w", encoding="utf-8")

    stack = {}
    chunks = 0

    # ---------- 조문 처리 ----------
    articles = (data.get("법령", {})
                    .get("조문", {})
                    .get("조문단위", []))

    for it in articles:
        kind = it.get("조문여부")  # '전문' 또는 '조문'
        content = (it.get("조문내용") or "").strip()
        if kind == "전문":
            # 경로 헤더 업데이트
            if content:
                parse_headers_stack(content, stack)
            # (민법 스크립트와 동일: 헤더 레코드는 메타에 포함하지 않음)
            continue
        if kind != "조문":
            continue

        # 조문 헤더 파싱: 제n조(제목) + 조문가지번호(의n)
        art_no_from_key = (it.get("조문번호","") or "").strip()
        content_header   = it.get("조문내용","") or ""
        art_no_from_hdr, art_title_hdr = article_key_from_content(content_header)
        ext = it.get("조문가지번호")  # ex) "2" → 제14조의2
        if ext and art_no_from_hdr:
            art_no = f"{art_no_from_hdr}의{ext}"
        else:
            art_no = art_no_from_hdr or art_no_from_key

        art_title = it.get("조문제목") or art_title_hdr or ""
        law  = args.law_name
        path = current_path(stack)
        article_key = it.get("조문키", "")

        paras = it.get("항")
        if paras:
            # 항 배열/단일 모두 처리
            hang_list = paras if isinstance(paras, list) else [paras]
            for p in hang_list:
                sub = NFKC((p.get("항번호","") or "").strip())  # ① → 1
                ptxt = p.get("항내용","") or ""
                clean_ptxt = clean_text_front_counter(ptxt)

                row = {
                    "law": law,
                    "article_no": art_no,
                    "unit": "항",
                    "id": f"{art_no}::{sub if sub else '1'}",
                    "title": art_title,
                    "path": path,
                    "key": article_key,
                    "text": clean_ptxt,
                }
                out.write(json.dumps(row, ensure_ascii=False) + "\n")
                chunks += 1

                # 하위 '호'까지 저장하고 싶으면 여기를 활성화
                if "호" in p and p["호"]:
                    ho_list = p["호"] if isinstance(p["호"], list) else [p["호"]]
                    for ho in ho_list:
                        ho_no  = NFKC((ho.get("호번호","") or "").strip()).rstrip(".)")
                        ho_txt = clean_text_front_counter(ho.get("호내용","") or "")
                        row_ho = {
                            "law": law,
                            "article_no": art_no,
                            "unit": "호",
                            "id": f"{art_no}::{ho_no if ho_no else '1'}",
                            "title": art_title,
                            "path": path,
                            "key": article_key,
                            "text": ho_txt,
                        }
                        out.write(json.dumps(row_ho, ensure_ascii=False) + "\n")
                        chunks += 1
        else:
            # 항이 없는 단일 조문 → 본문만 추출
            body = content_header
            m = ART_HEADER_RE.match(content_header)
            if m:
                body = content_header[m.end():].strip()
            row = {
                "law": law,
                "article_no": art_no,
                "unit": "조문",
                "id": f"{art_no}",
                "title": art_title,
                "path": path,
                "key": article_key,
                "text": body if body else content_header,
            }
            out.write(json.dumps(row, ensure_ascii=False) + "\n")
            chunks += 1

    # ---------- (옵션) 부칙 처리 ----------
    if args.include_supp:
        supps = data.get("법령", {}).get("부칙", {}).get("부칙단위", [])
        for s in supps:
            pub_no = s.get("부칙공포번호","")
            pub_date = s.get("부칙공포일자","")
            contents = s.get("부칙내용", [])
            # 2중 리스트 많음 → 평탄화
            flat_lines=[]
            for block in contents:
                if isinstance(block, list):
                    flat_lines.extend([str(x) for x in block])
                else:
                    flat_lines.append(str(block))
            for i, line in enumerate(flat_lines, 1):
                line = (line or "").strip()
                if not line: continue
                row = {
                    "law": f"{args.law_name}-부칙",
                    "article_no": f"부칙{pub_no}",
                    "unit": "부칙",
                    "id": f"부칙{pub_no}::{i}",
                    "title": f"부칙 {pub_no} ({pub_date})",
                    "path": "부칙",
                    "key": s.get("부칙키",""),
                    "text": line,
                    "type": classify_buchik(line),
                }
                out.write(json.dumps(row, ensure_ascii=False) + "\n")
                chunks += 1

    out.close()
    print(f"✅ chunk 생성 완료: {outp} (총 {chunks}개)")

if __name__ == "__main__":
    main()