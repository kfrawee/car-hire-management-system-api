from typing import List, Dict

FULL_CUSTOMER_DICT_KEYS = [
    "customer_id",
    "first_name",
    "last_name",
    "email",
    "phone_number",
    "address",
    "created_on",
    "updated_on",
]
SHORT_CUSTOMER_DICT_KEYS = ["customer_id", "first_name", "last_name", "email"]


def generate_customer_data(customer_raw: List, full=True) -> Dict:
    """Convert packed returned customer row to a dict
    Args:
        customer_raw (list): returned customer data
        full (bool): either to return full customer details or not

    Return:
        Dict: unpacked customer data.
    """
    cus_iter = iter(customer_raw)
    if full:
        return dict(zip(FULL_CUSTOMER_DICT_KEYS, cus_iter))
    else:
        return dict(zip(SHORT_CUSTOMER_DICT_KEYS, cus_iter))


def send_email():
    pass


def send_daily_report():
    pass
