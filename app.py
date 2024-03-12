import tkinter as tk
from tkinter import ttk
import importlib
import os

import sv_ttk

class PortfolioOptimizerApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Configure window
        self.title("Portfolio Optimizer")
        self.geometry("800x500")

        # Container for all the pages
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        # Dynamically load all pages from the 'pages' directory
        pages_path = "./views"
        for filename in os.listdir(pages_path):
            if filename.endswith(".py") and not filename.startswith("__"):
                module_name = f"views.{filename[:-3]}"
                page_module = importlib.import_module(module_name)
                class_name = filename[:-3]
                page_class = getattr(page_module, class_name)
                frame = page_class(parent=container, controller=self)
                self.frames[class_name] = frame
                frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("HomePage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

if __name__ == "__main__":
    app = PortfolioOptimizerApp()
    app.mainloop()
