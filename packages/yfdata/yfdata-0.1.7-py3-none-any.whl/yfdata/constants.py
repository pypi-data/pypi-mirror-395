# -*- coding: utf-8 -*-

# CONSTANTS.
CURRENCY_EUR = "eur"
T1W = "1W"
T1M = "1M"
T5Y = "5Y"

FREQ_DAILY = "1D"
FREQ_MINUTE = "1m"
FREQ_QUARTERLY = "Q"
FREQ_ANNUAL = "A"
TTM = "TTM"

MAPPING_INCOME_METRICS = {
    "total_revenue": {
        FREQ_QUARTERLY: "quarterlyTotalRevenue",
        FREQ_ANNUAL: "annualTotalRevenue",
        TTM: "trailingTotalRevenue",
    },
    "cost_of_revenue": {
        FREQ_QUARTERLY: "quarterlyCostOfRevenue",
        FREQ_ANNUAL: "annualCostOfRevenue",
        TTM: "trailingCostOfRevenue",
    },
    "gross_profit": {
        FREQ_QUARTERLY: "quarterlyGrossProfit",
        FREQ_ANNUAL: "annualGrossProfit",
        TTM: "trailingGrossProfit",
    },
    "operating_expense": {
        FREQ_QUARTERLY: "quarterlyOperatingExpense",
        FREQ_ANNUAL: "annualOperatingExpense",
        TTM: "trailingOperatingExpense",
    },
    "operating_income": {
        FREQ_QUARTERLY: "quarterlyOperatingIncome",
        FREQ_ANNUAL: "annualOperatingIncome",
        TTM: "trailingOperatingIncome",
    },
    "non_operating_interest_income_expense": {
        FREQ_QUARTERLY: "quarterlyNetNonOperatingInterestIncomeExpense",
        FREQ_ANNUAL: "annualNetNonOperatingInterestIncomeExpense",
        TTM: "trailingNetNonOperatingInterestIncomeExpense",
    },
    "other_income_expense": {
        FREQ_QUARTERLY: "quarterlyOtherIncomeExpense",
        FREQ_ANNUAL: "annualOtherIncomeExpense",
        TTM: "trailingOtherIncomeExpense",
    },
    "basic_eps": {
        FREQ_QUARTERLY: "quarterlyBasicEPS",
        FREQ_ANNUAL: "annualBasicEPS",
        TTM: "trailingBasicEPS",
    },
    "diluted_eps": {
        FREQ_QUARTERLY: "quarterlyDilutedEPS",
        FREQ_ANNUAL: "annualDilutedEPS",
        TTM: "trailingDilutedEPS",
    },
    "basic_average_shares": {
        FREQ_QUARTERLY: "quarterlyBasicAverageShares",
        FREQ_ANNUAL: "annualBasicAverageShares",
        TTM: "trailingBasicAverageShares",
    },
    "total_expense": {
        FREQ_QUARTERLY: "quarterlyTotalExpenses",
        FREQ_ANNUAL: "annualTotalExpenses",
        TTM: "trailingTotalExpenses",
    },
    "normalized_income": {
        FREQ_QUARTERLY: "quarterlyNormalizedIncome",
        FREQ_ANNUAL: "annualNormalizedIncome",
        TTM: "trailingNormalizedIncome",
    },
    "ebit": {
        FREQ_QUARTERLY: "quarterlyEBIT",
        FREQ_ANNUAL: "annualEBIT",
        TTM: "trailingEBIT",
    },
    "ebitda": {
        FREQ_QUARTERLY: "quarterlyEBITDA",
        FREQ_ANNUAL: "annualEBITDA",
        TTM: "trailingEBITDA",
    },
}

MAPPING_BALANCE_METRICS = {
    "total_assets": {
        FREQ_QUARTERLY: "quarterlyTotalAssets",
        FREQ_ANNUAL: "annualTotalAssets",
    },
    "total_liabilities_net_minority_interest": {
        FREQ_QUARTERLY: "quarterlyTotalLiabilitiesNetMinorityInterest",
        FREQ_ANNUAL: "annualTotalLiabilitiesNetMinorityInterest",
    },
    "total_equity_gross_minority_interest": {
        FREQ_QUARTERLY: "quarterlyTotalEquityGrossMinorityInterest",
        FREQ_ANNUAL: "annualTotalEquityGrossMinorityInterest",
    },
    "total_capitalization": {
        FREQ_QUARTERLY: "quarterlyTotalCapitalization",
        FREQ_ANNUAL: "annualTotalCapitalization",
    },
    "common_stock_equity": {
        FREQ_QUARTERLY: "quarterlyCommonStockEquity",
        FREQ_ANNUAL: "annualCommonStockEquity",
    },
    "capital_lease_obligations": {
        FREQ_QUARTERLY: "quarterlyCapitalLeaseObligations",
        FREQ_ANNUAL: "annualCapitalLeaseObligations",
    },
    "net_tangible_assets": {
        FREQ_QUARTERLY: "quarterlyNetTangibleAssets",
        FREQ_ANNUAL: "annualNetTangibleAssets",
    },
    "working_capital": {
        FREQ_QUARTERLY: "quarterlyWorkingCapital",
        FREQ_ANNUAL: "annualWorkingCapital",
    },
    "invested_capital": {
        FREQ_QUARTERLY: "quarterlyInvestedCapital",
        FREQ_ANNUAL: "annualInvestedCapital",
    },
    "tangible_book_value": {
        FREQ_QUARTERLY: "quarterlyTangibleBookValue",
        FREQ_ANNUAL: "annualTangibleBookValue",
    },
    "total_debt": {
        FREQ_QUARTERLY: "quarterlyTotalDebt",
        FREQ_ANNUAL: "annualTotalDebt",
    },
    "net_debt": {
        FREQ_QUARTERLY: "quarterlyNetDebt",
        FREQ_ANNUAL: "annualNetDebt",
    },
    "share_issued": {
        FREQ_QUARTERLY: "quarterlyShareIssued",
        FREQ_ANNUAL: "annualShareIssued",
    },
    "ordinary_shares_number": {
        FREQ_QUARTERLY: "quarterlyOrdinarySharesNumber",
        FREQ_ANNUAL: "annualOrdinarySharesNumber",
    },
}


BROWSERS = ["chrome", "edge", "firefox"]
