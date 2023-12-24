import customtkinter as ctk
import tkinter as tk
from PortfolioOptimizer.PortfolioOptimizer import PortfolioOptimizer
from ChatGPT.Prompt import Prompt
from ChatGPT.ApiGpt import GPT
import datetime

class ManageTickersApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Portfolio Optimizer")
        self.geometry("600x500")

        # Dropdown for User Risk Tolerance
        ctk.CTkLabel(self, text="Select Your Risk Tolerance:").pack(pady=10)
        self.risk_tolerance = ctk.StringVar()
        self.dropdown_risk = ctk.CTkOptionMenu(self, variable=self.risk_tolerance, values=["Low", "Moderate", "High"])
        self.risk_tolerance.set("Moderate")
        self.dropdown_risk.pack(pady=10)

        # Entry for User Investment Area
        ctk.CTkLabel(self, text="Enter Your Investment Area:").pack(pady=10)
        self.entry_investment_area = ctk.CTkEntry(self)
        self.entry_investment_area.pack(pady=10)

        # Dropdown for Investment Timeframe
        ctk.CTkLabel(self, text="Select Investment Timeframe:").pack(pady=10)
        self.investment_timeframe = ctk.StringVar()
        self.dropdown_timeframe = ctk.CTkOptionMenu(self, variable=self.investment_timeframe, values=["Short-Term",
                                                                                                      "Long-Term"])
        self.investment_timeframe.set("Long-Term")
        self.dropdown_timeframe.pack(pady=10)

        # Button to Validate and Calculate
        ctk.CTkButton(self, text="Validate and Calculate", command=self.validate_and_calculate).pack(pady=20)

        # Output Area
        self.output = ctk.CTkLabel(self, text="", wraplength=500)
        self.output.pack(pady=10)

if __name__ == "__main__":
    app = ManageTickersApp()
    app.mainloop()