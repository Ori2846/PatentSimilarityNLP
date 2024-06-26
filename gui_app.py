import tkinter as tk
from tkinter import messagebox
import requests
import threading
from patent_similarity_app import PatentSimilarityApp


class PatentSimilarityGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Patent Similarity Detection")
        self.root.geometry("600x400")

        self.label = tk.Label(root, text="Enter Patent Abstract:", font=("Arial", 14))
        self.label.pack(pady=10)

        self.text_area = tk.Text(root, wrap='word', height=10)
        self.text_area.pack(pady=10)

        self.submit_button = tk.Button(root, text="Check Similarity", command=self.check_similarity)
        self.submit_button.pack(pady=10)

        self.result_area = tk.Text(root, wrap='word', height=10, state='disabled')
        self.result_area.pack(pady=10)

        self.start_flask_app()

    def start_flask_app(self):
        self.flask_thread = threading.Thread(target=self.run_flask_app)
        self.flask_thread.daemon = True
        self.flask_thread.start()

    def run_flask_app(self):
        app = PatentSimilarityApp()
        initial_patent_numbers = ['US11888042B2', 'US8765432B2']
        for pn in initial_patent_numbers:
            data = app.fetch_patent_data(pn)
            if data:
                app.save_patent_data(data)
        app.run()

    def check_similarity(self):
        abstract_text = self.text_area.get("1.0", tk.END).strip()
        if not abstract_text:
            messagebox.showwarning("Input Error", "Please enter a patent abstract.")
            return

        data = {"query": abstract_text}
        try:
            response = requests.post("http://127.0.0.1:5000/similarity", json=data)
            response.raise_for_status()
            similarities = response.json()
            self.display_results(similarities)
        except requests.RequestException as e:
            messagebox.showerror("API Error", f"Failed to get similarity scores: {e}")

    def display_results(self, similarities):
        self.result_area.config(state='normal')
        self.result_area.delete("1.0", tk.END)
        for similarity in similarities:
            result_text = f"Patent Number: {similarity['patent_number']}\nSimilarity: {similarity['similarity']:.4f}\n\n"
            self.result_area.insert(tk.END, result_text)
        self.result_area.config(state='disabled')


if __name__ == "__main__":
    root = tk.Tk()
    gui = PatentSimilarityGUI(root)
    root.mainloop()