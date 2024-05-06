FROM python:3.12

COPY ./requirements.txt /app/requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir  -r /app/requirements.txt
COPY . /app
COPY ./entrypoint.sh /app/entrypoint.sh
WORKDIR /app
ENTRYPOINT [ "sh","/app/entrypoint.sh" ]
EXPOSE 80
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "80"]