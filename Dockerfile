FROM python:3.9
WORKDIR /backend
COPY . /backend
RUN pip3 install -r requriments.txt
EXPOSE 5000
RUN python3 main.py