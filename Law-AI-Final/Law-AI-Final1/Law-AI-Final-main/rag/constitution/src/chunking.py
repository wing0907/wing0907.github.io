# import requests
# import json

# OC = "peter.jaewoochang"  # 네 OC 값

# # 헌법 MST와 시행일자
# mst = "61603"
# efYd = "19880225"

# url = "http://www.law.go.kr/DRF/lawService.do"
# params = {
#     "OC": OC,
#     "target": "law",
#     "type": "JSON",   # JSON 형태로 받기
#     "MST": mst,
#     "efYd": efYd,
# }

# headers = {"User-Agent": "curl/8"}
# r = requests.get(url, params=params, headers=headers, timeout=60)
# r.raise_for_status()

# res = r.json()

# # 결과 저장
# out_path = "constitution_full.json"
# with open(out_path, "w", encoding="utf-8") as f:
#     json.dump(res, f, ensure_ascii=False, indent=2)

# print(f"헌법 본문 JSON 저장 완료 → {out_path}")

import requests
import json

OC = "peter.jaewoochang"   # 네 OC 값
mst = "265307"             # 민법 MST
efYd = "20250131"          # 시행일자

url = "https://www.law.go.kr/DRF/lawService.do"
params = {
    "OC": OC,
    "target": "law",
    "type": "JSON",   # JSON 형태로 받기
    "MST": mst,
    "efYd": efYd,
}

headers = {"User-Agent": "curl/8"}
r = requests.get(url, params=params, headers=headers, timeout=60)
r.raise_for_status()

res = r.json()

# 결과 저장
out_path = "civil_code_full.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(res, f, ensure_ascii=False, indent=2)

print(f"민법 본문 JSON 저장 완료 → {out_path}")