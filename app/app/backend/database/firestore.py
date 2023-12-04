from google.cloud import firestore
from dotenv import load_dotenv
import os

# Load the stored environment variables
load_dotenv()

# Set the path to your credentials JSON file
credentials_path = "app/backend/database/config/fir-credentials-store-firebase-adminsdk-g1ott-df958500e1.json"

# Set the project ID and specify the database ID (katanasa-db)
project_id = "fir-credentials-store"
database_id = os.getenv("DATABASE")

# Create a Firestore client with the specified database ID
db = firestore.Client.from_service_account_json(credentials_path, project=project_id, database=database_id)

# define sort order
descending_order = firestore.Query.DESCENDING

# name of the collection where customer are:
customers = db.collection("customers")

# name of the collection where customer_attendance records are:
customer_attendance = db.collection("customer_attendance")

# name of the collection where transactions are:
transactions = db.collection("transactions")

# name of the collection where users are:
users = db.collection("users")

# name of the collection where m-pesa transactions are:
mpesa_transactions = db.collection("mpesa_transactions")

# name of the collection where settings are:
settings = db.collection("settings")


