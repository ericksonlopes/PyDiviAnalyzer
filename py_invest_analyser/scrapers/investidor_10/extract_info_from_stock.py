from bs4 import Tag

from py_invest_analyser.models import StockModel
from py_invest_analyser.scrapers.investidor_10.extract_info_abstract import ExtractActiveInformation


class ExtractInfoFromStock(ExtractActiveInformation):

    def __init__(self):
        super().__init__()

    def get_appreciation(self, soup) -> str:
        appreciation = soup.find('div', class_='_card pl').find("div", class_="_card-body").find("span")
        return appreciation.text

    def get_value_cell(self, cell: Tag):
        try:
            return cell.div.text.replace("\n", "")
        except Exception as error:
            self.logger.error(f"Error to get value cell {error}")

    def get_active_keys_indicators(self, active_name) -> StockModel:
        try:
            return StockModel(name=active_name, type="acoes")
        except Exception as error:
            self.logger.error(f"Error to get active keys indicators {error}")

    def get_grade(self):
        try:
            grade = self.soup.find('div', id="checklist").find('div', class_='rating')
            grade_text = grade.text.replace("\n", "").replace(" ", "").replace("Nota", "").replace(":", "")
            return grade_text
        except Exception as error:
            self.logger.error(f"Error to get grade {error}")

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

    def get_info_active(self, active_name) -> StockModel:
        ret_stock = StockModel()
        ret_stock.name = active_name

        try:
            stock = self.get_page_infos_for_active(active_name, "acoes")

            list_keys_ref = list(StockModel().__dict__.keys())

            for key, value in stock.items():
                key = key.rstrip()

                if key in list_keys_ref:
                    ret_stock.__dict__[key] = value

                mean = ret_stock.get_meaning_of_fields()

                if key in mean.values():
                    key_mean = list(mean.keys())[list(mean.values()).index(key)]
                    ret_stock.__dict__[key_mean] = value

        except Exception as e:
            self.logger.error(f"Error to get information for active {active_name}")
            self.logger.error(e)

        finally:
            self.logger.info(f"Information for active {active_name} successfully obtained")

        return ret_stock
