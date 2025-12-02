

# URLA / 1003 Intake Data Model (`urlA_2021_v1`)

This module defines the initial application level data model for the Uniform Residential Loan Application (URLA, Form 1003). It is implemented with Pydantic and structured by the official URLA sections.

This is an internal domain schema for intake and validation.  
It is not the raw MISMO 3.4 schema. Mapping to ULAD / MISMO will be implemented in a separate layer.

---

## Scope

- Single borrower application
- Matches the URLA sections:
  - Section 1: Borrower Information
  - Section 2: Financial Information (Assets and Liabilities)
  - Section 3: Financial Information (Real Estate)
  - Section 4: Loan and Property Information
  - Section 5: Declarations
  - Section 6: Acknowledgments and Agreements
  - Section 7: Military Service
  - Section 8: Demographic Information
- Field level validation for:
  - Numeric ranges
  - Required relationships between fields
- Schema versioning with `schema_version`
- Designed to support:
  - Dynamic form rendering from JSON schema
  - Calculated fields (DTI, total assets, total liabilities)

---

## Top level structure

Main entrypoint:

```python
from models.urla_2021_v1 import Application

app = Application(
    schema_version="urlA_2021_v1",
    application_id="APP-001",
    loan_and_property=...,  # Section 4
    borrower=...,           # Sections 1,2,3,5,6,7,8
)
```

### Application Model

`Application` contains:
*   `schema_version`: literal string, currently "urlA_2021_v1"
*   `application_id`: internal application identifier
*   `lender_loan_number`: optional lender specific id
*   `agency_case_number`: optional agency id
*   `loan_and_property`: Section 4 (shared loan and subject property info)
*   `borrower`: a single Borrower instance

### Borrower Model

`Borrower` is a wrapper for the URLA sections that are specific to a borrower:
*   `personal_information` (Section 1)
*   `employment` and `assets_and_liabilities` (Section 2)
*   `real_estate` (Section 3)
*   `declarations` (Section 5)
*   `acknowledgments_and_agreements` (Section 6)
*   `military_service` (Section 7)
*   `demographic_information` (Section 8)
*   `loan_originator_information` (optional, used for originator metadata)

---

---

Section details

### Section 1: Borrower Information

*   **Model:** PersonalInformation

*   **Includes:**
    *   Name and identity
        *   `first_name`, `middle_name`, `last_name`, `suffix`
        *   `alternate_names` list
        *   `ssn_or_itin`
        *   `date_of_birth`
        *   `citizenship`
    *   Type of credit and borrowers
        *   `type_of_credit` (INDIVIDUAL or JOINT)
        *   `total_number_of_borrowers`
        *   `other_borrowers_names_raw`
        *   raw URLA field: “List Name(s) of Other Borrower(s) Applying for this Loan (First, Middle, Last, Suffix) – use a separator”
        *   `other_borrowers_names`
        *   parsed list (by semicolon) from the raw field
    *   Marital and dependents
        *   `marital_status`
        *   `dependents_number`
        *   `dependents_ages`
    *   Contact info
        *   `ContactInformation` (phones and email)
    *   Address history
        *   `current_address` as HousingAddress
        *   `former_address` (optional)
        *   `mailing_address` (optional)

*   **Validation examples:**
    *   `dependents_number` is greater than or equal to 0
    *   If `dependents_number` > 0 then `dependents_ages` must not be empty
    *   `months_at_address` is between 0 and 11
    *   `other_borrowers_names` is auto derived from `other_borrowers_names_raw` when not provided explicitly

---

### Section 2: Financial Information (Assets and Liabilities)

Section 2 is split into:
1.  EmploymentSection (employment and income)
2.  AssetsAndLiabilitiesSection (assets, liabilities, and related expenses)

#### Employment and income
*   **Model:** EmploymentSection with:
    *   `current_employment`: required EmploymentRecord
    *   `additional_employment`: list of EmploymentRecord
    *   `previous_employment`: list of EmploymentRecord
    *   `other_income_sources`: list of OtherIncomeSource
    *   `total_other_income`

*   **Each EmploymentRecord includes:**
    *   Employer identifiers (name, phone, address)
    *   Position and tenure (start and end dates, years and months in line of work)
    *   Flags:
        *   `is_self_employed`
        *   `employed_by_interested_party`
        *   `ownership_share_25_or_more`
    *   `gross_monthly_income` as GrossMonthlyIncome:
        *   `base`, `overtime`, `bonus`, `commission`, `military_entitlements`, `other`, `total`

*   **Validation:**
    *   All income components are non negative
    *   `GrossMonthlyIncome.total` must be at least the sum of all income components

#### Assets and liabilities
*   **Model:** AssetsAndLiabilitiesSection with:
    *   `assets_accounts`: list of AssetAccount
    *   `total_assets_accounts`
    *   `other_assets_and_credits`: list of OtherAssetOrCredit
    *   `total_other_assets_and_credits`
    *   `liabilities`: list of Liability
    *   `other_liabilities_and_expenses`: list of OtherLiabilityOrExpense

*   **Validation:**
    *   Asset values, balances, and monthly payments are non negative
    *   `total_assets_accounts` and `total_other_assets_and_credits` can be used as cross checks against computed sums

---

### Section 3: Financial Information (Real Estate)

*   **Model:** RealEstateSection

*   **Fields:**
    *   `owns_any_real_estate` (boolean)
    *   `properties`: list of RealEstateProperty

*   **Each RealEstateProperty has:**
    *   `address`
    *   `property_value`
    *   `status` (sold, pending sale, retained)
    *   `intended_occupancy` (primary residence, second home, investment)
    *   `monthly_taxes_insurance_assoc`
    *   `monthly_rental_income` and `net_monthly_rental_income`
    *   `mortgage_loans`: list of MortgageLoanOnProperty

*   **Each MortgageLoanOnProperty includes:**
    *   `creditor_name`
    *   `account_number`
    *   `monthly_mortgage_payment`
    *   `unpaid_balance`
    *   `to_be_paid_off_before_closing`
    *   `loan_type`
    *   `credit_limit` (for HELOC type products)

*   **Validation:**
    *   All monetary values are non negative
    *   If `owns_any_real_estate` is true, at least one property is expected downstream (enforced at business logic level)

---

### Section 4: Loan and Property Information

*   **Model:** LoanAndPropertySection at Application level

*   **Fields:**
    *   Loan info:
        *   `loan_amount`
        *   `loan_purpose` (PURCHASE, REFINANCE, OTHER)
        *   `loan_purpose_other_description` (used when purpose is OTHER)
    *   Subject property:
        *   `property_address`
        *   `number_of_units`
        *   `property_value`
        *   `occupancy`
        *   `is_mixed_use_property`
        *   `is_manufactured_home`
    *   Additional loans:
        *   `other_new_mortgage_loans`: list of OtherNewMortgageLoan
    *   Expected rental:
        *   `expected_rental_income` object
    *   Gifts and grants:
        *   `gifts_or_grants`: list of GiftOrGrant

*   **Validation:**
    *   Monetary fields and unit counts are non negative
    *   If `loan_purpose` == "OTHER", `loan_purpose_other_description` should be provided in the UX or business layer

---

### Section 5: Declarations

*   **Model:** Declarations

*   **Captures yes/no and related detail for:**
    *   Occupancy intent
    *   Ownership interest in the last three years
    *   Prior ownership type and title holding
    *   Relationship with seller
    *   Borrowing additional money for the transaction
    *   Other mortgages or new credit before closing
    *   Senior liens on the property
    *   Cosigner obligations
    *   Outstanding judgments
    *   Federal debt delinquencies
    *   Lawsuits
    *   Deeds in lieu, short sales, foreclosures
    *   Bankruptcy in the last seven years with `bankruptcy_types` detail

*   **Validation:**
    *   If `declared_bankruptcy_past_7_years` is true, `bankruptcy_types` should be non empty
    *   If `had_ownership_interest_last_three_years` is true, ownership type and title holding should be provided in the UX layer

---

### Section 6: Acknowledgments and Agreements

*   **Model:** AcknowledgmentsAndAgreements

*   **Fields:**
    *   `acknowledged`
    *   `borrower_signature`
    *   `borrower_signature_date`
    *   `additional_borrower_signature`
    *   `additional_borrower_signature_date`

Typically completed or updated when the borrower consents at the end of the application, or via an e signature integration.

---

### Section 7: Military Service

*   **Model:** MilitaryService

*   **Fields:**
    *   `has_military_service`
    *   `currently_serving_active_duty`
    *   `active_duty_expiration_date`
    *   `currently_retired_discharged_separated`
    *   `only_reserve_or_guard_non_activated`
    *   `is_surviving_spouse`

These values are used to determine eligibility for certain loan programs (for example VA loans).

---

### Section 8: Demographic Information

*   **Model:** DemographicInformation

*   **Fields:**
    *   `ethnicity` and `ethnicity_detail`
    *   `sex`
    *   `race` as RaceDetail with granular flags
    *   `collected_based_on_visual_observation`
    *   `collection_method` (face to face, telephone, fax or mail, email or internet)

Supports HMDA style demographic reporting and regulatory requirements.

---

### Schema versioning

The Application model includes a version field:

`schema_version: Literal["urlA_2021_v1"] = "urlA_2021_v1"`

Future URLA changes can be supported by:
*   Adding new versions, for example "urlA_2021_v2" or "urlA_20XX_v1"
*   Creating new versioned modules, for example `urla_2021_v2.py`
*   Writing migration helpers between versions

This makes it possible to persist older applications while evolving the schema over time.

---

### Dynamic form schema

The Pydantic models define the canonical data schema. We can generate JSON Schema via:

`Application.model_json_schema()`


You can retrieve the JSON schema for a specific form by using the following API endpoint:

```
GET /api/v1/forms/urla_2021_v1
```

### Calculated fields

The calculation logic is centralized in the `app/services/calculations.py` file. This service provides functions to compute key financial metrics based on the borrower's data.

The main calculated fields include:
-   `total_monthly_income`: Sum of the borrower's gross monthly income from all sources.
-   `total_monthly_debt`: Sum of all monthly debt payments, including liabilities and housing expenses.
-   `dti_ratio`: The debt-to-income ratio, calculated as `total_monthly_debt / total_monthly_income`.
-   `total_assets`: The sum of all the borrower's assets.
-   `total_liabilities`: The sum of all the borrower's liabilities.
