from app.backend.database.firestore import settings


# function to get till number from firestore:
async def get_till_number() -> str:

    # get the doc called config in the settings collection:
    doc_ref = settings.document("config")
    doc = doc_ref.get().to_dict()

    till_number = doc["till_number"]

    return till_number





