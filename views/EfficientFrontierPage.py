from PortfolioOptimizer.GptBasedFunctions import GptBasedFunctions
from app import PortfolioOptimizerApp

from datetime import datetime, timedelta
import customtkinter
from tkcalendar import DateEntry


class EfficientFrontierPage(customtkinter.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Title Label
        self.label_title = customtkinter.CTkLabel(self, text="Efficient Frontier Parameters", font=("Roboto Medium", -16))
        self.label_title.pack(pady=10)

