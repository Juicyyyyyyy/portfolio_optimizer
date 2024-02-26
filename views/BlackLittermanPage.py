import customtkinter
from PortfolioOptimizer.BlackLitterman import BlackLitterman
import matplotlib.pyplot as plt
import os
from xhtml2pdf import pisa

from _collections import OrderedDict
from PortfolioOptimizer.GptBasedFunctions import GptBasedFunctions as gpt

class BlackLittermanPage(customtkinter.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.portfolio_id = None
        self.label_volatility = None
        self.label_expected_return = None
        self.label_weights = None
        self.label_weights_raw = None
        self.portfolio_size = None
        self.controller = controller

        self.start_date = None
        self.end_date = None
        self.tickers_list = None
        self.tickers_df = None

        # Title for the BlackLitterman page
        self.label_title = customtkinter.CTkLabel(self, text="Black-Litterman Model", font=("Roboto Medium", -16))
        self.label_title.pack(pady=20)

        # Container for ticker views
        self.ticker_container = customtkinter.CTkFrame(self)
        self.ticker_container.pack(fill="both", expand=True)

        # Create headers once
        self.create_headers()

        # Placeholder for ticker widgets, to be filled in set_tickers
        self.ticker_widgets = []

        # Dictionary to store references to outperform_dropdowns
        self.outperform_dropdowns = {}

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

        self.label_sharpe_ratio = customtkinter.CTkLabel(self, text="Sharpe ratio:")
        self.label_sharpe_ratio.pack(pady=2)

    def create_headers(self):
        # Creating column headers
        header_frame = customtkinter.CTkFrame(self.ticker_container)
        customtkinter.CTkLabel(header_frame, text="Ticker", font=("Roboto", -14)).pack(side="left", padx=10)
        customtkinter.CTkLabel(header_frame, text="View", font=("Roboto", -14)).pack(side="left", padx=60)
        customtkinter.CTkLabel(header_frame, text="Value(%)", font=("Roboto", -14)).pack(side="left", padx=65)
        customtkinter.CTkLabel(header_frame, text="Confidence(%)", font=("Roboto", -14)).pack(side="left", padx=90)
        header_frame.pack(fill="x", padx=20, pady=5)

    def on_view_change(self, selection, ticker_frame, ticker):
        # Remove any existing outperform dropdown if it exists
        for widget in ticker_frame.winfo_children():
            if hasattr(widget, 'is_outperform_dropdown') and widget.is_outperform_dropdown:
                widget.destroy()

        # If "Will Outperform (->) by" is selected, add another dropdown
        if selection == "Will Outperform (->) by":
            outperform_dropdown = customtkinter.CTkOptionMenu(ticker_frame,
                                                              values=self.controller.get_home_page_tickers_list())
            outperform_dropdown.is_outperform_dropdown = True  # Set a custom attribute to identify this dropdown
            outperform_dropdown.pack(side="left", padx=10, after=ticker_frame.winfo_children()[1])

            # Store reference to outperform_dropdown
            self.outperform_dropdowns[ticker] = outperform_dropdown

    def set_tickers(self, tickers):
        # Clear previous widgets
        for widget in self.ticker_widgets:
            widget.destroy()
        self.ticker_widgets.clear()

        for ticker in tickers:
            ticker_frame = customtkinter.CTkFrame(self.ticker_container)
            ticker_label = customtkinter.CTkLabel(ticker_frame, text=f"Ticker: {ticker}", font=("Roboto", -14))

            view_options = ["Will Return", "Will Outperform (->) by"]
            view_dropdown = customtkinter.CTkOptionMenu(ticker_frame, values=view_options, command=lambda selection, t_frame=ticker_frame, t=ticker: self.on_view_change(selection, t_frame, t))
            value_entry = customtkinter.CTkEntry(ticker_frame, placeholder_text="Value")
            confidence_options = ['100', '75', '50', '25']
            confidence_dropdown = customtkinter.CTkOptionMenu(ticker_frame, values=confidence_options)

            ticker_label.pack(side="left", padx=10)
            view_dropdown.pack(side="left", padx=10)
            value_entry.pack(side="left", padx=10)
            confidence_dropdown.pack(side="left", padx=10)
            ticker_frame.pack(fill="x", padx=20, pady=5)
            self.ticker_widgets.append(ticker_frame)

    def fetch_home_page_data(self):
        self.start_date = self.controller.get_home_page_start_date()
        self.end_date = self.controller.get_home_page_end_date()
        self.tickers_list = self.controller.get_home_page_tickers_list()
        self.tickers_df = self.controller.get_home_page_tickers_df()
        self.portfolio_size = self.controller.get_home_page_portfolio_value()
        self.portfolio_id = self.controller.get_home_page_portfolio_id()

    def convert_html_to_pdf(self, html_string, pdf_path):
        with open(pdf_path, "wb") as pdf_file:
            pisa_status = pisa.CreatePDF(html_string, dest=pdf_file)

        return not pisa_status.err

    def analyze(self):
        self.fetch_home_page_data()
        views = []
        for ticker_frame in self.ticker_widgets:
            # Assuming the order of widgets is label, dropdown, entry, dropdown
            widgets = ticker_frame.winfo_children()
            view_dropdown = widgets[1]
            value_entry = widgets[2]
            confidence_dropdown = widgets[3]

            view_selection = view_dropdown.get()
            value = float(value_entry.get())
            confidence = float(confidence_dropdown.get()) / 100

            # Retrieve ticker name from label
            ticker = widgets[0].cget("text").replace("Ticker: ", "")

            if view_selection == "Will Outperform (->) by":
                outperform_dropdown = self.outperform_dropdowns.get(ticker)
                if outperform_dropdown:
                    outperform_selection = outperform_dropdown.get()
                    views.append(
                        {'type': 'relative', 'asset1': ticker, 'asset2': outperform_selection, 'difference': value})
            else:
                views.append({'type': 'absolute', 'asset': ticker, 'return': value})

        bl = BlackLitterman(self.tickers_df, self.tickers_list, views)
        weights, expected_return, volatility, sharpe_ratio = bl.optimize_with_black_litterman()

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

        expected_return_percent, volatility_percent = expected_return * 100, volatility * 100

        # Display the results
        wraplength = 400
        font = ("Roboto Medium", 12)
        self.label_weights.configure(text=f"Weights percent: {filtered_weights_string_percent}", wraplength=wraplength,
                                     fg_color="cadetblue1", font=font)
        self.label_weights_raw.configure(text=f"Weights raw: {filtered_dollar_sizes_string}$", wraplength=wraplength,
                                         fg_color="cadetblue1", font=font)

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

        # Display the saved image
        img = plt.imread(img_path)
        plt.imshow(img)
        plt.show()

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

        self.label_expected_return.configure(text=f"Expected Return: {round(expected_return_percent, 2)}% per Year",
                                             wraplength=wraplength, fg_color="blanchedalmond", font=font)
        self.label_volatility.configure(text=f"Volatility: {round(volatility_percent, 2)}% per Year",
                                        wraplength=wraplength, fg_color="darkolivegreen1", font=font)
        self.label_sharpe_ratio.configure(text=f"Sharpe Ratio: {round(sharpe_ratio, 4)}",
                                          wraplength=wraplength, fg_color="thistle1", font=font)