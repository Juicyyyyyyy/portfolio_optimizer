from collections import OrderedDict
import customtkinter

from PortfolioOptimizer.EfficientFrontierCalculator import EfficientFrontierCalculator


class EfficientFrontierPage(customtkinter.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.label_weights_raw = None
        self.label_dollar = None
        self.portfolio_size = None
        self.tickers_df = None
        self.tickers_list = None
        self.start_date = None
        self.end_date = None
        self.controller = controller

        # Title Label
        self.label_title = customtkinter.CTkLabel(self, text="Efficient Frontier Parameters", font=("Roboto Medium", -16))
        self.label_title.pack(pady=10)

        self.label_choose_expected_return_calculator = customtkinter.CTkLabel(self, text="Choose expected return calculator")
        self.label_choose_expected_return_calculator.pack(pady=2)
        self.models_expected_return_calculator = ["capm", "mean historical return"]
        self.optionmenu_expected_return_calculator = customtkinter.CTkOptionMenu(self, values=self.models_expected_return_calculator)
        self.optionmenu_expected_return_calculator.pack(pady=2)

        # Button to proceed with the analysis
        self.analyze_button = customtkinter.CTkButton(self, text="Analyze", command=self.analyze)
        self.analyze_button.pack(pady=20)

        self.label_weights = customtkinter.CTkLabel(self, text="Weights%:")
        self.label_weights.pack(pady=2)

        self.label_weights_raw = customtkinter.CTkLabel(self, text="Weights$:")
        self.label_weights_raw.pack(pady=2)

        self.label_expected_return = customtkinter.CTkLabel(self, text="Expected Return:")
        self.label_expected_return.pack(pady=2)

        self.label_volatility = customtkinter.CTkLabel(self, text="Volatility:")
        self.label_volatility.pack(pady=2)
        
    def fetch_home_page_data(self):
        self.start_date = self.controller.get_home_page_start_date()
        self.end_date = self.controller.get_home_page_end_date()
        self.tickers_list = self.controller.get_home_page_tickers_list()
        self.tickers_df = self.controller.get_home_page_tickers_df()
        self.portfolio_size = self.controller.get_home_page_portfolio_value()

    def analyze(self):
        self.fetch_home_page_data()
        chosen_expected_return_calculator = self.optionmenu_expected_return_calculator.get()
        efficient_frontier_calculator = EfficientFrontierCalculator(self.tickers_df, chosen_expected_return_calculator)

        weights = efficient_frontier_calculator.calculate_efficient_frontier_weights()

        filtered_weights = OrderedDict((key, value) for key, value in weights.items() if value != 0)
        filtered_weights_string_percent = ", ".join([f"{key}: {value * 100:.2f}%" for key, value in filtered_weights.items()])

        dollar_sizes = {key: value * self.portfolio_size for key, value in filtered_weights.items()}
        filtered_dollar_sizes_string = ", ".join([f"{key}: ${value:.2f}" for key, value in dollar_sizes.items()])

        expected_return, volatility, sharpe_ratio = efficient_frontier_calculator.calculate_efficient_frontier_performance()

        expected_return_percent, volatility_percent = expected_return*100, volatility*100

        # Display the results
        self.label_weights.configure(text=f"Weights percent: {filtered_weights_string_percent}")
        self.label_weights_raw.configure(text=f"Weights raw: {filtered_dollar_sizes_string}$")
        self.label_expected_return.configure(text=f"Expected Return: {round(expected_return_percent, 2)}% per Year")
        self.label_volatility.configure(text=f"Volatility: {round(volatility_percent, 2)}% per Year")
