# -*- coding: utf-8 -*-
# rag/parse_prec_detail.py
import re, html, xmltodict, json

def _untag(s: str) -> str:
    if not s:
        return ""
    s = html.unescape(s)
    s = re.sub(r"<br\s*/?>", "\n", s, flags=re.I)
    s = re.sub(r"<[^>]+>", " ", s)
    s = re.sub(r"\s+\n", "\n", s)
    s = re.sub(r"\n{3,}", "\n\n", s)
    s = re.sub(r"[ \t]+", " ", s)
    return s.strip()

def _norm_date(s: str) -> str:
    if not s: return ""
    s = s.strip().replace(".", "").replace("-", "")
    if re.fullmatch(r"\d{8}", s):
        return f"{s[:4]}-{s[4:6]}-{s[6:8]}"
    m = re.match(r"(\d{4})[.\-](\d{1,2})[.\-](\d{1,2})", s)
    if m:
        y, mo, d = m.groups()
        return f"{int(y):04d}-{int(mo):02d}-{int(d):02d}"
    return s

def _split_order_reason(full: str):
    if not full: return "", "", ""
    txt = _untag(full)
    pat = r"(?:^|\n)\s*【\s*(주문)\s*】|\s*【\s*(이유)\s*】"
    pos = []
    for m in re.finditer(pat, txt):
        label = "주문" if m.group(1) else ("이유" if m.group(2) else "")
        pos.append((m.start(), label))
    if not pos:
        return "", "", txt
    segments = []
    for i, (start, label) in enumerate(pos):
        end = pos[i+1][0] if i+1 < len(pos) else len(txt)
        segments.append((label, txt[start:end].strip()))
    order = "\n".join(seg for lab, seg in segments if lab == "주문")
    reason = "\n".join(seg for lab, seg in segments if lab == "이유")
    other = txt
    for _, seg in segments:
        other = other.replace(seg, "")
    return order.strip(), reason.strip(), other.strip()

def parse_prec_xml_to_labeled(xml_text: str) -> dict:
    d = xmltodict.parse(xml_text)
    root = d.get("PrecService", {}) or d  # 안전빵
    meta = {
        "prec_id"        : (root.get("판례정보일련번호") or "").strip(),
        "case_no"        : (root.get("사건번호") or "").strip(),
        "case_name"      : _untag(root.get("사건명")),
        "judgement_date" : _norm_date(root.get("선고일자") or ""),
        "judgement_type" : (root.get("판결유형") or "").strip(),
        "court"          : (root.get("법원명") or "").strip(),
        "court_code"     : (root.get("법원종류코드") or "").strip(),
    }
    sections = {
        "판시사항": _untag(root.get("판시사항")),
        "판결요지": _untag(root.get("판결요지")),
        "참조조문": _untag(root.get("참조조문")),
        "참조판례": _untag(root.get("참조판례")),
        "주문": "", "이유": "", "본문": ""
    }
    order, reason, other = _split_order_reason(root.get("판례내용") or "")
    sections["주문"] = order
    sections["이유"] = reason
    sections["본문"] = other
    parts = [sections["판시사항"], sections["판결요지"], sections["주문"], sections["이유"]]
    fulltext = "\n\n".join([p for p in parts if p]).strip()
    return {"source":"case","meta":meta,"sections":sections,"fulltext":fulltext}

def parse_prec_json_to_labeled(json_text: str) -> dict:
    data = json.loads(json_text)
    root = data.get("PrecService", {}) or data
    # DRF JSON은 키가 XML과 동일한 한글 키로 내려온다.
    meta = {
        "prec_id"        : (root.get("판례정보일련번호") or "").strip(),
        "case_no"        : (root.get("사건번호") or "").strip(),
        "case_name"      : _untag(root.get("사건명")),
        "judgement_date" : _norm_date(root.get("선고일자") or ""),
        "judgement_type" : (root.get("판결유형") or "").strip(),
        "court"          : (root.get("법원명") or "").strip(),
        "court_code"     : (root.get("법원종류코드") or "").strip(),
    }
    sections = {
        "판시사항": _untag(root.get("판시사항")),
        "판결요지": _untag(root.get("판결요지")),
        "참조조문": _untag(root.get("참조조문")),
        "참조판례": _untag(root.get("참조판례")),
        "주문": "", "이유": "", "본문": ""
    }
    order, reason, other = _split_order_reason(root.get("판례내용") or "")
    sections["주문"] = order
    sections["이유"] = reason
    sections["본문"] = other
    parts = [sections["판시사항"], sections["판결요지"], sections["주문"], sections["이유"]]
    fulltext = "\n\n".join([p for p in parts if p]).strip()
    return {"source":"case","meta":meta,"sections":sections,"fulltext":fulltext}