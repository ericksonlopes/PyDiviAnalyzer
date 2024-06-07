from bs4 import Tag

from py_invest_analyser.models import BDR
from py_invest_analyser.scrapers.investidor_10.extract_info_abstract import ExtractActiveInformation


class ExtractInfoFromBDR(ExtractActiveInformation):

    def __init__(self):
        super().__init__()

    def get_appreciation(self, soup) -> str:
        appreciation = soup.find('div', class_='_card pl').find("div", class_="_card-body").find("span")
        return appreciation.text

    def get_grade(self):
        return "-"

    def get_value_cell(self, cell: Tag):
        return cell.div.text.replace("\n", "")

    def get_active_keys_indicators(self, active_name) -> BDR:
        return BDR(name=active_name, type="bdrs")

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

        return indicators

    def get_info_active(self, active_name: str) -> BDR:
        ret_bdr = BDR()
        ret_bdr.name = active_name

        try:
            bdr = self.get_page_infos_for_active(active_name, "bdrs")
            list_bdr_keys = list(BDR().__dict__.keys())

            for key, value in bdr.items():
                if key in list_bdr_keys:
                    ret_bdr.__dict__[key] = value

                mean = ret_bdr.get_meaning_of_fields()

                if key in mean.values():
                    key_mean = list(mean.keys())[list(mean.values()).index(key)]
                    ret_bdr.__dict__[key_mean] = value

            return ret_bdr
        except Exception as e:
            self.logger.error(f"Error to get information for active {active_name}")
            self.logger.error(e)

        finally:
            self.logger.info(f"Information for active {active_name} successfully obtained")

        return ret_bdr
