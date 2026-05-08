"""
Merge LoRA adapter into base model and export as GGUF for llama-server.
Run: python export/export_gguf.py
"""
import os
from dotenv import load_dotenv
from unsloth import FastLanguageModel

load_dotenv()

LORA_DIR = os.getenv("OUTPUT_DIR", "../output/qwen-banking-lora")
MERGED_DIR = os.getenv("MERGED_MODEL_DIR", "../output/qwen-banking-merged")
GGUF_DIR = os.getenv("GGUF_OUTPUT_DIR", "../../ai-server/models")
QUANT = os.getenv("GGUF_QUANTIZATION", "Q4_K_M")

os.makedirs(MERGED_DIR, exist_ok=True)
os.makedirs(GGUF_DIR, exist_ok=True)


def main():
    print(f"Loading LoRA model from {LORA_DIR}...")
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name=LORA_DIR,
        max_seq_length=2048,
        dtype=None,
        load_in_4bit=True,
    )

    print(f"Saving merged model to {MERGED_DIR}...")
    model.save_pretrained_merged(MERGED_DIR, tokenizer, save_method="merged_16bit")

    print(f"Exporting GGUF ({QUANT}) to {GGUF_DIR}...")
    model.save_pretrained_gguf(GGUF_DIR, tokenizer, quantization_method=QUANT)
    print("Export complete!")
    print(f"GGUF file: {GGUF_DIR}/qwen-banking-{QUANT.lower()}.gguf")


if __name__ == "__main__":
    main()
