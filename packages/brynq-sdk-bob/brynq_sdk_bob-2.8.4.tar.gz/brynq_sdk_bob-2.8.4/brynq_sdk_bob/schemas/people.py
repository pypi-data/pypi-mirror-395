from datetime import datetime
from typing import Optional, List, Dict

import pandas as pd
import pandera as pa
from pandera import Bool
from pandera.typing import Series, String, Float
import pandera.extensions as extensions
from brynq_sdk_functions import BrynQPanderaDataFrameModel
from pandera.engines.pandas_engine import DateTime


@extensions.register_check_method()
def check_list(x):
    return isinstance(x, list)


class PeopleSchema(BrynQPanderaDataFrameModel):
    id: Optional[Series[String]] = pa.Field(coerce=True, description="Person ID", alias="id", metadata={"api_field": "root.id"})
    display_name: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Display Name", alias="displayName", metadata={"api_field": "root.displayName"})
    company_id: Optional[Series[String]] = pa.Field(coerce=True, description="Company ID", alias="companyId", metadata={"api_field": "root.companyId"})
    email: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Email", alias="email", metadata={"api_field": "root.email"})
    home_mobile_phone: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Personal Mobile Phone", alias="home.mobilePhone")
    home_private_email: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, alias='home.privateEmail')
    surname: Optional[Series[String]] = pa.Field(coerce=True, description="Surname", alias="surname", metadata={"api_field": "root.surname"})
    first_name: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="First Name", alias="firstName", metadata={"api_field": "root.firstName"})
    full_name: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Full Name", alias="fullName", metadata={"api_field": "root.fullName"})
    # the date is in DD/MM/YYYY format,
    personal_birth_date: Optional[Series[DateTime]] = pa.Field(coerce=True, nullable=True, description="Personal Birth Date", alias="personal.birthDate")
    personal_pronouns: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Personal Pronouns", alias="personal.pronouns")
    personal_honorific: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Personal Honorific", alias="personal.honorific")
    personal_nationality: Optional[Series[object]] = pa.Field(coerce=True, check_name=check_list, description="Personal Nationality", alias="personal.nationality")
    # employee_payroll_manager: Series[String] = pa.Field(coerce=True, nullable=True)
    # employee_hrbp: Series[String] = pa.Field(coerce=True, nullable=True)
    # employee_it_admin: Series[String] = pa.Field(coerce=True, nullable=True)
    # employee_buddy: Series[String] = pa.Field(coerce=True, nullable=True)
    employee_veteran_status: Optional[Series[object]] = pa.Field(coerce=True, check_name=check_list, description="Employee Veteran Status", alias="employee.veteranStatus")
    employee_disability_status: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Employee Disability Status", alias="employee.disabilityStatus")
    work_start_date: Optional[Series[DateTime]] = pa.Field(coerce=True, nullable=True, description="Work Start Date", alias="work.startDate")
    work_manager: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Work Manager", alias="work.manager")
    work_work_phone: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Work Work Phone", alias="work.workPhone")
    work_tenure_duration_period_i_s_o: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Work Tenure Duration Period ISO", alias="work.tenureDuration.periodISO")
    work_tenure_duration_sort_factor: Optional[Series[pd.Int64Dtype]] = pa.Field(coerce=True, nullable=False, description="Work Tenure Duration Sort Factor", alias="work.tenureDuration.sortFactor")
    work_tenure_duration_humanize: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Work Tenure Duration Humanize", alias="work.tenureDuration.humanize")
    work_duration_of_employment_period_i_s_o: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Work Duration of Employment Period ISO", alias="work.durationOfEmployment.periodISO")
    work_duration_of_employment_sort_factor: Optional[Series[String]] = pa.Field(coerce=True, nullable=False, description="Work Duration of Employment Sort Factor", alias="work.durationOfEmployment.sortFactor")
    work_duration_of_employment_humanize: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Work Duration of Employment Humanize", alias="work.durationOfEmployment.humanize")
    work_reports_to_id_in_company: Optional[Series[pd.Int64Dtype]] = pa.Field(coerce=True, nullable=True, description="Work Reports to ID in Company", alias="work.reportsToIdInCompany")
    work_employee_id_in_company: Optional[Series[pd.Int64Dtype]] = pa.Field(coerce=True, nullable=True, description="Work Employee ID in Company", alias="work.employeeIdInCompany")
    work_reports_to_display_name: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Work Reports to Display Name", alias="work.reportsTo.displayName")
    work_reports_to_surname: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Work Reports to Surname", alias="work.reportsTo.surname")
    work_reports_to_first_name: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Work Reports to First Name", alias="work.reportsTo.firstName")
    work_reports_to_id: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Work Reports to ID", alias="work.reportsTo.id")
    work_work_mobile: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Work Work Mobile", alias="work.workMobile")
    work_indirect_reports: Optional[Series[pd.Int64Dtype]] = pa.Field(coerce=True, nullable=True, description="Work Indirect Reports", alias="work.indirectReports")
    work_site_id: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Work Site ID", alias="work.siteId")
    work_department: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Work Department", alias="work.department")
    work_tenure_duration_years: Optional[Series[Float]] = pa.Field(coerce=True, nullable=True, description="Work Tenure Duration Years", alias="work.tenureDurationYears")
    work_tenure_years: Optional[Series[pd.Int64Dtype]] = pa.Field(coerce=True, nullable=True, description="Work Tenure Years", alias="work.tenureYears")
    work_is_manager: Optional[Series[Bool]] = pa.Field(coerce=True, nullable=True, description="Work Is Manager", alias="work.isManager")
    work_title: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Work Title", alias="work.title")
    work_site: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Work Site", alias="work.site")
    work_original_start_date: Optional[Series[DateTime]] = pa.Field(coerce=True, nullable=True, description="Work Original Start Date", alias="work.originalStartDate")
    work_active_effective_date: Optional[Series[DateTime]] = pa.Field(coerce=True, nullable=True, description="Work Active Effective Date", alias="work.activeEffectiveDate")
    work_direct_reports: Optional[Series[pd.Int64Dtype]] = pa.Field(coerce=True, nullable=True, description="Work Direct Reports", alias="work.directReports")
    # work_work_change_type: Series[String] = pa.Field(coerce=True, nullable=True)
    work_second_level_manager: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Work Second Level Manager", alias="work.secondLevelManager")
    work_days_of_previous_service: Optional[Series[pd.Int64Dtype]] = pa.Field(coerce=True, nullable=True, description="Work Days of Previous Service", alias="work.daysOfPreviousService")
    work_years_of_service: Optional[Series[Float]] = pa.Field(coerce=True, nullable=True, description="Work Years of Service", alias="work.yearsOfService")
    payroll_employment_contract: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Contract Type", alias="payroll.employment.contract")
    payroll_employment_type: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Employment Type", alias="payroll.employment.type")
    tax_id: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Tax ID", alias="payroll.taxCode")

    about_food_preferences: Optional[Series[object]] = pa.Field(coerce=True, check_name=check_list, description="About Food Preferences", alias="about.foodPreferences")
    # about_social_data_linkedin: Series[String] = pa.Field(coerce=True, nullable=True)
    about_social_data_twitter: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="About Social Data Twitter", alias="about.socialData.twitter")

    about_social_data_facebook: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="About Social Data Facebook", alias="about.socialData.facebook")

    about_superpowers: Optional[Series[object]] = pa.Field(coerce=True, check_name=check_list, description="About Superpowers", alias="about.superpowers")
    about_hobbies: Optional[Series[object]] = pa.Field(coerce=True, check_name=check_list, description="About Hobbies", alias="about.hobbies")
    about_about: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="About About", alias="about.about")
    about_avatar: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="About Avatar", alias="about.avatar")
    address_city: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Address City", alias="address.city")
    address_post_code: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Address Post Code", alias="address.postCode")
    address_zip_code: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Address ZIP Code", alias="address.zipCode")
    address_line1: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Address Line 1", alias="address.line1")
    address_line2: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Address Line 2", alias="address.line2")
    address_country: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Address Country", alias="address.country")
    address_active_effective_date: Optional[Series[DateTime]] = pa.Field(coerce=True, nullable=True, description="Address Active Effective Date", alias="address.activeEffectiveDate") # , dtype_kwargs={"to_datetime_kwargs": {"format": "%d/%m/%Y"}}
    address_full_address: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Address Full Address", alias="address.fullAddress")
    address_site_address1: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Address Site Address 1", alias="address.siteAddress1")
    address_site_address2: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Address Site Address 2", alias="address.siteAddress2")
    address_site_country: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Address Site Country", alias="address.siteCountry")
    address_site_postal_code: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Address Site Postal Code", alias="address.sitePostalCode")
    address_site_city: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Address Site City", alias="address.siteCity")
    address_site_state: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Address Site State", alias="address.siteState")
    home_legal_gender: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Legal Gender", alias="home.legalGender")
    home_family_status: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Family / Marital Status", alias="home.familyStatus")
    home_spouse_first_name: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Spouse First Name", alias="home.spouse.firstName")
    home_spouse_surname: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Spouse Surname", alias="home.spouse.surname")
    # home_spouse_birth_date: Series[DateTime] = pa.Field(coerce=True, nullable=True)
    home_spouse_gender: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Spouse Gender", alias="home.spouse.gender")
    identification_ssn_serial_number: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="SSN Serial Number", alias="identification.ssnSerialNumber")
    internal_termination_reason: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Internal Termination Reason", alias="internal.terminationReason")
    internal_termination_date: Optional[Series[DateTime]] = pa.Field(coerce=True, nullable=True, description="Internal Termination Date", alias="internal.terminationDate")
    internal_termination_type: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Internal Termination Type", alias="internal.terminationType")
    employee_last_day_of_work: Optional[Series[DateTime]] = pa.Field(coerce=True, nullable=True, description="Employee Last Day of Work", alias="employee.lastDayOfWork")
    financial_iban: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, alias='financial.iban')
    employee_band_effective_date_ote: Optional[Series[DateTime]] = pa.Field(coerce=True, nullable=True, description="Employee Band Effective Date OTE", alias="employee.band_effectiveDate_ote")
    employee_band_site_ote: Optional[Series[object]] = pa.Field(coerce=True, nullable=True, check_name=check_list, description="Employee Band Site OTE", alias="employee.band_site_ote")
    employee_band_min_ote: Optional[Series[Float]] = pa.Field(coerce=True, nullable=True, description="Employee Band Min OTE", alias="employee.band_min_ote")
    employee_band_mid_ote: Optional[Series[Float]] = pa.Field(coerce=True, nullable=True, description="Employee Band Mid OTE", alias="employee.band_mid_ote")
    employee_band_max_ote: Optional[Series[Float]] = pa.Field(coerce=True, nullable=True, description="Employee Band Max OTE", alias="employee.band_max_ote")
    employee_band_pay_period_ote: Optional[Series[object]] = pa.Field(coerce=True, nullable=True, check_name=check_list, description="Employee Band Pay Period OTE", alias="employee.band_payPeriod_ote")
    employee_band_currency_ote: Optional[Series[object]] = pa.Field(coerce=True, nullable=True, check_name=check_list, description="Employee Band Currency OTE", alias="employee.band_currency_ote")
    employee_band_ote_id: Optional[Series[object]] = pa.Field(coerce=True, nullable=True, check_name=check_list, description="Employee Band OTE ID", alias="employee.band_ote_id")
    employee_band_effective_date_base_salary: Optional[Series[DateTime]] = pa.Field(coerce=True, nullable=True, description="Employee Band Effective Date Base Salary", alias="employee.band_effectiveDate_baseSalary")
    employee_band_site_base_salary: Optional[Series[object]] = pa.Field(coerce=True, nullable=True, check_name=check_list, description="Employee Band Site Base Salary", alias="employee.band_site_baseSalary")
    employee_band_min_base_salary: Optional[Series[Float]] = pa.Field(coerce=True, nullable=True, description="Employee Band Min Base Salary", alias="employee.band_min_baseSalary")
    employee_band_mid_base_salary: Optional[Series[Float]] = pa.Field(coerce=True, nullable=True, description="Employee Band Mid Base Salary", alias="employee.band_mid_baseSalary")
    employee_band_max_base_salary: Optional[Series[Float]] = pa.Field(coerce=True, nullable=True, description="Employee Band Max Base Salary", alias="employee.band_max_baseSalary")
    employee_band_pay_period_base_salary: Optional[Series[object]] = pa.Field(coerce=True, nullable=True, check_name=check_list, description="Employee Band Pay Period Base Salary", alias="employee.band_payPeriod_baseSalary")
    employee_band_currency_base_salary: Optional[Series[object]] = pa.Field(coerce=True, nullable=True, check_name=check_list, description="Employee Band Currency Base Salary", alias="employee.band_currency_baseSalary")
    employee_band_base_salary_id: Optional[Series[object]] = pa.Field(coerce=True, nullable=True, check_name=check_list, description="Employee Band Base Salary ID", alias="employee.band_baseSalary_id")
    employee_band_compa_ratio_ote: Optional[Series[Float]] = pa.Field(coerce=True, nullable=True, description="Employee Band Compa Ratio OTE", alias="employee.band_compaRatio_ote")
    employee_band_range_positioning_ote: Optional[Series[Float]] = pa.Field(coerce=True, nullable=True, description="Employee Band Range Positioning OTE", alias="employee.band_rangePositioning_ote")
    employee_band_compa_ratio_base_salary: Optional[Series[Float]] = pa.Field(coerce=True, nullable=True, description="Employee Band Compa Ratio Base Salary", alias="employee.band_compaRatio_baseSalary")
    employee_band_range_positioning_base_salary: Optional[Series[Float]] = pa.Field(coerce=True, nullable=True, description="Employee Band Range Positioning Base Salary", alias="employee.band_rangePositioning_baseSalary")

    # Additional non-custom fields from available_fields.json
    # Root extras
    creation_date_time: Optional[Series[DateTime]] = pa.Field(coerce=True, nullable=True, description="Root Creation Date Time", alias="creationDateTime", metadata={"api_field": "root.creationDateTime"})
    cover_image_url: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Root Cover Image URL", alias="coverImageUrl", metadata={"api_field": "root.coverImageUrl"})
    avatar_url: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Root Avatar URL", alias="avatarUrl", metadata={"api_field": "root.avatarUrl"})
    second_name: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Middle Name", alias="secondName", metadata={"api_field": "root.secondName"})
    state: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="State", alias="state", metadata={"api_field": "root.state"})
    creation_date: Optional[Series[DateTime]] = pa.Field(coerce=True, nullable=True, description="Creation Date", alias="creationDate", metadata={"api_field": "root.creationDate"})

    # Personal extras
    personal_age: Optional[Series[Float]] = pa.Field(coerce=True, nullable=True, description="Age", alias="personal.age")
    personal_short_birth_date: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Birthday Short", alias="personal.shortBirthDate")

    # Personal contact
    home_private_phone: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Personal Phone", alias="home.privatePhone")

    # Identification extras
    financial_passport_number: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Passport Number", alias="financial.passportNumber")
    financial_identification_number: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Identification Number", alias="financial.identificationNumber")
    payroll_nin: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="NI Number", alias="payroll.nin")
    identification_ssn: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="SSN", alias="identification.ssn")
    employee_sin: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="SIN", alias="employee.sin")
    employee_sin_expiration_date: Optional[Series[DateTime]] = pa.Field(coerce=True, nullable=True, description="SIN Expiration Date", alias="employee.sinExpirationDate")

    # Work extras
    work_short_start_date: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Work Anniversary", alias="work.shortStartDate")
    work_duration_of_employment: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Accumulated Tenure (duration)", alias="work.durationOfEmployment")
    work_tenure_duration: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Tenure (duration)", alias="work.tenureDuration")
    work_work_change_type: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Work Change Type", alias="work.workChangeType")
    work_reports_to: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Reports To", alias="work.reportsTo")
    work_reports_to_email: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Manager Email", alias="work.reportsTo.email")

    # Work roles
    employee_buddy: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Buddy", alias="employee.buddy")
    employee_hrbp: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="HRBP", alias="employee.hrbp")
    employee_payroll_manager: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Payroll Manager", alias="employee.payrollManager")
    employee_it_admin: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="IT Admin", alias="employee.itAdmin")
    employee_org_level: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Org Level", alias="employee.orgLevel")

    # Work contact
    personal_communication_slack_username: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Slack Username", alias="personal.communication.slackUsername")
    personal_communication_skype_username: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Skype Username", alias="personal.communication.skypeUsername")

    # Address extras
    address_usa_state: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="USA State", alias="address.usaState")

    # Home extras
    home_number_of_kids: Optional[Series[Float]] = pa.Field(coerce=True, nullable=True, description="Number of Children", alias="home.numberOfKids")
    home_spouse_birth_date: Optional[Series[DateTime]] = pa.Field(coerce=True, nullable=True, description="Spouse Birth Date", alias="home.spouse.birthDate")
    home_spouse_short_birth_date: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Spouse Birthday", alias="home.spouse.shortBirthDate")

    # About social extras
    about_social_data_linkedin: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Social LinkedIn", alias="about.socialData.linkedin")

    # Right to work
    financial_right_to_work_expiry_date: Optional[Series[DateTime]] = pa.Field(coerce=True, nullable=True, description="Right to Work Expiry Date", alias="financial.rightToWorkExpiryDate")

    # Employment extras
    payroll_employment_active_effective_date: Optional[Series[DateTime]] = pa.Field(coerce=True, nullable=True, description="Employment Active Effective Date", alias="payroll.employment.activeEffectiveDate")
    payroll_employment_working_pattern: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Working Pattern", alias="payroll.employment.workingPattern")
    payroll_employment_standard_working_pattern: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Standard Working Pattern", alias="payroll.employment.standardWorkingPattern")
    payroll_employment_standard_working_pattern_id: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Standard Working Pattern ID", alias="payroll.employment.standardWorkingPattern.workingPatternId")
    payroll_employment_personal_working_pattern_type: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Personal Working Pattern Type", alias="payroll.employment.actualWorkingPattern.workingPatternType")
    payroll_employment_hours_in_day_not_worked: Optional[Series[Float]] = pa.Field(coerce=True, nullable=True, description="Hours in Day Not Worked", alias="payroll.employment.hoursInDayNotWorked")
    payroll_employment_site_working_pattern: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Site Working Pattern", alias="payroll.employment.siteWorkingPattern")
    payroll_employment_actual_working_pattern: Optional[Series[dict]] = pa.Field(coerce=True, nullable=True, description="Actual Working Pattern", alias="payroll.employment.actualWorkingPattern")
    payroll_employment_actual_working_pattern_days_sunday: Optional[Series[float]] = pa.Field(coerce=True, nullable=True, description="Actual Working Pattern - Sunday", alias="payroll.employment.actualWorkingPattern.days.sunday")
    payroll_employment_actual_working_pattern_days_tuesday: Optional[Series[float]] = pa.Field(coerce=True, nullable=True, description="Actual Working Pattern - Tuesday", alias="payroll.employment.actualWorkingPattern.days.tuesday")
    payroll_employment_actual_working_pattern_days_wednesday: Optional[Series[float]] = pa.Field(coerce=True, nullable=True, description="Actual Working Pattern - Wednesday", alias="payroll.employment.actualWorkingPattern.days.wednesday")
    payroll_employment_actual_working_pattern_days_monday: Optional[Series[float]] = pa.Field(coerce=True, nullable=True, description="Actual Working Pattern - Monday", alias="payroll.employment.actualWorkingPattern.days.monday")
    payroll_employment_actual_working_pattern_days_friday: Optional[Series[float]] = pa.Field(coerce=True, nullable=True, description="Actual Working Pattern - Friday", alias="payroll.employment.actualWorkingPattern.days.friday")
    payroll_employment_actual_working_pattern_days_thursday: Optional[Series[float]] = pa.Field(coerce=True, nullable=True, description="Actual Working Pattern - Thursday", alias="payroll.employment.actualWorkingPattern.days.thursday")
    payroll_employment_actual_working_pattern_days_saturday: Optional[Series[float]] = pa.Field(coerce=True, nullable=True, description="Actual Working Pattern - Saturday", alias="payroll.employment.actualWorkingPattern.days.saturday")
    payroll_employment_actual_working_pattern_hours_per_day: Optional[Series[float]] = pa.Field(coerce=True, nullable=True, description="Actual Working Pattern - Hours Per Day", alias="payroll.employment.actualWorkingPattern.hoursPerDay")
    payroll_employment_actual_working_pattern_working_pattern_id: Optional[Series[pd.Int64Dtype]] = pa.Field(coerce=True, nullable=True, description="Actual Working Pattern - Working Pattern ID", alias="payroll.employment.actualWorkingPattern.workingPatternId")
    payroll_employment_site_working_pattern_working_pattern_type: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Site Working Pattern - Working Pattern Type", alias="payroll.employment.siteWorkingPattern.workingPatternType")
    payroll_employment_site_working_pattern_days_sunday: Optional[Series[float]] = pa.Field(coerce=True, nullable=True, description="Site Working Pattern - Sunday", alias="payroll.employment.siteWorkingPattern.days.sunday")
    payroll_employment_site_working_pattern_days_tuesday: Optional[Series[float]] = pa.Field(coerce=True, nullable=True, description="Site Working Pattern - Tuesday", alias="payroll.employment.siteWorkingPattern.days.tuesday")
    payroll_employment_site_working_pattern_days_wednesday: Optional[Series[float]] = pa.Field(coerce=True, nullable=True, description="Site Working Pattern - Wednesday", alias="payroll.employment.siteWorkingPattern.days.wednesday")
    payroll_employment_site_working_pattern_days_monday: Optional[Series[float]] = pa.Field(coerce=True, nullable=True, description="Site Working Pattern - Monday", alias="payroll.employment.siteWorkingPattern.days.monday")
    payroll_employment_site_working_pattern_days_friday: Optional[Series[float]] = pa.Field(coerce=True, nullable=True, description="Site Working Pattern - Friday", alias="payroll.employment.siteWorkingPattern.days.friday")
    payroll_employment_site_working_pattern_days_thursday: Optional[Series[float]] = pa.Field(coerce=True, nullable=True, description="Site Working Pattern - Thursday", alias="payroll.employment.siteWorkingPattern.days.thursday")
    payroll_employment_site_working_pattern_days_saturday: Optional[Series[float]] = pa.Field(coerce=True, nullable=True, description="Site Working Pattern - Saturday", alias="payroll.employment.siteWorkingPattern.days.saturday")
    payroll_employment_site_working_pattern_hours_per_day: Optional[Series[float]] = pa.Field(coerce=True, nullable=True, description="Site Working Pattern - Hours Per Day", alias="payroll.employment.siteWorkingPattern.hoursPerDay")
    payroll_employment_site_working_pattern_working_pattern_id: Optional[Series[pd.Int64Dtype]] = pa.Field(coerce=True, nullable=True, description="Site Working Pattern - Working Pattern ID", alias="payroll.employment.siteWorkingPattern.workingPatternId")
    payroll_employment_calendar_id: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Calendar ID", alias="payroll.employment.calendarId")
    payroll_employment_salary_pay_type: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Salary Pay Type", alias="payroll.employment.salaryPayType")
    payroll_employment_flsa_code: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="FLSA Code", alias="payroll.employment.flsaCode")
    payroll_employment_fte: Optional[Series[Float]] = pa.Field(coerce=True, nullable=True, description="FTE %", alias="payroll.employment.fte")
    payroll_employment_weekly_hours: Optional[Series[Float]] = pa.Field(coerce=True, nullable=True, description="Weekly Hours", alias="payroll.employment.weeklyHours")

    # Salary information
    # SOLUTION NOW FOR MFT: TODO: FIX UNNESTING (including .value.value)
    payroll_salary_monthly_get: Optional[Series[str]] = pa.Field(coerce=True, nullable=True, description="Base salary (monthly), used for getting nested json", alias="payroll.salary.monthlyPayment")
    payroll_salary_monthly_payment: Optional[Series[Float]] = pa.Field(coerce=True, nullable=True, description="Base salary (monthly)", alias="payroll.salary.monthlyPayment.value")
    payroll_salary_monthly_payment_currency: Optional[Series[str]] = pa.Field(coerce=True, nullable=True, description="Base salary (monthly) currency", alias="payroll.salary.monthlyPayment.currency")

    payroll_salary_yearly_get: Optional[Series[str]] = pa.Field(coerce=True, nullable=True, description="Base salary (yearly), used for getting nested json", alias="payroll.salary.yearlyPayment")
    payroll_salary_yearly_payment: Optional[Series[Float]] = pa.Field(coerce=True, nullable=True, description="Base salary (yearly)", alias="payroll.salary.yearlyPayment.value")
    payroll_salary_yearly_payment_currency: Optional[Series[str]] = pa.Field(coerce=True, nullable=True, description="Base salary (yearly) currency", alias="payroll.salary.yearlyPayment.currency")

    payroll_salary_active_effective_date: Optional[Series[str]] = pa.Field(coerce=True, nullable=True, description="effective date payment", alias="payroll.salary.activeEffectiveDate")
    payroll_salary_payment: Optional[Series[Float]] = pa.Field(coerce=True, nullable=True, description="Base Salary", alias="payroll.salary.payment")

    # Emergency contact
    emergency_first_name: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Emergency First Name", alias="emergency.firstName")
    emergency_second_name: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Emergency Middle Name", alias="emergency.secondName")
    emergency_surname: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Emergency Last Name", alias="emergency.surname")
    emergency_relation: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Emergency Relation", alias="emergency.relation")
    emergency_phone: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Emergency Phone", alias="emergency.phone")
    emergency_mobile_phone: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Emergency Mobile Phone", alias="emergency.mobilePhone")
    emergency_email: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Emergency Email", alias="emergency.email")
    emergency_address: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Emergency Address", alias="emergency.address")
    emergency_city: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Emergency City", alias="emergency.city")
    emergency_post_code: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Emergency Post Code", alias="emergency.postCode")
    emergency_country: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Emergency Country", alias="emergency.country")

    # Temporary address
    temporary_address_line1: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Temporary Address Line 1", alias="temporaryAddress.line1")
    temporary_address_line2: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Temporary Address Line 2", alias="temporaryAddress.line2")
    temporary_address_city: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Temporary City", alias="temporaryAddress.city")
    temporary_address_usa_state: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Temporary State", alias="temporaryAddress.usaState")
    temporary_address_country: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Temporary Country", alias="temporaryAddress.country")
    temporary_address_post_code: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Temporary Post Code", alias="temporaryAddress.postCode")

    # Lifecycle extras
    internal_period_since_termination: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Period Since Termination", alias="internal.periodSinceTermination")
    internal_years_since_termination: Optional[Series[Float]] = pa.Field(coerce=True, nullable=True, description="Years Since Termination", alias="internal.yearsSinceTermination")
    internal_notice: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Notice Period", alias="internal.notice")
    internal_lifecycle_status: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Lifecycle Status", alias="internal.lifecycleStatus")
    internal_status: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Status", alias="internal.status")
    internal_probation_end_date: Optional[Series[DateTime]] = pa.Field(coerce=True, nullable=True, description="Probation End Date", alias="internal.probationEndDate")
    internal_current_active_status_start_date: Optional[Series[DateTime]] = pa.Field(coerce=True, nullable=True, description="Current Active Start Date", alias="internal.currentActiveStatusStartDate")

    # EEO extras
    eeo_ethnicity: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Ethnicity", alias="eeo.ethnicity")
    eeo_job_category: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Job Category", alias="eeo.jobCategory")

    # People analytics
    people_analytics_age_risk_indicator: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Age Risk Indicator", alias="peopleAnalytics.ageRiskIndicator")
    people_analytics_kids_risk_indicator: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Kids Risk Indicator", alias="peopleAnalytics.kidsRiskIndicator")
    people_analytics_is_manager_risk_indicator: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Is Manager Risk Indicator", alias="peopleAnalytics.isManagerRiskIndicator")
    people_analytics_num_with_same_title_risk_indicator: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Num With Same Title Risk Indicator", alias="peopleAnalytics.numWithSameTitleRiskIndicator")
    people_analytics_team_size_risk_indicator: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Team Size Risk Indicator", alias="peopleAnalytics.teamSizeRiskIndicator")
    people_analytics_years_with_current_title_risk_indicator: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Years With Current Title Risk Indicator", alias="peopleAnalytics.yearsWithCurrentTitleRiskIndicator")
    people_analytics_years_with_recent_salary_risk_indicator: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Years With Recent Salary Risk Indicator", alias="peopleAnalytics.yearsWithRecentSalaryRiskIndicator")
    people_analytics_manager_tenure_risk_indicator: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Manager Tenure Risk Indicator", alias="peopleAnalytics.managerTenureRiskIndicator")
    people_analytics_num_of_direct_reports_risk_indicator: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Number Of Direct Reports Risk Indicator", alias="peopleAnalytics.numOfDirectReportsRiskIndicator")
    people_analytics_team_recent_turnover_risk_indicator: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Team Recent Turnover Risk Indicator", alias="peopleAnalytics.teamRecentTurnoverRiskIndicator")
    people_analytics_timeoff_frequency_risk_indicator: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Timeoff Frequency Risk Indicator", alias="peopleAnalytics.timeoffFrequencyRiskIndicator")
    people_analytics_tenure_rank_risk_indicator: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Tenure Rank Risk Indicator", alias="peopleAnalytics.tenureRankRiskIndicator")
    people_analytics_recent_manager_change_risk_indicator: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Recent Manager Change Risk Indicator", alias="peopleAnalytics.recentManagerChangeRiskIndicator")
    people_analytics_low_risk_counter: Optional[Series[Float]] = pa.Field(coerce=True, nullable=True, description="Low Risk Counter", alias="peopleAnalytics.lowRiskCounter")
    people_analytics_some_risk_counter: Optional[Series[Float]] = pa.Field(coerce=True, nullable=True, description="Some Risk Counter", alias="peopleAnalytics.someRiskCounter")
    people_analytics_at_risk_counter: Optional[Series[Float]] = pa.Field(coerce=True, nullable=True, description="At Risk Counter", alias="peopleAnalytics.atRiskCounter")

    # Positions / Job profile
    employee_position_opening_id: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Position Opening ID", alias="employee.positionOpeningId")
    employee_job_profile_id: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Job Profile ID", alias="employee.jobProfileId")
    employee_recent_leave_start_date: Optional[Series[DateTime]] = pa.Field(coerce=True, nullable=True, description="Recent Leave Start Date", alias="employee.recentLeaveStartDate")
    employee_recent_leave_end_date: Optional[Series[DateTime]] = pa.Field(coerce=True, nullable=True, description="Recent Leave End Date", alias="employee.recentLeaveEndDate")
    employee_first_day_of_work: Optional[Series[DateTime]] = pa.Field(coerce=True, nullable=True, description="First Day Of Work", alias="employee.firstDayOfWork")

    class Config:
        coerce = True
