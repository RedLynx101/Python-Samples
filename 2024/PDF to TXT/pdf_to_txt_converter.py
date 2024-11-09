import os
import PyPDF2
from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class PDFConverterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF to TXT Converter")
        self.root.geometry("600x400")
        
        # Create directories
        self.create_directories()
        
        # Create main frame
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create GUI elements
        self.create_widgets()
        
    def create_directories(self):
        """Create input and output directories if they don't exist."""
        Path("pdf_input").mkdir(exist_ok=True)
        Path("txt_output").mkdir(exist_ok=True)
        
    def create_widgets(self):
        # Single file conversion section
        ttk.Label(self.main_frame, text="Single File Conversion", font=('Helvetica', 12, 'bold')).grid(row=0, column=0, columnspan=2, pady=10)
        
        ttk.Button(self.main_frame, text="Select PDF File", command=self.convert_single_file).grid(row=1, column=0, columnspan=2, pady=5)
        
        # Batch conversion section
        ttk.Label(self.main_frame, text="Batch Conversion", font=('Helvetica', 12, 'bold')).grid(row=2, column=0, columnspan=2, pady=10)
        
        ttk.Label(self.main_frame, text="Input folder: pdf_input/").grid(row=3, column=0, columnspan=2)
        ttk.Label(self.main_frame, text="Output folder: txt_output/").grid(row=4, column=0, columnspan=2)
        
        ttk.Button(self.main_frame, text="Convert All PDFs in Input Folder", command=self.batch_convert).grid(row=5, column=0, columnspan=2, pady=5)
        
        # Status section
        ttk.Label(self.main_frame, text="Status:", font=('Helvetica', 10, 'bold')).grid(row=6, column=0, columnspan=2, pady=10)
        
        self.status_text = tk.Text(self.main_frame, height=10, width=50)
        self.status_text.grid(row=7, column=0, columnspan=2)
        
        # Add scrollbar to status text
        scrollbar = ttk.Scrollbar(self.main_frame, orient='vertical', command=self.status_text.yview)
        scrollbar.grid(row=7, column=2, sticky='ns')
        self.status_text['yscrollcommand'] = scrollbar.set
        
    def update_status(self, message):
        """Update status text widget with new message."""
        self.status_text.insert(tk.END, message + "\n")
        self.status_text.see(tk.END)
        self.root.update()

    def convert_pdf_to_txt(self, pdf_path, txt_path):
        """Convert a single PDF file to TXT format."""
        try:
            with open(pdf_path, 'rb') as pdf_file:
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text()
                
                with open(txt_path, 'w', encoding='utf-8') as txt_file:
                    txt_file.write(text)
            return True
        except Exception as e:
            self.update_status(f"Error converting {pdf_path}: {str(e)}")
            return False

    def convert_single_file(self):
        """Handle single file conversion."""
        pdf_file = filedialog.askopenfilename(
            title="Select PDF file",
            filetypes=[("PDF files", "*.pdf")]
        )
        
        if pdf_file:
            pdf_path = Path(pdf_file)
            txt_path = Path("txt_output") / f"{pdf_path.stem}.txt"
            
            self.update_status(f"Converting {pdf_path.name} to text...")
            if self.convert_pdf_to_txt(pdf_path, txt_path):
                self.update_status(f"Successfully converted {pdf_path.name} to {txt_path.name}")
                messagebox.showinfo("Success", f"File converted successfully!\nSaved as: {txt_path}")
            else:
                messagebox.showerror("Error", "Failed to convert file")

    def batch_convert(self):
        """Handle batch conversion of all PDFs in input folder."""
        pdf_files = list(Path("pdf_input").glob("*.pdf"))
        
        if not pdf_files:
            self.update_status("No PDF files found in pdf_input directory!")
            messagebox.showwarning("Warning", "No PDF files found in pdf_input directory!")
            return
        
        success_count = 0
        for pdf_path in pdf_files:
            txt_path = Path("txt_output") / f"{pdf_path.stem}.txt"
            
            self.update_status(f"Converting {pdf_path.name} to text...")
            if self.convert_pdf_to_txt(pdf_path, txt_path):
                self.update_status(f"Successfully converted {pdf_path.name} to {txt_path.name}")
                success_count += 1
            
        self.update_status(f"\nConversion complete! Successfully converted {success_count} of {len(pdf_files)} files.")
        messagebox.showinfo("Batch Conversion Complete", 
                          f"Successfully converted {success_count} of {len(pdf_files)} files.")

def main():
    root = tk.Tk()
    app = PDFConverterGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
