# -*- coding: utf-8 -*-
# save as: chunking_law.py
"""
판례 본문 JSONL(한 줄당 한 건; {"PrecService": {...}, "_id": ...} 형태)을
청킹하여 RAG 인덱싱에 적합한 JSONL로 변환.

사용 예시:
  python chunking_law.py \
    --in_jsonl prec_detail.jsonl \
    --out_jsonl chunks.jsonl \
    --max_chars 3500 \
    --overlap_ratio 0.15 \
    --sections 판시사항 판결요지 판례내용 \
    --case_types 민사 형사 일반행정 가사 특허 \
    --date_from 19900101 --date_to 20251231

필드 설명(출력 1줄):
{
  "chunk_id": "191110|판례내용|0003",
  "text": "...",
  "meta": {
    "판례정보일련번호": "191110",
    "사건명": "...",
    "사건번호": "...",
    "사건종류명": "민사",
    "선고일자": "20001226",
    "법원명": "대법원",
    "판결유형": "판결",
    "section": "판례내용"
  },
  "weight": 1.0
}
"""

import re
import json
import argparse
from typing import List, Dict, Any, Iterable, Optional
from html import unescape

# 기본 섹션 키
SECTION_KEYS = ["판시사항", "판결요지", "판례내용"]

# -------------------------------
# 텍스트 전처리 & 청킹 유틸
# -------------------------------

def clean_html(s: str) -> str:
    """간단한 HTML → 텍스트 정리 + 공백 정규화."""
    if not s:
        return ""
    s = unescape(s)
    s = re.sub(r'<br\s*/?>', '\n', s, flags=re.I)
    s = re.sub(r'</?p[^>]*>', '\n', s, flags=re.I)
    s = re.sub(r'</?div[^>]*>', '\n', s, flags=re.I)
    s = re.sub(r'</?span[^>]*>', '', s, flags=re.I)
    s = re.sub(r'<[^>]+>', '', s)              # 태그 제거
    s = s.replace('\u00A0', ' ')               # nbsp
    s = re.sub(r'\r\n?', '\n', s)              # CRLF → LF
    s = re.sub(r'[ \t]+\n', '\n', s)           # 줄끝 공백
    s = re.sub(r'\n{3,}', '\n\n', s)           # 빈 줄 과다 축소
    s = re.sub(r'[ \t]{2,}', ' ', s)           # 스페이스 연속 축소
    return s.strip()

def split_paras(text: str) -> List[str]:
    """빈 줄 기준 문단 분리(번호/항목 보존)."""
    if not text:
        return []
    paras = [p.strip() for p in re.split(r'\n\s*\n', text) if p and p.strip()]
    return paras

def sliding_chunks(paras: List[str], max_chars=3500, overlap_ratio=0.15) -> List[str]:
    """
    문단 단위 슬라이딩 윈도우 청킹.
    - max_chars: 청크 최대 글자 수
    - overlap_ratio: 이전 청크의 문단 일부를 다음 청크 앞부분으로 겹치기 (문맥 보존)
    """
    chunks: List[str] = []
    buf: List[str] = []
    sizes = 0

    for p in paras:
        # 새 문단 p 추가 시 max 초과하면 플러시
        if buf and sizes + len(p) + 2 > max_chars:
            chunks.append('\n\n'.join(buf))
            # overlap: 뒤에서 일부 문단 유지
            keep_n = max(1, int(len(buf) * overlap_ratio))
            buf = buf[-keep_n:]
            sizes = sum(len(x) for x in buf) + 2 * (len(buf) - 1)
        # 현재 문단 누적
        buf.append(p)
        sizes += len(p) + 2

    if buf:
        chunks.append('\n\n'.join(buf))
    return chunks

def safe_get(d: Dict[str, Any], *keys, default=None):
    cur = d
    for k in keys:
        if isinstance(cur, dict) and k in cur:
            cur = cur[k]
        else:
            return default
    return cur

def normalize_date8(s: Optional[str]) -> Optional[str]:
    """YYYYMMDD 8자리만 남기고 숫자 외 제거."""
    if not s:
        return None
    digits = re.sub(r'[^0-9]', '', str(s))
    if len(digits) >= 8:
        return digits[:8]
    return None

def make_chunk_id(pid: str, section: str, idx: int) -> str:
    """판례일련번호|섹션|0001 형식 ID 생성."""
    return f"{pid}|{section}|{idx:04d}"

def section_aware_chunks(
    case_json: Dict[str, Any],
    max_chars: int = 3500,
    overlap_ratio: float = 0.15,
    sections: Optional[Iterable[str]] = None
) -> List[Dict[str, Any]]:
    """
    입력: PrecService 필드가 들어있는 dict (이미 JSON 파싱된 한 건)
    출력: [{chunk_id, text, meta{...}, weight}] 리스트
    """
    # 케이스 구조 안전 파싱
    ps = case_json.get("PrecService") or {}

    pid = str(ps.get("판례정보일련번호") or case_json.get("_id") or "").strip()
    meta_base = {
        "판례정보일련번호": pid or None,
        "사건명": ps.get("사건명"),
        "사건번호": ps.get("사건번호"),
        "사건종류명": ps.get("사건종류명"),
        "선고일자": normalize_date8(ps.get("선고일자")),
        "법원명": ps.get("법원명"),
        "판결유형": ps.get("판결유형"),
    }

    use_sections = list(sections) if sections else SECTION_KEYS
    out: List[Dict[str, Any]] = []
    idx_counter = 0

    # 1) 판시사항/판결요지: 짧은 청크(가중치 ↑)
    for k in ["판시사항", "판결요지"]:
        if k not in use_sections:
            continue
        raw = ps.get(k)
        if not raw:
            continue
        txt = clean_html(raw)
        for para in split_paras(txt):
            if not para:
                continue
            chunk_id = make_chunk_id(pid or "NA", k, idx_counter)
            out.append({
                "chunk_id": chunk_id,
                "text": para,
                "meta": {**meta_base, "section": k},
                "weight": 1.2
            })
            idx_counter += 1

    # 2) 판례내용: 길어서 문단 기반 슬라이딩
    if "판례내용" in use_sections:
        body = ps.get("판례내용")
        if body:
            body_txt = clean_html(body)
            paras = split_paras(body_txt)
            for ch in sliding_chunks(paras, max_chars=max_chars, overlap_ratio=overlap_ratio):
                chunk_id = make_chunk_id(pid or "NA", "판례내용", idx_counter)
                out.append({
                    "chunk_id": chunk_id,
                    "text": ch,
                    "meta": {**meta_base, "section": "판례내용"},
                    "weight": 1.0
                })
                idx_counter += 1

    return out

# -------------------------------
# 파일 드라이버 (CLI)
# -------------------------------

def case_pass_filters(
    case_json: Dict[str, Any],
    case_types: Optional[Iterable[str]] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None
) -> bool:
    """사건종류/선고일자 필터."""
    ps = case_json.get("PrecService") or {}
    t = (ps.get("사건종류명") or "").strip()
    d = normalize_date8(ps.get("선고일자"))

    if case_types:
        allow = set(str(x).strip() for x in case_types if str(x).strip())
        if t not in allow:
            return False

    if date_from:
        df = normalize_date8(date_from)
        if df and (not d or d < df):
            return False

    if date_to:
        dt = normalize_date8(date_to)
        if dt and (not d or d > dt):
            return False

    return True

def iter_jsonl(path: str) -> Iterable[Dict[str, Any]]:
    with open(path, "r", encoding="utf-8") as f:
        for ln, line in enumerate(f, 1):
            s = line.strip()
            if not s:
                continue
            try:
                yield json.loads(s)
            except Exception as e:
                # 손상된 라인 스킵
                print(f"[warn] JSON decode fail line {ln}: {e}")
                continue

def write_jsonl(path: str, rows: Iterable[Dict[str, Any]]):
    with open(path, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

def main():
    parser = argparse.ArgumentParser(description="판례 JSONL → 청크 JSONL 변환")
    parser.add_argument("--in_jsonl", required=True, help="입력: prec_detail.jsonl")
    parser.add_argument("--out_jsonl", required=True, help="출력: chunks.jsonl")
    parser.add_argument("--max_chars", type=int, default=3500, help="청크 최대 글자 수")
    parser.add_argument("--overlap_ratio", type=float, default=0.15, help="슬라이딩 겹침 비율(0~0.5 권장)")
    parser.add_argument("--sections", nargs="*", default=SECTION_KEYS, help="사용 섹션 선택 (기본: 판시사항 판결요지 판례내용)")
    parser.add_argument("--case_types", nargs="*", help="사건종류명 필터(예: 민사 형사 일반행정 가사 특허)")
    parser.add_argument("--date_from", type=str, help="선고일자 하한 YYYYMMDD")
    parser.add_argument("--date_to", type=str, help="선고일자 상한 YYYYMMDD")
    args = parser.parse_args()

    total_in = 0
    total_out = 0

    with open(args.out_jsonl, "w", encoding="utf-8") as fout:
        for case in iter_jsonl(args.in_jsonl):
            total_in += 1
            if not case_pass_filters(case, args.case_types, args.date_from, args.date_to):
                continue

            chunks = section_aware_chunks(
                case,
                max_chars=args.max_chars,
                overlap_ratio=args.overlap_ratio,
                sections=args.sections
            )
            for ch in chunks:
                fout.write(json.dumps(ch, ensure_ascii=False) + "\n")
                total_out += 1

    print(f"[done] cases read: {total_in}, chunks written: {total_out}")
    print(f"[out] {args.out_jsonl}")

if __name__ == "__main__":
    main()