from datetime import datetime
from pydantic import parse_obj_as
from operator import itemgetter

from app.backend.transactions.sales_models import SaleTransaction
from app.backend.transactions.mpesa.mpesa_models import MpesaRequest, PaymentConfirmation
from app.backend.database.firestore import transactions, mpesa_transactions

from app.backend.database.firestore import descending_order


# Sales and Transaction functions:
#
# Function to add/create a sale/transaction:
def add_transaction_sale(sale_transaction: SaleTransaction) -> str:
    date_today = (datetime.today()).strftime('%Y-%m-%d')

    # set the log entry date:
    sale_transaction.entry_date = date_today

    # Set the collection ref and store the transaction in the firestore:
    doc_ref = transactions.document()
    doc_ref.set(sale_transaction.dict())

    return doc_ref.id


# Function to get sales by customer:
def get_sales_by_customer(customer_id: str):
    list_of_sales = []
    query = transactions.where('customer_id', '==', customer_id)

    docs = query.get()

    for doc in docs:
        doc_dict = doc.to_dict()

        # Use parse_obj_as to parse the dictionary into an SaleTransaction object
        trans_obj = parse_obj_as(SaleTransaction, doc_dict)

        # Convert the SaleTransaction object to a dictionary before appending to the list
        transaction_dict = {"transaction_id": doc.id, "transaction_data": trans_obj.dict()}

        # add transaction to the list of all sales:
        list_of_sales.append(transaction_dict)

    return list_of_sales


# Function to get all sales:
def get_all_sales():
    list_of_sales = []

    docs = transactions.order_by('sales_date', direction=descending_order).get()

    for doc in docs:
        doc_dict = doc.to_dict()

        # Use parse_obj_as to parse the dictionary into an SaleTransaction object
        trans_obj = parse_obj_as(SaleTransaction, doc_dict)

        # Convert the SaleTransaction object to a dictionary before appending to the list:
        transaction_dict = {"transaction_id": doc.id, "transaction_data": trans_obj.dict()}

        # add transaction to the list of all sales:
        list_of_sales.append(transaction_dict)

    return list_of_sales


# Function to check for duplicate sales entries by amount received:
def check_for_duplicate_sale_entry(customer_id: str, sale_date: str, amount_received: float) -> bool:
    query = (transactions.where('customer_id', '==', customer_id)
             .where('sales_date', '==', sale_date)
             .where('amount_received', '==', amount_received))

    docs = query.get()

    if len(docs) > 0:
        return True
    else:
        return False


# Function to check for duplicate sales entries by transaction_ref:
def check_for_duplicate_sale_entry_by_transaction_ref(customer_id: str, sale_date: str, transaction_ref: str) -> bool:
    query = (transactions.where('customer_id', '==', customer_id)
             .where('sales_date', '==', sale_date)
             .where('transaction_ref', '==', transaction_ref))

    docs = query.get()

    if len(docs) > 0:
        return True
    else:
        return False


# delete a specific doc in the transactions collection:
def delete_transaction(doc_id: str) -> bool:
    success = False

    try:
        # Reference to the document you want to delete
        doc_ref = transactions.document(doc_id)

        # Delete the document
        doc_ref.delete()
        print(f"Transaction {doc_id} successfully deleted.")
        success = True
    except Exception as e:
        print(e)

    return success


# M-Pesa
# Function to get all m-pesa transactions:
def get_all_m_pesa_transactions():
    list_of_transactions = []

    docs = mpesa_transactions.order_by('request.TransTime', direction=descending_order).get()

    for doc in docs:
        doc_dict = doc.to_dict()

        # Use parse_obj_as to parse the dictionary into an PaymentConfirmation object
        trans_obj = parse_obj_as(PaymentConfirmation, doc_dict)

        # Convert the SaleTransaction object to a dictionary before appending to the list:
        transaction_dict = {"transaction_id": doc.id, "transaction_data": trans_obj.dict()}

        # add transaction to the list of all sales:
        list_of_transactions.append(transaction_dict)

    return list_of_transactions


# Function to get all m-pesa transactions by day:
def get_all_m_pesa_transactions_by_date(transaction_date: str):
    list_of_transactions = []

    query = mpesa_transactions.where('transaction_date', '==', transaction_date)

    docs = query.get()

    for doc in docs:
        doc_dict = doc.to_dict()

        # Use parse_obj_as to parse the dictionary into an PaymentConfirmation object
        trans_obj = parse_obj_as(PaymentConfirmation, doc_dict)

        # Access 'TransTime' within the 'request' attribute
        trans_time = trans_obj.request.TransTime if trans_obj.request else None

        # Convert the SaleTransaction object to a dictionary before appending to the list:
        transaction_dict = {"transaction_id": doc.id, "transaction_data": trans_obj.dict(), "TransTime": trans_time}

        # add transaction to the list of all sales:
        list_of_transactions.append(transaction_dict)

        # Sort the list_of_transactions by TransTime in descending order
    list_of_transactions.sort(key=itemgetter('TransTime'), reverse=True)

    return list_of_transactions


# Function to change a payment-confirmation allocation status:
def allocate_transaction(document_id: str):

    try:

        # Retrieve the document from firestore:
        doc_ref = mpesa_transactions.document(document_id=document_id)
        doc = doc_ref.get()

        # Check if the document exists:
        if doc.exists:
            # Get the data from the document:
            data = doc.to_dict()

            # Update the 'allocated' field:
            data["allocated"] = True

            # Update the document in Firestore:
            doc_ref.update(data)
            return True  # Indicate success
        else:
            # Handle the case where the document does not exist.
            return False  # Indicate failure

    except Exception as e:
        # Log the exception or handle it according to your application's needs.
        print(f"Error allocating transaction: {e}")
        return False  # Indicate failure
