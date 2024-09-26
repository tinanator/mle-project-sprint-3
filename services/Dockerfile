FROM python:3.11-slim


LABEL author=${AUTHOR}


COPY . ./app
WORKDIR app
RUN pip3 install -r requirements.txt


EXPOSE ${PORT}


CMD uvicorn ml_service.main:app --reload --port ${PORT} --host 0.0.0.0 