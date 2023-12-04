import google.cloud.logging

import os


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "app/backend/database/config/actisuremo-dc80f2531777.json"

log_client = google.cloud.logging.Client()
log_client.get_default_handler()
log_client.setup_logging()

