import tkinter as tk
from tkinter import filedialog, ttk
from pathlib import Path
import comtypes.client
import os

class PPTXtoPDFConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Powerpoint to PDF Converter")
        self.root.geometry("600x400")
        
        self.selected_files = []
        
        # Create main frame
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create and configure listbox to show selected files
        self.listbox_frame = ttk.Frame(self.main_frame)
        self.listbox_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.listbox = tk.Listbox(self.listbox_frame, width=70, height=15)
        self.listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Add scrollbar to listbox
        self.scrollbar = ttk.Scrollbar(self.listbox_frame, orient=tk.VERTICAL, command=self.listbox.yview)
        self.scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.listbox.configure(yscrollcommand=self.scrollbar.set)
        
        # Buttons
        self.add_button = ttk.Button(self.main_frame, text="Add Powerpoint Files", command=self.add_files)
        self.add_button.grid(row=1, column=0, pady=10, padx=5)
        
        self.convert_button = ttk.Button(self.main_frame, text="Convert to PDF", command=self.convert_files)
        self.convert_button.grid(row=1, column=1, pady=10, padx=5)
        
        # Status label
        self.status_label = ttk.Label(self.main_frame, text="")
        self.status_label.grid(row=2, column=0, columnspan=2, pady=5)

    def add_files(self):
        files = filedialog.askopenfilenames(
            title="Select PowerPoint files",
            filetypes=[("PowerPoint files", "*.pptx *.ppt")]
        )
        for file in files:
            if file not in self.selected_files:
                self.selected_files.append(file)
                self.listbox.insert(tk.END, Path(file).name)
        
    def convert_files(self):
        if not self.selected_files:
            self.status_label.config(text="Please select at least one PowerPoint file")
            return
            
        output_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            title="Save PDF as"
        )
        
        if output_path:
            try:
                powerpoint = comtypes.client.CreateObject("Powerpoint.Application")
                
                # Convert paths to absolute Windows paths
                first_file = str(Path(self.selected_files[0]).resolve())
                output_path = str(Path(output_path).resolve())
                
                pres = powerpoint.Presentations.Open(first_file)
                
                for pptx_path in self.selected_files[1:]:
                    abs_path = str(Path(pptx_path).resolve())
                    additional_pres = powerpoint.Presentations.Open(abs_path)
                    num_slides = additional_pres.Slides.Count
                    for i in range(1, num_slides + 1):
                        additional_pres.Slides(i).Copy()
                        pres.Slides.Paste()
                    additional_pres.Close()
                
                pres.SaveAs(output_path, 32)
                pres.Close()
                powerpoint.Quit()
                
                self.status_label.config(text="Conversion completed successfully!")
                
            except Exception as e:
                self.status_label.config(text=f"Error: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PPTXtoPDFConverter(root)
    root.mainloop()
