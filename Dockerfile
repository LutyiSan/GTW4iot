FROM    python:3.9-slim-buster

COPY ./gtw /gtw

RUN pip3 install -r /gtw/requirements.txt

RUN pip3 install psycopg2-binary

CMD python3 /gtw/main.py


