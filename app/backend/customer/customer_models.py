from pydantic import BaseModel
from typing import Optional


class Customer(BaseModel):
    creation_date: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    gender: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    city: Optional[str] = None
    source: Optional[str] = None


class CustomerOverview(BaseModel):
    customer_id: Optional[str] = None
    creation_date: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    gender: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    city: Optional[str] = None
    source: Optional[str] = None
    total_amount_received: Optional[float] = 0.0
    total_unearned_amount: Optional[float] = 0.0


class Attendance(BaseModel):
    customer_id: str
    customer_name: Optional[str] = None
    attendance_date: str
    added_by: Optional[str] = None
    entry_date: Optional[str] = None
