import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import json

class FileToGraphApp:
    def __init__(self, root):
        self.root = root
        self.root.title("VizFile")
        self.root.geometry("800x600")
        
        self.label = tk.Label(root, text="VizFile", padx=10, pady=10, font=("Verdana", 40))
        self.label.pack()

        self.label = tk.Label(root, text="Select a file type and load the file to generate a graph", padx=10, pady=10)
        self.label.pack()

        self.file_type = tk.StringVar(value="CSV")
        self.radio_csv = tk.Radiobutton(root, text="CSV", variable=self.file_type, value="CSV")
        self.radio_json = tk.Radiobutton(root, text="JSON", variable=self.file_type, value="JSON")
        self.radio_excel = tk.Radiobutton(root, text="Excel", variable=self.file_type, value="Excel")
        self.radio_csv.pack()
        self.radio_json.pack()
        self.radio_excel.pack()

        self.load_button = tk.Button(root, text="Load File", command=self.load_file)
        self.load_button.pack(pady=10)

        self.graph_type_label = tk.Label(root, text="Select Graph Type", padx=10, pady=10)
        self.graph_type_label.pack()

        self.graph_type = tk.StringVar(value="line")
        self.graph_line = tk.Radiobutton(root, text="Line", variable=self.graph_type, value="line")
        self.graph_bar = tk.Radiobutton(root, text="Bar", variable=self.graph_type, value="bar")
        self.graph_scatter = tk.Radiobutton(root, text="Scatter", variable=self.graph_type, value="scatter")
        self.graph_line.pack()
        self.graph_bar.pack()
        self.graph_scatter.pack()

        self.column_frame = tk.Frame(root)
        self.column_frame.pack(pady=10)

        self.column_label = tk.Label(self.column_frame, text="Select Columns for X and Y axes")
        self.column_label.pack()

        self.x_column_label = tk.Label(self.column_frame, text="X-axis Column")
        self.x_column_label.pack(side=tk.LEFT, padx=5)
        self.x_column_combo = ttk.Combobox(self.column_frame, state="readonly")
        self.x_column_combo.pack(side=tk.LEFT, padx=5)

        self.y_column_label = tk.Label(self.column_frame, text="Y-axis Column")
        self.y_column_label.pack(side=tk.LEFT, padx=5)
        self.y_column_combo = ttk.Combobox(self.column_frame, state="readonly")
        self.y_column_combo.pack(side=tk.LEFT, padx=5)

        self.generate_button = tk.Button(root, text="Generate Graph", command=self.generate_graph)
        self.generate_button.pack(pady=10)

        self.download_button = tk.Button(root, text="Download Graph", command=self.download_graph)
        self.download_button.pack(pady=10)

        self.canvas = None

    def load_file(self):
        file_type = self.file_type.get()
        try:
            if file_type == "CSV":
                file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
                if file_path:
                    self.data_frame = pd.read_csv(file_path)
            elif file_type == "JSON":
                file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
                if file_path:
                    with open(file_path, 'r') as file:
                        data = json.load(file)
                        self.data_frame = pd.json_normalize(data)
            elif file_type == "Excel":
                file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xls *.xlsx")])
                if file_path:
                    self.data_frame = pd.read_excel(file_path)

            if file_path:
                self.update_column_options()
            else:
                messagebox.showwarning("Warning", "No file selected")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file: {str(e)}")

    def update_column_options(self):
        if self.data_frame is not None:
            columns = self.data_frame.columns.tolist()
            self.x_column_combo['values'] = columns
            self.y_column_combo['values'] = columns

    def generate_graph(self):
        if self.data_frame is not None:
            x_column = self.x_column_combo.get()
            y_column = self.y_column_combo.get()
            graph_type = self.graph_type.get()
            
            if not x_column or not y_column:
                messagebox.showwarning("Warning", "Please select both X and Y columns")
                return

            try:
                fig, ax = plt.subplots(figsize=(6, 4))  # Reduced size of the graph

                if graph_type == "line":
                    self.data_frame.plot(kind='line', x=x_column, y=y_column, ax=ax)
                elif graph_type == "bar":
                    self.data_frame.plot(kind='bar', x=x_column, y=y_column, ax=ax)
                elif graph_type == "scatter":
                    self.data_frame.plot(kind='scatter', x=x_column, y=y_column, ax=ax)

                if self.canvas:
                    self.canvas.get_tk_widget().pack_forget()

                self.canvas = FigureCanvasTkAgg(fig, master=self.root)
                self.canvas.draw()
                self.canvas.get_tk_widget().pack()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to generate graph: {str(e)}")

    def download_graph(self):
        if self.canvas:
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
            if file_path:
                try:
                    self.canvas.figure.savefig(file_path)
                    messagebox.showinfo("Success", f"Graph saved as {file_path}")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to save graph: {str(e)}")
        else:
            messagebox.showwarning("Warning", "No graph to save")

if __name__ == "__main__":
    root = tk.Tk()
    app = FileToGraphApp(root)
    root.mainloop()