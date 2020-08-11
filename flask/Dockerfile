FROM python:3.7
WORKDIR flask
COPY ./requirements/prod.txt ./requirements.txt
RUN pip install -r requirements.txt
COPY . .
ENV PYTHONPATH=./
RUN pytest ./test
CMD ["uwsgi", "http.ini"]