import torch

print("torch: CUDA available:", torch.cuda.is_available())
print("torch: CUDA device count:", torch.cuda.device_count())
