from PortfolioOptimizer.GptBasedFunctions import GptBasedFunctions
from app import PortfolioOptimizerApp

from datetime import datetime, timedelta
import customtkinter
from tkcalendar import DateEntry


class Home(customtkinter.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.ticker_data = None
        self.gpt = GptBasedFunctions()

        # Divide the main frame into two columns
        self.column1 = customtkinter.CTkFrame(self)
        self.column2 = customtkinter.CTkFrame(self)

        self.column1.pack(side="left", fill="both", expand=True)
        self.column2.pack(side="right", fill="both", expand=True)

        # Title Label with updated font in column 1
        self.label_title = customtkinter.CTkLabel(self.column1, text="Tickers", font=("Roboto Medium", -16))
        self.label_title.pack(pady=20)

        # Radio Buttons for User Choice with modern design in column 1
        self.user_choice = customtkinter.StringVar(value="manual")
        self.rb_manual = customtkinter.CTkRadioButton(self.column1, text="Enter Tickers Manually", variable=self.user_choice,
                                                      value="manual", command=self.update_ui)
        self.rb_manual.pack(pady=2)
        self.rb_ai = customtkinter.CTkRadioButton(self.column1, text="Generate Tickers by AI", variable=self.user_choice,
                                                  value="ai", command=self.update_ui)
        self.rb_ai.pack(pady=2)

        # Entry for financial tickers with modern placeholder in column 1
        self.entry_tickers = customtkinter.CTkEntry(self.column1, width=200, placeholder_text="Enter tickers e.g., AAPL, GOOGL, AMZN")
        self.entry_tickers.pack(pady=2)  # Adjust as necessary for initial visibility

        # AI Generation Parameters (initially hidden) in column 1
        self.ai_frame = customtkinter.CTkFrame(self.column1)
        self.label_risk_tolerance = customtkinter.CTkLabel(self.ai_frame, text="Risk Tolerance (high, moderate, low):")
        self.entry_risk_tolerance = customtkinter.CTkEntry(self.ai_frame, width=200, placeholder_text="high")
        self.label_investment_area = customtkinter.CTkLabel(self.ai_frame, text="Investment Area (tech, commodities, ...):")
        self.entry_investment_area = customtkinter.CTkEntry(self.ai_frame, width=200, placeholder_text="tech")
        self.label_investment_timeframe = customtkinter.CTkLabel(self.ai_frame, text="Investment Timeframe (short term, long term):")
        self.entry_investment_timeframe = customtkinter.CTkEntry(self.ai_frame, width=200, placeholder_text="long term")
        self.generate_button = customtkinter.CTkButton(self.ai_frame, text="Generate", command=self.generate_tickers)

        self.ticker_display = customtkinter.CTkLabel(self.ai_frame, text="Generated Tickers will appear here", wraplength=500)

        self.label_risk_tolerance.pack(pady=(10, 0))  # Add padding on top and bottom
        self.entry_risk_tolerance.pack(pady=(5, 0))  # pady(top_padding, bottom_padding)
        self.label_investment_area.pack(pady=(10, 0))
        self.entry_investment_area.pack(pady=(5, 0))
        self.label_investment_timeframe.pack(pady=(10, 0))
        self.entry_investment_timeframe.pack(pady=(5, 0))
        self.generate_button.pack(pady=(20, 10), padx=20)  # Increase padding around the button

        # Packing the AI-specific widgets into the frame
        self.label_risk_tolerance.pack()
        self.entry_risk_tolerance.pack()
        self.label_investment_area.pack()
        self.entry_investment_area.pack()
        self.label_investment_timeframe.pack()
        self.entry_investment_timeframe.pack()
        self.generate_button.pack()
        self.ticker_display.pack()

        self.label_title_2 = customtkinter.CTkLabel(self.column2, text="Parameters", font=("Roboto Medium", -16))
        self.label_title_2.pack(pady=20)

        # Elements for column 2: Date Pickers and Financial Model Options
        # Date Picker for Start Date in column 2

        ten_years_ago = datetime.now() - timedelta(days=365 * 10)

        self.label_start_date = customtkinter.CTkLabel(self.column2, text="Start Date:")
        self.label_start_date.pack(pady=2)
        self.start_date = DateEntry(self.column2, width=18, background='darkblue',
                                    foreground='white', borderwidth=2, year=ten_years_ago.year,
                                    month=ten_years_ago.month, day=ten_years_ago.day,
                                    state="readonly")
        self.start_date.pack(pady=2)

        # Date Picker for End Date in column 2
        self.label_end_date = customtkinter.CTkLabel(self.column2, text="End Date:")
        self.label_end_date.pack(pady=2)
        self.end_date = DateEntry(self.column2, width=18, background='darkblue', foreground='white', borderwidth=2,
                                  state="readonly")
        self.end_date.pack(pady=2)

        # Option Menu for Financial Model in column 2
        self.label_fin_model = customtkinter.CTkLabel(self.column2, text="Choose Financial Model:")
        self.label_fin_model.pack(pady=2)
        self.models = ["EfficientFrontier", "Black Litterman", "Monte Carlo"]
        self.optionmenu_fin_model = customtkinter.CTkOptionMenu(self.column2, values=self.models)
        self.optionmenu_fin_model.pack(pady=2)

        # Continue Button with enhanced style in column 2
        self.button_continue = customtkinter.CTkButton(self.column2, text="Continue", command=self.on_continue)
        self.button_continue.pack(pady=20)

        # Initially update UI based on default choice
        self.update_ui()

    def update_ui(self):
        choice = self.user_choice.get()
        if choice == "ai":
            self.ai_frame.pack(pady=10)  # Show the AI frame
            self.entry_tickers.pack_forget()  # Hide the manual entry field
        else:
            self.ai_frame.pack_forget()  # Hide the AI frame
            self.entry_tickers.pack(pady=2)  # Show the manual entry field

        # Ensure Continue button is always at the bottom of column 2
        self.button_continue.pack(pady=20)

    def generate_tickers(self):
        risk_tolerance = self.entry_risk_tolerance.get()
        investment_area = self.entry_investment_area.get()
        investment_timeframe = self.entry_investment_timeframe.get()

        generated_tickers = self.gpt.generate_tickers(risk_tolerance, investment_area, investment_timeframe)
        self.ticker_display.configure(text="Generated Tickers: " + ", ".join(generated_tickers))

    def on_continue(self):
        app = PortfolioOptimizerApp()
        choice = self.user_choice.get()
        if choice == "manual":
            self.ticker_data = self.entry_tickers.get()
        elif choice == "ai":
            self.ticker_data = self.ticker_display['text'].split(": ")[1]

        chosenModel = self.optionmenu_fin_model.get()
        app.show_frame(chosenModel)  # not working needs to be corrected

