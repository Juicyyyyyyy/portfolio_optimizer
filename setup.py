from setuptools import find_packages, setup

setup(
    name="portfolio_optimizer",
    version="1.0.0",
    description="A user-friendly financial portfolio optimization tool simplified through the integration of AI",
    url="https://github.com/Juicyyyyyyy/portfolio_optimizer",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Corentin Dupaigne",
    packages=find_packages(exclude=["tests", ".github"]),
    install_requires=[
        'Markdown==3.4.1',
        'matplotlib==3.7.2',
        'numpy==1.24.3',
        'openai==1.35.13',
        'pandas==2.0.3',
        'python-dotenv==1.0.1',
        'tkcalendar==1.6.1',
        'xhtml2pdf==0.2.15',
        'yfinance==0.2.36',
        'pyportfolioopt==1.5.5'
    ],
    python_requires='>=3.9',
)
