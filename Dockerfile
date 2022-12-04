FROM python:3.9
WORKDIR /backend
COPY . /backend
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
EXPOSE 5000
CMD python3 main.py