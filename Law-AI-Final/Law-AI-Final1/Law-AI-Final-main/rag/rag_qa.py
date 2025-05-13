# rag/rag_qa.py
# -*- coding: utf-8 -*-
import os, json, argparse, faiss, re, unicodedata
from pathlib import Path
from sentence_transformers import SentenceTransformer
import numpy as np
from textwrap import shorten
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

# ---------- 공통: 메타/임베딩 ---------------------------------------------------
def load_meta(meta_path: Path):
    rows=[]
    with open(meta_path, "r", encoding="utf-8") as f:
        for line in f:
            s=line.strip()
            if s: rows.append(json.loads(s))
    return rows

def embed_query(q: str, model_name: str, device: str = "cpu"):
    model = SentenceTransformer(model_name, device=device)
    vec = model.encode([q], convert_to_numpy=True, normalize_embeddings=True)
    return model, vec

# ---------- 법령/판례 자동 감지 -------------------------------------------------
def is_case_row(row: dict) -> bool:
    """판례 인덱스인지 감지: PrecService 기반 필드/section/판례정보일련번호가 있으면 판례"""
    keys = set(row.keys())
    if "section" in keys and ("판례정보일련번호" in keys or "사건명" in keys or "사건번호" in keys):
        return True
    # 법령 전용 키가 아예 없고 사건 관련 필드가 있으면 케이스로 본다
    if {"사건명","사건번호","선고일자","법원명"} & keys and not ({"article_no","unit"} & keys):
        return True
    return False

def detect_corpus_kind(rows: list) -> str:
    if not rows: return "unknown"
    return "case" if is_case_row(rows[0]) else "law"

# ---------- 멀티 인덱스 로딩 ----------------------------------------------------
def load_bundles(index_root: Path):
    """
    index_root/<sub>/faiss.index + meta.jsonl 세트를 찾아 로드.
    반환: [(코퍼스명, kind('law'|'case'), faiss_index, rows, display_name)]
    """
    bundles=[]
    for sub in sorted([p for p in index_root.iterdir() if p.is_dir()]):
        idx_f = sub / "faiss.index"
        meta_f = sub / "meta.jsonl"
        if idx_f.exists() and meta_f.exists():
            index = faiss.read_index(str(idx_f))
            rows = load_meta(meta_f)
            kind = detect_corpus_kind(rows)
            # 대표 표시 이름
            display = rows[0].get("law", sub.name) if (kind=="law" and rows) else \
                      rows[0].get("법원명", sub.name) if rows else sub.name
            bundles.append((sub.name, kind, index, rows, display))
    if not bundles:
        raise FileNotFoundError(f"No FAISS+meta under {index_root}")
    return bundles

def retrieve_multi(bundles, qvec: np.ndarray, topk_each: int = 8):
    """
    각 인덱스에서 topk_each 검색 → 합쳐 점수 정렬.
    반환: [{"score": float, "row": dict, "kind": "law"|"case"} ...]
    """
    all_hits=[]
    qv = qvec.astype(np.float32)
    for corpus, kind, index, rows, display in bundles:
        D, I = index.search(qv, topk_each)
        for idx, sc in zip(I[0], D[0]):
            if idx < 0 or idx >= len(rows): continue
            r = dict(rows[idx])
            r["_score"] = float(sc)
            if kind == "law":
                r["law"] = r.get("law", display)
            else:
                # 판례에선 표시 이름 보강(없을 경우)
                r["법원명"] = r.get("법원명", display)
            all_hits.append({"score": float(sc), "row": r, "kind": kind})
    all_hits.sort(key=lambda x: x["score"], reverse=True)
    return all_hits

# ---------- 공통 유틸: 본문 키 통일 ---------------------------------------------
def _nfkc(s: str) -> str:
    return unicodedata.normalize("NFKC", s) if s else ""

def row_text(row: dict) -> str:
    """법령은 'text', 판례는 '전문'이 본문 키 → 통일해서 반환"""
    return (row.get("text") or row.get("전문") or "").strip()

# ---------- 원문자(①②…⑳) 정규화 유틸 -----------------------------------------
_CIRCLED_TO_DIGIT = {
    "①":"1","②":"2","③":"3","④":"4","⑤":"5",
    "⑥":"6","⑦":"7","⑧":"8","⑨":"9","⑩":"10",
    "⑪":"11","⑫":"12","⑬":"13","⑭":"14","⑮":"15",
    "⑯":"16","⑰":"17","⑱":"18","⑲":"19","⑳":"20",
}
_DIGIT_TO_CIRCLED = {v:k for k,v in _CIRCLED_TO_DIGIT.items()}

def _norm_subnum(s: str) -> str:
    """항/호/목 번호를 NFKC + 원문자→숫자 변환"""
    s = _nfkc(s or "")
    return _CIRCLED_TO_DIGIT.get(s, s)

# ---------- 표기/스니펫 유틸(법령) ---------------------------------------------
def extract_subnum(row) -> str:
    if row.get("unit") in {"항","호","목"} and "::" in row.get("id",""):
        sub = row["id"].split("::", 1)[1]
        return _norm_subnum(sub)  # 정규화 적용
    return ""

def format_ref_law(row) -> str:
    art = row.get("article_no","")
    unit= row.get("unit","")
    parts=[]
    if art: parts.append(f"제{art}조")
    sub = extract_subnum(row)
    if unit == "항" and sub: parts.append(f"제{sub}항")
    elif unit == "호" and sub: parts.append(f"{sub}호")
    elif unit == "목" and sub: parts.append(f"{sub}목")
    if not parts:
        t = row.get("title","")
        return t if t else row.get("path","")
    return " ".join(parts)

_LEADING_COUNTER = re.compile(r"^[\d①-⑳\.\)\-\s]+")

def clean_leading_counter_law(row, text: str) -> str:
    if not text: return text
    unit = row.get("unit","")
    if unit not in {"항","호","목"}: return text

    raw = row.get("id","").split("::",1)[1] if "::" in row.get("id","") else ""
    sub_num = _norm_subnum(raw)               # "1"
    sub_circ = _DIGIT_TO_CIRCLED.get(sub_num) # "①" or None

    t = text
    # 숫자 시작 제거
    if sub_num and t.startswith(sub_num):
        t = t[len(sub_num):]
        t = re.sub(r"^[\.\)\s\-]+", "", t)
        return t
    # 원문자 시작 제거
    if sub_circ and t.startswith(sub_circ):
        t = t[len(sub_circ):]
        t = re.sub(r"^[\.\)\s\-]+", "", t)
        return t
    return t

def format_hit_law(row, score, snippet_chars=160):
    law  = row.get("law","법령")
    ref  = format_ref_law(row)
    path = row.get("path","")
    txt  = clean_leading_counter_law(row, row_text(row))
    snip = shorten(txt.replace("\n"," "), width=snippet_chars, placeholder="…")
    return f"[{score:.3f}] {law} {ref} ({row.get('unit','')}) | path: {path} | \"{snip}\""

# ---------- 표기/스니펫 유틸(판례) ---------------------------------------------
def tidy_date(d: str) -> str:
    # "20001222" → "2000-12-22"
    if not d: return ""
    if len(d)==8 and d.isdigit():
        return f"{d[:4]}-{d[4:6]}-{d[6:8]}"
    return d

def format_ref_case(row) -> str:
    # [대법원 2000-12-22, 2000다56259, 급여등] 처럼 간결하게
    court = row.get("법원명","법원")
    date  = tidy_date(row.get("선고일자",""))
    num   = row.get("사건번호","")
    name  = row.get("사건명","")
    base  = f"{court} {date}, {num}"
    return f"{base}, {name}" if name else base

def format_hit_case(row, score, snippet_chars=160):
    ref  = format_ref_case(row)
    sec  = row.get("section","")
    txt  = row_text(row)
    snip = shorten(txt.replace("\n"," "), width=snippet_chars, placeholder="…")
    return f"[{score:.3f}] {ref} [{sec}] \"{snip}\""

# ---------- LLM 로딩 -----------------------------------------------------------
def load_llm_local_first(model_path: str):
    mp = Path(model_path)
    if not mp.exists():
        raise FileNotFoundError(f"모델 폴더가 없음: {mp}")
    print(f"🔗 로컬 모델 사용: {mp}")
    tok = AutoTokenizer.from_pretrained(str(mp), local_files_only=True)
    # pad 토큰 설정(주의: 일부 Llama 계열은 eos를 pad로 재사용)
    if tok.pad_token_id is None and tok.eos_token_id is not None:
        tok.pad_token_id = tok.eos_token_id
    model = AutoModelForCausalLM.from_pretrained(
        str(mp),
        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
        device_map="auto",
        local_files_only=True
    )
    return tok, model

# ---------- 법 이름 매칭/쿼리 파서 ---------------------------------------------
LAW_ALIASES = {
    "헌법": ["헌법", "대한민국헌법"],
    "민법": ["민법"],
    "형법": ["형법"],
}

def _normalize(s: str) -> str:
    return _nfkc(s).replace(" ", "")

def law_name_matches(row_law: str, want_name: str) -> bool:
    """row_law가 want_name(별칭 포함)과 실질적으로 동일한지 확인"""
    if not row_law or not want_name: return False
    rl = _normalize(row_law)
    for nm in LAW_ALIASES.get(want_name, [want_name]):
        if rl == _normalize(nm):
            return True
    # '대한민국헌법' vs '헌법' 같은 포함관계 허용
    if _normalize(want_name) in rl or rl in _normalize(want_name):
        return True
    return False

LAW_QUERY_RE = re.compile(
    r"(헌법|민법|형법)\s*제?\s*(\d+)\s*조(?:\s*제?\s*(\d+)\s*항)?",
    re.IGNORECASE
)

def parse_law_query(query: str):
    """쿼리에서 법령명/조/항(옵션)을 추출"""
    m = LAW_QUERY_RE.search(query)
    if not m:
        # '헌법 10조', '민법 245조 1항' 형태도 허용
        m = re.search(r"(헌법|민법|형법)\s*(\d+)\s*조(?:\s*(\d+)\s*항)?", query)
    if not m:
        return None
    want_law = m.group(1)
    want_art = m.group(2)
    want_sub = m.group(3) if len(m.groups()) >= 3 else None
    return {"law": want_law, "article": want_art, "sub": want_sub}

# ---------- “직접 정답” (LLM 우회) ---------------------------------------------
# 힌트/범위
MULTI_HINT_RE = re.compile(r"(모든|전부|전체|각\s*항|요건)")
RANGE_RE = re.compile(r"(\d+)\s*[-~]\s*(\d+)\s*항")

def _unit_sort_key(r):
    """항 정렬 키: 항이면 숫자 기준, 아니면 조금 앞에 두기"""
    if r.get("unit") == "항":
        raw = r.get("id","").split("::",1)[1] if "::" in r.get("id","") else ""
        sub = _norm_subnum(raw)
        return int(sub) if sub.isdigit() else 10**9
    return 10**9 - 1  # 조문은 항들보다 약간 앞쪽

def _format_one_line(r):
    law = r.get("law","법령")
    art = r.get("article_no","")
    unit = r.get("unit","")
    tail = ""
    if unit == "항" and "::" in r.get("id",""):
        sub = _norm_subnum(r["id"].split("::",1)[1])
        tail = f" 제{sub}항"
    ref = f"{law} 제{art}조{tail}"
    raw = row_text(r)
    text = clean_leading_counter_law(r, raw)
    return f"[{ref}] {text}"

def _pick_first_hang(cands):
    best = None
    bestn = 10**9
    for r in cands:
        if r.get("unit") == "항":
            raw = r.get("id","").split("::",1)[1] if "::" in r.get("id","") else ""
            sub = _norm_subnum(raw)
            if sub.isdigit():
                n = int(sub)
                if n < bestn:
                    bestn, best = n, r
    return best

def try_direct_answer(query: str, hits, max_multi: int = 12):
    """
    정확 매칭 시 LLM 우회. 단일/범위/전체항 자동 처리.
    hits: [(row, kind), ...]
    """
    p = parse_law_query(query)
    if not p:
        return None

    want_law, want_art, want_sub = p["law"], p["article"], p["sub"]
    want_sub_norm = _norm_subnum(want_sub) if want_sub else None

    # 키워드로 "전체 항" 강제
    force_all_keywords = ["정당행위", "정당방위", "긴급피난", "불법행위", "요건"]
    want_all = bool(MULTI_HINT_RE.search(query)) or any(k in query for k in force_all_keywords)

    rng = RANGE_RE.search(query)
    want_range = None
    if rng:
        a, b = int(rng.group(1)), int(rng.group(2))
        if a > b: a, b = b, a
        want_range = (a, b)

    # 같은 법/같은 조에서 후보 수집
    cands = []
    for r, kind in hits:
        if kind != "law":
            continue
        if not law_name_matches(r.get("law",""), want_law):
            continue
        if r.get("article_no","") != want_art:
            continue
        unit = r.get("unit","")
        if unit in {"조문", ""} or unit == "항":
            cands.append(r)

    if not cands:
        return None

    # 단일 항 지정만 있는 경우
    if want_sub_norm and not want_all and not want_range:
        for r in cands:
            if r.get("unit") == "항":
                raw = r.get("id","").split("::",1)[1] if "::" in r.get("id","") else ""
                sub = _norm_subnum(raw)
                if sub == want_sub_norm:
                    return _format_one_line(r)
        # 정확 항이 없으면 조문 본문으로 폴백
        for r in cands:
            if r.get("unit") in {"조문", ""}:
                return _format_one_line(r)
        return _format_one_line(cands[0])

    # 범위 요청(예: 1~3항)
    if want_range:
        lo, hi = want_range
        lines = []
        for r in sorted(cands, key=lambda x: _unit_sort_key(x)):
            if r.get("unit") != "항":
                continue
            raw = r.get("id","").split("::",1)[1] if "::" in r.get("id","") else ""
            sub = _norm_subnum(raw)
            if sub.isdigit():
                n = int(sub)
                if lo <= n <= hi:
                    lines.append(_format_one_line(r))
            if len(lines) >= max_multi:
                break
        return "\n".join(lines) if lines else None

    # 전체/요건/각 항 → 같은 조의 모든 항(가능하면 조문 본문은 맨 위 1줄만)
    if want_all:
        main = None
        for r in cands:
            if r.get("unit") in {"조문", ""}:
                main = r; break
        lines = []
        if main:
            lines.append(_format_one_line(main))
        for r in sorted(cands, key=lambda x: _unit_sort_key(x)):
            if r.get("unit") == "항":
                lines.append(_format_one_line(r))
            if len(lines) >= max_multi:
                break
        return "\n".join(lines) if lines else (_format_one_line(main) if main else None)

    # 기본: 조문 1줄 (없으면 1항)
    for r in cands:
        if r.get("unit") in {"조문", ""}:
            return _format_one_line(r)
    first_hang = _pick_first_hang(cands)
    if first_hang:
        return _format_one_line(first_hang)
    return _format_one_line(cands[0])

# ---------- 프롬프트 빌더 (법령/판례) ------------------------------------------
def build_prompt_law(question: str, contexts):
    ctx_lines=[]
    for i, c in enumerate(contexts, 1):
        law = c.get("law","법령")
        ref = format_ref_law(c)
        txt = clean_leading_counter_law(c, row_text(c))
        txt = txt.replace("\n"," ").strip()
        ctx_lines.append(f"{i}. [{law} {ref}] {txt}")
    ctx_text = "\n".join(ctx_lines)

    system = (
        "당신은 대한민국 법령 RAG 어시스턴트입니다.\n"
        "- 반드시 아래 '컨텍스트'만 근거로 답하세요(외부지식 금지).\n"
        "- 인용은 본문 안에 [법령명 제X조(제Y항)] 형식으로 최소 1개 이상 표기.\n"
        "- 답변은 반드시 한국어로 작성하세요.\n"
        "- 근거가 없으면 '제공된 발췌문에서 확인되지 않습니다.'라고 답하세요.\n"
        "- 과도한 추론 금지. 최대 5문장, 불릿 허용."
    )
    user = (
        "아래 컨텍스트만 활용해 답하세요.\n\n"
        f"질문:\n{question}\n\n"
        f"컨텍스트:\n{ctx_text}\n\n"
        "작성 지침:\n"
        "- 출력형식: plain\n"
        "- 먼저 핵심 결론 1~2문장, 필요 시 불릿으로 요건/근거 정리.\n"
        "- 각 근거 옆에 [법령명 제X조(제Y항)] 형태로 인용.\n"
        "\n답변:"
    )
    return system, user

def build_prompt_case(question: str, contexts):
    ctx_lines=[]
    for i, c in enumerate(contexts, 1):
        ref = format_ref_case(c)  # ex) 대법원 2000-12-22, 2000다56259, 급여등
        sec = c.get("section","")
        txt = row_text(c).replace("\n"," ").strip()
        ctx_lines.append(f"{i}. [{ref}] ({sec}) {txt}")
    ctx_text = "\n".join(ctx_lines)

    system = (
    "당신은 대한민국 법령·판례 RAG 어시스턴트입니다.\n"
    "- 반드시 아래 '컨텍스트'(법령 조문 또는 판결문 발췌)만 근거로 답하세요(외부지식 금지).\n"
    "- 질문이 법령 해석을 요구하면, 조문을 그대로 근거로 설명하세요.\n"
    "- 질문이 판례 관련이면, 판례의 판시사항·판결요지·판례내용을 중심으로 답하세요.\n"
    "- 답변은 반드시 한국어로 작성하세요.\n"
    "- 인용은 본문 안에 다음 형식으로 표기:\n"
    "  • 법령: [민법 제750조 제1항]\n"
    "  • 판례: [대법원 2000-12-22 2000다56259, 판결요지]\n"
    "- 컨텍스트에 없는 사실이나 판단은 임의로 만들지 말고, 부족하면 '제공된 발췌문에서 확인되지 않습니다.'라고 답하세요.\n"
    "- 최대 5문장 이내로, 필요 시 불릿으로 정리. 핵심 논지·법리만 간결히 요약."
    )
    user = (
        "아래 컨텍스트(판례 발췌)만 활용해 답하세요.\n\n"
        f"질문:\n{question}\n\n"
        f"컨텍스트:\n{ctx_text}\n\n"
        "작성 지침:\n"
        "- 출력형식: plain\n"
        "- 반드시 한국어로만 답하세요. 영어를 포함하지 마세요.\n"
        "- 먼저 핵심 결론 1~2문장, 필요 시 불릿로 법리/요건/사실관계 포인트 정리.\n"
        "- 인용은 [법원명 선고일자 사건번호, 섹션] 형식.\n"
        "\n답변:"
    )
    return system, user

def build_prompt_auto(kind: str, question: str, contexts):
    return build_prompt_case(question, contexts) if kind=="case" else build_prompt_law(question, contexts)

# ---------- LLM 템플릿 적용/후처리 ---------------------------------------------
def apply_chat_or_plain(tok: AutoTokenizer, sys_msg: str, user_msg: str) -> str:
    msgs = [{"role":"system","content":sys_msg},{"role":"user","content":user_msg}]
    if hasattr(tok, "apply_chat_template"):
        try:
            return tok.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True)
        except Exception:
            pass
    return sys_msg + "\n\n" + user_msg + "\n\n"

_STRIP_LINES_RE = re.compile(r"^\s*(\[?(SYSTEM|USER|ASSISTANT)\]?)\s*:?.*$", re.IGNORECASE)
def postprocess_answer(text: str) -> str:
    lines = text.splitlines()
    cleaned=[]
    for ln in lines:
        s=ln.strip()
        if _STRIP_LINES_RE.match(s): continue
        if re.fullmatch(r"\d{2,4}[-/.: ]\d{1,2}[-/.: ]\d{1,2}(?:\s+\d{1,2}:\d{2}(?::\d{2})?)?", s):
            continue
        if s: cleaned.append(ln)
    text="\n".join(cleaned).strip()
    # 3회 이상 반복 줄 제거
    dedup=[]; prev=None; repeat=0
    for ln in text.splitlines():
        cur=ln.strip()
        if cur==prev:
            repeat+=1
            if repeat>=2: continue
        else:
            prev=cur; repeat=0
        dedup.append(ln)
    return "\n".join(dedup).strip()

# ---------- 메인 ----------------------------------------------------------------
def main():
    ROOT = Path(__file__).resolve().parents[1]
    # 디바이스 기본값: cuda > mps > cpu
    default_dev = "cuda" if torch.cuda.is_available() else ("mps" if torch.backends.mps.is_available() else "cpu")

    ap = argparse.ArgumentParser()
    ap.add_argument("-q","--query", required=True)
    ap.add_argument("--index_root", default=str(ROOT / "index_mac"))  # 이 폴더 아래 각 코퍼스 폴더
    ap.add_argument("--embed_model", default="BAAI/bge-m3")
    ap.add_argument("--device", default=default_dev)  # 임베딩용 디바이스
    ap.add_argument("--topk", type=int, default=6)
    ap.add_argument("--topk_each", type=int, default=6)
    ap.add_argument("--min_score", type=float, default=0.5)
    ap.add_argument("--dedup", action="store_true", help="결과 디듑(법령: (law,조,단위) / 판례: (판례ID,섹션))")
    ap.add_argument("--show_retrieval", action="store_true")
    ap.add_argument("--snippet_chars", type=int, default=160)
    ap.add_argument("--max_ctx", type=int, default=12000)
    ap.add_argument("--llm", default=str(ROOT / "models" / "Meta-Llama-3-8B"))
    ap.add_argument("--max_new_tokens", type=int, default=512)
    args = ap.parse_args()

    index_root = Path(args.index_root)

    # 1) 쿼리 임베딩
    _, qvec = embed_query(args.query, args.embed_model, device=args.device)

    # 2) 인덱스 로드 & 검색
    bundles = load_bundles(index_root)
    merged_hits = retrieve_multi(bundles, qvec, topk_each=args.topk_each)

    # ======================================================================
    # 패치 A — 정확 조문 우선 리랭크 (법·조·항 인식 시 같은 조 우선)
    # ======================================================================
    m = LAW_QUERY_RE.search(args.query) or re.search(r"(헌법|민법|형법)\s*(\d+)\s*조(?:\s*(\d+)\s*항)?", args.query)
    if m:
        want_law, want_art, want_hang = m.group(1), m.group(2), m.group(3)

        def exact_row(h):
            r = h["row"]
            if h["kind"] != "law": return False
            if not law_name_matches(r.get("law"), want_law): return False
            if r.get("article_no") != want_art: return False
            if want_hang:
                return (r.get("unit") == "항") and (f"::{_norm_subnum(want_hang)}" in (r.get("id","")) or r.get("id","").endswith(f"::{want_hang}"))
            return True

        def same_article(h):
            r = h["row"]
            return h["kind"]=="law" and law_name_matches(r.get("law"), want_law) and (r.get("article_no")==want_art)

        def same_law(h):
            r = h["row"]
            return h["kind"]=="law" and law_name_matches(r.get("law"), want_law)

        exact = [h for h in merged_hits if exact_row(h)]
        loose = [h for h in merged_hits if h not in exact and same_article(h)]
        same  = [h for h in merged_hits if (h not in exact) and (h not in loose) and same_law(h)]
        other = [h for h in merged_hits if (h not in exact) and (h not in loose) and (h not in same)]
        merged_hits = exact + loose + same + other
    # ======================================================================

    # 3) 필터링/디듑 & 최종 상위
    hits=[]; seen=set()
    for h in merged_hits:
        r = h["row"]; s = h["score"]; kind = h["kind"]
        if s < args.min_score: continue
        if args.dedup:
            if kind=="law":
                key=(kind, r.get("law",""), r.get("article_no",""), r.get("unit",""))
            else:  # case
                pid = r.get("판례정보일련번호") or r.get("_id") or r.get("사건번호")
                key=(kind, pid, r.get("section",""))
            if key in seen: continue
            seen.add(key)
        r["_score"]=s
        hits.append((r, kind))
        if len(hits) >= args.topk: break

    # 3.5) 검색결과 표시
    if args.show_retrieval:
        print("\n=== RETRIEVAL ===")
        if not hits:
            print("(no hits above threshold)")
        else:
            for r, kind in hits:
                if kind=="law":
                    print(format_hit_law(r, r.get("_score",0.0), snippet_chars=args.snippet_chars))
                else:
                    print(format_hit_case(r, r.get("_score",0.0), snippet_chars=args.snippet_chars))

    # ---------- LLM 우회: 정확 조문이면 여기서 바로 답 출력 ----------
    direct = try_direct_answer(args.query, hits)
    if direct:
        print(f"\n(info) selected_ctx={len(hits)} total_chars={sum(len(row_text(r)) for r,_ in hits)} kind=law")
        print("\n=== ANSWER ===")
        print(direct)
        return

    # 4) 컨텍스트 누적
    contexts=[]; total_len=0; final_kind="law"
    if hits:
        final_kind = "case" if is_case_row(hits[0][0]) else "law"
    for r, kind in hits:
        t = row_text(r)
        if total_len + len(t) > args.max_ctx: break
        contexts.append(r); total_len += len(t)

    print(f"\n(info) selected_ctx={len(contexts)} total_chars={total_len} kind={final_kind}")

    if not contexts:
        print("\n=== ANSWER ===")
        print("제공된 발췌문에서 확인되지 않습니다.")
        return

    # 5) 프롬프트 구성(코퍼스 종류에 따라)
    sys_msg, user_msg = build_prompt_auto(final_kind, args.query, contexts)
    messages = [{"role":"system","content":sys_msg},{"role":"user","content":user_msg}]

    tok, model = load_llm_local_first(args.llm)

    # chat_template 있으면 사용 (MPS에서 attention_mask 필수 → 직접 생성)
    try:
        inputs_ids_only = tok.apply_chat_template(
            messages, return_tensors="pt", add_generation_prompt=True
        )
        if isinstance(inputs_ids_only, torch.Tensor):
            input_ids = inputs_ids_only.to(model.device)
            attention_mask = torch.ones_like(input_ids)  # MPS 오류 방지: 마스크 수동 생성
        else:
            rendered = tok.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
            enc = tok(rendered, return_tensors="pt", padding=True).to(model.device)
            input_ids = enc["input_ids"]
            attention_mask = enc["attention_mask"]
    except Exception:
        # Llama-3 수동 포맷
        def render_llama3(system_text, user_text):
            return ("<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n"
                    f"{system_text}\n"
                    "<|eot_id|><|start_header_id|>user<|end_header_id|>\n"
                    f"{user_text}\n"
                    "<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n")
        prompt = render_llama3(sys_msg, user_msg)
        enc = tok(prompt, return_tensors="pt", add_special_tokens=False, padding=True).to(model.device)
        input_ids = enc["input_ids"]
        attention_mask = enc.get("attention_mask", torch.ones_like(input_ids))

    eot_id = tok.convert_tokens_to_ids("<|eot_id|>")
    eos_id = eot_id if (eot_id is not None and eot_id != tok.unk_token_id) else tok.eos_token_id

    out = model.generate(
        input_ids=input_ids,
        attention_mask=attention_mask,  # 반드시 전달
        max_new_tokens=args.max_new_tokens,
        do_sample=False,
        eos_token_id=eos_id,
        repetition_penalty=1.05,
    )
    gen_ids = out[0][input_ids.shape[1]:]
    answer = tok.decode(gen_ids, skip_special_tokens=True).strip()
    answer = postprocess_answer(answer)

    print("\n=== ANSWER ===")
    print(answer if answer else "제공된 발췌문에서 확인되지 않습니다.")

if __name__=="__main__":
    main()