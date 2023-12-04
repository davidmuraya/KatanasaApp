from pydantic import BaseModel
from typing import Optional


class MpesaRequest(BaseModel):
    TransactionType: Optional[str]
    TransID: Optional[str]
    TransTime: Optional[str]
    TransAmount: Optional[float]
    BusinessShortCode: Optional[str]
    BillRefNumber: Optional[str]
    InvoiceNumber: Optional[str]
    OrgAccountBalance: Optional[float]
    ThirdPartyTransID: Optional[str]
    MSISDN: Optional[str]
    FirstName: Optional[str]
    MiddleName: Optional[str]
    LastName: Optional[str]


class PaymentConfirmation(BaseModel):
    transaction_date: Optional[str]
    allocated: Optional[bool] = False
    error: Optional[str]
    request: Optional[MpesaRequest]


class ProcessMpesaRequestResponse(BaseModel):
    transaction_id: Optional[str]
    success: bool = False
    error: Optional[str]
    request: Optional[MpesaRequest]


class PaymentValidationResponse(BaseModel):
    ResultCode: str = "0"
    ResultDesc: str = "Accepted"
    ThirdPartyTransID: str = ""


class PaymentValidation(BaseModel):
    ResultCode: str = "0"
    ResultDesc: str = "Accepted"
    ThirdPartyTransID: str = ""
    error: str = ""
    request: Optional[MpesaRequest]


class PaymentConfirmationResponse(BaseModel):
    ResultCode: Optional[str] = "0"
    ResultDesc: Optional[str] = "Success"
