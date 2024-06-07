from abc import ABC, abstractmethod

import requests
import urllib3
from bs4 import BeautifulSoup, Tag

from config import Logger
from py_invest_analyser.exceptions import ActiveSearchError
from py_invest_analyser.models import ActiveModel


class ExtractActiveInformation(ABC, Logger):
    def __init__(self):
        super().__init__()
        urllib3.disable_warnings()
        self.soup = None

    @abstractmethod
    def get_active_keys_indicators(self, active_name) -> dict:
        pass

    @abstractmethod
    def get_value_cell(self, cell: Tag):
        pass

    @abstractmethod
    def get_info_active(self, active_name: str):
        pass

    @abstractmethod
    def get_grade(self):
        pass

    @abstractmethod
    def get_indicators(self) -> dict:
        pass

    @abstractmethod
    def get_appreciation(self, soup) -> str:
        pass

    def get_page_infos_for_active(self, active_name, active_type, time_for_loop=0) -> dict or str:
        self.logger.info(f"Getting information {active_name}... {time_for_loop if time_for_loop > 0 else ''}")

        active = ActiveModel(name=active_name, type=active_type)

        try:
            if time_for_loop == 5:
                raise ActiveSearchError(f"Error to get information for active {active_name}")

            url = f"https://investidor10.com.br/{active_type}/{active_name}/"

            req = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=5, verify=False)

            soup = BeautifulSoup(req.text, "html.parser")
            self.soup = soup

            company_name = soup.find(class_='name-ticker').find("h2")
            active.company_name = company_name.text

            quotation = soup.find('div', class_='_card cotacao').find("div", class_="_card-body").find("span")
            active.quotation = quotation.text

            dividend_yield = soup.find('div', class_='_card dy').find("div", class_="_card-body").find("span")
            active.dividend_yield = dividend_yield.text

            price_to_book_ratio = soup.find('div', class_='_card vp').find("div", class_="_card-body").find("span")
            active.price_to_book_ratio = price_to_book_ratio.text

            daily_liquidity = soup.find('div', class_='_card val').find("div", class_="_card-body").find("span")
            daily_liquidity = daily_liquidity.text.replace("R$ ", "").replace(" K", "")
            active.daily_liquidity = daily_liquidity

            active.appreciation = self.get_appreciation(soup)

            active.grade = self.get_grade()

            indicators = self.get_indicators()

        except ActiveSearchError as error:
            self.logger.error(f"Maximum attempts to get information for active {active_name} {error}")
            return active_name

        except Exception as error:
            self.logger.error(f"Error to get information for active {active_name} {error}")
            return self.get_page_infos_for_active(active_name, active_type, time_for_loop + 1)

        if "-" in active.quotation or active.quotation is None:
            self.logger.warning(f"Error to get information for active {active_name} '-' quotation is not available")
            return self.get_page_infos_for_active(active_name, active_type, time_for_loop + 1)

        return {**active.__dict__, **indicators}
