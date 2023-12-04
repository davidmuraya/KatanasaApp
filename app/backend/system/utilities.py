import re
from dateutil import parser
import uuid


def is_valid_email(email):
    # Regular expression for a valid email address
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    # Check if the email matches the pattern
    if re.match(email_pattern, email):
        return True
    else:
        return False


# Function to check if string can be converted to datetime object. Function uses heuristics.
def convert_to_datetime(date_string):
    try:
        datetime_obj = parser.parse(date_string)
        return datetime_obj
    except ValueError:
        return None


# Function to generate uuids for mpesa:
async def generate_uuid() -> str:
    unique_id = uuid.uuid4()  # Generate a random UUID

    unique_id_str = str(unique_id).replace("-", "")

    return unique_id_str
