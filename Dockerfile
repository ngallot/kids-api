FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

# Install dependencies
ADD requirements.txt ./requirements.txt
RUN pip install --upgrade pip -r requirements.txt

# Install app
COPY app /app/app
COPY config /app/config

ENTRYPOINT /start-reload.sh

