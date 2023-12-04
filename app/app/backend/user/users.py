from app.backend.database.firestore import users
from app.backend.user.user_models import User
from datetime import datetime
from pydantic import parse_obj_as


# Function to check for duplicate username in the users collection/table:
def check_for_duplicate_username(username: str) -> bool:
    query = users.where('username', '==', username)

    docs = query.get()

    if len(docs) > 0:
        return True
    else:
        return False


# Function to get a list of all users:
def get_all_users():
    users_list = []

    # get all docs in the users collection:
    docs = users.get()

    for doc in docs:
        doc_dict = doc.to_dict()

        # Use parse_obj_as to parse the dictionary into a User object
        user_obj = parse_obj_as(User, doc_dict)

        # Convert the User object to a dictionary before appending to the list
        user_dict = {"user_id": doc.id, "user_data": user_obj.dict()}

        # add user_dict to the users_list:
        users_list.append(user_dict)

    return users_list


# Function to get a list users by username:
def get_user_by_username(username: str):
    user_dict = {}

    query = users.where('username', '==', username)

    # get all docs in the users collection:
    docs = query.get()

    for doc in docs:
        doc_dict = doc.to_dict()

        # Use parse_obj_as to parse the dictionary into a User object
        user_obj = parse_obj_as(User, doc_dict)

        # return the user_obj without converting to dict so that we can access the properties:
        user_dict = {"user_id": doc.id, "user_data": user_obj}

        return user_dict


# Function to add a user:
def add_user(user: User) -> str:
    date_today = (datetime.today()).strftime('%Y-%m-%d')

    user.creation_date = date_today

    # Store the users in the firestore:
    doc_ref = users.document()
    doc_ref.set(user.dict())

    return doc_ref.id


# delete a specific doc in the user's collection:
def delete_user(doc_id: str) -> bool:
    success = False

    try:
        # Reference to the document you want to delete
        doc_ref = users.document(doc_id)

        # Delete the document
        doc_ref.delete()
        print(f"User id {doc_id} successfully deleted.")
        success = True
    except Exception as e:
        print(e)

    return success


# Function to update the password for a user in the user's collection:
def update_user_password(doc_id: str, password: str) -> bool:
    # Initialize success flag as False
    success = False

    try:
        # Get reference to the document in the 'users' collection using the provided doc_id
        doc_ref = users.document(doc_id)

        # Retrieve the current data of the document
        doc = doc_ref.get()

        # Convert the document data to a dictionary
        data = doc.to_dict()

        # Update the password field in the data dictionary
        data["password"] = password

        # Update the document in the collection with the modified data
        doc_ref.update(data)

        # Print success message if the update is successful
        print(f"User id {doc_id} password successfully updated.")

        # Set success flag to True
        success = True
    except Exception as e:
        # Print any exceptions that occur during the update process
        print(e)

    # Return the success flag indicating whether the update was successful
    return success
