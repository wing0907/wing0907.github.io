# -*- coding: utf-8 -*-
import json
import re
from collections import Counter
from pathlib import Path
from typing import Dict, List

import numpy as np
import torch
from sentence_transformers import SentenceTransformer
import faiss  # (직접 사용 안 하지만 환경 검증 차 남겨둠)

# 재사용: rag_qa의 유틸 일부 가져오기 (필요 함수만 복사/임포트)
from rag.rag_qa import load_bundles, retrieve_multi, load_llm_local_first
from rag.rag_qa import postprocess_answer  # 그대로 재사용
from .heuristics import extract_citations, summarize_claim, spot_fact_mismatch
from .prompts import SYSTEM_TMPL, USER_TMPL

# ---- 임베딩 공용 캐시 --------------------------------------------------------
_EMBED = {}
def get_embedder(name: str, device: str):
    key = (name, device)
    if key not in _EMBED:
        _EMBED[key] = SentenceTransformer(name, device=device)
    return _EMBED[key]

def embed_query(q: str, model_name: str, device: str):
    mdl = get_embedder(model_name, device)
    vec = mdl.encode([f"query: {q}"], convert_to_numpy=True, normalize_embeddings=True)
    return vec

# ---- 최소 혼합(판례/법령) 보장 ------------------------------------------------
def ensure_min_mix(hits: List[Dict], min_cases=4, min_laws=2, max_total=8):
    cases = [h for h in hits if h.get("section")]     # 판례: section 존재
    laws  = [h for h in hits if not h.get("section")] # 법령: section 없음
    out = []
    out.extend(cases[:min_cases]); out.extend(laws[:min_laws])
    if len(out) < max_total:
        rest = [h for h in hits if h not in out]
        out.extend(rest[: max_total - len(out)])
    return out[:max_total]

# ---- 컨텍스트 라인 빌드 ------------------------------------------------------
def build_context_lines(ctxs: List[Dict], per_item_chars: int = 900):
    """
    각 컨텍스트를 한 줄로 정리하고, 아이템별 글자수(per_item_chars)로 잘라서 과도한 프롬프트 길이를 방지.
    """
    lines = []
    for i, c in enumerate(ctxs, 1):
        if c.get("section"):  # 판례
            court = c.get("법원명", "") or c.get("court", "")
            date  = c.get("선고일자", "") or c.get("date", "")
            if len(date) == 8:
                date = f"{date[:4]}-{date[4:6]}-{date[6:]}"
            no    = c.get("사건번호", "") or c.get("case_no", "")
            sec   = c.get("section", "")
            head  = f"[{court} {date} {no}, {sec}]"
        else:                 # 법령
            law   = c.get("law", "법령")
            art   = c.get("article_no")
            ref   = f"제{art}조" if art else (c.get("title", "") or c.get("path", ""))
            head  = f"[{law} {ref}]"

        text = (c.get("text") or "").replace("\n", " ").strip()
        if per_item_chars and per_item_chars > 0 and len(text) > per_item_chars:
            text = text[:per_item_chars - 1] + "…"

        lines.append(f"{i}. {head} {text}")
    return "\n".join(lines)

# ---- 간단 키워드 추출(언어불문, 의존성 최소) -----------------------------------
_KR_STOP = set([
    "및","또는","그리고","그러나","등","관련","여부","기준","요건","판단","관계",
    "인정","책임","의무","효력","요의","관","문제","사안","사건","해당","경우","것",
    "있다","없다","한다","될","수","있는","위","같은"
])
_EN_STOP = set(["and","or","the","of","to","in","on","with","for","by","about","case","issue","whether","shall","may"])

def _extract_keywords(text: str, topk: int = 8):
    toks = re.findall(r"[A-Za-z0-9]+|[가-힣]{2,}", (text or ""))
    toks = [t.lower() for t in toks]
    toks = [t for t in toks if t not in _EN_STOP and t not in _KR_STOP]
    toks = [t for t in toks if len(t) >= 2 and not t.isdigit()]
    return [w for w, _ in Counter(toks).most_common(topk)]

# ---- 질의어 빌더(주제 일반화) ------------------------------------------------
def build_base_queries(claim: str, opponent_text: str = "", cites: dict | None = None, max_expansion: int = 6):
    cites = cites or {"case_nos": [], "laws": []}
    kw = _extract_keywords((claim or "") + " " + (opponent_text or ""))

    queries = [
        claim,
        opponent_text if opponent_text else claim,
        f"{claim} 판례",
        f"{claim} 요지",
        f"{claim} 법리",
    ]

    # 키워드 확장
    for w in kw[:max_expansion]:
        queries.append(f"{w} 판례")
        queries.append(f"{w} 법리")
        queries.append(f"{w} 요지")

    # 인용에서 추출한 사건번호/법령
    queries.extend([f"사건번호 {c}" for c in (cites.get("case_nos") or [])])
    queries.extend([str(l) for l in (cites.get("laws") or [])])

    # 중복 제거
    seen, out = set(), []
    for q in queries:
        q = (q or "").strip()
        if q and q not in seen:
            seen.add(q); out.append(q)
    return out

# ---- 가벼운 리랭커: 키워드겹침 + 섹션가중치 + 원점수 혼합 ---------------------
def rerank_hits(query: str, rows: List[Dict], alpha: float = 0.75):
    """
    final = alpha * orig_score + (1-alpha) * (kw_overlap + section_boost)
    - kw_overlap: 질의 키워드가 텍스트에 포함된 갯수(0~0.1로 정규화)
    - section_boost: 판시사항/판결요지 +0.06, 판례내용 +0.02, 법령 +0.04
    """
    kws = set(_extract_keywords(query, topk=10))

    def kw_overlap(txt: str):
        if not txt:
            return 0.0
        t = txt.lower()
        hit = sum(1 for k in kws if k and k in t)
        return min(0.1, hit * 0.02)

    def sec_boost(r: Dict):
        sec = r.get("section")
        if sec == "판시사항": return 0.06
        if sec == "판결요지": return 0.06
        if sec == "판례내용": return 0.02
        if not sec:          return 0.04  # 법령
        return 0.0

    scored = []
    for r in rows:
        base = float(r.get("_score", 0.0))
        txt  = (r.get("text") or "")
        final = alpha * base + (1.0 - alpha) * (kw_overlap(txt) + sec_boost(r))
        rr = dict(r); rr["_score_final"] = final
        scored.append(rr)

    scored.sort(key=lambda x: x["_score_final"], reverse=True)
    return scored

# ---- 메인 로직 ----------------------------------------------------------------
def simulate_counter(
    opponent_text: str,
    index_root: Path,
    embed_model: str = "BAAI/bge-m3",
    device: str = "cuda",
    pre_k: int = 40,                 # ↓ 살짝 줄여 메모리/노이즈 감소
    final_k: int = 5,
    llm_path: Path = Path("models/Meta-Llama-3-8B"),
    max_new_tokens: int = 256,
    alpha: float = 0.75,             # 리랭커 혼합가중치
    # ★ 추가: 프롬프트/검색 안전 파라미터
    max_ctx_chars: int = 8000,       # LLM에 넣을 컨텍스트 총 글자 상한
    per_item_chars: int = 900,       # 컨텍스트 한 조각당 최대 글자
    min_score: float = 0.20,         # 너무 낮은 매칭 컷
):
    # 1) 파싱
    cites = extract_citations(opponent_text)
    claim = summarize_claim(opponent_text)

    # 2) 검색 쿼리들(일반화)
    base_queries = build_base_queries(claim=claim, opponent_text=opponent_text, cites=cites)

    # 3) 인덱스 로딩 + 멀티검색
    bundles = load_bundles(index_root)
    qvecs = [embed_query(q, embed_model, device=device) for q in base_queries]

    all_hits = []
    for qv in qvecs:
        merged = retrieve_multi(bundles, qv, topk_each=pre_k)
        # ★ 추가: 저점수 컷
        merged = [h for h in merged if h["score"] >= min_score]
        all_hits.extend([h["row"] for h in merged])

    # 3.5) 중복 제거
    uniq, seen = [], set()
    for r in all_hits:
        key = (
            r.get("판례정보일련번호") or r.get("id") or "",
            r.get("path", ""),
            r.get("section") or "",
            (r.get("text", "") or "")[:96],
        )
        if key in seen:
            continue
        seen.add(key); uniq.append(r)

    # 4) 리랭크
    uniq = rerank_hits(query=claim, rows=uniq, alpha=alpha)
    ctxs = ensure_min_mix(uniq, min_cases=4, min_laws=2, max_total=final_k)

    # 5) 휴리스틱
    ctx_snips = [c.get("text", "") for c in ctxs]
    gaps_from_heur = spot_fact_mismatch(opponent_text, ctx_snips)

    # 6) 프롬프트 구성 (★ 길이 하드캡)
    contexts_text = build_context_lines(ctxs, per_item_chars=per_item_chars)
    if len(contexts_text) > max_ctx_chars:
        contexts_text = contexts_text[:max_ctx_chars] + "…(trimmed)"

    sys_msg = SYSTEM_TMPL
    user_msg = USER_TMPL.format(
        claim=claim,
        case_refs=", ".join(cites.get("case_nos") or []) or "-",
        law_refs=", ".join(cites.get("laws") or []) or "-",
        contexts=contexts_text
    )

    # 7) LLM
    tok, mdl = load_llm_local_first(str(llm_path))
    # pad/eos 안전 설정
    if tok.pad_token_id is None and tok.eos_token_id is not None:
        tok.pad_token_id = tok.eos_token_id
    eot_id = tok.convert_tokens_to_ids("<|eot_id|>")
    eos_id = eot_id if (eot_id is not None and eot_id != tok.unk_token_id) else tok.eos_token_id

    try:
        inputs = tok.apply_chat_template(
            [{"role": "system", "content": sys_msg},
             {"role": "user", "content": user_msg}],
            return_tensors="pt", add_generation_prompt=True
        ).to(mdl.device)
        out = mdl.generate(
            inputs,
            max_new_tokens=max_new_tokens,
            do_sample=False,
            eos_token_id=eos_id,
            pad_token_id=tok.pad_token_id,
        )
        gen_ids = out[0][inputs.shape[1]:]
    except Exception:
        prompt = sys_msg + "\n\n" + user_msg + "\n\n"
        enc = tok(prompt, return_tensors="pt").to(mdl.device)
        out = mdl.generate(
            **enc,
            max_new_tokens=max_new_tokens,
            do_sample=False,
            eos_token_id=eos_id,
            pad_token_id=tok.pad_token_id,
        )
        gen_ids = out[0][enc["input_ids"].shape[1]:]

    text = tok.decode(gen_ids, skip_special_tokens=True).strip()
    text = postprocess_answer(text)

    # 8) JSON 파싱(fallback)
    try:
        obj = json.loads(text)
    except Exception:
        obj = {
            "logical_gaps": gaps_from_heur or ["컨텍스트 기반으로 추가 확인 필요"],
            "counter_points": [text],
            "supports": [],
            "followups": []
        }

    if gaps_from_heur:
        obj["logical_gaps"] = list(dict.fromkeys((obj.get("logical_gaps") or []) + gaps_from_heur))

    # 9) 소스 요약
    sources = []
    for c in ctxs:
        if c.get("section"):
            court = c.get("법원명", "") or c.get("court", "")
            date  = c.get("선고일자", "") or c.get("date", "")
            if len(date) == 8:
                date = f"{date[:4]}-{date[4:6]}-{date[6:]}"
            label = f"{court} {date} {c.get('사건번호','') or c.get('case_no','')} [{c.get('section','')}]"
            sources.append({"type": "case", "label": label})
        else:
            art = c.get("article_no")
            ref = f"제{art}조" if art else (c.get("title", "") or "")
            sources.append({"type": "law", "label": f"{c.get('law','법령')} {ref}"})

    return {"analysis": obj, "sources": sources}