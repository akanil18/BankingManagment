#!/bin/bash
# Start llama-server with the fine-tuned Qwen model
# Requires llama.cpp to be installed and in PATH

llama-server \
  --model ./models/qwen-banking-q4_k_m.gguf \
  --host 127.0.0.1 \
  --port 8080 \
  --n-gpu-layers 35 \
  --ctx-size 2048 \
  --threads 8 \
  --chat-template chatml
