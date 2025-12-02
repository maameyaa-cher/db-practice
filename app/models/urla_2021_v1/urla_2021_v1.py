from __future__ import annotations

from typing import List, Optional, Literal
from pydantic import BaseModel, EmailStr, conint, confloat, field_validator


"""
Application-level data model for URLA / 1003 (single borrower).

- Structured by official URLA sections:
  Section 1: Borrower Information
  Section 2: Financial Information (Assets/Liabilities)
  Section 3: Financial Information (Real Estate)
  Section 4: Loan and Property Information
  Section 5: Declarations
  Section 6: Acknowledgments and Agreements
  Section 7: Military Service
  Section 8: Demographic Information

"""

 
# Enums / Literals
 

CitizenshipType = Literal[
    "US_CITIZEN",
    "PERMANENT_RESIDENT_ALIEN",
    "NON_PERMANENT_RESIDENT_ALIEN",
]

TypeOfCredit = Literal["INDIVIDUAL", "JOINT"]

MaritalStatus = Literal["MARRIED", "SEPARATED", "UNMARRIED"]

HousingExpenseType = Literal["OWN", "RENT", "NONE"]

AccountType = Literal[
    "CHECKING",
    "SAVINGS",
    "MONEY_MARKET",
    "CD",
    "STOCKS",
    "BONDS",
    "MUTUAL_FUNDS",
    "RETIREMENT",
    "OTHER",
]

LiabilityAccountType = Literal[
    "REVOLVING",
    "INSTALLMENT",
    "OPEN_30_DAY",
    "LEASE",
    "OTHER",
]

OtherLiabilityExpenseType = Literal[
    "ALIMONY",
    "CHILD_SUPPORT",
    "SEPARATE_MAINTENANCE",
    "JOB_RELATED",
    "OTHER",
]

LoanPurposeType = Literal["PURCHASE", "REFINANCE", "OTHER"]

OccupancyType = Literal[
    "PRIMARY_RESIDENCE",
    "SECOND_HOME",
    "INVESTMENT",
]

PropertyStatus = Literal["SOLD", "PENDING_SALE", "RETAINED"]

LienType = Literal["FIRST_LIEN", "SUBORDINATE_LIEN"]

GiftAssetType = Literal["CASH_GIFT", "GIFT_OF_EQUITY", "GRANT"]

GiftSourceType = Literal[
    "RELATIVE",
    "EMPLOYER",
    "LABOR_UNION",
    "CHARITY",
    "GOVERNMENT_AGENCY",
    "OTHER",
]

EthnicityChoice = Literal[
    "HISPANIC_OR_LATINO",
    "NOT_HISPANIC_OR_LATINO",
    "NOT_PROVIDED",
]

SexChoice = Literal["MALE", "FEMALE", "NOT_PROVIDED"]

CollectionMethod = Literal[
    "FACE_TO_FACE",
    "TELEPHONE",
    "FAX_OR_MAIL",
    "EMAIL_OR_INTERNET",
]

PreviousOwnershipType = Literal["PR", "SR", "SH", "IP"]

PreviousTitleHoldingType = Literal["S", "SP", "O"]

BankruptcyType = Literal["CH7", "CH11", "CH12", "CH13"]


 
# Shared primitives
 

class ContactInformation(BaseModel):
    home_phone: Optional[str] = None
    cell_phone: Optional[str] = None
    work_phone: Optional[str] = None
    work_phone_ext: Optional[str] = None
    email: Optional[EmailStr] = None


class Address(BaseModel):
    street: str
    city: str
    state: str
    zip: str
    country: Optional[str] = "USA"
    unit: Optional[str] = None


class HousingAddress(Address):
    years_at_address: conint(ge=0)
    months_at_address: conint(ge=0, lt=12)
    housing_expense_type: HousingExpenseType
    housing_expense_amount: confloat(ge=0)


class AlternateName(BaseModel):
    first_name: str
    last_name: str
    middle_name: Optional[str] = None
    suffix: Optional[str] = None


 
# Section 1 – Borrower Information
 

class PersonalInformation(BaseModel):
    first_name: str
    last_name: str
    middle_name: Optional[str] = None
    suffix: Optional[str] = None

    alternate_names: List[AlternateName] = []

    ssn_or_itin: str
    date_of_birth: str  # YYYY-MM-DD (can be changed to date)

    citizenship: CitizenshipType
    type_of_credit: TypeOfCredit
    total_number_of_borrowers: conint(ge=1) = 1

    # URLA line:
    # "List Name(s) of Other Borrower(s) Applying for this Loan
    #  (First, Middle, Last, Suffix) – Use a separator between names"
    # We store both the raw string and a parsed list.
    other_borrowers_names_raw: Optional[str] = None
    other_borrowers_names: List[str] = []

    marital_status: MaritalStatus
    dependents_number: conint(ge=0) = 0
    dependents_ages: List[conint(ge=0)] = []

    contact_information: ContactInformation

    current_address: HousingAddress
    former_address: Optional[HousingAddress] = None
    mailing_address: Optional[Address] = None

    @field_validator("dependents_ages")
    @classmethod
    def dependents_ages_match_count(cls, v, values):
        if not values.data:
            return v
        num = values.data.get("dependents_number", 0)
        if num > 0 and len(v) == 0:
            raise ValueError("dependents_ages must be provided when dependents_number > 0")
        return v

    @field_validator("other_borrowers_names", mode="before")
    @classmethod
    def parse_other_borrower_names(cls, v, values):
        """
        If other_borrowers_names is not provided explicitly,
        parse other_borrowers_names_raw by splitting on semicolons.
        Example: "Jane Doe; John Q Public"
        """
        if v and len(v) > 0:
            return v
        if not values.data:
            return []
        raw = values.data.get("other_borrowers_names_raw")
        if not raw:
            return []
        return [name.strip() for name in raw.split(";") if name.strip()]


 
# Section 2 – Financial Information (Assets / Liabilities)
 

class GrossMonthlyIncome(BaseModel):
    base: confloat(ge=0)
    overtime: confloat(ge=0) = 0.0
    bonus: confloat(ge=0) = 0.0
    commission: confloat(ge=0) = 0.0
    military_entitlements: confloat(ge=0) = 0.0
    other: confloat(ge=0) = 0.0
    total: confloat(ge=0)

    @field_validator("total")
    @classmethod
    def validate_total(cls, total, values):
        if not values.data:
            return total
        components_sum = sum([
            values.data.get("base") or 0.0,
            values.data.get("overtime") or 0.0,
            values.data.get("bonus") or 0.0,
            values.data.get("commission") or 0.0,
            values.data.get("military_entitlements") or 0.0,
            values.data.get("other") or 0.0,
        ])
        if total < components_sum:
            raise ValueError("total income cannot be less than sum of income components")
        return total


class EmploymentRecord(BaseModel):
    employer_name: str
    employer_phone: Optional[str] = None
    street: Optional[str] = None
    unit: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip: Optional[str] = None
    country: Optional[str] = "USA"

    position_title: Optional[str] = None
    start_date: Optional[str] = None  # YYYY-MM-DD
    end_date: Optional[str] = None    # for previous employment
    years_in_line_of_work: Optional[conint(ge=0)] = None
    months_in_line_of_work: Optional[conint(ge=0, lt=12)] = None

    employed_by_interested_party: bool = False
    is_self_employed: bool = False
    ownership_share_25_or_more: bool = False

    gross_monthly_income: Optional[GrossMonthlyIncome] = None
    previous_gross_monthly_income: Optional[confloat(ge=0)] = None


class OtherIncomeSource(BaseModel):
    income_source_type: str  # could be restricted by Literal if needed
    monthly_income: confloat(ge=0)


class EmploymentSection(BaseModel):
    current_employment: EmploymentRecord
    additional_employment: List[EmploymentRecord] = []
    previous_employment: List[EmploymentRecord] = []
    other_income_sources: List[OtherIncomeSource] = []
    total_other_income: confloat(ge=0) = 0.0


class AssetAccount(BaseModel):
    account_type: AccountType
    financial_institution: str
    account_number: Optional[str] = None
    cash_or_market_value: confloat(ge=0)


class OtherAssetOrCredit(BaseModel):
    asset_or_credit_type: str
    cash_or_market_value: confloat(ge=0)


class Liability(BaseModel):
    account_type: LiabilityAccountType
    company_name: str
    account_number: Optional[str] = None
    unpaid_balance: confloat(ge=0)
    to_be_paid_off_before_closing: bool = False
    monthly_payment: confloat(ge=0)


class OtherLiabilityOrExpense(BaseModel):
    expense_type: OtherLiabilityExpenseType
    monthly_payment: confloat(ge=0)


class AssetsAndLiabilitiesSection(BaseModel):
    assets_accounts: List[AssetAccount] = []
    total_assets_accounts: confloat(ge=0) = 0.0

    other_assets_and_credits: List[OtherAssetOrCredit] = []
    total_other_assets_and_credits: confloat(ge=0) = 0.0

    liabilities: List[Liability] = []
    other_liabilities_and_expenses: List[OtherLiabilityOrExpense] = []


 
# Section 3 – Financial Information (Real Estate)
 

class MortgageLoanOnProperty(BaseModel):
    creditor_name: str
    account_number: Optional[str] = None
    monthly_mortgage_payment: confloat(ge=0)
    unpaid_balance: confloat(ge=0)
    to_be_paid_off_before_closing: bool = False
    loan_type: str
    credit_limit: Optional[confloat(ge=0)] = None


class RealEstateProperty(BaseModel):
    address: Address
    property_value: confloat(ge=0)
    status: PropertyStatus
    intended_occupancy: OccupancyType
    monthly_taxes_insurance_assoc: confloat(ge=0)
    monthly_rental_income: confloat(ge=0) = 0.0
    net_monthly_rental_income: confloat(ge=0) = 0.0
    mortgage_loans: List[MortgageLoanOnProperty] = []


class RealEstateSection(BaseModel):
    owns_any_real_estate: bool
    properties: List[RealEstateProperty] = []


 
# Section 4 – Loan and Property Information
# (Application-level, shared)
 

class ExpectedRentalIncome(BaseModel):
    expected_monthly_rental_income: confloat(ge=0)
    expected_net_monthly_rental_income: confloat(ge=0)


class OtherNewMortgageLoan(BaseModel):
    creditor_name: str
    lien_type: LienType
    monthly_payment: confloat(ge=0)
    loan_amount_or_amount_drawn: confloat(ge=0)
    credit_limit: Optional[confloat(ge=0)] = None


class GiftOrGrant(BaseModel):
    asset_type: GiftAssetType
    source_type: GiftSourceType
    cash_or_market_value: confloat(ge=0)
    deposited: bool = False


class LoanAndPropertySection(BaseModel):
    loan_amount: confloat(ge=0)
    loan_purpose: LoanPurposeType
    loan_purpose_other_description: Optional[str] = None

    property_address: Address
    number_of_units: conint(ge=1) = 1
    property_value: confloat(ge=0)

    occupancy: OccupancyType
    is_mixed_use_property: bool = False
    is_manufactured_home: bool = False

    other_new_mortgage_loans: List[OtherNewMortgageLoan] = []
    expected_rental_income: Optional[ExpectedRentalIncome] = None
    gifts_or_grants: List[GiftOrGrant] = []


 
# Section 5 – Declarations
 

class Declarations(BaseModel):
    will_occupy_as_primary_residence: bool
    had_ownership_interest_last_three_years: bool
    previous_property_ownership_type: Optional[PreviousOwnershipType] = None
    previous_property_title_holding: Optional[PreviousTitleHoldingType] = None

    has_relationship_with_seller: bool
    borrowing_additional_money_for_transaction: bool
    additional_money_amount: confloat(ge=0) = 0.0
    applying_for_other_mortgage_before_closing: bool
    applying_for_new_credit_before_closing: bool
    property_subject_to_senior_lien: bool

    is_cosigner_on_undisclosed_debt: bool
    has_outstanding_judgments: bool
    delinquent_or_default_on_federal_debt: bool
    party_to_lawsuit_with_financial_liability: bool
    conveyed_title_in_lieu_of_foreclosure_past_7_years: bool
    completed_short_sale_past_7_years: bool
    had_property_foreclosed_past_7_years: bool
    declared_bankruptcy_past_7_years: bool
    bankruptcy_types: List[BankruptcyType] = []

    @field_validator("bankruptcy_types")
    @classmethod
    def validate_bankruptcy_types(cls, v, values):
        if not values.data:
            return v
        if values.data.get("declared_bankruptcy_past_7_years") and not v:
            raise ValueError("bankruptcy_types must be provided if declared_bankruptcy_past_7_years is true")
        return v


 
# Section 6 – Acknowledgments and Agreements
 

class AcknowledgmentsAndAgreements(BaseModel):
    acknowledged: bool = False
    borrower_signature: Optional[str] = None
    borrower_signature_date: Optional[str] = None
    additional_borrower_signature: Optional[str] = None
    additional_borrower_signature_date: Optional[str] = None


 
# Section 7 – Military Service
 

class MilitaryService(BaseModel):
    has_military_service: bool = False
    currently_serving_active_duty: bool = False
    active_duty_expiration_date: Optional[str] = None
    currently_retired_discharged_separated: bool = False
    only_reserve_or_guard_non_activated: bool = False
    is_surviving_spouse: bool = False


 
# Section 8 – Demographic Information
 

class EthnicityDetail(BaseModel):
    is_hispanic_or_latino: bool = False
    mexican: bool = False
    puerto_rican: bool = False
    cuban: bool = False
    other_hispanic_or_latino: bool = False
    other_hispanic_or_latino_origin: Optional[str] = None


class RaceDetail(BaseModel):
    american_indian_or_alaska_native: bool = False
    american_indian_or_alaska_native_tribe: Optional[str] = None

    asian_indian: bool = False
    chinese: bool = False
    filipino: bool = False
    japanese: bool = False
    korean: bool = False
    vietnamese: bool = False
    other_asian: bool = False
    other_asian_description: Optional[str] = None

    black_or_african_american: bool = False

    native_hawaiian: bool = False
    guamanian_or_chamorro: bool = False
    samoan: bool = False
    other_pacific_islander: bool = False
    other_pacific_islander_description: Optional[str] = None

    white: bool = False


class CollectedBasedOnVisualObservation(BaseModel):
    ethnicity: bool = False
    sex: bool = False
    race: bool = False


class DemographicInformation(BaseModel):
    ethnicity: EthnicityChoice
    ethnicity_detail: Optional[EthnicityDetail] = None
    sex: SexChoice
    race: RaceDetail
    collected_based_on_visual_observation: CollectedBasedOnVisualObservation
    collection_method: CollectionMethod


 
# Loan Originator Info (optional per borrower)
 

class LoanOriginatorAddress(BaseModel):
    street: str
    city: str
    state: str
    zip: str


class LoanOriginatorInformation(BaseModel):
    organization_name: str
    organization_address: LoanOriginatorAddress
    organization_nmlsr_id: Optional[str] = None
    organization_state_license_id: Optional[str] = None

    loan_originator_name: Optional[str] = None
    loan_originator_nmlsr_id: Optional[str] = None
    loan_originator_state_license_id: Optional[str] = None

    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    signature: Optional[str] = None
    signature_date: Optional[str] = None


 
# Borrower (single borrower model)
 

class Borrower(BaseModel):
    # Section 1
    personal_information: PersonalInformation

    # Section 2
    employment: EmploymentSection
    assets_and_liabilities: AssetsAndLiabilitiesSection

    # Section 3
    real_estate: RealEstateSection

    # Section 5
    declarations: Declarations

    # Section 6
    acknowledgments_and_agreements: AcknowledgmentsAndAgreements

    # Section 7
    military_service: MilitaryService

    # Section 8
    demographic_information: DemographicInformation

    # Optional
    loan_originator_information: Optional[LoanOriginatorInformation] = None


 
# Application (top-level)
 

class Application(BaseModel):
    # Version control for URLA schema
    schema_version: Literal["urlA_2021_v1"] = "urlA_2021_v1"

    application_id: str
    lender_loan_number: Optional[str] = None
    agency_case_number: Optional[str] = None

    # Section 4 – shared subject property and loan info
    loan_and_property: LoanAndPropertySection

    # Single borrower for this initial scope
    borrower: Borrower