from decimal import Decimal
from app.models.urla_2021_v1.urla_2021_v1 import Application, Borrower


def total_monthly_income(borrower: Borrower) -> Decimal:
    current = borrower.employment.current_employment.gross_monthly_income
    base_total = current.total if current else Decimal("0.0")
    other = borrower.employment.total_other_income or Decimal("0.0")
    return Decimal(base_total) + Decimal(other)


def total_monthly_debt(borrower: Borrower) -> Decimal:
    liab_payments = sum(l.monthly_payment for l in borrower.assets_and_liabilities.liabilities)
    other_expenses = sum(e.monthly_payment for e in borrower.assets_and_liabilities.other_liabilities_and_expenses)
    housing = borrower.personal_information.current_address.housing_expense_amount
    return Decimal(liab_payments) + Decimal(other_expenses) + Decimal(housing)


def dti_ratio(borrower: Borrower) -> Decimal:
    income = total_monthly_income(borrower)
    if income <= 0:
        return Decimal("0.0")
    debt = total_monthly_debt(borrower)
    return Decimal(debt) / Decimal(income)


def total_assets(borrower: Borrower) -> Decimal:
    accounts_sum = sum(a.cash_or_market_value for a in borrower.assets_and_liabilities.assets_accounts)
    other_assets_sum = sum(o.cash_or_market_value for o in borrower.assets_and_liabilities.other_assets_and_credits)
    return Decimal(accounts_sum) + Decimal(other_assets_sum)


def total_liabilities(borrower: Borrower) -> Decimal:
    return sum(l.unpaid_balance for l in borrower.assets_and_liabilities.liabilities)
