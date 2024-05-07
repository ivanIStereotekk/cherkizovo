FROM python:3.9
LABEL author="Ivan Goncharov" email="ivan.stereotekk@gmail.com"
COPY ./requirements.txt /app/requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir  -r /app/requirements.txt
COPY . /app
WORKDIR /app
EXPOSE 80
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "80"]