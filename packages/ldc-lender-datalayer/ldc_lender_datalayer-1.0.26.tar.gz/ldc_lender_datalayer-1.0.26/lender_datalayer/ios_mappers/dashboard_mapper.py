"""
Dashboard Mapper using BaseDataLayer architecture
Converts the old dashboard_mapper.py to use the new data layer pattern
"""

from datetime import datetime

from django.conf import settings

from ..base_datalayer import BaseDataLayer, DataLayerUtils
from ..common.constants import (AccountAction, AddBankAccountConstant, ApplicationConfigDashboardConstant,
                                DashboardExtendedAccountAction, DashboardTransactionActionFilterMap,
                                DashboardTransactionStatusFilterMap, FMPPDatabaseLink, InvestmentFilter, InvestorSource,
                                NomineeType, ProductConstants, ProductFormConstants, ReferenceConstant,
                                ReferralLendingConstant, TimeZone, TransactionActionFilterMap, TransactionFilter,
                                TransactionSortBy, TransactionStatus, TransactionType, TransactionTypeFilterMap,
                                UserGroup)
from ..common.utils.datetime_utils import get_todays_date
from ..ims_mappers.investor_mapper import InvestorMapper


class DashboardMapper(BaseDataLayer):
    """
    Dashboard Mapper using BaseDataLayer for database operations
    Handles dashboard configuration and user management operations
    """

    def __init__(self, db_alias="default"):
        super().__init__(db_alias)

    def get_entity_name(self):
        """Return the entity name this mapper handles"""
        return "IOS_DASHBOARD"

    @staticmethod
    def get_dashboard_config_keys(logical_reference):
        query = """
            SELECT config_type, config_key
            FROM lendenapp_application_config
        """

        params = {}
        if "ALL" not in logical_reference:
            query += f"WHERE logical_reference = ANY(%s) "
            params = [logical_reference]

        query += """
            GROUP BY config_type, config_key
            ORDER BY config_type, config_key
        """

        return DashboardMapper().sql_execute_fetch_all(query, params, to_dict=True)

    @staticmethod
    def get_filter_set(filter_data, filter_key, filter_map):
        """Flatten filter selections into a set of values."""
        return set(
            item
            for key in filter_data.get(filter_key, [])
            for item in filter_map.get(key, [])
        )

    @staticmethod
    def get_all_form_configuration(logical_reference):
        refs = logical_reference or []
        required_logical_reference = [
            ProductFormConstants.PRODUCT_FORM,
            ProductFormConstants.FORM,
        ]
        has_all = "ALL" in refs
        has_required_subset = all(
            form_reference in refs for form_reference in required_logical_reference
        )

        if not has_all and not has_required_subset:
            return []

        query = """
          SELECT config_type, config_key
          FROM lendenapp_application_config
          WHERE form_configuration IS NOT NULL or logical_reference=%(logical_reference)s
        """
        params = {"logical_reference": ProductFormConstants.PRODUCT_FORM}

        return DashboardMapper().sql_execute_fetch_all(query, params, to_dict=True)

    @staticmethod
    def get_config_value_form_configuration(config_type, config_key):
        query = """
         SELECT config_value,form_configuration
         FROM lendenapp_application_config
         WHERE config_type = %s AND config_key = %s and form_configuration is not null
        """
        params = [config_type, config_key]
        return DashboardMapper().sql_execute_fetch_all(query, params, to_dict=True)

    def get_dashboard_users(self, allowed_roles):
        query = """
            SELECT 
            lc.first_name as name,
            lc.encoded_email as email,
            lc.id,
            array_agg(ag.name) as roles
            FROM
                lendenapp_customuser lc
            JOIN
                lendenapp_customuser_groups lcg ON lc.id = lcg.customuser_id
            JOIN
                auth_group ag ON ag.id = lcg.group_id
            WHERE
                ag.name = ANY(%(allowed_roles)s)
            GROUP BY
                lc.id;
        """

        params = {"allowed_roles": allowed_roles}
        return self.sql_execute_fetch_all(query, params, to_dict=True)

    def delete_user_role(self, user_pk, role):
        query = """
            DELETE FROM lendenapp_customuser_groups
            WHERE customuser_id = %(user_pk)s
            AND group_id = (SELECT id FROM auth_group WHERE name = %(role)s) RETURNING 1
        """
        params = {"user_pk": user_pk, "role": role}
        return self.sql_execute_fetch_all(query, params, to_dict=True)

    def search_user(self, search_term):
        query = """
            SELECT 
            lc.first_name as name,
            lc.encoded_email as email,
            lc.id,
            array_agg(ag.name) as roles
            FROM
                lendenapp_customuser lc
            LEFT JOIN
                lendenapp_customuser_groups lcg ON lc.id = lcg.customuser_id
            LEFT JOIN
                auth_group ag ON ag.id = lcg.group_id
            WHERE
                lc.email = %(search_term)s
            GROUP BY lc.id;
        """
        params = {"search_term": search_term}
        return self.sql_execute_fetch_all(query, params, to_dict=True)

    def get_roles(self, user_id):
        query = """
            SELECT ag.name
            FROM auth_group ag
            JOIN lendenapp_customuser_groups lcg ON ag.id = lcg.group_id
            WHERE lcg.customuser_id = %(user_id)s
        """
        params = {"user_id": user_id}
        return self.sql_execute_fetch_all(query, params, to_dict=True)

    def assign_role(self, user_id, role_name):
        query = """
            INSERT INTO lendenapp_customuser_groups (customuser_id, group_id)
            VALUES (%(user_id)s, (SELECT id FROM auth_group WHERE name = %(role_name)s))
            RETURNING 1
        """
        params = {"user_id": user_id, "role_name": role_name}
        return self.sql_execute_fetch_all(query, params, to_dict=True)

    @staticmethod
    def get_dashboard_data(query, params=None):
        if params is None:
            params = {}
        return DashboardMapper().sql_execute_fetch_all(query, params, to_dict=True)

    @staticmethod
    def daily_transaction_details(transaction_type, start_date, end_date):
        status_list = [
            ApplicationConfigDashboardConstant.ANALYTICS_CONSTANT["SUCCESS"],
            ApplicationConfigDashboardConstant.ANALYTICS_CONSTANT["FAILED"],
            ApplicationConfigDashboardConstant.ANALYTICS_CONSTANT["PROCESSING"],
        ]
        # return zero if no data
        query = """
        SELECT count(*), status 
        FROM lendenapp_transaction lt 
        WHERE type = %(transaction_type)s
        AND date >= %(start_date)s
        AND date < %(end_date)s
        AND status = ANY(%(status_list)s) 
        GROUP BY status
        """
        params = {
            "transaction_type": transaction_type,
            "start_date": start_date,
            "end_date": end_date,
            "status_list": status_list,
        }
        return DashboardMapper().sql_execute_fetch_all(query, params, to_dict=True)

        # In your dashboard_mapper.py file

    @staticmethod
    def funnel_data(start_date, end_date):
        query = """
        SELECT 
        DATE(lendenapp_timeline.created_date) AS activity_date,
        COUNT(DISTINCT CASE WHEN lendenapp_timeline.activity = 'SIGN_UP' THEN lendenapp_timeline.user_source_group_id END) AS SIGN_UP,
        COUNT(DISTINCT CASE WHEN lendenapp_timeline.activity = 'VERIFY_IDENTITY' THEN lendenapp_timeline.user_source_group_id END) AS VERIFY_IDENTITY,
        COUNT(DISTINCT CASE WHEN lendenapp_timeline.activity = 'LIVE_KYC' THEN lendenapp_timeline.user_source_group_id END) AS LIVE_KYC,
        COUNT(DISTINCT CASE WHEN lendenapp_timeline.activity = 'LEGAL_AUTHORIZATION' THEN lendenapp_timeline.user_source_group_id END) AS LEGAL_AUTHORIZATION,
        COUNT(DISTINCT CASE WHEN lendenapp_timeline.activity = 'BANK_ACCOUNT' THEN lendenapp_timeline.user_source_group_id END) AS BANK_ACCOUNT,
        COUNT(DISTINCT CASE WHEN lendenapp_timeline.activity = 'CONSENT AGREED' AND la.status = 'LISTED' THEN lendenapp_timeline.user_source_group_id END) AS LISTED,
        COUNT(DISTINCT CASE WHEN lendenapp_timeline.activity = 'CONSENT AGREED' AND la.status = 'OPEN' THEN lendenapp_timeline.user_source_group_id END) AS OPEN
        FROM lendenapp_timeline
        JOIN lendenapp_user_source_group lusg ON lusg.id = lendenapp_timeline.user_source_group_id
        LEFT JOIN lendenapp_account la ON la.user_source_group_id = lusg.id 
        WHERE lusg.source_id = 7 
        AND lendenapp_timeline.created_date >= %(start_date)s
        AND lendenapp_timeline.created_date <= %(end_date)s
        GROUP BY DATE(lendenapp_timeline.created_date)
        ORDER BY DATE(lendenapp_timeline.created_date) DESC"""

        params = {"start_date": start_date, "end_date": end_date}
        return DashboardMapper().sql_execute_fetch_all(query, params, to_dict=True)

    @staticmethod
    def kyc_failure_count(start_date, end_date):
        query = """
        SELECT
        luk.event_code,luk.service_type,
        COUNT(DISTINCT luk.id) AS failure_count
        FROM
            lendenapp_userkyctracker AS lukt 
        INNER JOIN
            lendenapp_userkyc AS luk ON luk.tracking_id = lukt.tracking_id
        WHERE
            lukt.kyc_type = 'LIVE KYC'
            AND lukt.kyc_source = 'KMI'
            AND lukt.created_date >= %(start_date)s
            AND lukt.created_date <= %(end_date)s
            AND lukt.status = 'FAILED'
        GROUP BY
            luk.event_code,luk.service_type
        ORDER BY
            failure_count DESC; """

        params = {"start_date": start_date, "end_date": end_date}
        return DashboardMapper().sql_execute_fetch_all(query, params, to_dict=True)

    @staticmethod
    def get_lending_summary_dashboard(from_date, to_date):
        fmpp_database_link = (
            FMPPDatabaseLink.PRODUCTION
            if settings.SERVER_TYPE == "PRODUCTION"
            else FMPPDatabaseLink.DEVELOPMENT
        )

        query = f"""
            SELECT 
            CASE 
                WHEN tmp.value_1 = 'LDC' THEN {ProductConstants.LDCProduct} 
                ELSE {ProductConstants.CPProduct}
            END AS partner_code,
            sum(investment_amount)
            FROM {fmpp_database_link}.t_investor_scheme tis
            INNER JOIN {fmpp_database_link}.t_mst_parameter tmp 
            ON tis.partner_code_id = tmp.id
            WHERE tis.created_date
        """

        if from_date and to_date:
            query += " BETWEEN %(from_date)s AND %(to_date)s"
            params = {"from_date": from_date, "to_date": to_date}
        else:
            todays_date = get_todays_date()
            query += " = %(todays_date)s"
            params = {"todays_date": todays_date}

        query += " GROUP BY partner_code"

        return DashboardMapper().sql_execute_fetch_all(query, params, to_dict=True)

    @staticmethod
    def get_pending_supply_tenure_wise(start_date, end_date):
        query = f"""
            SELECT
                CASE
                    WHEN ls2.source_name = ANY(ARRAY['{InvestorSource.LCP}', '{InvestorSource.MCP}']) THEN 'CP'
                    WHEN ls2.source_name = ANY(ARRAY['{InvestorSource.LDC}']) THEN 'Retail'
                END as source_name,
                lendenapp_transaction."date"::date as "Date",
                SUM(ls.amount) as "Total_supply",
                SUM(CASE WHEN ls.status IN ('SUCCESS') THEN ls.amount ELSE 0 END) as "Available_supply_deployed",
                SUM(CASE WHEN ls.status IN ('INITIATED') THEN ls.amount ELSE 0 END) as "Available_supply_to_deploy",
                SUM(CASE WHEN ls.tenure = 5 AND ls.status = 'INITIATED' THEN ls.amount ELSE 0 END) as "Available_5M_supply_to_deploy",
                SUM(CASE WHEN ls.tenure = 7 AND ls.status = 'INITIATED' THEN ls.amount ELSE 0 END) as "Available_7M_supply_to_deploy",
                SUM(CASE WHEN ls.tenure = 14 AND ls.status = 'INITIATED' THEN ls.amount ELSE 0 END) as "Available_14_supply_to_deploy"
            FROM lendenapp_schemeinfo ls
            INNER JOIN lendenapp_transaction ON lendenapp_transaction.id = ls.transaction_id
            INNER JOIN lendenapp_user_source_group lusg ON lusg.id = ls.user_source_group_id
            INNER JOIN lendenapp_source ls2 ON ls2.id = lusg.source_id
            WHERE lendenapp_transaction."date"::date >= (
                SELECT MIN(created_date::date) 
                FROM lendenapp_schemeinfo 
                WHERE status = 'INITIATED' 
                AND investment_type = ANY(ARRAY['ONE_TIME_LENDING', 'MEDIUM_TERM_LENDING'])
            )
            AND lendenapp_transaction."date"::date BETWEEN %(start_date)s AND %(end_date)s
            AND ls.status = ANY(ARRAY['INITIATED', 'SUCCESS'])
            AND ls.tenure = ANY(ARRAY[5, 7, 14])
            GROUP BY 
                lendenapp_transaction."date"::date,
                ls2.source_name
            ORDER BY 
                lendenapp_transaction."date"::date DESC;
        """
        params = {"start_date": start_date, "end_date": end_date}

        return DashboardMapper().sql_execute_fetch_all(query, params, to_dict=True)

    @staticmethod
    def get_pending_supply_date_wise(start_date, end_date):
        query = f"""
            SELECT 
            lendenapp_transaction."date"::date as "Date",
            CASE
                WHEN ls2.source_name = ANY(ARRAY['{InvestorSource.LCP}', '{InvestorSource.MCP}']) THEN 'CP'
                WHEN ls2.source_name = '{InvestorSource.LDC}' THEN 'Retail'
            END 
            as source_group_name,
            sum(case when ls.tenure = 5 and ls.status= 'INITIATED' then ls.amount else 0 end) as "Available_5M_supply_to_deploy",
            sum(case when ls.tenure = 7 and ls.status= 'INITIATED' then ls.amount else 0 end) as "Available_7M_supply_to_deploy",
            sum(case when ls.tenure = 11 and ls.status= 'INITIATED' then ls.amount else 0 end) as "Available_11M_supply_to_deploy",
            sum(case when ls.tenure = 14 and ls.status= 'INITIATED' 
                and (select product_type from lendenapp_otl_scheme_tracker lost 
                     where is_latest and lost.scheme_id = ls.scheme_id) = 'DAILY' 
                then ls.amount else 0 end) as "Available_14D_supply_to_deploy",
            sum(case when ls.tenure = 14 and ls.status= 'INITIATED' 
                and (select product_type from lendenapp_otl_scheme_tracker lost 
                     where is_latest and lost.scheme_id = ls.scheme_id) = 'MONTHLY' 
                then ls.amount else 0 end) as "Available_14M_supply_to_deploy"
        FROM lendenapp_schemeinfo ls
        INNER JOIN lendenapp_transaction ON lendenapp_transaction.id = ls.transaction_id 
        INNER JOIN lendenapp_user_source_group lusg ON lusg.id = ls.user_source_group_id
        INNER JOIN lendenapp_source ls2 on lusg.source_id = ls2.id
        WHERE lendenapp_transaction."date"::date >= (
            SELECT min(created_date::date) 
            FROM lendenapp_schemeinfo 
            WHERE status = 'INITIATED' 
            AND investment_type = ANY(ARRAY['ONE_TIME_LENDING','MEDIUM_TERM_LENDING'])
        ) 
        AND ls2.source_name = ANY(ARRAY['{InvestorSource.LCP}', '{InvestorSource.MCP}', '{InvestorSource.LDC}'])
        AND ls.status = ANY(ARRAY['INITIATED', 'SUCCESS'])
        AND ls.tenure = ANY(ARRAY[5, 7, 11, 14])
        AND lendenapp_transaction."date"::date BETWEEN %(start_date)s AND %(end_date)s
        GROUP BY 
            CASE
                WHEN ls2.source_name = ANY(ARRAY['{InvestorSource.LCP}', '{InvestorSource.MCP}']) THEN 'CP'
                WHEN ls2.source_name = '{InvestorSource.LDC}' THEN 'Retail'
                end,
                lendenapp_transaction."date"::date
        ORDER BY lendenapp_transaction."date"::date DESC, source_group_name
        """

        params = {"start_date": start_date, "end_date": end_date}
        return DashboardMapper().sql_execute_fetch_all(query, params, to_dict=True)

    def fetch_investor_details(self, data):

        sql = f"""
            select lc2.partner_id, ls.source_name as partner_code,
            lc3.first_name as cp_name, lc.user_id,lc.id as user_pk,
            lc.first_name, lc.gender, lc.encoded_mobile as mobile_number, lc.encoded_email as email, 
            lc.dob, lc.encoded_pan as pan, lc.type, 
            lc.gross_annual_income, 
            la2.user_source_group_id, lt.checklist, 
            la2.created_date::date, la2.balance, la2.status, 
            la2.listed_date, la2.number
            from lendenapp_user_source_group lusg 
            join lendenapp_account la2 on lusg.id = la2.user_source_group_id 
            join lendenapp_task lt on lt.user_source_group_id = lusg.id
            join lendenapp_source ls on ls.id = lusg.source_id 
            join lendenapp_customuser lc on lc.id = lusg.user_id
            left join lendenapp_channelpartner lc2 on 
            lc2.id = lusg.channel_partner_id  
            left join lendenapp_customuser lc3 on lc3.id = lc2.user_id 
            WHERE lusg.group_id = %(group)s 
            """

        params = {
            "group": UserGroup.LENDER,
        }

        search = data.get("search")
        search_query_type = data.get("search_query_type")

        if search:
            sql += f" and {InvestorMapper.dashboard_search_sql_query(params, search, search_query_type)}"

        if not data["is_download"]:
            params["limit"] = data["limit"]
            params["offset"] = data["offset"]
            sql += " LIMIT %(limit)s OFFSET %(offset)s"

        return DashboardMapper().sql_execute_fetch_all(sql, params, to_dict=True)

    def fetch_investor_profile_data(self, user_source_group_id):
        sql = f"""select lc2.partner_id, ls.source_name as partner_code,
            lc3.first_name as cp_name, lc.user_id,lc.id as user_pk,
            lc.first_name, lc.gender, lc.encoded_mobile as mobile_number, lc.encoded_email as email, 
            lc.dob, lc.encoded_pan as pan, lc.type, 
            lc.gross_annual_income, lc.mnrl_status,
            la2.user_source_group_id, lt.checklist, 
            la2.created_date::date, la2.balance, la2.status, 
            la2.listed_date, lusg.created_at as signed_up_date, la2.number
            from lendenapp_user_source_group lusg
            join lendenapp_account la2 on lusg.id = la2.user_source_group_id 
            join lendenapp_task lt on lt.user_source_group_id = lusg.id
            join lendenapp_source ls on ls.id = lusg.source_id 
            join lendenapp_customuser lc on lc.id = lusg.user_id
            left join lendenapp_channelpartner lc2 on 
            lc2.id = lusg.channel_partner_id  
            left join lendenapp_customuser lc3 on lc3.id = lc2.user_id 
            WHERE lusg.id = %(user_source_group_id)s 
            """

        params = {
            "user_source_group_id": user_source_group_id,
        }

        return self.sql_execute_fetch_one(sql, params, to_dict=True)

    @staticmethod
    def fetch_reserved_amount(user_id):
        sql = """
            SELECT COALESCE(SUM(ls.amount), 0) as reserved_amount
            FROM lendenapp_schemeinfo ls
            WHERE ls.user_source_group_id IN (
                SELECT lusg.id 
                FROM lendenapp_customuser lc
                JOIN lendenapp_user_source_group lusg ON lc.id = lusg.user_id
                WHERE lc.user_id = %(user_id)s
            )
            AND ls.status = 'INITIATED'
        """

        params = {"user_id": user_id}

        result = DashboardMapper().sql_execute_fetch_one(sql, params, to_dict=True)
        return result.get("reserved_amount", 0) if result else 0

    @staticmethod
    def fetch_nominee_details(user_source_group_id):
        """
        Fetch nominee details for a specific user source group

        Args:
            user_source_group_id: User source group ID

        Returns:
            dict with nominee details or None if not found
        """
        query = """
            SELECT
                lr.name as full_name,
                lr.dob as nominee_dob,
                lr.relation as nominee_relation,
                lr.mobile_number,
                lr.email as nominee_email,
                lr.type as nominee_type
            FROM
                lendenapp_reference lr
            WHERE
                lr.user_source_group_id = %(user_source_group_id)s
                AND lr.type = %(type)s
        """

        params = {
            "user_source_group_id": user_source_group_id,
            "type": NomineeType.NOMINEE,
        }

        return DashboardMapper().sql_execute_fetch_one(query, params, to_dict=True)

    @staticmethod
    def fetch_user_bank_account_details(user_source_group_id):
        """
        Fetch detailed bank account information for a user
        """
        query = """
            SELECT 
                lba.id as bank_id,
                lb.name,
                lba.number as acc_number,
                lba.type,
                lba.ifsc_code,
                lba.purpose as acc_status,
                la.primary_status_updated_at
            FROM 
                lendenapp_bankaccount lba 
            inner join lendenapp_bank lb on lb.id=lba.bank_id
            left join lendenapp_account la on lba.user_source_group_id =la.user_source_group_id
            WHERE 
                lba.user_source_group_id = %(user_source_group_id)s
                AND lba.is_active = True
        """

        params = {"user_source_group_id": user_source_group_id}

        return DashboardMapper().sql_execute_fetch_all(query, params, to_dict=True)

    @staticmethod
    def fetch_rm_name_by_user_id(user_source_group_id):
        query = """
            SELECT 
                lr.name 
            FROM 
                lendenapp_reference lr
            WHERE
                lr.user_source_group_id = %(user_source_group_id)s
                AND lr.relation = %(relation)s
        """

        params = {
            "user_source_group_id": user_source_group_id,
            "relation": ReferenceConstant.RELATION_RM,
        }

        return DashboardMapper().sql_execute_fetch_one(query, params, to_dict=True)

    @staticmethod
    def fetch_transactions_list(limit, offset, user_source_id, filter_data, sort_data):
        # Default configuration
        default_config = {
            "status": (
                TransactionStatus.FAILED,
                TransactionStatus.FAIL,
                TransactionStatus.SUCCESS,
                TransactionStatus.SCHEDULED,
                TransactionStatus.PROCESSING,
                TransactionStatus.PENDING,
                TransactionStatus.COMPLETED,
                TransactionStatus.CANCELLED,
                TransactionStatus.EXPIRED,
            ),
            "types": (
                TransactionType.ADD_MONEY,
                TransactionType.WITHDRAW_MONEY,
                TransactionType.MIP_AUTO_WITHDRAWAL,
                TransactionType.MANUAL_LENDING_AUTO_WITHDRAWAL,
                TransactionType.LUMPSUM_AUTO_WITHDRAWAL,
                TransactionType.IDLE_FUND_WITHDRAWAL,
                TransactionType.REPAYMENT_AUTO_WITHDRAWAL,
                TransactionType.AUTO_LENDING_REPAYMENT_WITHDRAWAL,
                TransactionType.CANCELLED_LOAN_REFUND,
                TransactionType.REJECTED_LOAN_REFUND,
                TransactionType.AUTO_LENDING_REPAYMENT_ADD_MONEY,
                TransactionType.FMPP_REPAYMENT_WITHDRAWAL,
                TransactionType.MANUAL_LENDING,
                TransactionType.MEDIUM_TERM_LENDING,
                TransactionType.SHORT_TERM_LENDING,
                TransactionType.FMPP_INVESTMENT,
                TransactionType.LUMPSUM,
            ),
            "failed_status": (TransactionStatus.FAILED, TransactionStatus.FAIL),
        }
        debit_types = list(
            DashboardTransactionActionFilterMap.ACTION_FILTER_MAP[AccountAction.DEBIT]
        )
        transaction_type_filter_map = dict(TransactionTypeFilterMap.TYPE_FILTER_MAP)
        transaction_type_filter_map["INVESTMENT"] = list(
            TransactionTypeFilterMap.TYPE_FILTER_MAP[
                InvestmentFilter.CATEGORY_INVESTMENT
            ]
        )
        transaction_type_filter_map["CANCELLED_LOAN_REFUND"] = list(
            TransactionTypeFilterMap.TYPE_FILTER_MAP[
                InvestmentFilter.CATEGORY_CANCELLED_LOAN_REFUND
            ]
        )
        action_filter_map = dict(DashboardTransactionActionFilterMap.ACTION_FILTER_MAP)

        params = {
            "indian_time": TimeZone.indian_time,
            "user_source_group_id": user_source_id,
            "limit": limit,
            "debit_types": tuple(debit_types),
            "credit_types": tuple(
                TransactionActionFilterMap.ACTION_FILTER_MAP[AccountAction.CREDIT]
            ),
            "add_money_types": tuple(
                transaction_type_filter_map[TransactionFilter.CATEGORY_ADD_FUNDS]
            ),
            "repayment_types": tuple(
                transaction_type_filter_map[TransactionFilter.CATEGORY_REPAYMENT]
            ),
            "withdrawal_types": tuple(
                transaction_type_filter_map[TransactionFilter.CATEGORY_WITHDRAWAL]
            ),
            "auto_withdrawal_types": tuple(
                transaction_type_filter_map[TransactionFilter.CATEGORY_AUTO_WITHDRAWAL]
            ),
            "investment_types": tuple(transaction_type_filter_map["INVESTMENT"]),
            "cancelled_loan_refund_types": tuple(
                TransactionTypeFilterMap.TYPE_FILTER_MAP[
                    InvestmentFilter.CATEGORY_CANCELLED_LOAN_REFUND
                ]
            ),
        }

        # Initialize base where conditions
        base_where_conditions = ["lt.user_source_group_id = %(user_source_group_id)s"]
        if filter_data:
            # Status filters
            status_set = DashboardMapper.get_filter_set(
                filter_data,
                "status",
                DashboardTransactionStatusFilterMap.STATUS_FILTER_MAP,
            )
            params["status"] = (
                tuple(status_set) if status_set else default_config["status"]
            )
            base_where_conditions.append("lt.status = ANY(%(status)s)")

            type_set = DashboardMapper.get_filter_set(
                filter_data, "type", transaction_type_filter_map
            )
            action_set = DashboardMapper.get_filter_set(
                filter_data, "action", action_filter_map
            )

            # Combine with AND logic (intersection) if both present
            if type_set and action_set:
                final_types = type_set & action_set  # Intersection
            elif type_set:
                final_types = type_set
            elif action_set:
                final_types = action_set
            else:
                final_types = set(default_config["types"])

            params["type"] = tuple(final_types) if final_types else ()
            base_where_conditions.append("lt.type = ANY(%(type)s)")

            # Date range filter
            period = filter_data.get("period", {})
            if period.get("from_date") and period.get("to_date"):
                # Validate date formats
                datetime.strptime(period["from_date"], "%Y-%m-%d")
                datetime.strptime(period["to_date"], "%Y-%m-%d")
                params["from_date"] = period["from_date"]
                params["to_date"] = period["to_date"]
                base_where_conditions.append(
                    "DATE(lt.created_date) BETWEEN %(from_date)s AND %(to_date)s"
                )
        else:
            # Set default values if no filters
            params["status"] = default_config["status"]
            params["type"] = default_config["types"]
            base_where_conditions.extend(
                ["lt.type = ANY(%(type)s)", "lt.status = ANY(%(status)s)"]
            )

        # Add failed status to params
        params["failed_status"] = default_config["failed_status"]

        # Build the base query
        query = (
            """
            WITH transaction_data AS (
                SELECT 
                    TO_CHAR(lt.created_date AT TIME ZONE %(indian_time)s, 'DD Mon YYYY HH12:MI AM') AS created_date,
                    lt.type as original_type,
                    CASE 
                        WHEN lt.type = ANY(%(add_money_types)s) THEN 'FUNDS ADDED'
                        WHEN lt.type = ANY(%(repayment_types)s) THEN 'REPAYMENT TRANSFERRED'
                        WHEN lt.type = ANY(%(withdrawal_types)s) THEN 'WITHDRAWAL'
                        WHEN lt.type = ANY(%(auto_withdrawal_types)s) THEN 'AUTO WITHDRAWAL'
                        WHEN lt.type = ANY(%(cancelled_loan_refund_types)s) THEN 'CANCELLED LOAN REFUND'
                        ELSE lt.type
                    END AS type,
                    lt.amount, 
                    lt.transaction_id,
                    lt.status <> ALL(%(failed_status)s) AS success,
                    CASE 
                        WHEN lt.status = ANY(%(failed_status)s) THEN '"""
            + TransactionStatus.FAILED
            + """' 
                        ELSE lt.status 
                    END AS label,
                    CASE 
                        WHEN lt.type = ANY(%(debit_types)s) THEN 'Dr'
                        WHEN lt.type = ANY(%(credit_types)s) THEN 'Cr'
                        ELSE NULL
                    END AS action,
                    CASE 
                        WHEN lb.number IS NOT NULL THEN 
                            CONCAT('XXXXXXX', RIGHT(lb.number, 4))
                        ELSE NULL
                    END AS bank_account_number,
                    lt.created_date as sort_date,
                    lt.id,
                    COUNT(*) OVER() AS total
                FROM lendenapp_transaction lt
                LEFT JOIN lendenapp_bankaccount lb ON lt.bank_account_id = lb.id
                WHERE """
            + " AND ".join(base_where_conditions)
            + """
            )
            SELECT 
                created_date,
                type,
                amount,
                transaction_id,
                success,
                label,
                action,
                bank_account_number,
                total
            FROM transaction_data
        """
        )

        # Add sorting
        if sort_data:
            sort_conditions = []
            for sort_option in sort_data:
                sort_condition = TransactionSortBy.SORT_CONDITIONS.get(sort_option)
                if sort_condition:
                    sort_conditions.append(sort_condition)

            if sort_conditions:
                query += " ORDER BY " + ", ".join(sort_conditions)
        else:
            # Default sorting by date descending
            query += " ORDER BY sort_date DESC, id DESC"

        # Add pagination
        query += " LIMIT %(limit)s"
        if offset is not None and offset >= 0:
            params["offset"] = offset
            query += " OFFSET %(offset)s"

        params = DataLayerUtils().prepare_sql_params(params)
        result = DashboardMapper().sql_execute_fetch_all(query, params, to_dict=True)

        if not result:
            return {"transaction_count": 0, "transaction_list": []}

        total_count = result[0]["total"] if result else 0

        # Remove 'total' from each row in the result
        for row in result:
            if "total" in row:
                del row["total"]

        return {"transaction_count": total_count, "transaction_list": result}

    @staticmethod
    def fetch_transactions_totals(user_source_id, filter_data):
        """
        Calculate totals (credit, debit, net) for transactions.
        """
        # Default configuration (same as fetch_transactions_list)
        default_config = {
            "status": (
                TransactionStatus.FAILED,
                TransactionStatus.FAIL,
                TransactionStatus.SUCCESS,
                TransactionStatus.SCHEDULED,
                TransactionStatus.PROCESSING,
                TransactionStatus.PENDING,
                TransactionStatus.COMPLETED,
                TransactionStatus.CANCELLED,
                TransactionStatus.EXPIRED,
            ),
            "types": (
                TransactionType.ADD_MONEY,
                TransactionType.WITHDRAW_MONEY,
                TransactionType.MIP_AUTO_WITHDRAWAL,
                TransactionType.MANUAL_LENDING_AUTO_WITHDRAWAL,
                TransactionType.LUMPSUM_AUTO_WITHDRAWAL,
                TransactionType.IDLE_FUND_WITHDRAWAL,
                TransactionType.REPAYMENT_AUTO_WITHDRAWAL,
                TransactionType.AUTO_LENDING_REPAYMENT_WITHDRAWAL,
                TransactionType.CANCELLED_LOAN_REFUND,
                TransactionType.REJECTED_LOAN_REFUND,
                TransactionType.AUTO_LENDING_REPAYMENT_ADD_MONEY,
                TransactionType.FMPP_REPAYMENT_WITHDRAWAL,
                TransactionType.MANUAL_LENDING,
                TransactionType.MEDIUM_TERM_LENDING,
                TransactionType.SHORT_TERM_LENDING,
                TransactionType.FMPP_INVESTMENT,
                TransactionType.LUMPSUM,
            ),
            "failed_status": (TransactionStatus.FAILED, TransactionStatus.FAIL),
        }

        debit_types = list(
            DashboardTransactionActionFilterMap.ACTION_FILTER_MAP[AccountAction.DEBIT]
        )
        transaction_type_filter_map = dict(TransactionTypeFilterMap.TYPE_FILTER_MAP)
        transaction_type_filter_map["INVESTMENT"] = list(
            TransactionTypeFilterMap.TYPE_FILTER_MAP[
                InvestmentFilter.CATEGORY_INVESTMENT
            ]
        )
        transaction_type_filter_map["CANCELLED_LOAN_REFUND"] = list(
            TransactionTypeFilterMap.TYPE_FILTER_MAP[
                InvestmentFilter.CATEGORY_CANCELLED_LOAN_REFUND
            ]
        )
        action_filter_map = dict(DashboardTransactionActionFilterMap.ACTION_FILTER_MAP)

        params = {
            "user_source_group_id": user_source_id,
            "debit_types": tuple(debit_types),
            "credit_types": tuple(
                TransactionActionFilterMap.ACTION_FILTER_MAP[AccountAction.CREDIT]
            ),
            "add_money_types": tuple(
                transaction_type_filter_map[TransactionFilter.CATEGORY_ADD_FUNDS]
            ),
            "repayment_types": tuple(
                transaction_type_filter_map[TransactionFilter.CATEGORY_REPAYMENT]
            ),
            "withdrawal_types": tuple(
                transaction_type_filter_map[TransactionFilter.CATEGORY_WITHDRAWAL]
            ),
            "auto_withdrawal_types": tuple(
                transaction_type_filter_map[TransactionFilter.CATEGORY_AUTO_WITHDRAWAL]
            ),
            "investment_types": tuple(transaction_type_filter_map["INVESTMENT"]),
            "cancelled_loan_refund_types": tuple(
                TransactionTypeFilterMap.TYPE_FILTER_MAP[
                    InvestmentFilter.CATEGORY_CANCELLED_LOAN_REFUND
                ]
            ),
            "success_status": (TransactionStatus.SUCCESS, TransactionStatus.COMPLETED),
        }

        # Initialize base where conditions
        # Note: We don't apply status filter here because totals should always
        # be calculated from all SUCCESS/COMPLETED transactions matching other filters
        base_where_conditions = ["lt.user_source_group_id = %(user_source_group_id)s"]

        if filter_data:
            # Don't apply status filter - totals should include all SUCCESS/COMPLETED
            # transactions matching other filters (type, date, etc.)

            type_set = DashboardMapper.get_filter_set(
                filter_data, "type", transaction_type_filter_map
            )
            action_set = DashboardMapper.get_filter_set(
                filter_data, "action", action_filter_map
            )

            # Combine with AND logic (intersection) if both present
            if type_set and action_set:
                final_types = type_set & action_set  # Intersection
            elif type_set:
                final_types = type_set
            elif action_set:
                final_types = action_set
            else:
                final_types = set(default_config["types"])

            params["type"] = tuple(final_types) if final_types else ()
            base_where_conditions.append("lt.type = ANY(%(type)s)")

            # Date range filter
            period = filter_data.get("period", {})
            if period.get("from_date") and period.get("to_date"):
                # Validate date formats
                datetime.strptime(period["from_date"], "%Y-%m-%d")
                datetime.strptime(period["to_date"], "%Y-%m-%d")
                params["from_date"] = period["from_date"]
                params["to_date"] = period["to_date"]
                base_where_conditions.append(
                    "DATE(lt.created_date) BETWEEN %(from_date)s AND %(to_date)s"
                )
        else:
            # Set default values if no filters
            params["type"] = default_config["types"]
            base_where_conditions.append("lt.type = ANY(%(type)s)")

        # Build query to calculate totals
        # Only count transactions with status SUCCESS or COMPLETED
        query = """
            SELECT 
                COALESCE(SUM(CASE 
                    WHEN lt.type = ANY(%(credit_types)s) 
                    AND lt.status = ANY(%(success_status)s)
                    THEN lt.amount 
                    ELSE 0 
                END), 0) AS total_credit,
                COALESCE(SUM(CASE 
                    WHEN lt.type = ANY(%(debit_types)s) 
                    AND lt.status = ANY(%(success_status)s)
                    THEN lt.amount 
                    ELSE 0 
                END), 0) AS total_debit
            FROM lendenapp_transaction lt
            WHERE """ + " AND ".join(
            base_where_conditions
        )

        params = DataLayerUtils().prepare_sql_params(params)
        result = DashboardMapper().sql_execute_fetch_one(query, params, to_dict=True)

        if not result:
            return {
                "total_credit": 0,
                "total_debit": 0,
                "net_amount": 0,
                "net_sign": "Cr",
            }

        total_credit = float(result.get("total_credit", 0) or 0)
        total_debit = float(result.get("total_debit", 0) or 0)
        net_amount = total_credit - total_debit

        return {
            "total_credit": total_credit,
            "total_debit": total_debit,
            "net_amount": abs(net_amount),
            "net_sign": "Cr" if net_amount >= 0 else "Dr",
        }

    @staticmethod
    def fetch_user_referral_details(
        user_source_group_id,
        limit=10,
        offset=0,
        start_date=None,
        end_date=None,
        first_lending_type=None,
        platform=None,
        cashback_status=None,
        referee_user_id=None,
        referee_pan=None,
        referee_mobile=None,
        referee_user_source_id=None,
        referee_email=None,
    ):

        filter_map = {
            "first_lending_type": (
                "td.txn_type = %(first_lending_type)s",
                first_lending_type,
            ),
            "platform": ("ai.platform = ANY(%(platform)s)", platform),
            "cashback_status": ("lr.status = %(cashback_status)s", cashback_status),
            "referee_user_id": ("lc2.user_id = %(referee_user_id)s", referee_user_id),
            "referee_pan": ("lc2.encoded_pan = %(referee_pan)s", referee_pan),
            "referee_mobile": (
                "lc2.encoded_mobile = %(referee_mobile)s",
                referee_mobile,
            ),
            "referee_email": ("lc2.encoded_email = %(referee_email)s", referee_email),
            "referee_user_source_id": (
                "lusg2.id = %(referee_user_source_id)s",
                referee_user_source_id,
            ),
        }

        # Build filter conditions dynamically for referrer query
        referrer_filter_conditions = []

        # Add date range filter
        if start_date and end_date:
            referrer_filter_conditions.append(
                "lr.created_date::date BETWEEN %(start_date)s AND %(end_date)s"
            )
        elif start_date:
            referrer_filter_conditions.append("lr.created_date::date >= %(start_date)s")
        elif end_date:
            referrer_filter_conditions.append("lr.created_date::date <= %(end_date)s")

        # Add other filters from map
        for param_name, (condition, param_value) in filter_map.items():
            if param_value is not None:
                referrer_filter_conditions.append(condition)

        # Combine all referrer filter conditions
        referrer_additional_filters = ""
        if referrer_filter_conditions:
            referrer_additional_filters = "AND " + " AND ".join(
                referrer_filter_conditions
            )

        # Query for users this person referred (they are the referrer) with pagination
        referrer_query = f"""
            SELECT 
                lc.first_name AS referrer_name,
                lc.user_id AS referrer_user_id,
                lc.encoded_mobile AS referrer_mobile,
                lc.encoded_email AS referrer_email,
                lc.encoded_pan AS referrer_pan,
                lusg.id AS referrer_user_source_id,
                lc2.first_name AS referee_name,
                lc2.user_id AS referee_user_id,
                lc2.encoded_mobile AS referee_mobile,
                lc2.encoded_email AS referee_email,
                lc2.encoded_pan AS referee_pan,
                lusg2.id AS referee_user_source_id,
                lr.amount AS bonus_amount,
                lr.created_date::date AS referral_date,
                lr.status AS cashback_status,
                la.status AS referee_status,
                lc2.created_date::date AS sign_up_date,
                la.listed_date,
                COALESCE(td.amount, null) AS first_lending_amount,
                COALESCE(td.txn_type, '-') AS first_lending_type,
                COALESCE(td.first_lending_date, null) AS first_lending_date,
                CASE 
                    WHEN lr.amount > 0 AND tl.total_lending IS NOT NULL 
                    THEN ROUND((tl.total_lending / lr.amount), 2)
                    ELSE NULL
                END AS roi,
                COALESCE(ai.platform, '-') AS referee_platform
            FROM lendenapp_reward lr
            JOIN lendenapp_campaign lc3 ON lc3.id = lr.campaign_id
            JOIN lendenapp_user_source_group lusg ON lusg.id = lr.user_source_group_id
            JOIN lendenapp_user_source_group lusg2 ON lusg2.id = lr.related_user_source_group_id
            JOIN lendenapp_customuser lc ON lc.id = lusg.user_id
            JOIN lendenapp_customuser lc2 ON lc2.id = lusg2.user_id
            JOIN lendenapp_account la ON la.user_source_group_id = lusg2.id
            LEFT JOIN LATERAL (
                SELECT 
                    detail AS amount,
                    CASE 
                        WHEN activity = %(first_lending_ml)s THEN 'MANUAL LENDING'
                        WHEN activity = %(first_lending_lumpsum)s THEN 'LUMPSUM'
                        ELSE activity
                    END AS txn_type,
                    created_date::date AS first_lending_date
                FROM lendenapp_timeline t
                WHERE t.id = (
                    SELECT MIN(id)
                    FROM lendenapp_timeline
                    WHERE user_source_group_id = lusg2.id
                      AND activity = ANY(%(first_lending_types)s)
                )
            ) td ON true
            LEFT JOIN LATERAL (
                SELECT 
                    SUM(amount) AS total_lending
                FROM lendenapp_transaction 
                WHERE user_source_group_id = lusg2.id
                  AND type = ANY(%(investment_types)s)
                  AND status = 'COMPLETED'
            ) tl ON true
            LEFT JOIN LATERAL (
                SELECT comment AS platform
                FROM lendenapp_applicationinfo
                WHERE user_source_group_id = lusg2.id
                ORDER BY id ASC
                LIMIT 1
            ) ai ON true
            WHERE lr.user_source_group_id = %(user_source_group_id)s
            AND lr.user_source_group_id != lr.related_user_source_group_id
            AND lc3.type = 'referral'
            {referrer_additional_filters}
            ORDER BY lr.id DESC
            LIMIT %(limit)s OFFSET %(offset)s
        """

        # Query for who referred this person (they are the referee)
        referee_query = """
            SELECT 
                lc.first_name AS referrer_name,
                lc.user_id AS referrer_user_id,
                lusg.id AS referrer_user_source_id,
                lr.amount AS bonus_amount,
                lr.created_date::date AS referral_date,
                COALESCE((
                    SELECT amount 
                    FROM lendenapp_transaction 
                    WHERE user_source_group_id = %(user_source_group_id)s
                    AND type = ANY(%(investment_types)s)
                    AND status = 'COMPLETED' 
                    ORDER BY date ASC 
                    LIMIT 1
                ), 0) AS first_lending_amount
            FROM lendenapp_reward lr
            JOIN lendenapp_campaign lc3 ON lc3.id = lr.campaign_id
            JOIN lendenapp_user_source_group lusg ON lusg.id = lr.user_source_group_id
            JOIN lendenapp_customuser lc ON lc.id = lusg.user_id
            WHERE lr.related_user_source_group_id = %(user_source_group_id)s
            AND lr.user_source_group_id != lr.related_user_source_group_id
            AND lc3.type = 'referral'
            ORDER BY lr.created_date DESC
            LIMIT 1
        """

        params = {
            "user_source_group_id": user_source_group_id,
            "limit": limit,
            "offset": offset,
            "investment_types": list(
                TransactionType.CS_DASHBOARD_REFERRAL_INVESTMENT_TYPES
            ),
            "first_lending_ml": ReferralLendingConstant.FIRST_LENDING_ML,
            "first_lending_lumpsum": ReferralLendingConstant.FIRST_LENDING_LUMPSUM,
            "first_lending_types": ReferralLendingConstant.first_lending_types,
        }

        # Add optional filter params using map
        optional_params = {
            "start_date": start_date,
            "end_date": end_date,
            "first_lending_type": first_lending_type,
            "platform": platform,
            "cashback_status": cashback_status,
            "referee_user_id": referee_user_id,
            "referee_pan": referee_pan,
            "referee_mobile": referee_mobile,
            "referee_email": referee_email,
            "referee_user_source_id": referee_user_source_id,
        }

        # Add only non-None values to params
        for key, value in optional_params.items():
            if value is not None:
                params[key] = value

        # Execute queries
        referrals_made = (
            DashboardMapper().sql_execute_fetch_all(
                referrer_query, params, to_dict=True
            )
            or []
        )
        referred_by = DashboardMapper().sql_execute_fetch_one(
            referee_query, params, to_dict=True
        )

        return {
            "referrals_made": referrals_made,  # List of people this user referred (paginated)
            "referred_by": referred_by,  # Single person who referred this user (or None)
            "current_page_count": len(referrals_made),  # Count in current page
            "offset": offset,
            "limit": limit,
        }

    @staticmethod
    def get_jobs():
        query = """
            SELECT 
                id as job_id,
                created_date,
                updated_date,
                job_name,
                is_job_enabled,
                is_batch_enabled,
                remark,
                is_ecs_enabled
            FROM lendenapp_job_master
            ORDER BY job_name
        """

        return DashboardMapper().sql_execute_fetch_all(query, params={}, to_dict=True)

    @staticmethod
    def update_job(
        job_id, job_name, is_job_enabled, is_batch_enabled, is_ecs_enabled, remark
    ):

        query = f"""
            UPDATE lendenapp_job_master
            SET is_job_enabled = %(is_job_enabled)s, 
            is_batch_enabled = %(is_batch_enabled)s, 
            is_ecs_enabled = %(is_ecs_enabled)s, 
            remark = %(remark)s, 
            updated_date = NOW()
            WHERE job_name = %(job_name)s
            AND id = %(job_id)s
        """
        params = {
            "job_id": job_id,
            "job_name": job_name,
            "is_job_enabled": is_job_enabled,
            "is_batch_enabled": is_batch_enabled,
            "is_ecs_enabled": is_ecs_enabled,
            "remark": remark,
        }
        DashboardMapper().execute_sql(query, params)
        return True

    @staticmethod
    def get_user_kyc_details(user_source_group_id):

        query = """
        select lukt.tracking_id,
        lukt.status,
        lukt.next_kyc_date,
        lukt.created_date,
        luk.event_code,
        luk.service_type
        from lendenapp_userkyctracker lukt 
        inner join 
        lendenapp_userkyc luk
        on lukt.tracking_id =luk.tracking_id
        where lukt.is_latest_kyc=true and lukt.user_source_group_id =%(user_source_group_id)s
        order by luk.id desc limit 1"""

        params = {"user_source_group_id": user_source_group_id}
        return DashboardMapper().sql_execute_fetch_one(query, params, to_dict=True)

    @staticmethod
    def user_account_deletion_request(user_source_group_id):
        deletion_activity = (
            ApplicationConfigDashboardConstant.ACCOUNT_DELETION_CONSTANT["DELETION"]
        )
        cancel_deletion_activity = (
            ApplicationConfigDashboardConstant.ACCOUNT_DELETION_CONSTANT[
                "CANCEL_DELETION"
            ]
        )

        query = """ WITH ranked_events AS 
        ( SELECT lt.user_source_group_id, 
        lt.detail AS request_id, 
        lt.activity, 
        lt.created_date, 
        ROW_NUMBER() 
        OVER ( PARTITION BY lt.detail, 
        lt.activity ORDER BY lt.created_date DESC ) as rn 
        FROM lendenapp_timeline lt 
        WHERE lt.activity = ANY(%(activity_list)s)
        AND lt.detail IS NOT NULL 
        AND lt.user_source_group_id = %(user_source_group_id)s), 
        timeline_data AS ( SELECT user_source_group_id, request_id, 
        MAX(CASE WHEN activity = %(deletion_activity)s AND rn = 1 THEN created_date END) AS deletion_date_req,
        MAX(CASE WHEN activity = %(cancel_activity)s AND rn = 1 THEN created_date END) AS cancelled_deletion_date 
        FROM ranked_events GROUP BY user_source_group_id, 
        request_id ) SELECT cu.user_id AS lender_id, cu.ucic_code AS ucic_number, td.request_id, td.deletion_date_req, td.cancelled_deletion_date 
        FROM lendenapp_customuser cu 
        INNER JOIN lendenapp_user_source_group lusg ON cu.id = lusg.user_id 
        INNER JOIN timeline_data td ON lusg.id = td.user_source_group_id 
        ORDER BY td.deletion_date_req DESC;"""

        params = {
            "user_source_group_id": user_source_group_id,
            "activity_list": [deletion_activity, cancel_deletion_activity],
            "deletion_activity": deletion_activity,
            "cancel_activity": cancel_deletion_activity,
        }
        return DashboardMapper().sql_execute_fetch_all(query, params, to_dict=True)

    @staticmethod
    def user_account_deactivation_request(user_source_group_id):

        deactivation_activity = (
            ApplicationConfigDashboardConstant.ACCOUNT_DEACTIVATION_CONSTANT[
                "ACCOUNT_DEACTIVATION"
            ]
        )
        reactivation_activity = (
            ApplicationConfigDashboardConstant.ACCOUNT_DEACTIVATION_CONSTANT[
                "ACCOUNT_REACTIVATION"
            ]
        )
        query = """
        WITH ranked_events AS 
        ( SELECT lt.user_source_group_id, lt.detail AS request_id, lt.activity, lt.created_date, 
        ROW_NUMBER() OVER ( PARTITION BY lt.detail, lt.activity ORDER BY lt.created_date DESC ) as rn 
        FROM lendenapp_timeline lt WHERE lt.activity = ANY(%(activity_list)s) 
        AND lt.detail IS NOT NULL 
        AND lt.user_source_group_id = %(user_source_group_id)s), 
        timeline_data as
        ( SELECT user_source_group_id, 
        request_id, MAX(CASE WHEN activity = %(deactivation_activity)s 
        AND rn = 1 THEN created_date END) AS deactivate_date_req, 
        MAX(CASE WHEN activity = %(reactivation_activity)s 
        AND rn = 1 THEN created_date END) AS reactivation_date FROM ranked_events GROUP BY user_source_group_id, request_id ) 
        SELECT cu.user_id AS lender_id, 
        cu.ucic_code AS ucic_number,
        td.request_id, 
        td.deactivate_date_req, 
        td.reactivation_date 
        FROM lendenapp_customuser cu 
        INNER JOIN lendenapp_user_source_group lusg ON cu.id = lusg.user_id 
        INNER JOIN timeline_data td ON lusg.id = td.user_source_group_id 
        ORDER BY td.deactivate_date_req DESC;"""

        params = {
            "user_source_group_id": user_source_group_id,
            "activity_list": [deactivation_activity, reactivation_activity],
            "deactivation_activity": deactivation_activity,
            "reactivation_activity": reactivation_activity,
        }

        return DashboardMapper().sql_execute_fetch_all(query, params, to_dict=True)

    @staticmethod
    def get_id_from_role(role_name):
        query = """
            SELECT id
            FROM auth_group
            WHERE name = %(role_name)s
        """
        params = {"role_name": role_name}
        result = DashboardMapper().sql_execute_fetch_one(query, params, to_dict=True)
        return result.get("id") if result else None

    @staticmethod
    def fetch_falcon_timeline_changes(start_date, end_date, role_ids):
        query = """
            SELECT lt.user_id, lc.first_name, lt.activity, lt.detail, lt.created_date
            FROM lendenapp_timeline lt
            JOIN lendenapp_customuser_groups lcg
              ON lt.user_id = lcg.customuser_id
            JOIN lendenapp_customuser lc ON lt.user_id = lc.id
            WHERE lcg.group_id = ANY(%(role_ids)s)
            AND lt.created_date BETWEEN %(start_date)s AND %(end_date)s
        """
        params = {"start_date": start_date, "end_date": end_date, "role_ids": role_ids}
        return DashboardMapper().sql_execute_fetch_all(query, params, to_dict=True)

    @staticmethod
    def get_scheme_info_date_wise(start_date, end_date):
        query = """
                SELECT 
                    ls.created_date::date,
                    ls2.source_name as "source",
                    ls.tenure,
                    count(*) as "total count",
                    sum(ls.amount) as "total amount",
                    sum(case when ls.status = 'SUCCESS' then ls.amount else 0 end) as "success amount",
                    sum(case when ls.status = 'SUCCESS' then 1 else 0 end) as "success count",
                    sum(case when ls.status = 'INITIATED' then ls.amount else 0 end) as "pending amount",
                    sum(case when ls.status = 'INITIATED' then 1 else 0 end) as "pending count",
                    sum(case when ls.status = 'CANCELLED' then ls.amount else 0 end) as "cancel amount",
                    sum(case when ls.status = 'CANCELLED' then 1 else 0 end) as "cancel count"
                FROM lendenapp_schemeinfo ls 
                INNER JOIN lendenapp_user_source_group lusg ON lusg.id = ls.user_source_group_id 
                INNER JOIN lendenapp_source ls2 ON ls2.id = lusg.source_id 
                WHERE ls.investment_type IN ('ONE_TIME_LENDING','MEDIUM_TERM_LENDING')
                AND ls.created_date::date BETWEEN %(start_date)s AND %(end_date)s
                GROUP BY ls.created_date::date, ls2.source_name, ls.tenure
                ORDER BY ls.created_date::date DESC
            """

        params = {"start_date": start_date, "end_date": end_date}
        return DashboardMapper().sql_execute_fetch_all(query, params, to_dict=True)
