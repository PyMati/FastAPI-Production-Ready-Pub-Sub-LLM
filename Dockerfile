FROM python:3.14.3

WORKDIR /app
COPY requirements.txt /app
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt
COPY ./src /app
EXPOSE 8000

CMD ["./prod.sh"]