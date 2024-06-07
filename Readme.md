# PyInvestAnalyser

![Star](https://img.shields.io/github/stars/ericksonlopes/PyInvestAnalyser?style=social) [![LinkedIn](https://img.shields.io/badge/LinkedIn-Erickson_Lopes%20-blue)](https://www.linkedin.com/in/ericksonlopes/) ![wakatime](https://wakatime.com/badge/user/541772df-f19f-4145-a40c-cf7ffac73ea5/project/5bfa867f-031e-4498-bdf3-a918ec816f88.svg) [![Test](https://github.com/ericksonlopes/PyInvestAnalyser/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/ericksonlopes/PyInvestAnalyser/actions/workflows/tests.yml)

![Python](https://img.shields.io/badge/-Python-3776AB?&logo=Python&logoColor=FFFFFF)
![Docker](https://img.shields.io/badge/-Docker-2496ED?&logo=Docker&logoColor=FFFFFF)
![Pytest](https://img.shields.io/badge/-Pytest-0A9EDC?&logo=Pytest&logoColor=FFFFFF)
![Selenium](https://img.shields.io/badge/-Selenium-43B02A?&logo=Selenium&logoColor=FFFFFF)

[//]: # (![FastAPI]&#40;https://img.shields.io/badge/-FastAPI-009688?&logo=FastAPI&logoColor=FFFFFF&#41;)

[//]: # (![Redis]&#40;https://img.shields.io/badge/-Redis-DC382D?&logo=Redis&logoColor=FFFFFF&#41;)

[//]: # (![Gunicorn]&#40;https://img.shields.io/badge/-Gunicorn-499848?&logo=gunicorn&logoColor=FFFFFF&#41;)

PyInvestAnalyser is a Python project that uses web scraping to obtain data on financial assets. With the help of
Selenium, Docker, and Pyenv libraries, you can analyze relevant information about different assets in an automated
manner.

## Prerequisites

Before you start, make sure you have the following prerequisites installed:

- Python (recommended to use Pyenv for package management)
- Docker

## Installation

Follow the steps below to install the project:

1. Clone this repository:

   ```
   $ git clone https://github.com/ericksonlopes/PyInvestAnalyser.git
   ```

2. Access the project directory:

   ```
   $ cd PyInvestAnalyser
   ```

3. Create and Install project dependencies:

   ```
   $ pip install pipenv
   $ pipenv install
   ```

4. activate a virtual environment with Pyenv:

   ```
   $ pipenv shell
   ```

5. Make sure Docker is running.
6. Run Docker Compose to start the execution environment:

   ```
   $ docker-compose up -d
   ```

## Usage

To use PyInvestAnalyser, follow these steps:

Import the ExtractInfoFromStock class for the respective type of asset you want to analyze (stocks, real estate funds,
and DBRs):

Here is an example of how to import the ExtractInfoFromStock class to obtain information about the B3SA3 stock:

```python
from py_invest_analyser.services import ExtractInfoFromStock

stock = ExtractInfoFromStock().get_info_active('B3SA3')

print(stock)
# StockModel(name='B3SA3', company_nam...
```

Additionally, providing context to a more complex example, you can execute a multi-threaded script to obtain information
about multiple assets at the same time:

In this case, the script will obtain information about the stocks B3SA3, BBDC3, BBSE3, and BMGB4 and save the results in
a CSV file.

```python
import concurrent.futures
import csv

from py_invest_analyser.models import StockModel
from py_invest_analyser.services import ExtractInfoFromStock

actives = [
    'B3SA3',
    'BBDC3',
    'BBSE3',
    'BMGB4'
]

result_actives = []

with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = [executor.submit(ExtractInfoFromStock().get_info_active, active) for active in actives]

    for future in concurrent.futures.as_completed(futures):
        try:
            active = future.result()

            if isinstance(active, str):
                active = ExtractInfoFromStock().get_active_keys_indicators(active)

            result_actives.append(active)

        except Exception as e:
            print(f'Error1: {str(e)}')

with open('result_for_actives.csv', 'w', newline='', encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(StockModel().get_meaning_of_fields().values())

    for active in result_actives:
        writer.writerow(active.__dict__.values())
```

## Contributing

If you want to contribute to the PyInvestAnalyser project, follow the steps below:

1. Fork the project

2. Create a new branch (git checkout -b feature/new-feature)

3. Make your changes

4. Commit your changes (git commit -am 'Add new feature')

5. Push to the branch (git push origin feature/new-feature)

6. Open a Pull Request

## Authors

- [Erickson Lopes](<https://www.linkedin.com/in/ericksonlopes/>)

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).

## References

- [Python](https://www.python.org/)
- [Selenium](https://www.selenium.dev/)
- [Docker](https://www.docker.com/)
- [Pyenv](https://pypi.org/project/pyenv/)
- [Pytest](https://docs.pytest.org/)
- [Investidor10](https://investidor10.com.br)
