import tkinter
import customtkinter
from tkcalendar import DateEntry

# Set appearance and color theme
customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class PortfolioOptimizerApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # Configure window
        self.title("Portfolio Optimizer")
        self.geometry(f"{800}x{600}")

        # Title Label
        self.label_title = customtkinter.CTkLabel(self, text="Portfolio Optimizer", font=("Roboto Medium", -16))  # Use appropriate size
        self.label_title.pack(pady=20)

        # Entry for financial tickers
        self.label_tickers = customtkinter.CTkLabel(self, text="Enter Tickers (comma-separated):")
        self.label_tickers.pack(pady=2)
        self.entry_tickers = customtkinter.CTkEntry(self, width=200, placeholder_text="AAPL, GOOGL, AMZN")
        self.entry_tickers.pack(pady=2)

        # Date Picker for Start Date
        self.label_start_date = customtkinter.CTkLabel(self, text="Start Date:")
        self.label_start_date.pack(pady=2)
        self.start_date = DateEntry(self, width=18, background='darkblue', foreground='white', borderwidth=2)
        self.start_date.pack(pady=2)

        # Date Picker for End Date
        self.label_end_date = customtkinter.CTkLabel(self, text="End Date:")
        self.label_end_date.pack(pady=2)
        self.end_date = DateEntry(self, width=18, background='darkblue', foreground='white', borderwidth=2)
        self.end_date.pack(pady=2)

        # Option Menu for Financial Model
        self.label_fin_model = customtkinter.CTkLabel(self, text="Choose Financial Model:")
        self.label_fin_model.pack(pady=2)
        self.optionmenu_fin_model = customtkinter.CTkOptionMenu(self, values=["EfficientFrontier", "Black Litterman", "Monte Carlo"])
        self.optionmenu_fin_model.pack(pady=2)

        # Continue Button
        self.button_continue = customtkinter.CTkButton(self, text="Continue", command=self.on_continue)
        self.button_continue.pack(pady=20)

    def on_continue(self):
        # Functionality for what happens when continue is pressed
        ticker_data = self.entry_tickers.get()
        start_date = self.entry_start_date.get()
        end_date = self.entry_end_date.get()
        model_selected = self.optionmenu_fin_model.get()
        print(f"Optimizing portfolio with tickers {ticker_data}, from {start_date} to {end_date} using {model_selected} model.")
        # Proceed with processing the data and optimizing the portfolio

if __name__ == "__main__":
    app = PortfolioOptimizerApp()
    app.mainloop()
