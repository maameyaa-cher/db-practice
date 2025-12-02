import pytest
from decimal import Decimal
from app.models.urla_2021_v1 import urla_2021_v1 as urla
from app.services.calculations import (
    total_monthly_income,
    total_monthly_debt,
    dti_ratio,
    total_assets,
    total_liabilities,
)

# Helper to create a minimally viable borrower for testing
def create_mock_borrower() -> urla.Borrower:
    """Creates a Borrower object with default empty values for testing."""
    return urla.Borrower(
        personal_information=urla.PersonalInformation(
            first_name="John",
            last_name="Doe",
            ssn_or_itin="123-456-7890",
            date_of_birth="1990-01-01",
            citizenship="US_CITIZEN",
            type_of_credit="INDIVIDUAL",
            marital_status="MARRIED",
            contact_information=urla.ContactInformation(
                email="john.doe@example.com"
            ),
            current_address=urla.HousingAddress(
                street="123 Main St",
                city="Anytown",
                state="CA",
                zip="12345",
                years_at_address=2,
                months_at_address=3,
                housing_expense_type="RENT",
                housing_expense_amount=0
            )
        ),
        employment=urla.EmploymentSection(
            current_employment=urla.EmploymentRecord(
                employer_name="Default Corp",
                gross_monthly_income=urla.GrossMonthlyIncome(base=0, total=0)
            )
        ),
        assets_and_liabilities=urla.AssetsAndLiabilitiesSection(),
        declarations=urla.Declarations(
            will_occupy_as_primary_residence=True,
            had_ownership_interest_last_three_years=False,
            has_relationship_with_seller=False,
            borrowing_additional_money_for_transaction=False,
            applying_for_other_mortgage_before_closing=False,
            applying_for_new_credit_before_closing=False,
            property_subject_to_senior_lien=False,
            is_cosigner_on_undisclosed_debt=False,
            has_outstanding_judgments=False,
            delinquent_or_default_on_federal_debt=False,
            party_to_lawsuit_with_financial_liability=False,
            conveyed_title_in_lieu_of_foreclosure_past_7_years=False,
            completed_short_sale_past_7_years=False,
            had_property_foreclosed_past_7_years=False,
            declared_bankruptcy_past_7_years=False,
        ),
        military_service=urla.MilitaryService(),
        demographic_information=urla.DemographicInformation(
            ethnicity="NOT_PROVIDED",
            sex="NOT_PROVIDED",
            race=urla.RaceDetail(),
            collected_based_on_visual_observation=urla.CollectedBasedOnVisualObservation(),
            collection_method="EMAIL_OR_INTERNET",
        ),
        acknowledgments_and_agreements=urla.AcknowledgmentsAndAgreements(),
        real_estate=urla.RealEstateSection(owns_any_real_estate=False),
    )

def test_total_monthly_income():
    borrower = create_mock_borrower()
    borrower.employment.current_employment.gross_monthly_income.base = Decimal("5000.00")
    borrower.employment.current_employment.gross_monthly_income.total = Decimal("5000.00")
    borrower.employment.total_other_income = Decimal("500.50")
    
    assert total_monthly_income(borrower) == Decimal("5500.50")

def test_total_monthly_income_no_other_income():
    borrower = create_mock_borrower()
    borrower.employment.current_employment.gross_monthly_income.base = Decimal("5000.00")
    borrower.employment.current_employment.gross_monthly_income.total = Decimal("5000.00")
    
    assert total_monthly_income(borrower) == Decimal("5000.00")

def test_total_monthly_debt():
    borrower = create_mock_borrower()
    borrower.personal_information.current_address.housing_expense_amount = Decimal("1200.00")
    borrower.assets_and_liabilities.liabilities = [
        urla.Liability(account_type="REVOLVING", company_name="Car Co", unpaid_balance=10000, monthly_payment=Decimal("350.00")),
        urla.Liability(account_type="INSTALLMENT", company_name="School", unpaid_balance=20000, monthly_payment=Decimal("150.25")),
    ]
    borrower.assets_and_liabilities.other_liabilities_and_expenses = [
        urla.OtherLiabilityOrExpense(expense_type="OTHER", monthly_payment=Decimal("50.00"))
    ]
    
    assert total_monthly_debt(borrower) == Decimal("1750.25")

def test_dti_ratio_normal():
    borrower = create_mock_borrower()
    # Income = 6000
    borrower.employment.current_employment.gross_monthly_income.base = Decimal("6000.00")
    borrower.employment.current_employment.gross_monthly_income.total = Decimal("6000.00")
    
    # Debt = 1500
    borrower.personal_information.current_address.housing_expense_amount = Decimal("1000.00")
    borrower.assets_and_liabilities.liabilities = [
        urla.Liability(account_type="INSTALLMENT", company_name="Debt Co", unpaid_balance=5000, monthly_payment=Decimal("500.00"))
    ]
    
    # DTI = 1500 / 6000 = 0.25
    assert dti_ratio(borrower) == Decimal("0.25")

def test_dti_ratio_zero_income():
    borrower = create_mock_borrower()
    borrower.employment.current_employment.gross_monthly_income.base = Decimal("0")
    borrower.employment.current_employment.gross_monthly_income.total = Decimal("0")
    borrower.personal_information.current_address.housing_expense_amount = Decimal("1000.00")
    
    assert dti_ratio(borrower) == Decimal("0.0")

def test_total_assets():
    borrower = create_mock_borrower()
    borrower.assets_and_liabilities.assets_accounts = [
        urla.AssetAccount(account_type="CHECKING", financial_institution="Bank A", cash_or_market_value=Decimal("10000.00")),
        urla.AssetAccount(account_type="SAVINGS", financial_institution="Bank B", cash_or_market_value=Decimal("25000.50")),
    ]
    borrower.assets_and_liabilities.other_assets_and_credits = [
        urla.OtherAssetOrCredit(asset_or_credit_type="OTHER", cash_or_market_value=Decimal("5000.00"))
    ]
    
    assert total_assets(borrower) == Decimal("40000.50")

def test_total_liabilities():
    borrower = create_mock_borrower()
    borrower.assets_and_liabilities.liabilities = [
        urla.Liability(account_type="INSTALLMENT", company_name="Car Co", monthly_payment=350, unpaid_balance=Decimal("15000.00")),
        urla.Liability(account_type="INSTALLMENT", company_name="Mortgage Co", monthly_payment=1200, unpaid_balance=Decimal("250000.00")),
    ]
    
    assert total_liabilities(borrower) == Decimal("265000.00")

def test_calculations_with_empty_borrower():
    borrower = create_mock_borrower()
    
    assert total_monthly_income(borrower) == Decimal("0.0")
    assert total_monthly_debt(borrower) == Decimal("0.0")
    assert dti_ratio(borrower) == Decimal("0.0")
    assert total_assets(borrower) == Decimal("0.0")
    assert total_liabilities(borrower) == Decimal("0.0")