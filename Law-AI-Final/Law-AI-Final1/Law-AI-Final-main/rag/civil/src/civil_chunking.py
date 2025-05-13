# -*- coding: utf-8 -*-
"""
민법 JSON (law.go.kr) → 조문/항 단위 chunking
입력: civil_code_full.json
출력: civil_meta.jsonl  (RAG 메타)
옵션: --include_supp  부칙도 chunking (요약/검색용)
"""
import json, re, unicodedata, argparse
from pathlib import Path

HEAD_PATTERNS = [
    (re.compile(r"^제\d+편\b"), "편"),
    (re.compile(r"^제\d+장\b"), "장"),
    (re.compile(r"^제\d+절\b"), "절"),
    (re.compile(r"^제\d+관\b"), "관"),
    (re.compile(r"^제\d+목\b"), "목"),
    (re.compile(r"^제\d+절의\d+\b"), "절의"),  # 드물게 '절의2' 같은 것
]

ART_HEADER_RE = re.compile(r"^제(?P<num>[\d]+(?:의\d+)?)조(?:\((?P<title>[^)]+)\))?")  # 제1004조의2 대응
NFKC = lambda s: unicodedata.normalize("NFKC", s) if s else s

def parse_headers_stack(item_text, stack):
    """'제1편 총칙', '제1장 통칙' 같은 전문(heading) 갱신."""
    t = item_text.strip()
    for pat, label in HEAD_PATTERNS:
        if pat.search(t):
            # 같은 계층(label) 이후 레벨은 지워주고 현재 라벨을 교체
            # 순서: 편 > 장 > 절 > 관 > 목 (대략적)
            order = ["편","장","절","관","목","절의"]
            lvl = order.index(label)
            # stack 은 dict
            for k in order[lvl:]:
                stack.pop(k, None)
            stack[label] = t
            break

def current_path(stack):
    order = ["편","장","절","관","목","절의"]
    parts = [stack[k] for k in order if k in stack]
    return " / ".join(parts)

def clean_text_front_counter(s):
    """항 텍스트 앞의 '①.', '1)', '1.' 등 카운터 제거(있으면)."""
    if not s: return s
    t = s.lstrip()
    # 이미 항번호 포함해서 넘어오는 경우도 있어 안전 처리
    t = NFKC(t)
    # 맨 앞에 숫자/원형숫자 + 구분자 제거
    t = re.sub(r"^(?:\d+|[①-⑳])(?:[\.\)\s\-]*)(?=\D)", "", t)
    return t.strip()

def article_key_from_content(content):
    """조문내용에서 제n조(제목) 패턴 파싱 → (article_no, title)"""
    m = ART_HEADER_RE.match(content.strip())
    if not m:
        return "", ""
    return m.group("num") or "", m.group("title") or ""

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--infile", default="/Users/jaewoo000/Desktop/Law_AI/rag/civil/data/civil_code_full.json")
    ap.add_argument("--outfile", default="/Users/jaewoo000/Desktop/Law_AI/rag/civil/data/civil_meta.jsonl")
    ap.add_argument("--law_name", default="민법")
    ap.add_argument("--include_supp", action="store_true", help="부칙도 chunk로 포함")
    args = ap.parse_args()

    data = json.load(open(args.infile, encoding="utf-8"))
    out = open(args.outfile, "w", encoding="utf-8")

    # ---------- 조문 처리 ----------
    stack = {}  # 편/장/절/관/목 등 헤더 경로
    chunks = 0

    articles = data.get("법령", {}).get("조문", {}).get("조문단위", [])
    for it in articles:
        kind = it.get("조문여부")  # '전문' or '조문'
        text = (it.get("조문내용") or "").strip()

        if kind == "전문":
            # 헤더 갱신
            if text:
                parse_headers_stack(text, stack)
            continue

        if kind != "조문":
            continue

        # 조문 헤더 파싱
        art_no_from_key = it.get("조문번호", "").strip()  # "14"
        content_header = it.get("조문내용", "")            # "제14조(한정후견종료의 심판)" 등
        art_no_from_hdr, art_title = article_key_from_content(content_header)
        # 조문가지번호(예: 제14조의2) 처리
        ext = it.get("조문가지번호")  # "2" -> 제14조의2
        if ext and art_no_from_hdr:
            art_no = f"{art_no_from_hdr}의{ext}"
        else:
            art_no = art_no_from_hdr or art_no_from_key

        art_title = it.get("조문제목", art_title) or ""
        law = args.law_name
        path = current_path(stack)
        article_key = it.get("조문키", "")

        # 항이 있으면 항 단위로, 없으면 조문 전체를 본문으로
        paras = it.get("항")
        if paras and isinstance(paras, list):
            for p in paras:
                sub = NFKC(p.get("항번호","")).strip() or ""   # ① → 1
                sub = NFKC(sub)
                # 항번호가 ① 같은 경우 숫자로 바꿔 동일화
                sub_nfkc = sub
                # 항 텍스트
                ptxt = p.get("항내용","") or ""
                clean_ptxt = clean_text_front_counter(ptxt)

                row = {
                    "law": law,
                    "article_no": art_no,           # 예: "14의2" or "2"
                    "unit": "항",
                    "id": f"{art_no}::{sub_nfkc}",  # "14의2::1"
                    "title": art_title,
                    "path": path,
                    "key": article_key,
                    "text": clean_ptxt,
                }
                out.write(json.dumps(row, ensure_ascii=False) + "\n")
                chunks += 1
        else:
            # 항이 없는 조문 (제1조 같이 본문이 한 줄)
            # content_header 자체가 '제n조(제목) + 본문' 형태이므로,
            # 제목 헤더 부분을 떼고 뒤쪽 본문만 추출(없으면 전체 사용)
            body = content_header
            m = ART_HEADER_RE.match(content_header)
            if m:
                body = content_header[m.end():].strip(" \n\r\t")
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
            # 내용은 2중 리스트가 많음
            flat_lines = []
            for block in contents:
                if isinstance(block, list):
                    flat_lines.extend([str(x) for x in block])
                else:
                    flat_lines.append(str(block))
            # 문단 단위로 chunk (너무 잘게 쪼개지 않도록 1줄=1청크)
            for i, line in enumerate(flat_lines, 1):
                line = line.strip()
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
                }
                out.write(json.dumps(row, ensure_ascii=False) + "\n")
                chunks += 1

    out.close()
    print(f"✅ chunk 생성 완료: {args.outfile} (총 {chunks}개)")
    

if __name__ == "__main__":
    main()