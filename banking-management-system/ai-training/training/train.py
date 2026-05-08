"""
Fine-tune Qwen2.5-1.5B using Unsloth + QLoRA.
Run inside conda banking-ai env:
  python training/train.py
"""
import os
import yaml
from dotenv import load_dotenv
from datasets import load_dataset
from unsloth import FastLanguageModel
from trl import SFTTrainer
from transformers import TrainingArguments

load_dotenv()

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.yaml")
with open(CONFIG_PATH) as f:
    cfg = yaml.safe_load(f)

BASE_DIR = os.path.dirname(__file__)


def main():
    # Load model with Unsloth
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name=cfg["model"]["name"],
        max_seq_length=cfg["model"]["max_seq_length"],
        dtype=cfg["model"]["dtype"],
        load_in_4bit=cfg["model"]["load_in_4bit"],
        token=os.getenv("HF_TOKEN"),
    )

    # Apply QLoRA adapters
    model = FastLanguageModel.get_peft_model(
        model,
        r=cfg["lora"]["r"],
        lora_alpha=cfg["lora"]["alpha"],
        lora_dropout=cfg["lora"]["dropout"],
        target_modules=cfg["lora"]["target_modules"],
        use_gradient_checkpointing="unsloth",
        random_state=42,
    )

    # Load datasets
    train_path = os.path.join(BASE_DIR, cfg["data"]["train_file"])
    eval_path = os.path.join(BASE_DIR, cfg["data"]["eval_file"])
    train_ds = load_dataset("json", data_files=train_path, split="train")
    eval_ds = load_dataset("json", data_files=eval_path, split="train")

    print(f"Train: {len(train_ds)} | Eval: {len(eval_ds)}")

    t = cfg["training"]
    output_dir = os.path.join(BASE_DIR, t["output_dir"])

    trainer = SFTTrainer(
        model=model,
        tokenizer=tokenizer,
        train_dataset=train_ds,
        eval_dataset=eval_ds,
        dataset_text_field=cfg["data"]["dataset_text_field"],
        max_seq_length=cfg["model"]["max_seq_length"],
        args=TrainingArguments(
            output_dir=output_dir,
            per_device_train_batch_size=t["per_device_train_batch_size"],
            gradient_accumulation_steps=t["gradient_accumulation_steps"],
            learning_rate=t["learning_rate"],
            num_train_epochs=t["num_train_epochs"],
            warmup_ratio=t["warmup_ratio"],
            lr_scheduler_type=t["lr_scheduler_type"],
            fp16=t["fp16"],
            bf16=t["bf16"],
            logging_steps=t["logging_steps"],
            save_steps=t["save_steps"],
            eval_steps=t["eval_steps"],
            evaluation_strategy=t["evaluation_strategy"],
            save_total_limit=t["save_total_limit"],
            load_best_model_at_end=t["load_best_model_at_end"],
            report_to=t["report_to"],
        ),
    )

    print("Starting training...")
    trainer.train()
    print(f"Training complete. Model saved to {output_dir}")


if __name__ == "__main__":
    main()
