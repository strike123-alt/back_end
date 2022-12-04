FROM python:3.9

COPY . /backend
WORKDIR /backend
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
EXPOSE 8080




# 4

# 5
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:app