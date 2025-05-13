# -*- coding: utf-8 -*-
import re
from typing import List, Dict

CASE_PAT = re.compile(r"(?:\d{2,4})(?:다|도|두|후|마|자)\d{3,6}")
LAW_PAT  = re.compile(r"(민법|형법|헌법|민사소송법|형사소송법|상표법|행정소송법|개발이익환수에관한법률|.*법)\s*제?\s*(\d+)\s*조(?:\s*제?\s*(\d+)\s*항)?")

def extract_citations(text: str):
    cases = list(set(CASE_PAT.findall(text)))
    laws  = list(set("".join(m[0]) if isinstance(m, tuple) else m for m in LAW_PAT.findall(text)))
    return {"case_nos": cases, "laws": laws}

def summarize_claim(text: str, max_len=200):
    # 아주 러프하게 핵심 주장 구간 추출(첫 단락/결론 문장 위주)
    s = text.strip().split("\n")[0]
    return (s[:max_len]+"…") if len(s) > max_len else s

KEY_FACTS = ["소음", "진동", "악취", "손해액", "불법행위", "과실", "인과관계",
             "야간", "지속성", "측정치", "공동주택", "관리주체", "입주자대표회의"]

def spot_fact_mismatch(op_text: str, ctx_snippets: List[str]) -> List[str]:
    found = []
    lower = op_text.lower()
    for k in KEY_FACTS:
        present_op   = (k in lower) or (k in op_text)
        present_ctx  = any((k in c or k in c.lower()) for c in ctx_snippets)
        if present_op and not present_ctx:
            found.append(f"상대가 강조한 '{k}' 요소에 대한 근거가 컨텍스트에서 확인되지 않음")
    return found