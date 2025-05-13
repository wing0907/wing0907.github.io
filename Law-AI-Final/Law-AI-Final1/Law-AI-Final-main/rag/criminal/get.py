import requests, json

OC = "peter.jaewoochang"      # 네 OC 값
mst = "270563"                # 형법 MST (문헌 기반)
efYd = "20250408"             # 시행일 (YYYYMMDD)

url = "https://www.law.go.kr/DRF/lawService.do"
params = {
    "OC": OC,
    "target": "law",
    "type": "JSON",
    "MST": mst,
    "efYd": efYd,
}
headers = {"User-Agent": "curl/8"}

r = requests.get(url, params=params, headers=headers, timeout=60)
r.raise_for_status()
res = r.json()

with open("criminal_code_full.json", "w", encoding="utf-8") as f:
    json.dump(res, f, ensure_ascii=False, indent=2)

print("형법 본문 JSON 저장 완료 → criminal_code_full.json")