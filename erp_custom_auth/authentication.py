import frappe
from frappe.core.doctype.user.user import generate_keys


@frappe.whitelist(allow_guest=True)
def login(**kwargs):
    try:
        usr, pwd, cmd = frappe.form_dict.values()
        auth = frappe.auth.LoginManager()
        auth.authenticate(user=usr, pwd=pwd)
        auth.post_login()
        msg={
        'status_code':200,
        'text':frappe.local.response.message,
        'user': frappe.session.user
        }
        user = frappe.get_doc('User', frappe.session.user)
        if(user.api_key and user.api_secret):
            msg['token'] = f"{user.api_key}:{user.get_password('api_secret')}"
        else:
            generate_keys(user.name)
            user.reload()
            msg['token'] = f"{user.api_key}:{user.get_password('api_secret')}"
        return msg
    except frappe.exceptions.AuthenticationError:
        return {'status_code':401, 'text':frappe.local.response.message}
    except Exception as e:
        return {'status_code':500, 'text':str(e)}


@frappe.whitelist(allow_guest = True)
def getDataDB(doctype,search):
    return frappe.db.count(doctype,search)
    
@frappe.whitelist(allow_guest = True)
def get_home_page(doctype_id=None):
    return frappe.db.sql(f"""select field,value from `tabSingles` where doctype = 'News Home Page'""",as_dict=True)

@frappe.whitelist(allow_guest = True)
def get_home_page_key(news_id=None):
    return frappe.db.sql(f"""select title from `tabNews Category Child` where parent='News Home Page'""",as_dict=True)
   
