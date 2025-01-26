import gradio as gr
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# print(torch.cuda.is_available())  # Should return True
# print(torch.__version__)  # Needs to be 2.0+

# Add these to generation config
torch.backends.cuda.enable_flash_sdp(True)
torch.backends.cuda.enable_mem_efficient_sdp(True)

# Configuration
MODEL_NAME = "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
TORCH_DTYPE = torch.float16 if DEVICE == "cuda" else torch.float32

# Remove flash_attention_2 from model loading
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    trust_remote_code=True,  # Required for DeepSeek models
    device_map="auto",
    torch_dtype=TORCH_DTYPE
)

# Set padding token properly
tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME,
    trust_remote_code=True,  # Required
    use_fast=False  # Essential for compatibility
)
tokenizer.pad_token = tokenizer.eos_token

def generate_response(prompt):
    try:
        inputs = tokenizer(prompt, return_tensors="pt").to(DEVICE)
        
        # Generation parameters
        outputs = model.generate(
            **inputs,
            max_new_tokens=2048,  # Reduce from 3000 (official benchmark uses 32k max)
            temperature=0.6,       # Strictly recommended range: 0.5-0.7
            top_p=0.95,
            do_sample=True,
            eos_token_id=tokenizer.eos_token_id,
            pad_token_id=tokenizer.eos_token_id,
            repetition_penalty=1.1  # Add to prevent looping
        )
        
        # Clean decoding
        response = tokenizer.decode(
            outputs[0][inputs.input_ids.shape[1]:], 
            skip_special_tokens=True
        )
        return response.strip()
    
    except Exception as e:
        return f"Error: {str(e)}"

# Create interface
iface = gr.Interface(
    fn=generate_response,
    inputs=gr.Textbox(label="Input Prompt", lines=3),
    outputs=gr.Textbox(label="Model Response", lines=5),
    title="DeepSeek-1.5B Chat",
    allow_flagging="never"
)

if __name__ == "__main__":
    iface.launch(
        server_name="localhost",
        server_port=7860,
        share=False
    )


# Example Prompt:

# Please reason step by step, and put your final answer within \boxed{}.
# User: Create a Python function to calculate Fibonacci sequence with O(n) time complexity