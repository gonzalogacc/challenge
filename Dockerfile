FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

ENV PYTHONUNBUFFERED True

ENV APP_HOME /app
WORKDIR $APP_HOME

COPY requirements.txt ./

RUN pip install -r requirements.txt 

COPY . ./

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
