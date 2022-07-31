FROM    python:latest

ADD /gtw /gtw

RUN pip3 install -r /gtw/requirements.txt

CMD python3 /gtw/main.py

