import os
from enum import Enum

from integrify.utils import Environment

VERSION = '1.0.1'  # version of client documentation

# ENV VARS HERE
CLOPOS_CLIENT_ID: str = os.getenv('CLOPOS_CLIENT_ID', '')
CLOPOS_CLIENT_SECRET: str = os.getenv('CLOPOS_CLIENT_SECRET', '')
CLOPOS_BRAND: str = os.getenv('CLOPOS_BRAND', '')
CLOPOS_VENUE_ID: str = os.getenv('CLOPOS_VENUE_ID', '')
CLOPOS_ENV: str = os.getenv('CLOPOS_ENV', Environment.TEST.value)


class API(str, Enum):
    """Endpoint constant-ları"""

    BASE_URL = 'https://integrations.clopos.com/open-api/'

    AUTH = 'auth'

    VENUES = 'venues'

    USERS = 'users'
    USER_BY_ID = 'users/{id}'

    CUSTOMERS = 'customers'
    CUSTOMER_BY_ID = 'customers/{id}'
    CUSTOMER_GROUPS = 'customer-groups'

    CATEGORIES = 'categories'
    CATEGORY_BY_ID = 'categories/{id}'

    STATIONS = 'stations'
    STATION_BY_ID = 'stations/{id}'

    PRODUCTS = 'products'
    PRODUCT_BY_ID = 'products/{id}'
    STOP_LIST = 'products/stop-list'

    SALE_TYPES = 'sale-types'
    PAYMENT_METHODS = 'payment-methods'

    ORDERS = 'orders'
    ORDER_BY_ID = 'orders/{id}'

    RECEIPTS = 'receipts'
    RECEIPT_BY_ID = 'receipts/{id}'


__all__ = [
    'VERSION',
    'CLOPOS_CLIENT_ID',
    'CLOPOS_CLIENT_SECRET',
    'CLOPOS_ENV',
    'API',
]
