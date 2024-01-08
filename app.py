import tkinter
import customtkinter
import importlib
import os

# Set appearance and color theme
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

class PortfolioOptimizerApp(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Configure window
        self.title("Portfolio Optimizer")
        self.geometry("1000x600")

        # Container for all the pages
        container = customtkinter.CTkFrame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        # Dynamically load all pages from the 'pages' directory
        pages_path = "./views"  # Adjust this path if necessary
        for filename in os.listdir(pages_path):
            if filename.endswith(".py") and not filename.startswith("__"):
                # Format module name for import
                module_name = f"views.{filename[:-3]}"  # Remove '.py' from file name
                # Import the module
                page_module = importlib.import_module(module_name)
                # Get the class (assuming class name is the same as file name)
                class_name = filename[:-3]
                page_class = getattr(page_module, class_name)
                # Initialize the page and add to frames
                frame = page_class(parent=container, controller=self)
                self.frames[class_name] = frame
                frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Home")  # or the name of the default page you want to show first

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

if __name__ == "__main__":
    app = PortfolioOptimizerApp()
    app.mainloop()
