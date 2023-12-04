from pydantic import BaseModel
from typing import Optional


class SaleTransaction(BaseModel):
    customer_id: str
    customer_name: Optional[str] = None
    sales_date: str
    payment_method: Optional[str] = None
    discount: Optional[str] = None
    amount_received: float = 0.00
    added_by: Optional[str] = None
    entry_date: Optional[str] = None
    plan: Optional[str] = None
    transaction_ref: Optional[str] = None
