FROM python:3.8

WORKDIR /usr/src/app

ADD main.py .
COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

CMD [ "python", "./main.py" ]