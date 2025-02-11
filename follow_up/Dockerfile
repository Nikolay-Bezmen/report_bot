FROM python:3.10

WORKDIR /app

COPY main.py requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 6000

CMD ["python", "main.py"]


# docker build -t follow_up-analyzer .
# docker run -d -p 6000:6000 follow_up-analyzer
