from dataclasses import dataclass
from types import MappingProxyType

from py_invest_analyser.models.investidor10.ActiveModel import ActiveModel


@dataclass
class StockModel(ActiveModel):
    p_l: str = None
    p_vp: str = None
    dividend_yield_stock: str = None
    payout: str = None
    net_margin: str = None
    gross_margin: str = None
    ebit_margin: str = None
    ebitda_margin: str = None
    ev_ebitda: str = None
    ev_ebit: str = None
    p_ebitda: str = None
    p_ebit: str = None
    p_assets: str = None
    p_working_capital: str = None
    p_net_current_assets: str = None
    psr: str = None
    vpa: str = None
    lpa: str = None
    asset_turnover: str = None
    roe: str = None
    roic: str = None
    roa: str = None
    net_debt_equity_ratio: str = None
    net_debt_ebitda_ratio: str = None
    net_debt_ebit_ratio: str = None
    gross_debt_equity_ratio: str = None
    equity_assets_ratio: str = None
    liabilities_assets_ratio: str = None
    current_ratio: str = None
    cagr_revenues_5_years: str = None
    cagr_earnings_5_years: str = None

    @classmethod
    def get_meaning_of_fields(cls) -> MappingProxyType:
        active_default = super().get_meaning_of_fields()

        stock = {
            'p_l': 'P/L',
            'payout': 'PAYOUT',
            'net_margin': 'MARGEM LÍQUIDA',
            'gross_margin': 'MARGEM BRUTA',
            'ebit_margin': 'MARGEM EBIT',
            'ebitda_margin': 'MARGEM EBITDA',
            'ev_ebitda': 'EV/EBITDA',
            'ev_ebit': 'EV/EBIT',
            'p_ebitda': 'P/EBITDA',
            'p_ebit': 'P/EBIT',
            'p_assets': 'P/ATIVO',
            'p_working_capital': 'P/CAP.GIRO',
            'p_net_current_assets': 'P/ATIVO CIRC LIQ',
            'psr': 'PSR',
            'vpa': 'VPA',
            'lpa': 'LPA',
            'asset_turnover': 'GIRO ATIVOS',
            'roe': 'ROE',
            'roic': 'ROIC',
            'roa': 'ROA',
            'net_debt_equity_ratio': 'DÍVIDA LÍQUIDA / PATRIMÔNIO',
            'net_debt_ebitda_ratio': 'DÍVIDA LÍQUIDA / EBITDA',
            'net_debt_ebit_ratio': 'DÍVIDA LÍQUIDA / EBIT',
            'gross_debt_equity_ratio': 'DÍVIDA BRUTA / PATRIMÔNIO',
            'equity_assets_ratio': 'PATRIMÔNIO / ATIVOS',
            'liabilities_assets_ratio': 'PASSIVOS / ATIVOS',
            'current_ratio': 'LIQUIDEZ CORRENTE',
            'cagr_revenues_5_years': 'CAGR RECEITAS 5 ANOS',
            'cagr_earnings_5_years': 'CAGR LUCROS 5 ANOS'
        }

        return MappingProxyType(dict(active_default, **stock))
