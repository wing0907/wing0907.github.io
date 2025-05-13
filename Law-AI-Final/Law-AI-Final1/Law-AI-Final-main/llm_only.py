# llm_only.py
import argparse
from pathlib import Path
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

def load_llm(model_path: str):
    mp = Path(model_path)
    if not mp.exists():
        raise FileNotFoundError(f"모델 경로 없음: {mp}")
    print(f"🔗 로컬 Llama-3 모델 로드: {mp}")
    tok = AutoTokenizer.from_pretrained(str(mp), local_files_only=True)
    if tok.pad_token_id is None and tok.eos_token_id is not None:
        tok.pad_token_id = tok.eos_token_id
    model = AutoModelForCausalLM.from_pretrained(
        str(mp),
        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
        device_map="auto",
        local_files_only=True
    )
    return tok, model

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-q", "--query", required=True, help="질문 문장")
    ap.add_argument("--llm", default="models/Meta-Llama-3-8B", help="모델 경로")
    ap.add_argument("--max_new_tokens", type=int, default=512)
    args = ap.parse_args()

    tok, model = load_llm(args.llm)

    # 간단한 system/user 프롬프트 구성
    system_msg = "당신은 대한민국 법학 전문가입니다. 질문에 대해 명확하고 간결하게 한국어로 답하세요."
    user_msg = args.query

    # Llama-3 전용 프롬프트 형식 (chat template 없을 때 대비)
    prompt = (
        "<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n"
        f"{system_msg}\n"
        "<|eot_id|><|start_header_id|>user<|end_header_id|>\n"
        f"{user_msg}\n"
        "<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n"
    )

    inputs = tok(prompt, return_tensors="pt").to(model.device)

    out = model.generate(
        **inputs,
        max_new_tokens=args.max_new_tokens,
        do_sample=True,      # ← 샘플링 켜서 다양성 확보
        temperature=0.7,
        top_p=0.9,
        eos_token_id=tok.eos_token_id,
    )

    gen_ids = out[0][inputs["input_ids"].shape[1]:]
    answer = tok.decode(gen_ids, skip_special_tokens=True)
    print("\n=== ANSWER ===")
    print(answer.strip())

if __name__ == "__main__":
    main()