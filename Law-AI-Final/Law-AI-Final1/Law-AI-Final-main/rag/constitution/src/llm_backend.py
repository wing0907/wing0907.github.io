# rag/llm_backend.py
import os
from pathlib import Path
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

ROOT = Path(__file__).resolve().parents[1]  # Kings_final_project/
DEFAULT_MODEL_DIR = ROOT / "models" / "Meta-Llama-3-8B"  # 화면에 보인 경로

class TransformersLLM:
    def __init__(self, model_name_or_path=None, load_in_8bit=False):
        # 우선순위: 인자 > env LLM_MODEL > 기본 로컬 디렉토리
        self.model_name = str(model_name_or_path or os.environ.get("LLM_MODEL", DEFAULT_MODEL_DIR))
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name, use_fast=True)
        kwargs = {}
        if load_in_8bit:
            kwargs["load_in_8bit"] = True
            kwargs["device_map"]   = "auto"
        else:
            kwargs["torch_dtype"]  = torch.float16 if torch.cuda.is_available() else torch.float32
            kwargs["device_map"]   = "auto"
        self.model = AutoModelForCausalLM.from_pretrained(self.model_name, **kwargs)

    def generate(self, prompt, max_new_tokens=512, temperature=0.2, top_p=0.9):
        tok = self.tokenizer
        inputs = tok(prompt, return_tensors="pt").to(self.model.device)
        out = self.model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=(temperature > 0),
            temperature=temperature,
            top_p=top_p,
            eos_token_id=tok.eos_token_id
        )
        return tok.decode(out[0], skip_special_tokens=True)

def get_llm(model_name_or_path=None):
    return TransformersLLM(model_name_or_path)