from django.conf import settings


class GroupName:
    LENDER = "LENDER"
    MCP = "MASTER CHANNEL PARTNER"


class UserGroupSourceStatus:
    ACTIVE = "ACTIVE"
    CLOSED = "CLOSED"


class AccountStatus:
    LISTED = "LISTED"
    OPEN = "OPEN"


class UserGroup:
    MCP = 39
    CP = 37
    LENDER = 6
    BORROWER = 5


class AddressType:
    PERMANENT = "PERMANENT"
    COMMUNICATION = "COMMUNICATION"


class AddressConstants:
    COMMUNICATION_TYPE = "COMMUNICATION"
    PERMANENT_TYPE = "PERMANENT"


class DateFormat:
    YEAR_MONTH_DAY = "%Y-%m-%d"


class ServerType:
    PRODUCTION = "PRODUCTION"
    DEVELOPMENT = "DEVELOPMENT"


class TimeZone:
    indian_time = "Asia/Kolkata"


class DashboardFilterTypes:
    ALL = "all"
    ALL_CP = "all_cp"
    SELF = "self"
    CP_USER_ID = "cp_user_id"


class InvestorSource:
    LDC = "LDC"
    LCP = "LCP"
    MCP = "MCP"
    INTERNAL_SOURCES = ["LDC", "LCP", "MCP"]


class AccountAction:
    CREDIT = "CREDIT"
    DEBIT = "DEBIT"


class NomineeType:
    FAMILY = "FAMILY"
    NOMINEE = "NOMINEE"
    BENEFICIARY_OWNER = "BENEFICIARY_OWNER"
    COMPANY_DETAILS = "COMPANY_DETAILS"


class TransactionSortBy:
    amount_low_high = "amount_low_high"
    amount_high_low = "amount_high_low"
    date_low_high = "date_low_high"
    date_high_low = "date_high_low"

    SORT_CONDITIONS = {
        amount_low_high: "amount ASC",
        amount_high_low: "amount DESC",
        date_low_high: "sort_date ASC",
        date_high_low: "sort_date DESC",
    }


class AddBankAccountConstant:
    PRIMARY_PURPOSE = "PRIMARY"
    RAZOR_PAY_URL = settings.RAZOR_PAY_URL
    MAX_BANK_UPDATE_ATTEMPT = 5
    TITLE = "Bank Account Added Successfully"
    DESCRIPTION = "Your new bank account ending with XX{} is now set as default and ready to use for lending. Any repayments already in process will be credited to your previous bank account ending with XX{}"
    CP_TITLE = "Bank account added successfully"
    CP_DESCRIPTION = "Lender can start using the new bank account for add fund related transactions .However, all repayments and withdrawals will be processed to the primary bank only."
    MAX_LIMIT = 5
    SECONDARY_PURPOSE = "SECONDARY"
    CHANGE_BANK_ENABLE = False
    CP_MAX_BANK_ACCOUNT = 5
    MAX_ATTEMPT = 3


class ChecklistStep:
    LIVE_KYC = "LIVE KYC"


class KMIServices:
    INITIATE_KYC = "INITIATE KYC"


class DocumentConstant:
    SIGNED_NETWORTH_CERTIFICATE = "signed_networth_certificate"
    TERMS_AND_CONDITIONS = "TERMS AND CONDITIONS"
    AUTHORIZATION_LETTER = "authorization_letter"
    LENDER_AGREEMENT = "lender_agreement"
    PHOTOGRAPH = "photograph"
    DIGITAL_CERTIFICATE = "fmpp_digital_certificate"
    NETWORTH_CERTIFICATE_TYPE = "signed_networth_certificate"
    AADHAR_CARD_FRONT_BOTTOM = "aadhaar_front_bottom"
    BROKERAGE_INVOICE = "brokerage_invoice"
    PAN_CARD = "pan_card"
    RELATIONSHIP = "relationship"
    HUF_DEED = "huf_deed"
    BANK_VERIFICATION_DOCUMENT = "bank_verification_document"


class DocumentRemark:
    SUBMITTED = "SUBMITTED"
    REJECTED = "REJECTED"


class KmiCallBackStatus:
    INITIATED = "INITIATED"


class FMPPInvestmentType:
    MANUAL_LENDING = "MANUAL_LENDING"
    AUTO_LENDING = "AUTO_LENDING"
    ONE_TIME_LENDING = "ONE_TIME_LENDING"
    MEDIUM_TERM_LENDING = "MEDIUM_TERM_LENDING"


class TransactionStatus:
    SUCCESS = "SUCCESS"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    PENDING = "PENDING"
    FAIL = "FAIL"
    SCHEDULED = "SCHEDULED"
    IN_REVIEW = "IN REVIEW"
    EXPIRED = "EXPIRED"
    INITIATED = "INITIATED"
    HOLD = "HOLD"
    CREATED = "CREATED"
    ON_HOLD = "ON HOLD"
    IN_PROGRESS = "IN PROGRESS"


class NotificationStatus:
    READ = "READ"
    UNREAD = "UNREAD"


class CKYCServiceType:
    NAME_MATCH = "NAME_MATCH"


class KYCConstant:
    FAILED = "FAILED"
    IN_PROGRESS = "IN_PROGRESS"
    INITIATED = "INITIATED"
    SUCCESS = "SUCCESS"
    PENDING = "PENDING"
    RISK_HIGH = "HIGH"
    MANUAL = "MANUAL"


class CashFreeConstants:
    ESIGN = "ESIGN"
    SUCCESS = "SUCCESS"
    BANK_ACCOUNT = "BANK ACCOUNT"
    VALID = "VALID"


class KycServices:
    NAME_MATCH = "NAME_MATCH"


class ConsentData:
    LDC_kyc_consent_data = {
        "consent_type": "Verify_your_Identity",
        "remark": "I authorize the company to fetch my KYC details via Central "
        "KYC (CKYC) Registry.",
    }
    politically_exposed = {
        "consent_type": "Politically_exposed",
        "remark": "Are you a politically exposed person?",
    }


class KYCSource:
    MANUAL_SOURCE = "MANUAL"


class ReferenceConstant:
    TYPE_RM = "REFERRED_BY"
    RELATION_RM = "RM"
    TYPE_COMPANY_DETAILS = "COMPANY_DETAILS"
    DEFAULT_RM_EMAIL = (
        "7ee88f6bdc78d21ee5a387e6262be6cca90ed34ea4d2a2f7ab0db61a3e94ecbf"
    )


class RMReference:
    RELATION_RM = "RM"
    TYPE_RM = "REFERRED_BY"


class MandateConstants:
    CANCEL_MANDATE_REMARK = "Mandate Cancelled"
    NACH_ADD_MONEY = "NACH_ADD_MONEY"


class NachStatus:
    NOT_INITIATED = "NOT INITIATED"
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"


class MandateStatus:
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    INITIATED = "INITIATED"


class NMIConstants:
    CANCEL_MANDATE_REMARK = "Mandate Cancelled"


class SchemeStatus:
    INITIATED = "INITIATED"
    PROCESSING = "PROCESSING"
    SUCCESS = "SUCCESS"
    CANCELLED = "CANCELLED"
    EXPIRED = "EXPIRED"
    PENDING = "PENDING"
    ALL = "ALL"


class ReportFilterType:
    ALL = "all"


class ReportFilterKey:
    SCHEME_MATURITY = "SCHEME MATURITY"
    INACTIVITY_WITHDRAWAL = "INACTIVITY WITHDRAWAL"


class InvestorSourceId:
    LCP = "3"
    MCP = "8"


class TransactionType:
    FMPP_INVESTMENT = "FMPP INVESTMENT"
    MANUAL_LENDING = "MANUAL LENDING"
    AUTO_LENDING = "AUTO LENDING"
    SHORT_TERM_LENDING = "SHORT TERM LENDING"
    MEDIUM_TERM_LENDING = "MEDIUM TERM LENDING"
    LUMPSUM = "LUMPSUM"
    WITHDRAW_MONEY = "WITHDRAW MONEY"
    ADD_MONEY = "ADD MONEY"
    SCHEME_CANCELLATION = "SCHEME CANCELLATION"
    MANUAL_LENDING_AUTO_WITHDRAWAL = "MANUAL LENDING AUTO WITHDRAWAL"
    LUMPSUM_AUTO_WITHDRAWAL = "LUMPSUM AUTO WITHDRAWAL"
    SHORT_TERM_LENDING_AUTO_WITHDRAWAL = "SHORT TERM LENDING AUTO WITHDRAWAL"
    MEDIUM_TERM_LENDING_AUTO_WITHDRAWAL = "MEDIUM TERM LENDING AUTO WITHDRAWAL"
    AUTO_LENDING_REPAYMENT_WITHDRAWAL = "AUTO LENDING REPAYMENT WITHDRAWAL"
    MIP_AUTO_WITHDRAWAL = "MIP AUTO WITHDRAWAL"
    FMPP_REDEMPTION = "FMPP REDEMPTION"
    WITHDRAW_REQUEST_CANCELLED = "WITHDRAW REQUEST CANCELLED"
    LUMPSUM_REFUND = "LUMPSUM REFUND"
    SHORT_TERM_LENDING_REFUND = "SHORT TERM LENDING REFUND"
    MANUAL_LENDING_REFUND = "MANUAL LENDING REFUND"
    AUTO_LENDING_REPAYMENT_ADD_MONEY = "AUTO LENDING REPAYMENT ADD MONEY"
    MEDIUM_TERM_LENDING_REFUND = "MEDIUM TERM LENDING REFUND"
    CANCELLED_LOAN_REFUND = "CANCELLED LOAN REFUND"
    MANUAL_REPAYMENT_TRANSFER = "MANUAL REPAYMENT TRANSFER"
    MEDIUM_TERM_LENDING_REPAYMENT_TRANSFER = "MEDIUM TERM LENDING REPAYMENT TRANSFER"
    SHORT_TERM_LENDING_REPAYMENT_TRANSFER = "SHORT TERM LENDING REPAYMENT TRANSFER"
    IDLE_FUND_WITHDRAWAL = "IDLE FUND WITHDRAWAL"
    STL_LOAN_CANCELLATION = "STL LOAN CANCELLATION"
    MTL_LOAN_CANCELLATION = "MTL LOAN CANCELLATION"
    REVERSE_ADD_MONEY = "REVERSE ADD MONEY"
    REVENUE_TRANSFER = "REVENUE TRANSFER"
    REPAYMENT_AUTO_WITHDRAWAL = "REPAYMENT AUTO WITHDRAWAL"
    FMPP_REPAYMENT_WITHDRAWAL = "FMPP REPAYMENT WITHDRAWAL"
    REFUND_WITHDRAW_MONEY = "REFUND WITHDRAW MONEY"
    REJECTED_LOAN_REFUND = "REJECTED LOAN REFUND"
    LUMPSUM_REPAYMENT_TRANSFER = "LUMPSUM REPAYMENT TRANSFER"

    WITHDRAWAL_TRANSACTION_TYPE = [
        "WITHDRAW MONEY",
        "MANUAL LENDING AUTO WITHDRAWAL",
        "MIP AUTO WITHDRAWAL",
        "SHORT TERM LENDING AUTO WITHDRAWAL",
        "LUMPSUM AUTO WITHDRAWAL",
        "MEDIUM TERM LENDING AUTO WITHDRAWAL",
        "AUTO LENDING REPAYMENT WITHDRAWAL",
        "LUMPSUM REFUND",
        "SHORT TERM LENDING REFUND",
        "MANUAL LENDING REFUND",
        "MEDIUM TERM LENDING REFUND",
        "CANCELLED LOAN REFUND",
        "IDLE FUND WITHDRAWAL",
        "REVENUE TRANSFER",
        "REPAYMENT AUTO WITHDRAWAL",
        "REJECTED LOAN REFUND",
        "FMPP REPAYMENT WITHDRAWAL",
    ]
    ADD_MONEY_TRANSACTION_TYPES = [
        "ADD MONEY",
        "AUTO LENDING REPAYMENT ADD MONEY",
        "FMPP REDEMPTION",
    ]
    REPAYMENT_TYPES = [
        "MANUAL REPAYMENT TRANSFER",
        "MEDIUM TERM LENDING REPAYMENT TRANSFER",
        "SHORT TERM LENDING REPAYMENT TRANSFER",
    ]
    BORROWER_ESCROW_TXN_TYPE = [
        "MANUAL LENDING AUTO WITHDRAWAL",
        "MIP AUTO WITHDRAWAL",
        "SHORT TERM LENDING AUTO WITHDRAWAL",
        "LUMPSUM AUTO WITHDRAWAL",
        "REPAYMENT AUTO WITHDRAWAL",
        "AUTO LENDING REPAYMENT WITHDRAWAL",
        "REVENUE TRANSFER",
    ]
    SCHEME_CREATION_TYPES = (
        "MANUAL LENDING",
        "AUTO LENDING",
        "LUMPSUM",
        "SHORT TERM LENDING",
        "FMPP INVESTMENT",
    )
    ACTIVE_SCHEME_CREATION_TYPES = ("MANUAL LENDING", "LUMPSUM")
    CS_DASHBOARD_REFERRAL_INVESTMENT_TYPES = (
        "MANUAL LENDING",
        "LUMPSUM",
        "MEDIUM TERM LENDING",
        "SHORT TERM LENDING",
        "FMPP INVESTMENT",
        "AUTO LENDING",
    )


class AppRating:
    SUBMITTED = "SUBMITTED"
    SKIPPED = "SKIPPED"
    USER = "USER"
    SCHEME = "SCHEME"


class RPDStatus:
    SUCCESS = "SUCCESS"


class SearchKey:
    USER_ID = "USER_ID"
    EMAIL = "EMAIL"
    MOBILE_NO = "MOBILE_NO"
    PAN = "PAN"
    FIRST_NAME = "FIRST_NAME"


class AMLConstants:
    IN_REVIEW = "IN_REVIEW"


class NameMatchStatus:
    IN_REVIEW = "IN_REVIEW"


class SortConstant:
    FMPP = "fmpps"
    VALUE_OF_INVESTMENT = "value_of_investment"
    CREATED_DATE = "created_date"
    BALANCE = "balance"
    DESC = "desc"


class SummaryType:
    CMC = "CMC"


class DashboardInvestorFilter:
    PROFILE_NOT_COMPLETED = "PROFILE_NOT_COMPLETED"
    INACTIVE_WITH_ZERO_AUM = "INACTIVE_WITH_ZERO_AUM"


class PMIConstants:
    NACH = "NACH"


class DummyUserConstant:
    DUMMY_USER_ID = settings.DUMMY_USER_ID


class TransactionBlockForUser:
    user_pk_list = [
        782405,
        1054975,
        2982945,
        6745866,
        8110318,
        14906656,
        14905035,
        15351488,
        15363924,
    ]

    withdrawal_block = [
        782405,
        1054975,
        2982945,
        6745866,
        8110318,
        14906656,
        14905035,
        15351488,
        15363924,
    ]


class ReferralDetails:
    NO_REFERRAL_TEXT = "🚀 No referrals yet! Start sharing & earn ₹100 cash reward every time a friend lends!"
    REWARD_EARNED_TEXT = "You have earned cashback"
    REWARD_NOT_EARNED_TEXT = "Minimum lending not done yet"
    SEND_REMINDER = "SEND_REMINDER"
    INELIGIBLE_TEXT = "First lending amount was below ₹1000"
    PROCESSING_TEXT = "Cashback is being processed"
    FAILURE_TEXT = "Processing failed! Could not be completed"


class CampaignType:
    REFERRAL = "referral"


class RewardStatus:
    COMPLETED = "COMPLETED"
    PENDING = "PENDING"
    INELIGIBLE = "INELIGIBLE"
    PROCESSING = "PROCESSING"
    FAILED = "FAILED"
    IN_REVIEW = "IN REVIEW"
    REJECTED = "REJECTED"


class RMLenderFilterTypes:
    ASSIGNED_RM = "assigned_rm"
    UNASSIGNED_RM = "unassigned_rm"


class TransactionConstants:
    REJECTION_REASON = {"REFUND_OTL": "Loans were not available"}


class OfflinePaymentStatus:
    IN_REVIEW = "IN-REVIEW"
    PROCESSING = "PROCESSING"


class CashfreeConstant:
    ACTION = {
        "BANK_ACCOUNT": "BANK ACCOUNT",
    }


class InvoiceType:
    INDIVIDUAL = "INDIVIDUAL"


class RedisConstants:
    ML_FILTER_AND_SORT = "MLFilterAndSort"


class OTLInvestment:
    OTL_LOAN_TENURE_TYPE = " Month(s)"


class SchemeInfoListStatus:
    ALL = "ALL"
    SUCCESS = "SUCCESS"
    CANCELLED = "CANCELLED"
    FAILED = "FAILED"


class CPPaymentTypes:
    NACH = "NACH"
    ONLINE = "ONLINE"


class CancellationExpiryBuffer:
    INTERVAL_ONE_DAY = "1 day"


class ProductFormConstants:
    PRODUCT_FORM = "PRODUCT_FORM"
    FORM = "FORM"


class STLSchemePriorityOrderValues:
    ALLOW_COMPLETE_SCHEME_CREATION = 0


class FMITransactionStatus:
    FAILED = "F"
    IN_PROGRESS = "IP"


class FMISystem:
    MIN_AMOUNT = 1


class UPIMandateStatus:
    PAUSED = "PAUSED"
    CANCELLED = "CANCELLED"
    REVOKED = "REVOKED"


class ExpiredTransaction:
    FALSE = "FALSE"


class HOFMember:
    REFERENCE_TYPE = "FAMILY_MEMBER"


class MaskingConstants:
    EMAIL = {"masking_char": "*", "masking_format": "MASK_BETWEEN"}
    PAN = {"masking_char": "X", "masking_format": "MASK_LEFT"}
    MOBILE = {"masking_char": "X", "masking_format": "MASK_LEFT"}
    AADHAR = {"masking_char": "X", "masking_format": "MASK_LEFT"}
    MASK_BETWEEN = "MASK_BETWEEN"
    MASK_LEFT = "MASK_LEFT"
    MASK_RIGHT = "MASK_RIGHT"
    MASK_SOURCE_LIST = settings.MASK_SOURCE_LIST


class BankVerificationStatus:
    APPROVED = "APPROVED"
    PENDING = "PENDING"
    REJECTED = "REJECTED"


class ApplicationConfigDashboardConstant:
    UPDATE_PRODUCT_CONFIG_ACTIONS = {
        "UPDATE_LOAN_AMOUNT": "UPDATE_LOAN_AMOUNT",
        "ADD_SLABS_BY_TENURE": "ADD_SLABS_BY_TENURE",
        "ADD_LOAN_TENURE": "ADD_LOAN_TENURE",
        "REMOVE_LOAN_TENURE": "REMOVE_LOAN_TENURE",
        "UPDATE_SCHEME_MASTER_MIN_MAX": "UPDATE_SCHEME_MASTER_MIN_MAX",
    }
    SCHEME_PRIORITIZATION_CONSTANT = {
        "CONFIG_TYPE": "SCHEME_PRIORITIZATION",
        "CONFIG_KEY": "SCHEME_CREATION",
    }
    LUMPSUM = {"MONTHLY": "LUMPSUM_MONTHLY", "DAILY": "LUMPSUM_DAILY"}
    PRODUCT_CONFIGURATION_CONSTANT = {
        "CONFIG_TYPE": "PRODUCT_CONFIGURATION",
        "CONFIG_KEY": "PRODUCT_CONFIGURATION",
    }
    LIVE_LOAN_CONSTANT = {"CONFIG_TYPE": "LIVE_LOAN", "CONFIG_KEY": "LIVE_LOAN"}
    LIVE_LOAN_ACTIONS = {
        "GET_LOAN_CONFIGURATION_PARAMETERS": "GET_LOAN_CONFIGURATION_PARAMETERS",
        "GET_LOAN_DATA": "GET_LOAN_DATA",
        "GET_LOAN_SUMMARY": "GET_LOAN_SUMMARY",
        "RELEASE_SELECTED_LOANS": "RELEASE_SELECTED_LOANS",
    }
    ANALYTICS_CONSTANT = {
        "WITHDRAW_MONEY": "WITHDRAW MONEY",
        "ADD_MONEY": "ADD MONEY",
        "SUCCESS": "SUCCESS",
        "FAILED": "FAILED",
        "PROCESSING": "PROCESSING",
    }
    ACCOUNT_DELETION_CONSTANT = {
        "DELETION": "ACCOUNT_DELETION",
        "CANCEL_DELETION": "CANCEL_DELETION_REQUEST",
    }
    ACCOUNT_DEACTIVATION_CONSTANT = {
        "ACCOUNT_DEACTIVATION": "ACCOUNT_DEACTIVATION",
        "ACCOUNT_REACTIVATION": "ACCOUNT_REACTIVATION",
    }


class FMPPDatabaseLink:
    DEVELOPMENT = "qafmpp"
    PRODUCTION = "fmpp"


class ProductConstants:
    LDCProduct = "RETAIL"
    CPProduct = "CP"
    ExternalPartnerProduct = "ALLIANCES"


class DashboardExtendedAccountAction:
    INVESTMENT_ACTION_FILTER_MAP = {
        AccountAction.DEBIT: [
            TransactionType.MANUAL_LENDING,
            TransactionType.MEDIUM_TERM_LENDING,
            TransactionType.SHORT_TERM_LENDING,
            TransactionType.FMPP_INVESTMENT,
            TransactionType.LUMPSUM,
        ]
    }


class TransactionActionFilterMap:
    ACTION_FILTER_MAP = {
        AccountAction.CREDIT: [
            TransactionType.ADD_MONEY,
            TransactionType.AUTO_LENDING_REPAYMENT_ADD_MONEY,
        ],
        AccountAction.DEBIT: [
            TransactionType.WITHDRAW_MONEY,
            TransactionType.MIP_AUTO_WITHDRAWAL,
            TransactionType.MANUAL_LENDING_AUTO_WITHDRAWAL,
            TransactionType.LUMPSUM_AUTO_WITHDRAWAL,
            TransactionType.IDLE_FUND_WITHDRAWAL,
            TransactionType.AUTO_LENDING_REPAYMENT_WITHDRAWAL,
            TransactionType.REPAYMENT_AUTO_WITHDRAWAL,
            TransactionType.CANCELLED_LOAN_REFUND,
            TransactionType.REJECTED_LOAN_REFUND,
            TransactionType.FMPP_REPAYMENT_WITHDRAWAL,
        ],
    }


class TransactionFilter:  # Valid category values
    CATEGORY_ADD_FUNDS = "ADD_FUNDS"
    CATEGORY_REPAYMENT = "REPAYMENT"
    CATEGORY_WITHDRAWAL = "WITHDRAWAL"
    CATEGORY_AUTO_WITHDRAWAL = "AUTO_WITHDRAWAL"


class DashboardTransactionStatusFilterMap:
    STATUS_FILTER_MAP = {
        TransactionStatus.SUCCESS: [
            TransactionStatus.SUCCESS,
            TransactionStatus.COMPLETED,
        ],
        TransactionStatus.FAILED: [
            TransactionStatus.FAILED,
            TransactionStatus.FAIL,
            TransactionStatus.EXPIRED,
            TransactionStatus.CANCELLED,
        ],
        TransactionStatus.PROCESSING: [
            TransactionStatus.PROCESSING,
            TransactionStatus.PENDING,
            TransactionStatus.SCHEDULED,
        ],
    }


class ReferralLendingConstant:
    FIRST_LENDING_ML = "FIRST_LENDING_ML"
    FIRST_LENDING_LUMPSUM = "FIRST_LENDING_LUMPSUM"
    first_lending_types = ["FIRST_LENDING_ML", "FIRST_LENDING_LUMPSUM"]


class InvestmentFilter:
    CATEGORY_INVESTMENT = "INVESTMENT"
    CATEGORY_CANCELLED_LOAN_REFUND = "CANCELLED_LOAN_REFUND"


class DashboardTransactionActionFilterMap:
    ACTION_FILTER_MAP = {
        AccountAction.CREDIT: [
            TransactionType.ADD_MONEY,
            TransactionType.AUTO_LENDING_REPAYMENT_ADD_MONEY,
        ],
        AccountAction.DEBIT: [
            TransactionType.WITHDRAW_MONEY,
            TransactionType.MIP_AUTO_WITHDRAWAL,
            TransactionType.MANUAL_LENDING_AUTO_WITHDRAWAL,
            TransactionType.LUMPSUM_AUTO_WITHDRAWAL,
            TransactionType.IDLE_FUND_WITHDRAWAL,
            TransactionType.AUTO_LENDING_REPAYMENT_WITHDRAWAL,
            TransactionType.REPAYMENT_AUTO_WITHDRAWAL,
            TransactionType.CANCELLED_LOAN_REFUND,
            TransactionType.REJECTED_LOAN_REFUND,
            TransactionType.FMPP_REPAYMENT_WITHDRAWAL,
            TransactionType.MANUAL_LENDING,
            TransactionType.MEDIUM_TERM_LENDING,
            TransactionType.SHORT_TERM_LENDING,
            TransactionType.FMPP_INVESTMENT,
            TransactionType.LUMPSUM,
        ],
    }


class TransactionTypeFilterMap:
    TYPE_FILTER_MAP = {
        TransactionFilter.CATEGORY_ADD_FUNDS: [TransactionType.ADD_MONEY],
        TransactionFilter.CATEGORY_WITHDRAWAL: [TransactionType.WITHDRAW_MONEY],
        TransactionFilter.CATEGORY_REPAYMENT: [
            TransactionType.MIP_AUTO_WITHDRAWAL,
            TransactionType.MANUAL_LENDING_AUTO_WITHDRAWAL,
            TransactionType.LUMPSUM_AUTO_WITHDRAWAL,
            TransactionType.REPAYMENT_AUTO_WITHDRAWAL,
            TransactionType.AUTO_LENDING_REPAYMENT_WITHDRAWAL,
            TransactionType.AUTO_LENDING_REPAYMENT_ADD_MONEY,
            TransactionType.FMPP_REPAYMENT_WITHDRAWAL,
        ],
        TransactionFilter.CATEGORY_AUTO_WITHDRAWAL: [
            TransactionType.IDLE_FUND_WITHDRAWAL,
            TransactionType.REJECTED_LOAN_REFUND,
        ],
        InvestmentFilter.CATEGORY_INVESTMENT: [
            TransactionType.MANUAL_LENDING,
            TransactionType.MEDIUM_TERM_LENDING,
            TransactionType.SHORT_TERM_LENDING,
            TransactionType.FMPP_INVESTMENT,
            TransactionType.LUMPSUM,
        ],
        InvestmentFilter.CATEGORY_CANCELLED_LOAN_REFUND: [
            TransactionType.CANCELLED_LOAN_REFUND
        ],
    }


class ReferralBlockForUser:
    user_source_group_id_list = []


class AccountSource:
    LDC = "LDC"
    CP = "CP"
    MCP = "MCP"


class TransactionStatusFilterMap:
    STATUS_FILTER_MAP = {
        TransactionStatus.SUCCESS: [TransactionStatus.SUCCESS],
        TransactionStatus.FAILED: [TransactionStatus.FAILED, TransactionStatus.FAIL],
        TransactionStatus.PROCESSING: [
            TransactionStatus.PROCESSING,
            TransactionStatus.PENDING,
            TransactionStatus.SCHEDULED,
        ],
    }
