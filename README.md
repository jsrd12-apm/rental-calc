# rental-calc

Rental property financial calculators for investors and landlords. No dependencies, pure Python.

Built by landlords who use these calculations to evaluate real deals on real properties.

## Highlights

**Full Deal Analyzer** — analyze_deal() runs a complete 5-year proforma with dual financing (mortgage + line of credit), carrying costs during rehab, tax deductions with depreciation, and net worth accumulation. Based on a real landlord's evaluation workflow for SFR acquisitions.

**18 Individual Calculators** — NOI, Cap Rate, Cash-on-Cash, DSCR, amortization schedules, depreciation schedules, capital gains tax estimates, and more.

**Zero Dependencies** — Pure Python 3.7+. Just download and import.

## Deal Analyzer

```python
from rental_calc import analyze_deal, print_deal_analysis

result = analyze_deal(
    address="1006 Potomac Ave, Portsmouth",
    purchase_price=85000,
    down_payment=1700,
    loan_interest_rate=7.5,
    loan_term_years=20,
    property_tax_rate_per_100=1.32,
    annual_insurance=550,
    monthly_maintenance=370,
    monthly_rent=1400,
    rent_increase_pct=3.0,
    prepaid_items=1097,
    closing_costs=3393,
)

print_deal_analysis(result)
```

## What Makes This Different

Most rental calculators give you a snapshot. This analyzer models what actually happens over time:

- **Dual financing**: Mortgage + optional line of credit with separate rates and terms
- **Carrying costs during rehab**: Mortgage/taxes/insurance paid while property sits vacant
- **Compounding inflation**: Insurance, taxes, and maintenance grow at configurable rate
- **Actual amortization interest**: Uses real amortization schedule, not flat estimates
- **Tax deductions**: Depreciation + interest + expenses, with configurable tax bracket
- **After-tax cash flow**: What you actually keep after the IRS
- **Net worth tracking**: Cash flow + principal paydown + appreciation = true wealth building
- **Breakeven price**: Maximum purchase price where the deal still works
- **Flexible tax rates**: Input your local property tax rate per $100 — works for any city

## Dual Financing (Mortgage + LOC)

Many landlords use a line of credit for down payments or rehab:

```python
result = analyze_deal(
    purchase_price=150000,
    down_payment=30000,
    loan_interest_rate=7.0,
    loan_term_years=30,
    loc_amount=20000,
    loc_interest_rate=11.5,
    loc_term_years=7,
    monthly_rent=1500,
    repairs_estimate=20000,
    months_to_rent=2,
)
```

## Individual Calculators

```python
from rental_calc import *

noi = net_operating_income(gross_rent=24000, vacancy_rate=0.05, operating_expenses=9600)
cap = cap_rate(noi=13200, purchase_price=250000)
payment = monthly_mortgage_payment(200000, 0.07, 30)
schedule = amortization_schedule(200000, 0.07, 30, extra_payment=200)
dep = depreciation_schedule(250000, 50000, method='residential')
tax = capital_gains_tax_estimate(sale_price=350000, original_cost_basis=250000, accumulated_depreciation=36364)
```

## All Functions

| Function | Description |
|----------|-------------|
| analyze_deal() | Full 5-year proforma with dual financing and tax impact |
| print_deal_analysis() | Pretty-print deal analysis results |
| analyze_property() | Quick snapshot of all key metrics |
| net_operating_income() | NOI = Effective Income - Operating Expenses |
| cap_rate() | Cap Rate = NOI / Purchase Price |
| cash_on_cash_return() | CoC = Cash Flow / Cash Invested |
| gross_rent_multiplier() | GRM = Price / Annual Rent |
| rent_to_price_ratio() | Monthly Rent / Price (1% Rule) |
| break_even_ratio() | (Expenses + Debt) / Income |
| debt_service_coverage_ratio() | DSCR = NOI / Debt Service |
| monthly_mortgage_payment() | Standard amortization P&I |
| amortization_schedule() | Full schedule with extra payments |
| loan_to_value() | LTV = Loan / Value |
| operating_expense_ratio() | OER = Expenses / Income |
| price_per_unit() | Multi-family comparison |
| annual_depreciation() | IRS straight-line (27.5yr / 39yr) |
| depreciation_schedule() | Full schedule with book values |
| capital_gains_tax_estimate() | Sale tax with depreciation recapture |

## License

MIT License

## About

Part of the [APM (Assistant Property Manager)](https://jsrd12-apm.github.io) open-source toolkit for landlords.
