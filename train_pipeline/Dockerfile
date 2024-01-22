#Dockerfile
FROM python:3.11.7

WORKDIR /HouseML_Pipeline

COPY ./requirements.txt .

RUN pip install --upgrade -r ./requirements.txt

COPY . .

EXPOSE 5000

CMD ["mlflow", "server", "--backend-store-uri", "sqlite:///mlflow.db", "--default-artifact-root", "./artifacts", "--host", "0.0.0.0", "--port", "5000"]