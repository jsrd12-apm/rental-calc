"""
Rental Property Financial Calculators
======================================
A collection of financial calculators for rental property investors.
Covers acquisition analysis, ongoing performance metrics, and tax-related calculations.

Built by landlords, for landlords.
https://github.com/jsrd12-apm

Usage:
    from rental_calc import *
    
    # Analyze a potential purchase
    noi = net_operating_income(gross_rent=24000, vacancy_rate=0.05, operating_expenses=9600)
    cap = cap_rate(noi=noi, purchase_price=250000)
    coc = cash_on_cash_return(annual_cashflow=noi - 12000, total_cash_invested=62500)
    
    # Generate a mortgage amortization schedule
    schedule = amortization_schedule(principal=200000, annual_rate=0.07, years=30)
    
    # Calculate depreciation
    dep = annual_depreciation(cost_basis=220000, land_value=50000)
"""

from dataclasses import dataclass
from typing import Optional


# =============================================================================
# ACQUISITION ANALYSIS
# =============================================================================

def net_operating_income(
    gross_rent: float,
    vacancy_rate: float = 0.05,
    operating_expenses: float = 0.0,
    other_income: float = 0.0
) -> float:
    """
    Calculate Net Operating Income (NOI).
    
    NOI = Effective Gross Income - Operating Expenses
    
    Args:
        gross_rent: Total annual scheduled rent (all units combined)
        vacancy_rate: Expected vacancy as decimal (default 5%)
        operating_expenses: Total annual operating expenses
                           (taxes, insurance, maintenance, management, etc.)
                           Does NOT include mortgage payments.
        other_income: Laundry, parking, late fees, pet fees, etc.
    
    Returns:
        Annual Net Operating Income
    
    Example:
        >>> net_operating_income(24000, vacancy_rate=0.05, operating_expenses=9600)
        13200.0
    """
    effective_gross_income = (gross_rent * (1 - vacancy_rate)) + other_income
    return effective_gross_income - operating_expenses


def cap_rate(noi: float, purchase_price: float) -> float:
    """
    Calculate Capitalization Rate.
    
    Cap Rate = NOI / Purchase Price
    
    A higher cap rate means higher potential return but often higher risk.
    Typical ranges: 4-6% (low risk/urban), 8-12% (higher risk/rural).
    
    Args:
        noi: Annual Net Operating Income
        purchase_price: Total purchase price of the property
    
    Returns:
        Cap rate as decimal (multiply by 100 for percentage)
    
    Example:
        >>> cap_rate(noi=13200, purchase_price=250000)
        0.0528
    """
    if purchase_price == 0:
        raise ValueError("Purchase price cannot be zero")
    return noi / purchase_price


def cash_on_cash_return(annual_cashflow: float, total_cash_invested: float) -> float:
    """
    Calculate Cash-on-Cash Return.
    
    CoC = Annual Pre-Tax Cash Flow / Total Cash Invested
    
    Unlike cap rate, this accounts for financing. Measures return on YOUR money.
    
    Args:
        annual_cashflow: NOI minus annual debt service (mortgage payments)
        total_cash_invested: Down payment + closing costs + rehab costs
    
    Returns:
        Cash-on-cash return as decimal
    
    Example:
        >>> cash_on_cash_return(annual_cashflow=4800, total_cash_invested=62500)
        0.0768
    """
    if total_cash_invested == 0:
        raise ValueError("Total cash invested cannot be zero")
    return annual_cashflow / total_cash_invested


def gross_rent_multiplier(purchase_price: float, gross_annual_rent: float) -> float:
    """
    Calculate Gross Rent Multiplier (GRM).
    
    GRM = Purchase Price / Gross Annual Rent
    
    Quick screening metric. Lower GRM = potentially better deal.
    Typical range: 4-10 depending on market.
    
    Args:
        purchase_price: Total purchase price
        gross_annual_rent: Total annual scheduled rent
    
    Returns:
        Gross Rent Multiplier (number of years of gross rent to pay off purchase)
    
    Example:
        >>> gross_rent_multiplier(250000, 24000)
        10.42
    """
    if gross_annual_rent == 0:
        raise ValueError("Gross annual rent cannot be zero")
    return round(purchase_price / gross_annual_rent, 2)


def rent_to_price_ratio(monthly_rent: float, purchase_price: float) -> float:
    """
    Calculate the Rent-to-Price Ratio (the '1% Rule' test).
    
    Ratio = Monthly Rent / Purchase Price
    
    The '1% rule' suggests monthly rent should be >= 1% of purchase price.
    The '2% rule' is more aggressive (often unrealistic in most markets).
    
    Args:
        monthly_rent: Total monthly rent for the property
        purchase_price: Total purchase price
    
    Returns:
        Rent-to-price ratio as decimal
    
    Example:
        >>> rent_to_price_ratio(2000, 250000)
        0.008  # Below the 1% rule
    """
    if purchase_price == 0:
        raise ValueError("Purchase price cannot be zero")
    return monthly_rent / purchase_price


def break_even_ratio(
    operating_expenses: float,
    debt_service: float,
    gross_operating_income: float
) -> float:
    """
    Calculate Break-Even Ratio (BER).
    
    BER = (Operating Expenses + Debt Service) / Gross Operating Income
    
    Shows what percentage of income is needed to cover all costs.
    Below 85% is generally considered healthy.
    
    Args:
        operating_expenses: Annual operating expenses
        debt_service: Annual mortgage payments (P&I)
        gross_operating_income: Gross rent minus vacancy
    
    Returns:
        Break-even ratio as decimal
    
    Example:
        >>> break_even_ratio(9600, 15972, 22800)
        1.12  # Over 100% = losing money
    """
    if gross_operating_income == 0:
        raise ValueError("Gross operating income cannot be zero")
    return (operating_expenses + debt_service) / gross_operating_income


def debt_service_coverage_ratio(noi: float, annual_debt_service: float) -> float:
    """
    Calculate Debt Service Coverage Ratio (DSCR).
    
    DSCR = NOI / Annual Debt Service
    
    Lenders typically require DSCR >= 1.2 for investment properties.
    Below 1.0 means the property doesn't cover its mortgage.
    
    Args:
        noi: Annual Net Operating Income
        annual_debt_service: Annual mortgage payments (P&I)
    
    Returns:
        DSCR ratio
    
    Example:
        >>> debt_service_coverage_ratio(13200, 15972)
        0.83  # Below 1.0 = negative cash flow
    """
    if annual_debt_service == 0:
        raise ValueError("Annual debt service cannot be zero")
    return noi / annual_debt_service


# =============================================================================
# MORTGAGE & FINANCING
# =============================================================================

def monthly_mortgage_payment(
    principal: float,
    annual_rate: float,
    years: int
) -> float:
    """
    Calculate monthly mortgage payment (P&I only, no escrow).
    
    Uses standard amortization formula:
    M = P * [r(1+r)^n] / [(1+r)^n - 1]
    
    Args:
        principal: Loan amount
        annual_rate: Annual interest rate as decimal (e.g., 0.07 for 7%)
        years: Loan term in years
    
    Returns:
        Monthly payment amount (principal + interest only)
    
    Example:
        >>> monthly_mortgage_payment(200000, 0.07, 30)
        1330.60
    """
    monthly_rate = annual_rate / 12
    num_payments = years * 12
    
    if monthly_rate == 0:
        return principal / num_payments
    
    payment = principal * (monthly_rate * (1 + monthly_rate) ** num_payments) / \
              ((1 + monthly_rate) ** num_payments - 1)
    return round(payment, 2)


@dataclass
class AmortizationRow:
    """Single row in an amortization schedule."""
    month: int
    payment: float
    principal: float
    interest: float
    balance: float
    cumulative_interest: float
    cumulative_principal: float


def amortization_schedule(
    principal: float,
    annual_rate: float,
    years: int,
    extra_payment: float = 0.0
) -> list:
    """
    Generate a full mortgage amortization schedule.
    
    Args:
        principal: Loan amount
        annual_rate: Annual interest rate as decimal
        years: Loan term in years
        extra_payment: Additional monthly principal payment (default 0)
    
    Returns:
        List of AmortizationRow objects, one per month
    
    Example:
        >>> schedule = amortization_schedule(200000, 0.07, 30)
        >>> schedule[0].interest   # First month interest
        1166.67
        >>> schedule[0].principal  # First month principal
        163.94
        >>> schedule[-1].balance   # Final balance
        0.0
        >>> schedule[-1].cumulative_interest  # Total interest paid
        279017.80
    """
    monthly_rate = annual_rate / 12
    base_payment = monthly_mortgage_payment(principal, annual_rate, years)
    total_payment = base_payment + extra_payment
    
    balance = principal
    cumulative_interest = 0
    cumulative_principal = 0
    schedule = []
    month = 0
    
    while balance > 0.01 and month < years * 12:
        month += 1
        interest = round(balance * monthly_rate, 2)
        principal_paid = min(round(total_payment - interest, 2), round(balance, 2))
        
        if principal_paid < 0:
            principal_paid = 0
        
        balance = round(balance - principal_paid, 2)
        cumulative_interest = round(cumulative_interest + interest, 2)
        cumulative_principal = round(cumulative_principal + principal_paid, 2)
        
        schedule.append(AmortizationRow(
            month=month,
            payment=round(principal_paid + interest, 2),
            principal=principal_paid,
            interest=interest,
            balance=max(balance, 0),
            cumulative_interest=cumulative_interest,
            cumulative_principal=cumulative_principal
        ))
    
    return schedule


def loan_to_value(loan_amount: float, property_value: float) -> float:
    """
    Calculate Loan-to-Value ratio.
    
    LTV = Loan Amount / Property Value
    
    Investment properties typically require LTV <= 75-80%.
    
    Args:
        loan_amount: Current mortgage balance
        property_value: Current appraised or estimated value
    
    Returns:
        LTV as decimal
    
    Example:
        >>> loan_to_value(200000, 250000)
        0.8  # 80% LTV
    """
    if property_value == 0:
        raise ValueError("Property value cannot be zero")
    return loan_amount / property_value


# =============================================================================
# PROPERTY PERFORMANCE
# =============================================================================

def operating_expense_ratio(operating_expenses: float, gross_income: float) -> float:
    """
    Calculate Operating Expense Ratio.
    
    OER = Operating Expenses / Gross Operating Income
    
    Typical range: 35-80% depending on property type and market.
    Higher ratios may indicate deferred maintenance or mismanagement.
    
    Args:
        operating_expenses: Total annual operating expenses
        gross_income: Effective gross income (after vacancy)
    
    Returns:
        OER as decimal
    """
    if gross_income == 0:
        raise ValueError("Gross income cannot be zero")
    return operating_expenses / gross_income


def price_per_unit(purchase_price: float, num_units: int) -> float:
    """
    Calculate price per unit for multi-family analysis.
    
    Useful for comparing properties of different sizes.
    
    Args:
        purchase_price: Total purchase price
        num_units: Number of rental units
    
    Returns:
        Price per unit
    
    Example:
        >>> price_per_unit(500000, 4)
        125000.0
    """
    if num_units == 0:
        raise ValueError("Number of units cannot be zero")
    return purchase_price / num_units


def cost_per_sqft(purchase_price: float, total_sqft: float) -> float:
    """
    Calculate cost per square foot.
    
    Args:
        purchase_price: Total purchase price
        total_sqft: Total rentable square footage
    
    Returns:
        Cost per square foot
    """
    if total_sqft == 0:
        raise ValueError("Total square footage cannot be zero")
    return round(purchase_price / total_sqft, 2)


def rent_per_sqft(monthly_rent: float, sqft: float) -> float:
    """
    Calculate monthly rent per square foot.
    
    Useful for comparing rents across different-sized units.
    
    Args:
        monthly_rent: Monthly rent amount
        sqft: Unit square footage
    
    Returns:
        Monthly rent per square foot
    """
    if sqft == 0:
        raise ValueError("Square footage cannot be zero")
    return round(monthly_rent / sqft, 2)


# =============================================================================
# TAX & DEPRECIATION
# =============================================================================

def annual_depreciation(
    cost_basis: float,
    land_value: float,
    method: str = "residential",
    year: int = 1
) -> float:
    """
    Calculate annual straight-line depreciation for rental property.
    
    IRS rules:
    - Residential rental: 27.5 years
    - Commercial: 39 years
    
    Land is NOT depreciable. Only the building/improvements portion.
    
    Args:
        cost_basis: Total purchase price + closing costs + improvements
        land_value: Assessed land value (from tax assessment or appraisal)
        method: 'residential' (27.5 yrs) or 'commercial' (39 yrs)
        year: Which year of ownership (for partial first/last year handling)
    
    Returns:
        Annual depreciation amount
    
    Example:
        >>> annual_depreciation(250000, 50000, method='residential')
        7272.73  # ($250K - $50K land) / 27.5 years
    """
    depreciable_basis = cost_basis - land_value
    
    if depreciable_basis <= 0:
        raise ValueError("Depreciable basis must be positive (cost_basis > land_value)")
    
    if method == "residential":
        useful_life = 27.5
    elif method == "commercial":
        useful_life = 39.0
    else:
        raise ValueError("Method must be 'residential' or 'commercial'")
    
    return round(depreciable_basis / useful_life, 2)


@dataclass
class DepreciationRow:
    """Single year in a depreciation schedule."""
    year: int
    annual_depreciation: float
    accumulated_depreciation: float
    book_value: float


def depreciation_schedule(
    cost_basis: float,
    land_value: float,
    method: str = "residential"
) -> list:
    """
    Generate a full depreciation schedule.
    
    Args:
        cost_basis: Total cost basis (purchase + closing + improvements)
        land_value: Non-depreciable land value
        method: 'residential' (27.5 yrs) or 'commercial' (39 yrs)
    
    Returns:
        List of DepreciationRow objects, one per year
    
    Example:
        >>> schedule = depreciation_schedule(250000, 50000)
        >>> len(schedule)
        28  # 27.5 years rounds to 28 rows (last year is partial)
        >>> schedule[0].annual_depreciation
        7272.73
        >>> schedule[-1].book_value
        50000.0  # Land value remains
    """
    depreciable_basis = cost_basis - land_value
    annual_dep = annual_depreciation(cost_basis, land_value, method)
    
    useful_life = 27.5 if method == "residential" else 39.0
    full_years = int(useful_life)
    partial_year_fraction = useful_life - full_years
    
    schedule = []
    accumulated = 0
    
    for year in range(1, full_years + 1):
        accumulated = round(accumulated + annual_dep, 2)
        book_value = round(cost_basis - accumulated, 2)
        schedule.append(DepreciationRow(
            year=year,
            annual_depreciation=annual_dep,
            accumulated_depreciation=accumulated,
            book_value=book_value
        ))
    
    # Handle partial final year
    if partial_year_fraction > 0:
        final_dep = round(annual_dep * partial_year_fraction, 2)
        remaining = round(depreciable_basis - accumulated, 2)
        final_dep = min(final_dep, remaining)
        accumulated = round(accumulated + final_dep, 2)
        schedule.append(DepreciationRow(
            year=full_years + 1,
            annual_depreciation=final_dep,
            accumulated_depreciation=accumulated,
            book_value=round(cost_basis - accumulated, 2)
        ))
    
    return schedule


def capital_gains_tax_estimate(
    sale_price: float,
    original_cost_basis: float,
    accumulated_depreciation: float,
    selling_costs: float = 0.0,
    capital_improvements: float = 0.0,
    holding_period_months: int = 24,
    federal_tax_bracket: float = 0.22,
    state_tax_rate: float = 0.0
) -> dict:
    """
    Estimate capital gains tax on property sale.
    
    Accounts for depreciation recapture (taxed at 25%) and
    long-term capital gains.
    
    Args:
        sale_price: Gross sale price
        original_cost_basis: Original purchase price + closing costs
        accumulated_depreciation: Total depreciation taken
        selling_costs: Agent commissions, closing costs, etc.
        capital_improvements: Value of improvements added to basis
        holding_period_months: How long property was held
        federal_tax_bracket: Marginal tax bracket for ordinary income
        state_tax_rate: State capital gains tax rate
    
    Returns:
        Dictionary with gain breakdown and estimated taxes
    
    Example:
        >>> capital_gains_tax_estimate(
        ...     sale_price=350000,
        ...     original_cost_basis=250000,
        ...     accumulated_depreciation=36364,
        ...     selling_costs=21000
        ... )
    """
    adjusted_basis = original_cost_basis + capital_improvements - accumulated_depreciation
    net_sale_price = sale_price - selling_costs
    total_gain = net_sale_price - adjusted_basis
    
    is_long_term = holding_period_months > 12
    
    # Depreciation recapture (taxed at 25% federal)
    depreciation_recapture = min(accumulated_depreciation, max(total_gain, 0))
    
    # Remaining capital gain
    remaining_gain = max(total_gain - depreciation_recapture, 0)
    
    # Tax calculations
    if is_long_term:
        recapture_tax = depreciation_recapture * 0.25
        # Long-term capital gains rate (simplified - actual depends on income)
        capital_gains_tax = remaining_gain * 0.15
    else:
        # Short-term = ordinary income rates
        recapture_tax = depreciation_recapture * federal_tax_bracket
        capital_gains_tax = remaining_gain * federal_tax_bracket
    
    state_tax = total_gain * state_tax_rate if total_gain > 0 else 0
    total_tax = round(recapture_tax + capital_gains_tax + state_tax, 2)
    
    return {
        "sale_price": sale_price,
        "selling_costs": selling_costs,
        "net_sale_price": net_sale_price,
        "original_cost_basis": original_cost_basis,
        "capital_improvements": capital_improvements,
        "accumulated_depreciation": accumulated_depreciation,
        "adjusted_basis": adjusted_basis,
        "total_gain": round(total_gain, 2),
        "depreciation_recapture": round(depreciation_recapture, 2),
        "remaining_capital_gain": round(remaining_gain, 2),
        "is_long_term": is_long_term,
        "depreciation_recapture_tax": round(recapture_tax, 2),
        "capital_gains_tax": round(capital_gains_tax, 2),
        "state_tax": round(state_tax, 2),
        "total_estimated_tax": total_tax,
        "net_proceeds_after_tax": round(net_sale_price - total_tax, 2),
        "note": "This is an estimate only. Consult a tax professional for actual liability."
    }


# =============================================================================
# PROPERTY ANALYSIS REPORT
# =============================================================================

def analyze_property(
    purchase_price: float,
    monthly_rent: float,
    down_payment_pct: float = 0.25,
    interest_rate: float = 0.07,
    loan_term_years: int = 30,
    closing_costs: float = 0.0,
    rehab_costs: float = 0.0,
    vacancy_rate: float = 0.05,
    annual_operating_expenses: float = 0.0,
    land_value_pct: float = 0.20,
    other_monthly_income: float = 0.0
) -> dict:
    """
    Complete property analysis — run all key metrics at once.
    
    This is the function most investors will use for quick deal analysis.
    
    Args:
        purchase_price: Total purchase price
        monthly_rent: Total monthly rent (all units)
        down_payment_pct: Down payment as decimal (default 25%)
        interest_rate: Annual mortgage rate as decimal
        loan_term_years: Mortgage term
        closing_costs: Buyer closing costs
        rehab_costs: Renovation costs
        vacancy_rate: Expected vacancy rate
        annual_operating_expenses: Annual opex (taxes, insurance, maintenance, etc.)
        land_value_pct: Land value as percentage of purchase price
        other_monthly_income: Additional monthly income (parking, laundry, etc.)
    
    Returns:
        Dictionary with all key metrics
    
    Example:
        >>> result = analyze_property(
        ...     purchase_price=250000,
        ...     monthly_rent=2000,
        ...     annual_operating_expenses=9600
        ... )
        >>> print(f"Cap Rate: {result['cap_rate_pct']}%")
        >>> print(f"Cash-on-Cash: {result['cash_on_cash_pct']}%")
        >>> print(f"Monthly Cash Flow: ${result['monthly_cashflow']}")
    """
    # Financing
    down_payment = purchase_price * down_payment_pct
    loan_amount = purchase_price - down_payment
    total_cash_invested = down_payment + closing_costs + rehab_costs
    monthly_payment = monthly_mortgage_payment(loan_amount, interest_rate, loan_term_years)
    annual_debt_service = monthly_payment * 12
    
    # Income
    gross_annual_rent = monthly_rent * 12
    other_annual_income = other_monthly_income * 12
    
    # NOI
    noi = net_operating_income(
        gross_rent=gross_annual_rent,
        vacancy_rate=vacancy_rate,
        operating_expenses=annual_operating_expenses,
        other_income=other_annual_income
    )
    
    # Cash flow
    annual_cashflow = noi - annual_debt_service
    monthly_cashflow = round(annual_cashflow / 12, 2)
    
    # Depreciation
    land_value = purchase_price * land_value_pct
    annual_dep = annual_depreciation(purchase_price + closing_costs, land_value)
    
    # Metrics
    cap = cap_rate(noi, purchase_price)
    coc = cash_on_cash_return(annual_cashflow, total_cash_invested) if total_cash_invested > 0 else 0
    grm = gross_rent_multiplier(purchase_price, gross_annual_rent)
    rtp = rent_to_price_ratio(monthly_rent, purchase_price)
    dscr = debt_service_coverage_ratio(noi, annual_debt_service) if annual_debt_service > 0 else float('inf')
    ber = break_even_ratio(annual_operating_expenses, annual_debt_service, gross_annual_rent * (1 - vacancy_rate))
    ltv = loan_to_value(loan_amount, purchase_price)
    oer = operating_expense_ratio(annual_operating_expenses, gross_annual_rent * (1 - vacancy_rate))
    
    return {
        "purchase_price": purchase_price,
        "down_payment": down_payment,
        "loan_amount": loan_amount,
        "total_cash_invested": total_cash_invested,
        "monthly_mortgage_payment": monthly_payment,
        "annual_debt_service": annual_debt_service,
        "gross_annual_rent": gross_annual_rent,
        "net_operating_income": noi,
        "annual_cashflow": round(annual_cashflow, 2),
        "monthly_cashflow": monthly_cashflow,
        "annual_depreciation": annual_dep,
        "cap_rate": round(cap, 4),
        "cap_rate_pct": round(cap * 100, 2),
        "cash_on_cash": round(coc, 4),
        "cash_on_cash_pct": round(coc * 100, 2),
        "gross_rent_multiplier": grm,
        "rent_to_price_ratio": round(rtp, 4),
        "one_pct_rule": "PASS" if rtp >= 0.01 else "FAIL",
        "dscr": round(dscr, 2),
        "break_even_ratio": round(ber, 4),
        "break_even_pct": round(ber * 100, 2),
        "ltv": round(ltv, 4),
        "ltv_pct": round(ltv * 100, 2),
        "operating_expense_ratio": round(oer, 4),
        "operating_expense_ratio_pct": round(oer * 100, 2),
    }


# =============================================================================
# CLI INTERFACE
# =============================================================================

if __name__ == "__main__":
    import sys
    
    print("=" * 60)
    print("  APM Rental Property Analyzer")
    print("  https://github.com/jsrd12-apm")
    print("=" * 60)
    
    # Demo analysis
    result = analyze_property(
        purchase_price=250000,
        monthly_rent=2000,
        down_payment_pct=0.25,
        interest_rate=0.07,
        loan_term_years=30,
        closing_costs=5000,
        vacancy_rate=0.05,
        annual_operating_expenses=9600,
    )
    
    print(f"\n  SAMPLE ANALYSIS: $250,000 property, $2,000/mo rent")
    print("-" * 60)
    print(f"  Purchase Price:        ${result['purchase_price']:>12,.2f}")
    print(f"  Down Payment (25%):    ${result['down_payment']:>12,.2f}")
    print(f"  Loan Amount:           ${result['loan_amount']:>12,.2f}")
    print(f"  Monthly Mortgage:      ${result['monthly_mortgage_payment']:>12,.2f}")
    print("-" * 60)
    print(f"  Gross Annual Rent:     ${result['gross_annual_rent']:>12,.2f}")
    print(f"  Net Operating Income:  ${result['net_operating_income']:>12,.2f}")
    print(f"  Annual Cash Flow:      ${result['annual_cashflow']:>12,.2f}")
    print(f"  Monthly Cash Flow:     ${result['monthly_cashflow']:>12,.2f}")
    print("-" * 60)
    print(f"  Cap Rate:              {result['cap_rate_pct']:>11.2f}%")
    print(f"  Cash-on-Cash Return:   {result['cash_on_cash_pct']:>11.2f}%")
    print(f"  GRM:                   {result['gross_rent_multiplier']:>11.2f}")
    print(f"  1% Rule:               {result['one_pct_rule']:>11}")
    print(f"  DSCR:                  {result['dscr']:>11.2f}")
    print(f"  Break-Even Ratio:      {result['break_even_pct']:>10.2f}%")
    print(f"  LTV:                   {result['ltv_pct']:>10.2f}%")
    print(f"  Operating Expense %:   {result['operating_expense_ratio_pct']:>10.2f}%")
    print(f"  Annual Depreciation:   ${result['annual_depreciation']:>12,.2f}")
    print("=" * 60)
    print("  Note: For informational purposes only.")
    print("  Consult a financial advisor for investment decisions.")
    print("=" * 60)
