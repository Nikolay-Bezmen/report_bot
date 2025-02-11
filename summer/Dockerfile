FROM python:3.10

WORKDIR /app

COPY main.py requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "main.py"]


# docker build -t flask-analyzer .
# docker run -d -p 5000:5000 flask-analyzer
