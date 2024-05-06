FROM python:3.12
WORKDIR /usr/src/cherkiz
COPY ./app ./app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
#CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]