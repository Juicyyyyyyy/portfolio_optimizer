from PortfolioOptimizer.GptBasedFunctions import GptBasedFunctions
from PortfolioOptimizer.MarketDataProvider import MarketDataProvider

from collections import OrderedDict

from PortfolioOptimizer.EfficientFrontierCalculator import EfficientFrontierCalculator
from PortfolioOptimizer.GptBasedFunctions import GptBasedFunctions as gpt

import matplotlib.pyplot as plt
from xhtml2pdf import pisa

import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
from datetime import datetime, timedelta
import os



# Assuming the rest of your imports are correct and necessary for your application

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.gpt = GptBasedFunctions()

        self.column1 = tk.Frame(self)
        self.column2 = tk.Frame(self)
        self.column1.pack(side="left", fill="both", expand=True)
        self.column2.pack(side="right", fill="both", expand=True)

        self.label_title = tk.Label(self.column1, text="Tickers", font=("Roboto Medium", 16))
        self.label_title.pack(pady=20)

        self.user_choice = tk.StringVar(value="manual")
        self.rb_manual = ttk.Radiobutton(self.column1, text="Enter Tickers Manually", variable=self.user_choice,
                                         value="manual", command=self.update_ui)
        self.rb_manual.pack(pady=2)
        self.rb_ai = ttk.Radiobutton(self.column1, text="Generate Tickers by AI", variable=self.user_choice, value="ai",
                                     command=self.update_ui)
        self.rb_ai.pack(pady=10)

        self.entry_tickers = tk.Entry(self.column1)
        self.entry_tickers.pack(pady=2)

        self.ai_frame = tk.Frame(self.column1)

        self.label_risk_tolerance = tk.Label(self.ai_frame, text="Risk Tolerance:")
        # Define the options for risk tolerance
        self.risk_tolerance_options = ['high', 'moderate', 'low']
        self.risk_tolerance_combobox = ttk.Combobox(self.ai_frame, values=self.risk_tolerance_options, state='readonly')
        self.risk_tolerance_combobox.set('moderate')  # Set default value

        self.label_investment_area = tk.Label(self.ai_frame, text="Investment Area:")
        # Define the options for investment area
        self.investment_area_options = [
            'tech', 'commodities', 'finance', 'healthcare', 'energy',
            'consumer goods', 'real estate', 'utilities', 'telecommunications',
            'industrials', 'materials', 'biotechnology', 'pharmaceuticals', 'information technology',
            'consumer services', 'automotive', 'aerospace', 'defense', 'entertainment',
            'retail', 'agriculture', 'food & beverage', 'construction', 'education',
            'transportation', 'logistics', 'media', 'sports', 'renewable energy',
            'environmental services', 'government and public sector', 'non-profit and NGO', 'cryptocurrencies'
        ]
        self.investment_area_combobox = ttk.Combobox(self.ai_frame, values=self.investment_area_options,
                                                     state='readonly')
        self.investment_area_combobox.set('tech')  # Set default value

        self.label_investment_timeframe = tk.Label(self.ai_frame, text="Investment Timeframe:")
        # Define the options for investment timeframe
        self.investment_timeframe_options = ['short term', 'long term']
        self.investment_timeframe_combobox = ttk.Combobox(self.ai_frame, values=self.investment_timeframe_options,
                                                          state='readonly')
        self.investment_timeframe_combobox.set('long term')  # Set default value

        self.label_risk_tolerance.pack(pady=(10, 0))
        self.risk_tolerance_combobox.pack(pady=(5, 0))
        self.label_investment_area.pack(pady=(10, 0))
        self.investment_area_combobox.pack(pady=(5, 0))
        self.label_investment_timeframe.pack(pady=(10, 0))
        self.investment_timeframe_combobox.pack(pady=(5, 0))

        self.generate_button = tk.Button(self.ai_frame, text="Generate", command=self.generate_tickers)
        self.ticker_display = tk.Label(self.ai_frame, text="Generated Tickers will appear here", wraplength=400)

        self.label_risk_tolerance.pack(pady=(10, 0))
        self.label_investment_area.pack(pady=(10, 0))
        self.label_investment_timeframe.pack(pady=(10, 0))
        self.generate_button.pack(pady=(20, 10), padx=20)
        self.ticker_display.pack()

        self.ai_frame.pack_forget()  # Hide AI frame initially

        self.label_title_2 = tk.Label(self.column2, text="Parameters", font=("Roboto Medium", 16))
        self.label_title_2.pack(pady=20)

        # Load the image and keep a reference to it
        self.image = tk.PhotoImage(file="logo.png")  # Use self.image instead of image

        # Use the image in a label
        label = tk.Label(self.column2, image=self.image)  # Reference self.image here
        label.pack()

        ten_years_ago = datetime.now() - timedelta(days=365 * 10)
        self.label_start_date = tk.Label(self.column2, text="Start Date:")
        self.start_date = DateEntry(self.column2, width=18, borderwidth=2, year=ten_years_ago.year,
                                    month=ten_years_ago.month, day=ten_years_ago.day, state="readonly")
        self.label_end_date = tk.Label(self.column2, text="End Date:")
        self.end_date = DateEntry(self.column2, width=18, borderwidth=2, state="readonly")

        self.label_start_date.pack(pady=2)
        self.start_date.pack(pady=2)
        self.label_end_date.pack(pady=2)
        self.end_date.pack(pady=2)

        self.label_portfolio_size = tk.Label(self.column2, text="Choose your portfolio size in $:")
        self.portfolio_size_input = tk.Entry(self.column2)
        self.label_portfolio_size.pack(pady=2)
        self.portfolio_size_input.pack(pady=2)

        self.button_continue = tk.Button(self.column2, text="Continue", command=self.on_continue)
        self.button_continue.pack(pady=20)

        self.update_ui()

    def update_ui(self):
        if self.user_choice.get() == "ai":
            self.ai_frame.pack(pady=10)
            self.entry_tickers.pack_forget()
        else:
            self.ai_frame.pack_forget()
            self.entry_tickers.pack(pady=2)

    def generate_tickers(self):
        risk_tolerance = self.risk_tolerance_combobox.get()
        investment_area = self.investment_area_combobox.get()
        investment_timeframe = self.investment_timeframe_combobox.get()

        generated_tickers = self.gpt.generate_tickers(risk_tolerance, investment_area, investment_timeframe)
        self.ticker_display.configure(text="Generated Tickers: " + ", ".join(generated_tickers) + "\n" + "\n" + "If the generated tickers suit your needs, click Continue. Else, generate again or enter your tickers manually.")

    def download_data(self, tickers, start_date, end_date, return_updated_tickers: bool):
        return MarketDataProvider().get_data(tickers=tickers, start_date=start_date, end_date=end_date, return_updated_tickers=return_updated_tickers)

    def convert_html_to_pdf(self, html_string, pdf_path):
        with open(pdf_path, "wb") as pdf_file:
            pisa_status = pisa.CreatePDF(html_string, dest=pdf_file)

        return not pisa_status.err

    def analyze(self):

        efficient_frontier_calculator = EfficientFrontierCalculator(self.tickers_df)

        weights = efficient_frontier_calculator.calculate_efficient_frontier_weights()

        filtered_weights = OrderedDict((key, value) for key, value in weights.items() if value != 0)
        dollar_sizes = {key: value * self.portfolio_size for key, value in filtered_weights.items()}

        sorted_weights = OrderedDict(sorted(filtered_weights.items(), key=lambda x: x[1], reverse=True))
        sorted_dollar_sizes = OrderedDict(sorted(dollar_sizes.items(), key=lambda x: x[1], reverse=True))

        self.sorted_tickers_list = list(sorted_weights.keys())
        self.tickers_string = ' '.join(self.sorted_tickers_list)
        self.tickers_string = self.tickers_string.replace(" ", ", ")

        filtered_weights_string_percent = ", ".join(
            [f"{key}: {value * 100:.2f}%" for key, value in sorted_weights.items()])
        filtered_dollar_sizes_string = ", ".join([f"{key}: ${value:.2f}" for key, value in sorted_dollar_sizes.items()])

        expected_return, volatility, sharpe_ratio = efficient_frontier_calculator.calculate_efficient_frontier_performance()

        expected_return_percent, volatility_percent = expected_return * 100, volatility * 100

        # Create pie chart based on weights
        labels = sorted_dollar_sizes.keys()
        sizes = list(sorted_dollar_sizes.values())

        # Create a static Pie chart using Matplotlib
        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)

        # Equal aspect ratio ensures that the pie is drawn as a circle.
        ax.axis('equal')

        # Save the static pie chart as an image
        img_path = f"created_portfolios/{self.portfolio_id}/pie_chart.png"
        plt.savefig(img_path)

        ticker_reviews = gpt.generate_tickers_review(
            self.tickers_string)  # review of each ticker in markdown html format

        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Portfolio Analysis</title>
            <style>
                body {{
                    font-family: 'Arial', sans-serif;
                    line-height: 1.6;
                    margin: 20px;
                    max-width: 800px;
                    margin-left: auto;
                    margin-right: auto;
                    background-color: #f8f9fa;
                    color: #495057;
                }}

                h1 {{
                    font-size: 24px;
                    color: #007bff;
                    margin-bottom: 20px;
                }}

                h2 {{
                    font-size: 20px;
                    color: #007bff;
                    margin-bottom: 15px;
                }}

                img {{
                    max-width: 100%;
                    height: auto;
                    margin-bottom: 20px;
                }}

                p {{
                    font-size: 16px;
                    margin-bottom: 10px;
                    color: #000;
                }}

                strong {{
                    font-weight: bold;
                }}

                #ticker-reviews{{
                    font-size: 16px;
                    margin-bottom: 10px;
                    color: #000;
                }}
            </style>
        </head>
        <body>
            <h1>Portfolio Analysis</h1>
            <img src="{img_path}" alt="Portfolio Weights">
            <h2>Weights Percent</h2>
            <p><strong>{filtered_weights_string_percent}</strong></p>
            <h2>Weights Raw</h2>
            <p><strong>{filtered_dollar_sizes_string}</strong></p>
            <h2>Expected Return</h2>
            <p><strong>{round(expected_return_percent, 2)}% per Year</strong></p>
            <h2>Volatility</h2>
            <p><strong>{round(volatility_percent, 2)}% per Year</strong></p>
            <h2>Sharpe Ratio</h2>
            <p><strong>{round(sharpe_ratio, 4)}</strong></p>
            <h2>Ticker Reviews</h2>
            <p><strong id="ticker-reviews">{ticker_reviews}</strong></p>
        </body>
        </html>
        """

        # Convert HTML to PDF
        pdf_path = f"created_portfolios/{self.portfolio_id}/analysis.pdf"
        if self.convert_html_to_pdf(html_content, pdf_path):
            print(f"PDF generated and saved at {pdf_path}")

        # Display the saved PDF
        os.system(f"start {pdf_path}")

    def on_continue(self):
        messagebox.showinfo("Information", "The analysis may take a few minutes to complete. A browser window will open containing the analysis. Please don't close the app.")
        choice = self.user_choice.get()

        if choice == "manual":
            self.ticker_data = self.entry_tickers.get().strip()
            self.ticker_string = self.entry_tickers.get().strip()
        elif choice == "ai":
            generated_text = self.ticker_display.cget("text")
            self.ticker_data = generated_text.split(": ")[1] if ":" in generated_text else ""
            self.ticker_string = generated_text.split(": ")[1] if ":" in generated_text else ""

        # Check if ticker data is empty
        if not self.ticker_data:
            messagebox.showerror("Error", "Please enter or generate tickers before continuing.")
            return

        try:
            self.portfolio_size = float(self.portfolio_size_input.get())
        except ValueError:
            messagebox.showerror("Error", "Please ensure you enter a valid number for portfolio size.")
            return

        self.tickers_list = [ticker.strip() for ticker in self.ticker_string.split(',')]

        if len(self.tickers_list) < 2:
            messagebox.showerror("Error", "Please enter at least two tickers.")
            return

        # create the portfolio folder
        now = datetime.now()
        now_str = now.strftime("%Y-%m-%d_%H-%M-%S")  # date creation will work as portfolio ID

        self.portfolio_id = now_str

        if not os.path.exists('created_portfolios'):
            os.makedirs('created_portfolios')

        os.makedirs('created_portfolios/' + now_str)

        self.tickers_df, self.tickers_list = self.download_data(self.tickers_list, self.start_date.get_date(), self.end_date.get_date(), return_updated_tickers=True)

        self.ticker_string = ' '.join(self.tickers_list)
        self.ticker_string = self.ticker_string.replace(" ", ", ")

        self.analyze()


