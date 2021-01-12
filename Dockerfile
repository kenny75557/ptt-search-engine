FROM python:3.6.9

WORKDIR /PTTapp

ADD . /PTTapp

RUN pip install -r requirements.txt

CMD python main.py