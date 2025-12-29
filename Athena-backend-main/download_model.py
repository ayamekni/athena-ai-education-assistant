"""
Download Mistral-7B model with resume capability
"""
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from huggingface_hub import snapshot_download
import os

print("="*70)
print("🚀 Downloading Mistral-7B-Instruct-v0.2")
print("="*70)

# Check GPU
if torch.cuda.is_available():
    print(f"\n✅ GPU: {torch.cuda.get_device_name(0)}")
    print(f"✅ VRAM: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.2f} GB\n")
else:
    print("\n⚠️ No GPU detected - using CPU\n")

MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.2"

print("📥 Downloading model files...")
print("   This will download ~14GB of data")
print("   Download will resume if interrupted\n")

try:
    # Use snapshot_download for better resume support
    cache_dir = snapshot_download(
        repo_id=MODEL_NAME,
        resume_download=True,
        max_workers=4
    )
    
    print(f"\n✅ Model downloaded successfully!")
    print(f"   Cache location: {cache_dir}")
    
    # Try to load tokenizer to verify
    print("\n🔄 Verifying download by loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    print("✅ Tokenizer loaded successfully!")
    
    print("\n" + "="*70)
    print("✅ Download complete! You can now start the server.")
    print("="*70)
    
except KeyboardInterrupt:
    print("\n\n⚠️ Download interrupted by user")
    print("   Run this script again to resume download")
except Exception as e:
    print(f"\n\n❌ Error: {e}")
    print("   Run this script again to retry/resume download")
