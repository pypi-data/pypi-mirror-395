




from __future__ import annotations
from typing import TYPE_CHECKING
from tbapi.common.decorators import tb_interface
from tbapi.common.converters import to_python_datetime, to_net_datetime
from datetime import datetime
from Tickblaze.Scripts.Api.Interfaces import IAccount as _IAccount
from typing import Any, overload
from abc import ABC, abstractmethod

@tb_interface(_IAccount)
class IAccount():
    """Represents trading account with balance, margin, positions, and equity details."""

    @property
    def name(self) -> str:
        """The account name."""
        val = self._value.Name
        return val
    @property
    def base_currency_code(self) -> str:
        """The currency code for the account's base currency."""
        val = self._value.BaseCurrencyCode
        return val
    @property
    def buying_power(self) -> float:
        """The available buying power for the account."""
        val = self._value.BuyingPower
        return val
    @property
    def cash_value(self) -> float:
        """The current cash value in the account."""
        val = self._value.CashValue
        return val
    @property
    def excess_initial_margin(self) -> float:
        """The excess initial margin available in the account."""
        val = self._value.ExcessInitialMargin
        return val
    @property
    def excess_intraday_margin(self) -> float:
        """The excess intraday margin available in the account."""
        val = self._value.ExcessIntradayMargin
        return val
    @property
    def gross_realized_pn_l(self) -> float:
        """The gross realized profit and loss for the account."""
        val = self._value.GrossRealizedPnL
        return val
    @property
    def initial_cash(self) -> float:
        """The initial cash amount deposited into the account."""
        val = self._value.InitialCash
        return val
    @property
    def initial_margin(self) -> float:
        """The initial margin required for opening positions in the account."""
        val = self._value.InitialMargin
        return val
    @property
    def intraday_margin(self) -> float:
        """The intraday margin requirement for the account."""
        val = self._value.IntradayMargin
        return val
    @property
    def net_liquidation(self) -> float:
        """The net liquidation value, which is the current total value of the account."""
        val = self._value.NetLiquidation
        return val
    @property
    def realized_pn_l(self) -> float:
        """The realized profit and loss, representing closed positions."""
        val = self._value.RealizedPnL
        return val
    @property
    def total_pn_l(self) -> float:
        """The total profit and loss, combining both realized and unrealized profits/losses."""
        val = self._value.TotalPnL
        return val
    @property
    def unrealized_pn_l(self) -> float:
        """The unrealized profit and loss from open positions in the account."""
        val = self._value.UnrealizedPnL
        return val
    @property
    def cash(self) -> float:
        """The cash balance in the account."""
        val = self._value.Cash
        return val
    @property
    def equity(self) -> float:
        """The equity in the account, which is the value of the account's assets."""
        val = self._value.Equity
        return val
    @property
    def excess_equity(self) -> float:
        """The excess equity available in the account."""
        val = self._value.ExcessEquity
        return val
    @property
    def market_value(self) -> float:
        """The market value of all positions held in the account."""
        val = self._value.MarketValue
        return val
    @property
    def initial_margin_overnight(self) -> float:
        """The initial margin required for holding overnight positions."""
        val = self._value.InitialMarginOvernight
        return val
    @property
    def maintenance_margin(self) -> float:
        """The maintenance margin requirement for the account."""
        val = self._value.MaintenanceMargin
        return val
    @property
    def maintenance_margin_overnight(self) -> float:
        """The maintenance margin required for holding overnight positions."""
        val = self._value.MaintenanceMarginOvernight
        return val
    @property
    def net_liquidation_value(self) -> float:
        """The net liquidation value including all assets and liabilities in the account."""
        val = self._value.NetLiquidationValue
        return val
    @property
    def total_net_value(self) -> float:
        """The total net value of the account, which combines equity and any liabilities."""
        val = self._value.TotalNetValue
        return val
    @property
    def positions(self) -> IReadOnlyList:
        """A list of positions currently held in the account."""
        val = self._value.Positions
        return val


