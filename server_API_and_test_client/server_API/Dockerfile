#Dockerfile
FROM python:3.11.7

WORKDIR /HouseAPI

COPY ./requirements.txt .

RUN pip install --upgrade -r ./requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "API_main_mlflow:app", "--reload","--host","0.0.0.0", "--port", "8000"]