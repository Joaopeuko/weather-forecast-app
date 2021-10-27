FROM python:3.8

WORKDIR /weather-forecast-server

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./lib ./lib
ADD .env .
ADD server.py .

EXPOSE 5000

CMD ["python", "./server.py"]