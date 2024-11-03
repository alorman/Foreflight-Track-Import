
<!-- PROJECT SHIELDS -->
<!-- -->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]






<!-- ABOUT THE PROJECT -->
## About The Project

![KTG Screen Shot](screenshot.png?raw=true)

A CLI app to convert FlightAware KML tracklogs to G1000 CSV for importing to ForeFlight for those who do not have mobile ADS-B that can connect directly to ForeFlight for breadcrumbs. This is a forked project that extends the basic functionality and code structure of the existing project. 

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple example steps.

### Prerequisites

You will need the following modules to run this program:

* Python 3.10
* lxml
* glob
* requests
* beautifulsoup4
* datetime
* pandas

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/dscpsyl/FlightawareToForeflight.git
   ```
2. Install the dependencies listed above. (requirements.txt coming soon...)
3. run the program
   ```sh
   python3.10 main.py
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

There are currently three different options to use the CLI:

1. **Local**: Convert KML files from a local directory. Supply the full path to the directory. Otherwise, it defaults to the `Downloads` folder.
2. **Flight** Search: Search for a flight on flightaware.com and download the KML tracklog. Supply the tailnumber, and the CLI will guide you.
3. **Flight Link**: Supply a direct link to a flightaware.com KML tracklog. The link should end with `.../tracklog`.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

SimYouLater - [@SimYouLater28](https://twitter.com/SimYouLater28)

Project Link: [https://github.com/dscpsyl/FlightawareToForeflight](https://github.com/dscpsyl/FlightawareToForeflight)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/dscpsyl/FlightawareToForeflight.svg?style=for-the-badge
[contributors-url]: https://github.com/dscpsyl/FlightawareToForeflight/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/dscpsyl/FlightawareToForeflight.svg?style=for-the-badge
[forks-url]: https://github.com/dscpsyl/FlightawareToForeflight/network/members
[stars-shield]: https://img.shields.io/github/stars/dscpsyl/FlightawareToForeflight.svg?style=for-the-badge
[stars-url]: https://github.com/dscpsyl/FlightawareToForeflight/stargazers
[issues-shield]: https://img.shields.io/github/issues/dscpsyl/FlightawareToForeflight.svg?style=for-the-badge
[issues-url]: https://github.com/dscpsyl/FlightawareToForeflight/issues
[license-shield]: https://img.shields.io/github/license/dscpsyl/FlightawareToForeflight.svg?style=for-the-badge
[license-url]: https://github.com/dscpsyl/FlightawareToForeflight/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/davidjsim
[product-screenshot]: images/screenshot.png
