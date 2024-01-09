import tkinter
import customtkinter
import importlib
import os

# Set appearance and color theme
customtkinter.set_appearance_mode("System")  # Consider allowing users to toggle between light and dark mode
customtkinter.set_default_color_theme("blue")


class PortfolioOptimizerApp(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Configure window
        self.title("Portfolio Optimizer")
        self.geometry("800x500")

        # Container for all the pages
        container = customtkinter.CTkFrame(self)
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

        self.show_frame("Home")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


if __name__ == "__main__":
    app = PortfolioOptimizerApp()
    app.mainloop()
