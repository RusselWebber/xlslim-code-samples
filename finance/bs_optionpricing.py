# An example of how option portfolios are risk managed
# Requires Python 3.8+ due to the use of NormalDist
import logging
from datetime import datetime, timedelta
from dataclasses import dataclass
from math import nan, log, sqrt, exp
from statistics import NormalDist
from enum import Enum
from typing import List, Dict, Callable

LOG = logging.getLogger(__name__)

# Using the recent NormalDist added in Py3.8
ND = NormalDist(0.0, 1.0)


@dataclass(frozen=True, repr=True)
class OptionResults:
    """An option price and analytical greeks."""

    pv: float = nan
    delta: float = nan
    gamma: float = nan
    vega: float = nan
    theta: float = nan


class OptionType(Enum):
    """Option type enum - CALL or PUT"""

    CALL = 0
    PUT = 1


@dataclass(frozen=True, repr=True)
class VanillaEuropeanOption:
    """A vanilla European option"""

    strike: float = nan
    expiry: datetime = datetime.utcnow()
    underlying: str = None
    option_type: OptionType = OptionType.CALL
    currency: str = None


class OptionPortfolio:
    """A portfolio of options"""

    def __init__(self, options: List[VanillaEuropeanOption], notionals: List[float]):

        # Exclude zero notionals
        notionals = [n for n in notionals if n != 0.0]

        if len(options) != len(notionals):
            raise ValueError(
                f"The number of options {len(options)} must equal the number of notionals {len(notionals)}"
            )
        self._options = options
        self._notionals = notionals

    @property
    def options(self):
        return self._options

    @property
    def notionals(self):
        return self._notionals


class VolatilityCurve:
    """A very simplistic volatility curve.

    In practice volatilities are stored on a surface with strike and expiry dimensions.
    Volatility surfaces also usually support interpolation and extrapolation in the strike and expiry dimensions.
    """

    def __init__(self, expiries: List[datetime], volatilties: List[float]):
        if len(expiries) != len(volatilties):
            raise ValueError("The lengths of the expiries and volatilties must match.")
        self._vol_curve = dict(zip(expiries, volatilties))

    def __getitem__(self, key: str):
        vol = self._vol_curve.get(key)
        if vol is None:
            msg = f"Failed to find a vol level for {key}"
            LOG.error(msg)
            raise ValueError(msg)
        return vol


class OptionPortfolioCalculator:
    """Calculate pv and risk for a portfolio of options."""

    def __init__(
        self,
        models: Dict[str, Callable],
        option_portfolio: OptionPortfolio,
        asof: datetime,
        spot_dict: Dict[str, float],
        vol_dict: Dict[str, VolatilityCurve],
        cost_of_carry_dict: Dict[str, float],
        risk_free_rate_dict: Dict[str, float],
    ):

        self._asof = asof
        self._models = models
        self._option_portfolio = option_portfolio
        self._spot_dict = spot_dict
        self._vol_dict = vol_dict
        self._cost_of_carry_dict = cost_of_carry_dict
        self._risk_free_rate_dict = risk_free_rate_dict
        self._option_results = []
        self._pv = nan
        self._delta = nan
        self._gamma = nan
        self._vega = nan
        self._theta = nan

        self._calculate()

    def _calculate(self):
        asof = self._asof

        for n, o in zip(
            self._option_portfolio.notionals, self._option_portfolio.options
        ):

            # Loop through the options
            try:
                # Fetch the inputs
                model = self._models[o.__class__.__name__]
                spot = self._spot_dict[o.underlying]
                cost_of_carry = self._cost_of_carry_dict[o.underlying]
                vol_curve = self._vol_dict[o.underlying]
                risk_free_rate = self._risk_free_rate_dict[o.currency]

                # And call the valuation model for each option

                self._option_results.append(
                    (n, model(o, spot, asof, risk_free_rate, cost_of_carry, vol_curve))
                )
            except:
                LOG.error(f"Failed to calculate {o}", exc_info=True)

        # The portfolio risks are the sum of the individual options * their notionals
        self._pv = sum((n * o.pv for n, o in self._option_results))
        self._delta = sum((n * o.delta for n, o in self._option_results))
        self._gamma = sum((n * o.gamma for n, o in self._option_results))
        self._vega = sum((n * o.vega for n, o in self._option_results))
        self._theta = sum((n * o.theta for n, o in self._option_results))

    def __repr__(self):
        return f"OptionPortfolioCalculator(pv={self.pv:.2f}, delta={self.delta:.2f}, gamma={self.gamma:.2f}, vega={self.vega:.2f}, theta={self.theta:.2f})"

    @property
    def pv(self):
        return self._pv

    @property
    def delta(self):
        return self._delta

    @property
    def gamma(self):
        return self._gamma

    @property
    def vega(self):
        return self._vega

    @property
    def theta(self):
        return self._theta


def get_bsm_option_calculator() -> Callable:
    """Get a function pointer to the Black-Scholes-Merton calculator."""
    return bsm_option_calculator


def bsm_option_calculator(
    opt: VanillaEuropeanOption,
    spot: float,
    asof: datetime,
    risk_free_rate: float,
    cost_of_carry: float,
    volatility_curve: VolatilityCurve,
) -> OptionResults:
    """The Black-Scholes-Merton calculation."""

    t = (opt.expiry - asof).days / 365
    return_instrinsic = False

    if t <= 0:
        # A simple test for expiry, in practice you would value up until expiry time.
        # After expiry the intrinsic value is returned
        return_instrinsic = True

    volatility = volatility_curve[opt.expiry]

    if volatility <= 0:
        # Return the intrinsic value if the vol level goes to 0 or below
        return_instrinsic = True

    if not return_instrinsic:

        # Note how calculations are reused and the pv and greeks are calculated
        # at once for maximum efficiency
        sqrt_t = sqrt(t)
        vol_sqrt_t = volatility * sqrt_t
        d1 = (
            log(spot / opt.strike) + (cost_of_carry + volatility**2.0 / 2.0) * t
        ) / (vol_sqrt_t)
        cdf_d1 = ND.cdf(d1)
        cdf_neg_d1 = ND.cdf(-d1)
        pdf_d1 = ND.pdf(d1)
        d2 = d1 - vol_sqrt_t
        cdf_d2 = ND.cdf(d2)
        cdf_neg_d2 = ND.cdf(-d2)

        df = exp(-risk_free_rate * t)
        net_r = cost_of_carry - risk_free_rate
        carry = exp((net_r) * t)
        carry_pdf_d1 = carry * pdf_d1
        spot_carry_pdf_d1 = spot * carry_pdf_d1
        disc_strike = opt.strike * df

        if opt.option_type == OptionType.CALL:
            delta = carry * cdf_d1
            value = spot * delta - disc_strike * cdf_d2
            theta = (
                -spot_carry_pdf_d1 * volatility / (2.0 * sqrt_t)
                - (net_r) * spot * delta
                - risk_free_rate * disc_strike * cdf_d2
            )
        elif opt.option_type == OptionType.PUT:
            delta = -carry * cdf_neg_d1
            value = disc_strike * cdf_neg_d2 - spot * -delta
            theta = (
                -spot_carry_pdf_d1 * volatility / (2.0 * sqrt_t)
                + (net_r) * spot * -delta
                + risk_free_rate * disc_strike * cdf_neg_d2
            )
        gamma = carry_pdf_d1 / (spot * vol_sqrt_t) * spot**2.0 / 100.0
        vega = spot_carry_pdf_d1 * sqrt_t / 100.0
        theta = theta / 365.0  # One day theta)
        delta = delta * spot
        return OptionResults(pv=value, delta=delta, gamma=gamma, vega=vega, theta=theta)
    else:
        return OptionResults(
            pv=max(0.0, spot - opt.strike)
            if opt.option_type is OptionType.CALL
            else max(0.0, opt.strike - spot),
            delta=spot if opt.option_type is OptionType.CALL else -spot,
            gamma=0,
            vega=0,
            theta=0,
        )


if __name__ == "__main__":
    asof = datetime.utcnow()
    expiry = asof + timedelta(days=365 / 4)
    o = VanillaEuropeanOption(
        strike=100.0,
        expiry=asof + timedelta(days=365 / 4),
        underlying="SPX",
        option_type=OptionType.CALL,
        currency="USD",
    )
    p = OptionPortfolio([o], [1.0])
    spots = {"SPX": 102.0}
    risk_free_rate = {"USD": 0.1}
    cost_of_carry = {"SPX": 0.05}
    vols = {"SPX": VolatilityCurve([expiry], [0.2])}
    models = {"VanillaEuropeanOption": bsm_option_calculator}
    pr = OptionPortfolioCalculator(
        models, p, asof, spots, vols, cost_of_carry, risk_free_rate
    )
    print(pr)
