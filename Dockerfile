FROM python:3.9-slim-buster

WORKDIR /katanasa-app

# Step 1: Copy requirements file to the working directory.
COPY ./requirements.txt /katanasa-app/requirements.txt

# Step 2: Install requirements from requirements.txt.
RUN pip install --no-cache-dir --upgrade -r /katanasa-app/requirements.txt

# Step 3: copy from app to /katanasa-app/app.
COPY ./app /katanasa-app/app

# Step 4: Run the web service on container startup using gunicorn webserver.
CMD exec gunicorn --bind :$PORT --workers 1 --worker-class uvicorn.workers.UvicornWorker  --threads 8 app.main:app


# Debugging on localhost:
# EXPOSE 8080

# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]

