import time

from fastapi import APIRouter, Header
from fastapi import Response, status, BackgroundTasks, Request
from fastapi.responses import RedirectResponse
from typing import Union


from app.backend.transactions.mpesa.mpesa_process_request import process_mpesa_request
from app.backend.transactions.mpesa.mpesa_models import MpesaRequest, PaymentConfirmationResponse, PaymentConfirmation

router = APIRouter()


# Redirect get requests to the not-found page:
@router.get("/transactions/payment-confirmation", include_in_schema=False)
async def mpesa_validation_get_resource():
    return RedirectResponse("/not-found")


@router.post("/transactions/payment-confirmation", tags=["Receipts"],
             response_model=PaymentConfirmationResponse, include_in_schema=False)
async def mpesa_confirmation_resource(request: Request,
                                      mpesa_request: MpesaRequest, background_tasks: BackgroundTasks, response: Response,
                                      user_agent: Union[str, None] = Header(default=None, include_in_schema=False)):
    # log time
    start = time.perf_counter()

    # internal response:
    payment_confirmation = PaymentConfirmation()
    payment_confirmation.request = mpesa_request

    # external response:
    payment_confirmation_response = PaymentConfirmationResponse()

    # log request headers:
    list_of_headers = ["request headers"]
    for header, value in request.headers.items():
        list_of_headers.append(f"{header}: {value}")

    # logging.info(f"confirmation request_headers:{list_of_headers}", extra={"labels": {"app": "katanasa"}})

    # log request body:
    body = await request.body()
    # logging.info(f"confirmation request_body: {body}", extra={"labels": {"app": "katanasa"}})

    process_mpesa_request_response = await process_mpesa_request(mpesa_request=mpesa_request, request=request)

    # performance monitoring
    request_time = time.perf_counter() - start

    # set the error in the response and log:
    if process_mpesa_request_response.success:
        response.status_code = status.HTTP_200_OK

        payment_confirmation_response.ResultDesc = f"Accepted. Transaction ref {process_mpesa_request_response.transaction_id}"

    else:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        payment_confirmation_response.ResultDesc = process_mpesa_request_response.error

    return payment_confirmation_response
