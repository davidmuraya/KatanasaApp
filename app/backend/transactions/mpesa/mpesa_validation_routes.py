import logging
import time

from fastapi import APIRouter, Header, HTTPException, Response, status, BackgroundTasks, Request
from fastapi.responses import RedirectResponse

from app.backend.system.application_log import log_client
from app.backend.system.utilities import generate_uuid

from typing import Union


from app.backend.transactions.mpesa.mpesa_models import MpesaRequest, PaymentValidation, PaymentValidationResponse


router = APIRouter()


# Redirect get requests to the not-found page:
@router.get("/transactions/payment-validation", include_in_schema=False)
async def mpesa_validation_get_resource():
    return RedirectResponse("/not-found")


api_summary = "Mpesa Validation End-point"
api_description = "This API validates the MPESA request."


@router.post("/transactions/payment-validation", tags=["Receipts"], summary=api_summary, description=api_description,
             response_model=PaymentValidationResponse, include_in_schema=False)
async def mpesa_validation_post_resource(background_tasks: BackgroundTasks, response: Response, request: Request,
                                         mpesa_request: MpesaRequest,
                                         user_agent: Union[str, None] = Header(default=None, include_in_schema=False)):
    payment_validation = PaymentValidation()

    # log time
    start = time.perf_counter()

    # log request headers:
    list_of_headers = ["request headers"]
    for header, value in request.headers.items():
        list_of_headers.append(f"{header}: {value}")

    logging.info(f"validation request_headers:{list_of_headers}", extra={"labels": {"app": "katanasa"}})

    # log request body:
    body = await request.body()
    logging.info(f"validation request_body: {body}", extra={"labels": {"app": "katanasa"}})

    # generate the unique id:
    third_party_id = await generate_uuid()

    # set the following values:
    payment_validation.ThirdPartyTransID = third_party_id
    payment_validation.request = mpesa_request

    # check the requesting till number:

    # performance monitoring
    request_time = time.perf_counter() - start

    # create a new object to create the response:
    payment_validation_response = PaymentValidationResponse()
    payment_validation_response.ThirdPartyTransID = payment_validation.ThirdPartyTransID

    # save this activity:

    # print(payment_validation)
    return payment_validation_response


"""
Other Result Error Codes
ResultCode ResultDesc
C2B00011 Invalid MSISDN
C2B00012 Invalid Account Number
C2B00013 Invalid Amount
C2B00014 Invalid KYC Details
C2B00015 Invalid Shortcode
C2B00016 Other Error
"""
