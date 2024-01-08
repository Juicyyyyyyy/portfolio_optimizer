import customtkinter
from tkcalendar import DateEntry
from PortfolioOptimizer.GptBasedFunctions import GptBasedFunctions


class Home(customtkinter.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.gpt = GptBasedFunctions()

        # Title Label
        self.label_title = customtkinter.CTkLabel(self, text="Portfolio Optimizer", font=("Roboto Medium", -16))
        self.label_title.pack(pady=20)

        # Radio Buttons for User Choice
        self.user_choice = customtkinter.StringVar(value="manual")
        self.rb_manual = customtkinter.CTkRadioButton(self, text="Enter Tickers Manually", variable=self.user_choice,
                                                      value="manual", command=self.update_ui)
        self.rb_manual.pack(pady=2)
        self.rb_ai = customtkinter.CTkRadioButton(self, text="Generate Tickers by AI", variable=self.user_choice,
                                                  value="ai", command=self.update_ui)
        self.rb_ai.pack(pady=2)

        # Entry for financial tickers
        self.entry_tickers = customtkinter.CTkEntry(self, width=200, placeholder_text="AAPL, GOOGL, AMZN")

        # AI Generation Parameters (initially hidden)
        self.ai_frame = customtkinter.CTkFrame(self)
        self.label_risk_tolerance = customtkinter.CTkLabel(self.ai_frame, text="Risk Tolerance (high, moderate, low):")
        self.entry_risk_tolerance = customtkinter.CTkEntry(self.ai_frame, width=200, placeholder_text="high")
        self.label_investment_area = customtkinter.CTkLabel(self.ai_frame,
                                                            text="Investment Area (tech, commodities, ...):")
        self.entry_investment_area = customtkinter.CTkEntry(self.ai_frame, width=200, placeholder_text="tech")
        self.label_investment_timeframe = customtkinter.CTkLabel(self.ai_frame,
                                                                 text="Investment Timeframe (short term, long term):")
        self.entry_investment_timeframe = customtkinter.CTkEntry(self.ai_frame, width=200, placeholder_text="long term")
        self.generate_button = customtkinter.CTkButton(self.ai_frame, text="Generate", command=self.generate_tickers)
        self.ticker_display = customtkinter.CTkLabel(self.ai_frame, text="Generated Tickers will appear here",
                                                     wraplength=500)

        # Packing the AI-specific widgets into the frame
        self.label_risk_tolerance.pack()
        self.entry_risk_tolerance.pack()
        self.label_investment_area.pack()
        self.entry_investment_area.pack()
        self.label_investment_timeframe.pack()
        self.entry_investment_timeframe.pack()
        self.generate_button.pack()
        self.ticker_display.pack()

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
        self.optionmenu_fin_model = customtkinter.CTkOptionMenu(self, values=["EfficientFrontier", "Black Litterman",
                                                                              "Monte Carlo"])
        self.optionmenu_fin_model.pack(pady=2)

        # Continue Button (for manual entry)
        self.button_continue = customtkinter.CTkButton(self, text="Continue", command=self.on_continue)

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

        # Ensure Continue button is always at the bottom
        self.button_continue.pack(pady=20)

    def generate_tickers(self):
        risk_tolerance = self.entry_risk_tolerance.get()
        investment_area = self.entry_investment_area.get()
        investment_timeframe = self.entry_investment_timeframe.get()

        generated_tickers = self.gpt.generate_tickers(risk_tolerance, investment_area, investment_timeframe)
        self.ticker_display.configure(text="Generated Tickers: " + ", ".join(generated_tickers))

    def on_continue(self):
        choice = self.user_choice.get()
        if choice == "manual":
            ticker_data = self.entry_tickers.get()
        elif choice == "ai":
            ticker_data = self.ticker_display['text'].split(": ")[1]
        print("Processing with tickers:", ticker_data)

