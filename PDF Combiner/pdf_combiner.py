import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PyPDF2 import PdfMerger

class PDFCombinerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("PDF Combiner")
        self.master.geometry("400x400")

        self.pdf_files = []

        # Create and pack widgets
        self.file_listbox = tk.Listbox(self.master, selectmode=tk.MULTIPLE)
        self.file_listbox.pack(pady=10, padx=10, expand=True, fill=tk.BOTH)

        add_button = ttk.Button(self.master, text="Add PDFs", command=self.add_pdfs)
        add_button.pack(pady=5)

        remove_button = ttk.Button(self.master, text="Remove Selected", command=self.remove_selected)
        remove_button.pack(pady=5)

        combine_button = ttk.Button(self.master, text="Combine PDFs", command=self.combine_pdfs)
        combine_button.pack(pady=5)

    def add_pdfs(self):
        files = filedialog.askopenfilenames(filetypes=[("PDF Files", "*.pdf")])
        self.pdf_files.extend(files)
        for file in files:
            self.file_listbox.insert(tk.END, file)

    def remove_selected(self):
        selected_indices = self.file_listbox.curselection()
        for index in reversed(selected_indices):
            self.pdf_files.pop(index)
            self.file_listbox.delete(index)

    def combine_pdfs(self):
        if not self.pdf_files:
            messagebox.showwarning("No PDFs", "Please add PDF files to combine.")
            return

        output_file = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
        if not output_file:
            return

        merger = PdfMerger()
        for pdf in self.pdf_files:
            merger.append(pdf)

        merger.write(output_file)
        merger.close()

        messagebox.showinfo("Success", f"PDFs combined and saved as {output_file}")
        self.pdf_files.clear()
        self.file_listbox.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFCombinerApp(root)
    root.mainloop()
