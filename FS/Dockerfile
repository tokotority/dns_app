FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY fibonacci_server.py .

CMD ["python", "fibonacci_server.py"]