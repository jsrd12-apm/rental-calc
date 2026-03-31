# rental-calc

Rental property financial calculators for investors and landlords. No dependencies, pure Python.

Built by landlords who use these calculations to evaluate real deals on real properties.

## What's Included

**Acquisition Analysis:** Net Operating Income (NOI), Cap Rate, Cash-on-Cash Return, Gross Rent Multiplier, Rent-to-Price Ratio (1% Rule test), Break-Even Ratio, Debt Service Coverage Ratio

**Mortgage & Financing:** Monthly payment calculator, full amortization schedule with optional extra payments, Loan-to-Value ratio

**Tax & Depreciation:** Straight-line depreciation (residential 27.5yr, commercial 39yr), full depreciation schedule, capital gains tax estimator with depreciation recapture

**Complete Deal Analyzer:** Run all metrics at once with `analyze_property()` — one function call, full picture.

## Quick Start

```python
from rental_calc import analyze_property

result = analyze_property(
    purchase_price=250000,
    monthly_rent=2000,
    down_payment_pct=0.25,
    interest_rate=0.07,
    annual_operating_expenses=9600
)

print(f"Cap Rate: {result['cap_rate_pct']}%")
print(f"Cash-on-Cash: {result['cash_on_cash_pct']}%")
print(f"Monthly Cash Flow: ${result['monthly_cashflow']}")
print(f"1% Rule: {result['one_pct_rule']}")
```

## CLI Demo

```bash
python rental_calc.py
```

Outputs a formatted analysis of a sample property showing all key metrics.

## Individual Calculators

```python
from rental_calc import *

# NOI
noi = net_operating_income(
    gross_rent=24000,
    vacancy_rate=0.05,
    operating_expenses=9600
)

# Cap Rate
cap = cap_rate(noi=13200, purchase_price=250000)

# Mortgage Payment
payment = monthly_mortgage_payment(
    principal=200000,
    annual_rate=0.07,
    years=30
)

# Full Amortization Schedule
schedule = amortization_schedule(200000, 0.07, 30)
print(f"Total interest paid: ${schedule[-1].cumulative_interest:,.2f}")

# Depreciation Schedule
dep = depreciation_schedule(
    cost_basis=250000,
    land_value=50000,
    method='residential'
)

# Capital Gains Tax Estimate
tax = capital_gains_tax_estimate(
    sale_price=350000,
    original_cost_basis=250000,
    accumulated_depreciation=36364,
    selling_costs=21000
)
print(f"Estimated tax: ${tax['total_estimated_tax']:,.2f}")
```

## All Functions

| Function | Description |
|----------|-------------|
| `net_operating_income()` | NOI = Effective Income - Operating Expenses |
| `cap_rate()` | Cap Rate = NOI / Purchase Price |
| `cash_on_cash_return()` | CoC = Cash Flow / Cash Invested |
| `gross_rent_multiplier()` | GRM = Price / Annual Rent |
| `rent_to_price_ratio()` | Monthly Rent / Price (1% Rule) |
| `break_even_ratio()` | (Expenses + Debt) / Income |
| `debt_service_coverage_ratio()` | DSCR = NOI / Debt Service |
| `monthly_mortgage_payment()` | Standard amortization P&I |
| `amortization_schedule()` | Full schedule with extra payments |
| `loan_to_value()` | LTV = Loan / Value |
| `operating_expense_ratio()` | OER = Expenses / Income |
| `price_per_unit()` | Multi-family comparison |
| `cost_per_sqft()` | Price per square foot |
| `rent_per_sqft()` | Rent per square foot |
| `annual_depreciation()` | IRS straight-line (27.5yr / 39yr) |
| `depreciation_schedule()` | Full schedule with book values |
| `capital_gains_tax_estimate()` | Sale tax with recapture |
| `analyze_property()` | All metrics in one call |

## No Dependencies

Zero external packages. Works with Python 3.7+. Just download `rental_calc.py` and import it.

## License

MIT License — use it however you want.

## About

Part of the [APM (Assistant Property Manager)](https://jsrd12-apm.github.io) open-source toolkit for landlords.
