import gradio as gr
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import warnings

# print(torch.cuda.is_available())  # Should return True for GPU
# print(torch.__version__)  # Needs to be 2.0+

# Suppress warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning, module="transformers")

# Configure flash attention if available
if torch.cuda.is_available():
    torch.backends.cuda.enable_flash_sdp(True)
    torch.backends.cuda.enable_mem_efficient_sdp(True)

# Model configuration
MODEL_NAME = "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
TORCH_DTYPE = torch.float16 if DEVICE == "cuda" else torch.float32

# Load model with conversation capabilities
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    trust_remote_code=True,
    device_map="auto",
    torch_dtype=TORCH_DTYPE
).eval()

# Initialize tokenizer
tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME,
    trust_remote_code=True,
    use_fast=False
)
tokenizer.pad_token = tokenizer.eos_token

def format_conversation(history):
    """Convert Gradio history to DeepSeek's format"""
    return "\n".join([f"User: {entry[0]}\nAssistant: {entry[1]}" for entry in history])

def generate_response(message, history):
    try:
        conv_history = format_conversation(history)
        full_prompt = f"{conv_history}\nUser: {message}\nAssistant:" if history else f"User: {message}\nAssistant:"
        
        inputs = tokenizer(
            full_prompt,
            return_tensors="pt",
            truncation=True,
            max_length=40000 # Limit to ~40k tokens
        ).to(DEVICE)
        
        outputs = model.generate(
            **inputs,
            max_new_tokens=4096,  # Official benchmark uses 32k max
            temperature=0.7,
            top_p=0.9,
            repetition_penalty=1.1,
            do_sample=True,
            eos_token_id=tokenizer.eos_token_id,
            pad_token_id=tokenizer.eos_token_id
        )
        
        response = tokenizer.decode(
            outputs[0][inputs.input_ids.shape[1]:],
            skip_special_tokens=True
        ).strip()
        
        return response
    
    except Exception as e:
        return f"Error: {str(e)}"

# Create chat interface
chat_interface = gr.ChatInterface(
    fn=generate_response,
    title="DeepSeek-1.5B Chat",
    description="Conversational AI with DeepSeek-R1-Distill-Qwen-1.5B",
    examples=[
        ["Explain quantum computing in simple terms"],
        ["Write a Python function to reverse a string"],
        ["How does photosynthesis work?"]
    ]
)

if __name__ == "__main__":
    try:
        chat_interface.launch(
            server_name="localhost",
            server_port=7860,
            share=False
        )
    except KeyboardInterrupt:
        print("\nServer closed gracefully")
    finally:
        # Cleanup resources
        if torch.cuda.is_available():
            torch.cuda.empty_cache()


# Example Prompt:

# Please reason step by step, and put your final answer within \boxed{}.
# User: Create a Python function to calculate Fibonacci sequence with O(n) time complexity