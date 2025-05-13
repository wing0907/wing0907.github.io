# constitution_to_chunks.py
import json, re, unicodedata, argparse
from pathlib import Path
from typing import Dict, List, Any

def norm(s: str) -> str:
    if not s: return ""
    s = unicodedata.normalize("NFKC", s)
    s = re.sub(r"[ \t\r\f\v]+", " ", s)
    s = re.sub(r"\u00A0", " ", s)  # nbsp
    s = re.sub(r"\s+\n", "\n", s)
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip()

def join_nonempty(parts: List[str], sep=" "):
    return sep.join([p for p in parts if p and p.strip()])

def textify_list(x):
    # XML→JSON 변환 과정에서 본문이 [[...]] 같은 중첩리스트로 올 때 안전하게 펴기
    if isinstance(x, str): return x
    out=[]
    def walk(o):
        if isinstance(o, list):
            for v in o: walk(v)
        elif isinstance(o, dict):
            for v in o.values(): walk(v)
        elif isinstance(o, str):
            out.append(o)
    walk(x)
    return "\n".join(out)

# --- 헤더/구조 탐지 유틸 ---
_struct_re = re.compile(r"^제\s*(\d+)\s*(장|절|관)\s*(.*)$")
_pure_article_header_re = re.compile(r"^제\s*\d+\s*조\s*$")

def parse_structure_heading(text: str):
    """
    '제10장 헌법개정' 같은 구조 헤더면 (unit, no, title) 반환. 아니면 None.
    unit은 '장'/'절'/'관'
    """
    if not text: return None
    m = _struct_re.match(text.strip())
    if not m: return None
    no, unit, title = m.group(1), m.group(2), (m.group(3) or "").strip()
    return unit, no, title

def is_pure_article_header(text: str) -> bool:
    """'제128조'처럼 내용 없이 조문 머리만 들어온 경우"""
    if not text: return False
    return bool(_pure_article_header_re.match(text.strip()))

# --- 본문 청킹 ---
def chunk_article(article: Dict[str, Any], path_prefix: str, law_name: str, out_rows: List[Dict[str, Any]]):
    num  = article.get("조문번호") or article.get("조번호") or ""
    atit = article.get("조문제목") or article.get("조제목") or ""
    atext_raw = article.get("조문내용")
    atext = textify_list(atext_raw) if atext_raw is not None else ""
    atext = norm(atext)

    # 0) 조문내용이 구조 헤더(제10장/제1절/제2관 ...)로 잘못 들어온 경우: 조문으로 넣지 말고 구조로 분리
    parsed = parse_structure_heading(atext)
    if parsed:
        unit, no, title = parsed
        struct_path = join_nonempty([path_prefix, f"{unit} {no} {title}".strip()])
        out_rows.append({
            "id": f"struct:{unit}-{no}",
            "law": law_name,
            "unit": unit,              # '장' / '절' / '관'
            "path": struct_path,
            "article_no": "",          # 조문과 무관
            "title": title,
            "text": atext              # 그대로 보존
        })
        # 조문으로는 추가하지 않고 종료
        atext = ""  # 아래 조문 추가 로직 타지 않도록 비움

    # 1) '제128조'처럼 내용 없는 조문 헤더만 온 경우는 스킵
    if atext and is_pure_article_header(atext):
        atext = ""

    base_path = join_nonempty([path_prefix, f"{num} {atit}".strip()])

    # 2) 조문 본문 청크
    if atext:
        out_rows.append({
            "id": f"{num}::0" if num else f"root::{len(out_rows)}",
            "law": law_name,
            "unit": "조문",
            "path": base_path,
            "article_no": num,
            "title": atit,
            "text": atext
        })

    # 3) 항/호/목 재귀
    def handle_ho_list(ho_list: List[Dict[str,Any]], current_path: str, article_no: str):
        for ho in ho_list or []:
            if not isinstance(ho, dict):
                continue
            hnum  = ho.get("호번호","")
            htxt  = norm(textify_list(ho.get("호내용","")))
            path  = join_nonempty([current_path, f"{hnum}"])
            if htxt:
                out_rows.append({
                    "id": f"{article_no}::{hnum}",
                    "law": law_name,
                    "unit": "호",
                    "path": path,
                    "article_no": article_no,
                    "title": "",
                    "text": htxt
                })
            # 목
            for mok in ho.get("목",[]) or []:
                if not isinstance(mok, dict):
                    continue
                mnum = mok.get("목번호","")
                mtxt = norm(textify_list(mok.get("목내용","")))
                mpath= join_nonempty([path, f"{mnum}"])
                if mtxt:
                    out_rows.append({
                        "id": f"{article_no}::{hnum}-{mnum}",
                        "law": law_name,
                        "unit": "목",
                        "path": mpath,
                        "article_no": article_no,
                        "title": "",
                        "text": mtxt
                    })

    for hang in article.get("항",[]) or []:
        if isinstance(hang, dict):
            hnum  = hang.get("항번호","")
            htxt  = norm(textify_list(hang.get("항내용","")))
            hpath = join_nonempty([base_path, f"{hnum}"])
            if htxt:
                out_rows.append({
                    "id": f"{num}::{hnum}",
                    "law": law_name,
                    "unit": "항",
                    "path": hpath,
                    "article_no": num,
                    "title": "",
                    "text": htxt
                })
            handle_ho_list(hang.get("호"), hpath, num)
        elif isinstance(hang, str):  # "제2항 생략" 등
            htxt = norm(hang)
            if htxt:
                out_rows.append({
                    "id": f"{num}::free{len(out_rows)}",
                    "law": law_name,
                    "unit": "항",
                    "path": base_path,
                    "article_no": num,
                    "title": "",
                    "text": htxt
                })

def walk_structure(node: Any, law_name: str, trail: List[str], out_rows: List[Dict[str,Any]]):
    if isinstance(node, dict):
        # 전문
        if "전문" in node and isinstance(node["전문"], (str, list, dict)):
            preface = norm(textify_list(node["전문"]))
            if preface:
                out_rows.append({
                    "id": "preface",
                    "law": law_name,
                    "unit": "전문",
                    "path": "전문",
                    "article_no": "",
                    "title": "전문",
                    "text": preface
                })

        # 조문 묶음 키 후보
        for key in ["조문단위","조문","조항호목"]:
            if key in node:
                items = node[key]
                if isinstance(items, dict):
                    if any(k in items for k in ("조문번호","조문제목","조문내용","항")):
                        chunk_article(items, " > ".join(trail), law_name, out_rows)
                elif isinstance(items, list):
                    for art in items:
                        if isinstance(art, dict) and any(k in art for k in ("조문번호","조문제목","조문내용","항")):
                            chunk_article(art, " > ".join(trail), law_name, out_rows)

        # 계층 키(편/장/절/관 등) 후보
        for level_key, name_key, no_key in [
            ("편","편명","편번호"),
            ("장","장명","장번호"),
            ("절","절명","절번호"),
            ("관","관명","관번호"),
            ("장관절","명","번호"),
        ]:
            if level_key in node:
                lv = node[level_key]
                lv_list = lv if isinstance(lv, list) else [lv]
                for lv_item in lv_list:
                    title = lv_item.get(name_key,"")
                    no    = lv_item.get(no_key,"")
                    next_trail = trail + [f"{no} {title}".strip()]
                    # 구조 자체를 별도 레코드로 남기고 싶으면 아래 주석 해제
                    # if title or no:
                    #     out_rows.append({
                    #         "id": f"struct:{level_key}-{no}",
                    #         "law": law_name,
                    #         "unit": level_key,
                    #         "path": " > ".join(next_trail),
                    #         "article_no": "",
                    #         "title": title,
                    #         "text": f"제{no}{level_key} {title}".strip()
                    #     })
                    walk_structure(lv_item, law_name, next_trail, out_rows)

        # 일반 재귀
        for v in node.values():
            walk_structure(v, law_name, trail, out_rows)

    elif isinstance(node, list):
        for v in node:
            walk_structure(v, law_name, trail, out_rows)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", default="constitution_full.json", help="lawService JSON (대한민국헌법)")
    ap.add_argument("--out", default="data/constitution/constitution_chunks.jsonl")
    ap.add_argument("--min_chars", type=int, default=0, help="짧은 청크 필터(0이면 모두 포함)")
    args = ap.parse_args()

    raw = json.load(open(args.input, "r", encoding="utf-8"))
    law = raw.get("법령") or raw.get("law") or raw
    basic = ((law or {}).get("기본정보")) or {}
    law_name = basic.get("법령명_한글") or basic.get("법령명한글") or "대한민국헌법"

    rows: List[Dict[str,Any]] = []
    walk_structure(law, law_name, [], rows)

    # 길면 분할(1500자, overlap 150자)
    final=[]
    CHUNK=1500; OVER=150
    for r in rows:
        t=r["text"]
        if len(t) <= CHUNK:
            if len(t) >= args.min_chars:
                final.append(r)
        else:
            start=0; idx=0
            while start < len(t):
                piece = t[start:start+CHUNK]
                if len(piece) >= args.min_chars:
                    nr=r.copy()
                    nr["id"] = f'{r["id"]}#part{idx}'
                    nr["text"]=piece
                    final.append(nr)
                if start+CHUNK >= len(t): break
                start += CHUNK-OVER
                idx+=1

    outp = Path(args.out)
    outp.parent.mkdir(parents=True, exist_ok=True)
    with open(outp, "w", encoding="utf-8") as f:
        for row in final:
            f.write(json.dumps(row, ensure_ascii=False)+"\n")

    print(f"✔ 청크 저장: {outp}  (rows={len(final)})  law={law_name}")

if __name__ == "__main__":
    main()