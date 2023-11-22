FROM python:3.10-slim

WORKDIR /opt/alloxentric

RUN apt-get update && apt-get -y install curl

COPY ./requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

# Para desarrollo
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# Para producción
#ENTRYPOINT ["gunicorn", "main:app", "--worker-class", "uvicorn.workers.UvicornWorker"]
#CMD ["-w", "4", "--timeout", "90"]