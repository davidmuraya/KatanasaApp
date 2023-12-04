from datetime import datetime
from google.cloud.exceptions import GoogleCloudError
from dotenv import load_dotenv
import os

from fastapi import HTTPException, Request

from app.backend.transactions.mpesa.mpesa_models import MpesaRequest, PaymentConfirmation, ProcessMpesaRequestResponse
from app.backend.system.utilities import convert_to_datetime
from app.backend.database.firestore import mpesa_transactions
from app.backend.system.ip_address_utils import get_ip_address
from app.backend.transactions.mpesa.safaricom_ip_addresses import ip_addresses
from app.backend.system.config import get_till_number

# Load the stored environment variables
load_dotenv()


# Function to process an m-pesa transaction:
async def process_mpesa_request(mpesa_request: MpesaRequest, request: Request) -> ProcessMpesaRequestResponse:

    # 0. check and validate callback ip_address:
    validate_callback_ip_address = os.getenv("SAFARICOM_IP_ADDRESS_VALIDATION")
    # we have to validate with the word "true"!
    if validate_callback_ip_address.lower() == "true":

        ip_address = await get_ip_address(request=request)
        if ip_address not in ip_addresses.c2b_callback_ip_addresses:
            error = "Invalid Safaricom Callback IP Address."
            raise HTTPException(status_code=400, detail=error)

    # check transaction time:
    # default date time:
    transaction_date_time = (datetime.today()).strftime('%Y-%m-%d %H:%M')
    transaction_date = (datetime.today()).strftime('%Y-%m-%d')

    # check the TransTime:
    if convert_to_datetime(mpesa_request.TransTime) is not None:
        mpesa_request_time = convert_to_datetime(mpesa_request.TransTime)
        transaction_date_time = mpesa_request_time.strftime('%Y-%m-%d %H:%M:%S')
        transaction_date = mpesa_request_time.strftime('%Y-%m-%d')
    else:
        error_on_date_conversion = f"M-Pesa Date conversion error: Date:{mpesa_request.TransTime} does not conform to %d %b %Y"

    # response:
    payment_confirmation = PaymentConfirmation()
    payment_confirmation.transaction_date = transaction_date
    payment_confirmation.request = mpesa_request

    # external response:
    process_mpesa_request_response = ProcessMpesaRequestResponse()
    process_mpesa_request_response.request = mpesa_request

    # 1. validate the third-party trans id:

    # 2. check if the BillRefNumber is empty:

    # 3. check the requesting till number:
    # this business till number:
    till_number = await get_till_number()
    if mpesa_request.BusinessShortCode != till_number:
        error = "Invalid Till Number."
        raise HTTPException(status_code=400, detail=error)

    # 4. Add transaction to database:
    transaction_id_response = add_mpesa_transaction(payment_confirmation=payment_confirmation)
    if transaction_id_response is not None:
        process_mpesa_request_response.transaction_id = transaction_id_response
        process_mpesa_request_response.success = True
    else:
        process_mpesa_request_response.error = "Google Cloud Error..."

    return process_mpesa_request_response


# Function to add an m-pesa transaction:
def add_mpesa_transaction(payment_confirmation: PaymentConfirmation):
    try:

        # Store the mpesa transaction in the firestore:
        doc_ref = mpesa_transactions.document()

        doc_ref.set(payment_confirmation.dict())
    except GoogleCloudError as e:
        return None

    return doc_ref.id
