FROM python:3-alpine


WORKDIR /chanreader_telegram

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN apk --no-cache add gcc musl-dev
RUN pip install -r requirements.txt

COPY . .


CMD [ "python", "./telegram.py" ]
