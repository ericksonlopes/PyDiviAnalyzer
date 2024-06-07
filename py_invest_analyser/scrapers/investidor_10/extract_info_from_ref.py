from bs4 import Tag

from py_invest_analyser.exceptions import IndicatorNotFound
from py_invest_analyser.models import RealEstateFundsModel
from py_invest_analyser.scrapers.investidor_10.extract_info_abstract import ExtractActiveInformation


class ExtractInfoFromREF(ExtractActiveInformation):
    def get_appreciation(self, soup) -> str:
        appreciation = soup.findAll('div', class_='_card dy')[-1].find("div", class_="_card-body").find("span")
        return appreciation.text

    def __init__(self):
        super().__init__()

    def get_grade(self):
        return "-"

    def get_value_cell(self, cell: Tag) -> str:
        return cell.find("div", class_="value").text.replace("\n", "")

    def get_active_keys_indicators(self, active_name) -> RealEstateFundsModel:
        return RealEstateFundsModel(name=active_name, type="ref")

    def get_indicators(self) -> dict:
        indicators = {}

        try:

            table_indicators = self.soup.find('div', id='table-indicators').find_all("div", class_="cell")

            for cell in table_indicators:
                indicator = cell.span.text.replace("\n", "")

                value = self.get_value_cell(cell)

                indicators[indicator] = value

        except Exception as error:
            self.logger.error(f"Error to get indicators {error}")

        if indicators["SEGMENTO"] is None:
            raise IndicatorNotFound("segment not found")

        return indicators

    def get_info_active(self, active_name: str) -> RealEstateFundsModel:
        ret_ref = RealEstateFundsModel()
        ret_ref.name = active_name

        try:
            ref = self.get_page_infos_for_active(active_name, "fiis")

            list_keys_ref = list(RealEstateFundsModel().__dict__.keys())

            for key, value in ref.items():
                if key in list_keys_ref:
                    ret_ref.__dict__[key] = value

                mean = ret_ref.get_meaning_of_fields()

                if key in mean.values():
                    key_mean = list(mean.keys())[list(mean.values()).index(key)]
                    ret_ref.__dict__[key_mean] = value

        except Exception as e:
            self.logger.error(f"Error to get information for active {active_name}")
            self.logger.error(e)

        finally:
            self.logger.info(f"Information for active {active_name} successfully obtained")

        return ret_ref
