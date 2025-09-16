# expense_manager/api.py
import frappe
from pydantic import BaseModel, validator, ValidationError
from typing import Optional, List
import frappe.utils

def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "http://localhost:8080"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return response


frappe.utils.logger.set_log_level("DEBUG")
logger = frappe.logger("expense_api", allow_site=True, file_count=50)
class ExpenseInput(BaseModel):
    expense_date: str
    category: str
    amount: float
    description: Optional[str] = "No description provided"
    payment_method: str

    @validator("amount")
    def check_amount(cls, v):
        if v <= 0:
            raise ValueError("Amount must be greater than 0")
        if v > 10000:
            raise ValueError("Amount exceeds company limit of 10000")
        return v


@frappe.whitelist(allow_guest=False)
def add_expense(**kwargs):
    try:
        data = ExpenseInput(**kwargs)
        logger.info(f"add_expense called by {frappe.session.user} with data={kwargs}")
        
        doc = frappe.get_doc({
            "doctype": "Expense",
            "expense_date": data.expense_date,
            "category": data.category,
            "amount": data.amount,
            "description": data.description,
            "payment_method": data.payment_method,
        })
        doc.insert(ignore_permissions=True)
        frappe.db.commit()

        logger.info(f"EXpense {doc.name} created sucessfully amount={data.amount}")
        return {"success": True, "message": "Expense created", "expense_id": doc.name}

    except ValidationError as ve:
        logger.warning(f"Validation error in add_expense by {frappe.session.user}: {ve}")
        frappe.log_error(message=str(ve), title="Add Expense Validation Error")
        return {"success": False, "error": "validation_error", "details": ve.errors()}

    except Exception as e:
        logger.error(f"Unexpected error in add_expense: {str(e)}", exc_info=True)
        frappe.log_error(f"Error creating expense: {str(e)}", "Add Expense API")
        return {"success": False, "error": str(e)}


def after_insert_expense(doc, method):
    """Hook: logs and shows Desk popup after inserting Expense"""
    try:
        frappe.logger().info(
            f"[after_insert] Expense {doc.name} created — amount={doc.amount} desc={doc.description}"
        )
        # show popup in Desk UI
        frappe.msgprint(
            f"[after_insert] Expense {doc.name} created\n"
            f"Amount: {doc.amount}\nDescription: {doc.description}"
        )
    except Exception as e:
        frappe.log_error(f"after_insert_expense failed: {e}", "after_insert_expense")


def before_insert_expense(doc, method):
    """Hook: set default description if missing before insert"""
    if not getattr(doc, "description", None):
        doc.description = "No description provided"
        frappe.logger().info(
            f"[before_insert] Description set to default for Expense {getattr(doc,'name', '<new>')}"
        )


def before_save_expense(doc, method):
    """Hook: validate amount before save"""
    try:
        if doc.amount is None:
            frappe.throw("Expense amount is required.")
        if float(doc.amount) <= 0:
            frappe.throw("Expense amount must be greater than zero.")
        if float(doc.amount) > 10000:
            frappe.throw("Expense amount exceeds company limit of 10,000.")
        frappe.logger().info(f"[before_save] Expense {getattr(doc,'name', '<new>')} validated successfully")
    except Exception:
        raise



def send_daily_expense_summary():
    """
    Scheduled job (daily): email total expenses in the last 24 hours to System Managers.
    Add to hooks.py:
      scheduler_events = {
        "daily": ["expense_manager.api.send_daily_expense_summary"]
      }
    """
    try:
        yesterday = frappe.utils.add_days(frappe.utils.nowdate(), -1)
        expenses = frappe.get_all(
            "Expense",
            filters={"creation": (">=", yesterday)},
            fields=["name", "amount", "description"]
        )

        total = sum([float(e.get("amount") or 0) for e in expenses])
        body = f"Total Expenses in last 24 hours: {total}\n\nDetails:\n"
        for e in expenses:
            body += f"- {e.get('name')}: {e.get('amount')} ({e.get('description')})\n"

        recipients = frappe.get_all(
           "Has Role",
           filters={"role" : "System Manager", "parenttype" : "User", "parentfield": ""},
           fields=["parent"]
       )
    
        recipients = [r["parent"] for r in recipients if frappe.get_value("User", r["parent"], "enabled")]



        print("---- DAILY EXPENSE SUMMARY ----")
        print("Recipients:", recipients)
        print(body)
        print("---- END OF SUMMARY ----")
    except Exception as e:
        frappe.log_error(f"Failed to send daily expense summary: {e}", "send_daily_expense_summary")



@frappe.whitelist(allow_guest=False)
def get_expenses(start_date: Optional[str] = None, end_date: Optional[str] = None,
                 category: Optional[str] = None, payment_method: Optional[str] = None,
                 page: Optional[int] = 1, limit: Optional[int] = 10):

    try:
        logger.info('get_expenses called by {frappe.session.user}'
                    f"with filters start={start_date}, end={end_date},"
                    f"category={category}, payemnt_method={payment_method},"
                    f"page={page}, limit={limit}")
        try:
            page = int(page) if page is not None else 1
            limit = int(limit) if limit is not None else 10
        except (TypeError, ValueError):
            page = 1
            limit = 10

        filters = {}
        if start_date and end_date:
            filters["expense_date"] = ["between", [start_date, end_date]]
        elif start_date:
            filters["expense_date"] = [">=", start_date]
        elif end_date:
            filters["expense_date"] = ["<=", end_date]

        if category:
            filters["category"] = category
        if payment_method:
            filters["payment_method"] = payment_method

        offset = (page - 1) * limit

        expenses = frappe.get_all(
            "Expense",
            filters=filters,
            fields=["name", "expense_date", "category", "amount", "description", "payment_method"],
            limit_start=offset,
            limit_page_length=limit
        )

        logger.debug(f"Fetched {len(expenses)} expenses for user={frappe.session.user}")
        return {"success": True, "data": expenses, "page": page, "limit": limit}
    except Exception as e:
        logger.error(f"Error in get_expenses: {e}", exc_info=True)
        frappe.log_error(f"Error fetching expenses: {e}", "get_expenses")
        return {"success": False, "error": str(e)}
    

@frappe.whitelist(allow_guest=True)
def custom_login(usr, pwd):
    try:
        frappe.local.login_manager.authenticate(user=usr, pwd=pwd)
        frappe.local.login_manager.post_login()

        sid = frappe.session.sid

        return {
            "status" : "success",
            "message": ("Logged In"),
            "full_name" : frappe.local.session.data.full_name,
            "sid" : sid
        }
    except Exception as e:
        frappe.local.response.http_status_code = 401
        return {
            "status" : "error",
            "message" : str(e)
        }



