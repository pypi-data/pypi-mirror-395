# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
from enum import StrEnum, auto

class AutoLower(StrEnum):
    """
    StrEnum contrary to simple Enum is of type `str`, so it can be used as a string.
    StrEnum whose `auto()  # type: ignore` values are lower-case.
    (Identical to StrEnum's own default, but keeps naming symmetrical.)
    """
    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        return name.lower()            # StrEnum already does this

class AutoUpper(StrEnum):
    """
    StrEnum contrary to simple Enum is of type `str`, so it can be used as a string.
    StrEnum whose `auto()  # type: ignore` values stay as-is (UPPER_CASE).
    """
    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        return name                    # keep original upper-case

# ────────────────────────────────────────────────────────
# 0. Asset Rating
# ────────────────────────────────────────────────────────

class AssetRating(AutoUpper):
    STRONG_BUY = auto()  # type: ignore
    BUY = auto()  # type: ignore
    HOLD = auto()  # type: ignore
    PARTIALLY_SELL = auto()  # type: ignore
    SELL_ALL = auto()  # type: ignore
    NOT_RATED = auto()  # type: ignore

# ────────────────────────────────────────────────────────
# 1. Top-level economic exposure (stock / bond …)
# ────────────────────────────────────────────────────────

# ────────────────────────────────────────────────────────
# 2. Detailed Category which must go hand in hand with ContractOrOwnershipType
# ────────────────────────────────────────────────────────
class FincoreCategoryDetailed(AutoLower):
    # — Stocks —
    COMMON_STOCK            = auto()  # type: ignore
    PREFERRED_STOCK         = auto()  # type: ignore
    REIT                    = auto()  # type: ignore # Often traded like stock, represents Real Estate
    SPAC                    = auto()  # type: ignore
    PRIVATE_EQUITY          = auto()  # type: ignore

    # - Cryptocurrencies —
    CRYPTO_COIN              = auto()  # type: ignore
    CRYPTO_TOKEN             = auto()  # type: ignore
    STABLECOIN               = auto()  # type: ignore
    DEFI_GOV_TOKEN    = auto()  # type: ignore

    # Fixed income
    GOVERNMENT_BOND      = auto()  # type: ignore
    CORPORATE_BOND       = auto()  # type: ignore
    MUNICIPAL_BOND       = auto()  # type: ignore
    CONVERTIBLE_BOND     = auto()  # type: ignore
    PERPETUAL_BOND       = auto()  # type: ignore
    SUKUK                = auto()  # type: ignore
    INFLATION_LINKED     = auto()  # type: ignore
    FLOATING_RATE_NOTE   = auto()  # type: ignore
    ZERO_COUPON_BOND     = auto()  # type: ignore
    ABS                  = auto()  # type: ignore
    MBS                  = auto()  # type: ignore

    # — Funds —
    
    EQUITY_FUND              = auto()  # type: ignore
    BOND_FUND                = auto()  # type: ignore
    COMMODITY_FUND           = auto()  # type: ignore
    BALANCED_FUND            = auto()  # type: ignore
    INDEX_FUND               = auto()  # type: ignore
    HEDGE_FUND               = auto()  # type: ignore
    REAL_ESTATE_FUND         = auto()  # type: ignore

    # — Commodities —
    PRECIOUS_METAL          = auto()  # type: ignore
    INDUSTRIAL_METAL        = auto()  # type: ignore
    ENERGY                  = auto()  # type: ignore
    AGRICULTURE             = auto()  # type: ignore

     # — FX —
    CURRENCY          = auto()  # type: ignore
    CURRENCY_PAIR     = auto()  # type: ignore

    # — Benchmarks / references —
    INDEX             = auto()  # type: ignore

    MULTIPLE           = auto()  # type: ignore  # Used when multiple categories apply, e.g., a stock that is also in an ETF
    OTHER              = auto()  # type: ignore



class RealEstateCategoryDetailed(AutoLower):
    # — Real Estate (Direct Ownership) —
    RESIDENTIAL_PROPERTY    = auto()  # type: ignore # Combines Apartment, Villa
    COMMERCIAL_PROPERTY     = auto()  # type: ignore
    INDUSTRIAL_PROPERTY     = auto()  # type: ignore
    LAND                    = auto()  # type: ignore
    INFRASTRUCTURE          = auto()  # type: ignore


class RealAssetCategoryDetailed(AutoLower):
    # — Real Assets (Collectibles, etc.) —
    ART                     = auto()  # type: ignore
    WINE                    = auto()  # type: ignore
    VEHICLE                 = auto()  # type: ignore
    JEWELRY_WATCHES         = auto()  # type: ignore


# ────────────────────────────────────────────────────────
# 3. Contract / wrapper form (spot, future, ETF …)
# ────────────────────────────────────────────────────────
class FincoreContractOrOwnershipType(AutoLower): #ContractType
    # Direct holding
    SPOT     = auto()  # type: ignore # Same as direct ownership, proffessional term used for stocks, crypto, bonds and other liquid exchange tradeable items
    ADR      = auto()  # type: ignore # American Depository receipt of the underlying stock, used to trade international equities. Big Risk, example what happenned to Russian ADRs, GDRs
    GDR      = auto()  # type: ignore # Global Depository receipt of the underlying stock, used to trade international equities. Big Risk, example what happenned to Russian ADRs, GDRs
    DIRECT_OWNERSHIP       = auto()  # type: ignore # Direct ownership of physical assets (e.g., real estate title deed, private equity stocks, art , watch etc.)
    CUSTODIAL_OWNERSHIP = auto()  # type: ignore # Custodial ownership of physical assets (e.g., gold held by a custodian)
    # Wrappers for foreign stocks
  
    # Fund vehicles (tradable forms)
    ETF           = auto()  # type: ignore
    MUTUAL_FUND   = auto()  # type: ignore
    CLOSED_END_FUND = auto()  # type: ignore
    UNIT_TRUST    = auto()  # type: ignore
    ETN           = auto()  # type: ignore
    # Derivatives
    FUTURE       = auto()  # type: ignore
    OPTION              = auto()  # type: ignore
    FORWARD             = auto()  # type: ignore
    SWAP                = auto()  # type: ignore
    PERPETUAL_SWAP      = auto()  # type: ignore
    CFD                 = auto()  # type: ignore
    WARRANT             = auto()  # type: ignore
    RIGHTS              = auto()  # type: ignore
    STRUCTURED_NOTE     = auto()  # type: ignore
    TOTAL_RETURN_SWAP   = auto()  # type: ignore
    # References (non-tradable levels like SPX)
    REFERENCE           = auto()  # type: ignore
    MULTIPLE            = auto()  # type: ignore # Used when multiple contract types apply, e.g., a stock that is also in an ETF
    OTHER               = auto()  # type: ignore


class FincorePositionType (AutoUpper):

    LONG = auto()  # type: ignore
    LEVERAGED_LONG = auto()  # type: ignore
    SHORT = auto()  # type: ignore
    LEVERAGED_SHORT = auto()  # type: ignore
    

class FincoreContractOrPropertyKeeper (AutoLower):
    """Who holds the asset?"""
    SELF = auto()  # type: ignore  # Individual person
    SELF_OFFLINE_CRYPTO_WALLET = auto()  # type: ignore  # Offline cryptocurrency wallet
    SELF_MOBILE_CRYPTO_WALLET = auto()  # type: ignore  # Mobile cryptocurrency wallet
    PARTNER = auto()  # type: ignore  # Business partner or co-investor
    BANK_ACCOUNT = auto()  # type: ignore  # Bank or financial institution
    BANK_SAFEBOX = auto()  # type: ignore
    BROKER = auto()  # type: ignore  # Brokerage firm
    TRUST = auto()  # type: ignore
    CUSTODIAN = auto()  # type: ignore  # Custodian or trust company
    COMPANY = auto()  # type: ignore  # Company or corporation
    GOVERNMENT = auto()  # type: ignore  # Government or state entity
    EXCHANGE = auto()  # type: ignore  # Exchange or trading platform
    OTHER = auto()  # type: ignore  # Other entity not listed above
# ────────────────────────────────────────────────────────
# 4. Corporate Actions
# ────────────────────────────────────────────────────────
class CorporateActionType(AutoLower):
    SPLITS = auto()  # type: ignore
    DIVIDENDS = auto()  # type: ignore


