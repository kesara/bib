FROM python:3.11

WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY app.py /app/
COPY scripts/load-data.py /app/scripts/

CMD python3 app.py
