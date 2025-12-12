from datetime import datetime

def get_transaction_date(date_obj):
    return date_obj.strftime("%b %d %Y")

def get_transaction_code(prefix="TXN"):
    now = datetime.now()
    return f"{prefix}{now.strftime('%Y%m%d%H%M%S')}"

def get_current_date():
    return get_transaction_date(datetime.now())


print("date:", get_transaction_date(datetime.now()))