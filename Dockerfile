FROM python:3.9

COPY ./requirements.txt /app/requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir  -r /app/requirements.txt
COPY . /app
COPY ./entrypoint.sh /app/entrypoint.sh
WORKDIR /app
ENTRYPOINT [ "sh","/app/entrypoint.sh" ]
EXPOSE 80
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "80"]