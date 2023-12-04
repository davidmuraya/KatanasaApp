from app.backend.database.firestore import customers, customer_attendance
from app.backend.customer.customer_models import Customer, Attendance
from datetime import datetime
from pydantic import parse_obj_as


def get_customer_by_name(name: str):
    customers_list = []

    query = customers.where('name', '==', name)

    docs = query.get()

    for doc in docs:
        doc_dict = doc.to_dict()
        customer = {doc_dict["name"]: doc.to_dict()}
        customers_list.append(customer)

    return customers_list


# Function to check for duplicate phone numbers in the customers collection/table:
def check_for_duplicate_phone_numbers(phone: str) -> bool:
    query = customers.where('phone', '==', phone)

    docs = query.get()

    if len(docs) > 0:
        return True
    else:
        return False


# Function to check for duplicate email addresses in the customers collection/table:
def check_for_duplicate_email(email: str) -> bool:
    query = customers.where('email', '==', email)

    docs = query.get()

    if len(docs) > 0:
        return True
    else:
        return False


# Function to get a list of all customers:
def get_all_customers():
    customers_list = []

    # Order the records by 'first_name'
    docs = customers.order_by('first_name').get()

    for doc in docs:
        doc_dict = doc.to_dict()

        # Use parse_obj_as to parse the dictionary into a Customer object
        customer_obj = parse_obj_as(Customer, doc_dict)

        # Convert the Customer object to a dictionary before appending to the list
        customer_dict = {"customer_id": doc.id, "customer_data": customer_obj.dict()}

        customers_list.append(customer_dict)

    return customers_list


# Function to add a customer:
def add_customer(customer: Customer) -> str:
    date_today = (datetime.today()).strftime('%Y-%m-%d')

    customer.creation_date = date_today

    # Store the customer in the firestore:
    doc_ref = customers.document()
    doc_ref.set(customer.dict())

    return doc_ref.id


# delete a specific doc in the customer's collection:
def delete_customer(doc_id: str) -> bool:
    success = False

    try:
        # Reference to the document you want to delete
        doc_ref = customers.document(doc_id)

        # Delete the document
        doc_ref.delete()
        print(f"Customer/Document with ID {doc_id} successfully deleted.")
        success = True
    except Exception as e:
        print(e)

    return success


# delete a specific doc in the attendance collection:
def delete_customer_attendance_record(doc_id: str) -> bool:
    success = False

    try:
        # Reference to the document you want to delete
        doc_ref = customer_attendance.document(doc_id)

        # Delete the document
        doc_ref.delete()
        print(f"Customer Attendance record with id {doc_id} successfully deleted.")
        success = True
    except Exception as e:
        print(e)

    return success


#
#
# Customer Attendance Functions:
#
# Function to add a customer attendance record:
def add_customer_attendance(attendance: Attendance):
    # check for duplicate attendance_entry
    duplicate = check_for_duplicate_attendance_entry(customer_id=attendance.customer_id, attendance_date=attendance.attendance_date)

    if duplicate:
        return None
    else:
        entry_today = (datetime.today()).strftime('%Y-%m-%d')

        attendance.entry_date = entry_today

        # Store the customer in the firestore:
        doc_ref = customer_attendance.document()
        doc_ref.set(attendance.dict())

        return doc_ref.id


# Function to check for duplicate attendance entries:
def check_for_duplicate_attendance_entry(customer_id: str, attendance_date: str) -> bool:
    query = customer_attendance.where('customer_id', '==', customer_id).where('attendance_date', '==', attendance_date)

    docs = query.get()

    if len(docs) > 0:
        return True
    else:
        return False


# Function to get attendance entries by customer:
def get_attendance_entries_by_customer(customer_id: str):
    list_of_entries = []
    query = customer_attendance.where('customer_id', '==', customer_id)

    docs = query.get()

    for doc in docs:
        doc_dict = doc.to_dict()

        # Use parse_obj_as to parse the dictionary into an Attendance object
        entry_obj = parse_obj_as(Attendance, doc_dict)

        # Convert the Attendance object to a dictionary before appending to the list
        entry_dict = {"entry_id": doc.id, "entry_data": entry_obj.dict()}

        list_of_entries.append(entry_dict)

    return list_of_entries


# Function to get all attendance entries:
def get_all_attendance_entries():
    list_of_entries = []

    docs = customer_attendance.get()

    for doc in docs:
        doc_dict = doc.to_dict()

        # Use parse_obj_as to parse the dictionary into an Attendance object
        entry_obj = parse_obj_as(Attendance, doc_dict)

        # Convert the Attendance object to a dictionary before appending to the list
        entry_dict = {"entry_id": doc.id, "entry_data": entry_obj.dict()}

        list_of_entries.append(entry_dict)

    return list_of_entries
