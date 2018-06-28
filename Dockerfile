FROM python:2.7-slim

WORKDIR /app

ADD . /app

LABEL "hackathon"="scigility"

RUN pip install pipreqs
RUN pipreqs .
RUN pip install scipy
RUN pip install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 80

ENV NAME World

CMD ["python", "webservice.py"]