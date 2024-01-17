import customtkinter

class BlackLitterman(customtkinter.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Title for the BlackLitterman page
        self.label_title = customtkinter.CTkLabel(self, text="Black-Litterman Model", font=("Roboto Medium", -16))
        self.label_title.pack(pady=20)

        # Container for ticker views
        self.ticker_container = customtkinter.CTkFrame(self)
        self.ticker_container.pack(fill="both", expand=True)

        # Placeholder for ticker widgets, to be filled in set_tickers
        self.ticker_widgets = []

        # Button to proceed with the analysis
        self.analyze_button = customtkinter.CTkButton(self, text="Analyze", command=self.analyze)
        self.analyze_button.pack(pady=20)

    def set_tickers(self, tickers):
        # Clear previous widgets
        for widget in self.ticker_widgets:
            widget.destroy()
        self.ticker_widgets.clear()

        # Create a view for each ticker
        for ticker in tickers:
            ticker_frame = customtkinter.CTkFrame(self.ticker_container)
            ticker_label = customtkinter.CTkLabel(ticker_frame, text=f"Ticker: {ticker}", font=("Roboto", -14))

            view_options = ["Will Return", "Will Outperform (->) by"]
            view_dropdown = customtkinter.CTkOptionMenu(ticker_frame, values=view_options)
            value_entry = customtkinter.CTkEntry(ticker_frame, placeholder_text="Value")
            confidence_slider = customtkinter.CTkSlider(ticker_frame, from_=0, to=100)

            ticker_label.pack(side="left", padx=10)
            view_dropdown.pack(side="left", padx=10)
            value_entry.pack(side="left", padx=10)
            confidence_slider.pack(side="left", padx=10)
            ticker_frame.pack(fill="x", padx=20, pady=5)
            #self.ticker_widgets.append(ticker_frame)

            ticker_label.pack(side="left", padx=10, pady=10)
            ticker_frame.pack(fill="x", padx=20, pady=5)
            #self.ticker_widgets.append(ticker_frame)

    def analyze(self):
        # Implement the logic to analyze based on user inputs for each ticker
        pass

# Add the BlackLitterman class to your application, similar to how other pages are added
