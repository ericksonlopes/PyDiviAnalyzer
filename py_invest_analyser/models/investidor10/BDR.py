from dataclasses import dataclass
from types import MappingProxyType

from py_invest_analyser.models.investidor10.ActiveModel import ActiveModel


@dataclass
class BDR(ActiveModel):
    p_l: str = None
    p_vp: str = None
    p_e: str = None
    dividend_yield: str = None
    roa: str = None
    roe: str = None
    roic: str = None
    net_margin: str = None
    gross_margin: str = None
    operating_margin: str = None
    p_ebit: str = None
    p_ebitda: str = None
    p_assets: str = None
    vpa: str = None
    lpa: str = None
    equity_assets_ratio: str = None
    liabilities_assets_ratio: str = None
    cagr_revenues_5_years: str = None
    cagr_earnings_5_years: str = None

    @classmethod
    def get_meaning_of_fields(cls) -> MappingProxyType:
        active_default = super().get_meaning_of_fields()

        bdr = {
            'p_l': 'P/L',
            'p_vp': 'P/VP',
            'p_e': 'P/E',
            'dividend_yield_dy': 'DIVIDEND YIELD (DY)',
            'roa': 'ROA',
            'roe': 'ROE',
            'roic': 'ROIC',
            'net_margin': 'MARGEM LÍQUIDA',
            'gross_margin': 'MARGEM BRUTA',
            'operating_margin': 'MARGEM OPERACIONAL',
            'p_ebit': 'P/EBIT',
            'p_ebitda': 'P/EBITDA',
            'p_assets': 'P/ATIVO',
            'vpa': 'VPA',
            'lpa': 'LPA',
            'equity_assets_ratio': 'PATRIMÔNIO / ATIVOS',
            'liabilities_assets_ratio': 'PASSIVOS / ATIVOS',
            'cagr_revenues_5_years': 'CAGR RECEITAS 5 ANOS',
            'cagr_earnings_5_years': 'CAGR LUCROS 5 ANOS',
        }

        return MappingProxyType(dict(**active_default, **bdr))
