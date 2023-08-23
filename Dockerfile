FROM python

WORKDIR /app/home

COPY . .

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "server.py"]