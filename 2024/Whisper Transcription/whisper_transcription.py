import os
import tkinter as tk
from tkinter import filedialog
from openai import OpenAI
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Now you can access the environment variables using os.getenv()
openai_api_key = os.getenv('OPENAI_API_KEY')
input_dir = os.getenv('INPUT_DIR')
output_dir = os.getenv('OUTPUT_DIR')
# language = os.getenv('LANGUAGE')

# Initialize OpenAI client
client = OpenAI(
    api_key=openai_api_key
)

# Create directories if they don't exist
input_dir = Path("2024/Whisper Transcription") / input_dir
output_dir = Path("2024/Whisper Transcription") / output_dir
input_dir.mkdir(parents=True, exist_ok=True)
output_dir.mkdir(parents=True, exist_ok=True)

def select_file():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    file_path = filedialog.askopenfilename(
        initialdir=input_dir,
        title="Select audio file",
        filetypes=(
            ("Audio files", "*.mp3 *.m4a"),
            ("MP3 files", "*.mp3"),
            ("M4A files", "*.m4a"),
            ("All files", "*.*")
        )
    )
    return file_path

def transcribe_audio(file_path):
    with open(file_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model='whisper-1',
            file=audio_file,
            response_format="text"
        )
    return transcript

def save_transcript(transcript, original_filename):
    output_filename = f"{Path(original_filename).stem}_transcript.txt"
    output_path = output_dir / output_filename
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(transcript)
    return output_path

def main():
    print("Please select an audio file to transcribe.")
    file_path = select_file()
    
    if not file_path:
        print("No file selected. Exiting.")
        return
    
    print(f"Transcribing: {file_path}")
    transcript = transcribe_audio(file_path)
    
    output_path = save_transcript(transcript, Path(file_path).name)
    print(f"Transcription saved to: {output_path}")

if __name__ == "__main__":
    main()
