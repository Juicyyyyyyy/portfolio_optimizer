<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<div align="center" id="readme-top">
  <a>
    <img src="images/logo.png" alt="Logo" width="160" height="160">
  </a>

  <h3 align="center">AI Portfolio Optimizer App</h3>

  <p align="center">
    Financial portfolio optimization made easy !
    <br />
    <br />
    <a href="https://github.com/othneildrew/Best-README-Template">View Demo</a>
    ·
    <a href="https://github.com/othneildrew/Best-README-Template/issues">Report Bug</a>
    ·
    <a href="https://github.com/othneildrew/Best-README-Template/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

![Product Name Screen Shot](images/main_app.png)

I think there is a real lack of financial opensource projects on the web. It's pretty hard to find resources to learn about this complex field. 
It is especially unfortunate in an era like ours where a simple diversification portfolio strategy can majorly improve your purchasing
power over the long term. 

I made this tool to simplify portfolio optimization theory to make it accessible for everyone who has read
the basics of portfolio optimization.

The tool use some well known mathematical concepts :
* Modern Portfolio Theory by Harry Markowitz
![Product Name Screen Shot](images/efficient_frontier.png)
* Black Litterman model by Fischer Black and Robert Litterman
![Product Name Screen Shot](images/black_litterman.png)

The tool also use AI (gpt 3.5 turbo) to generate a list of stock tickers based on 
a few parameters. Which simplify a lot the process of portfolio optimization
because you do not even have to find the tickers by yourself.

Then, once the portofolio optimization is finished, an analysis of the portfolio
will be saved as a pdf in the created_portfolios folder. The analysis will contain :
the weights in %, the weights in $, the expected volatility (per year), the expected
return (per year), the sharpe ratio. And finally a review of each ticker of the portfolio
containing : the company name, the history about the company and a reason to invest
on this asset. The review is created using a prompt for gpt 3.5 turbo.

Portfolio analysis:
![Product Name Screen Shot](images/pdf_1.png)
![Product Name Screen Shot](images/pdf_2.png)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With


* ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
* ![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
* ![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started



### Prerequisites

* Python

### Installation

1. Get your Open AI API Key at [https://platform.openai.com/docs/overview](https://platform.openai.com/docs/overview)
2. Clone the repo
   ```sh
   git clone https://github.com/Juicyyyyyyy/portfolio_optimizer
   ```
3. Install requirements
   ```sh
   pip install -r requirements. txt
   ```
4. Create a .env file in the root folder and enter your API key
   ```dotenv
   OPENAI_API_KEY=ENTER_YOUR_API
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- LICENSE -->
## License

Distributed under the MIT License. </br>
![NumPy](https://img.shields.io/github/license/Ileriayo/markdown-badges?style=for-the-badge)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

[![Linkedin](https://img.shields.io/badge/linkedin-%230077B5.svg?style=for-the-badge&logo=linkedin&logoColor=white)](https://pandas.pydata.org/)

Mail: corentin.dupaigne@gmail.com
</br>
Portfolio: https://corentindupaigne.herokuapp.com

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

Some of the resources that helped me into creating this project

* [Yahoo Finance API](https://developer.yahoo.com/api/)
* [PyPortfolioOpt](https://github.com/robertmartin8/PyPortfolioOpt)
* [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
* [Quantinsti](https://blog.quantinsti.com/calculating-covariance-matrix-portfolio-variance/)
* [Quantgestion](https://quantgestion.fr/le-modele-de-fisher-black-et-robert-litterman/)
* [Best-README-Template](https://github.com/othneildrew/Best-README-Template)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/othneildrew/Best-README-Template.svg?style=for-the-badge
[contributors-url]: https://github.com/othneildrew/Best-README-Template/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/othneildrew/Best-README-Template.svg?style=for-the-badge
[forks-url]: https://github.com/othneildrew/Best-README-Template/network/members
[stars-shield]: https://img.shields.io/github/stars/othneildrew/Best-README-Template.svg?style=for-the-badge
[stars-url]: https://github.com/othneildrew/Best-README-Template/stargazers
[issues-shield]: https://img.shields.io/github/issues/othneildrew/Best-README-Template.svg?style=for-the-badge
[issues-url]: https://github.com/othneildrew/Best-README-Template/issues
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/othneildrew/Best-README-Template/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/corentin-dupaigne-b449a1242
[product-screenshot]: images/main_app.png
[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[Next-url]: https://nextjs.org/
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[Vue-url]: https://vuejs.org/
[Angular.io]: https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white
[Angular-url]: https://angular.io/
[Svelte.dev]: https://img.shields.io/badge/Svelte-4A4A55?style=for-the-badge&logo=svelte&logoColor=FF3E00
[Svelte-url]: https://svelte.dev/
[Laravel.com]: https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white
[Laravel-url]: https://laravel.com
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com 
