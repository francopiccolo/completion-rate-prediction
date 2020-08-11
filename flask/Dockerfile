FROM python:3.7
COPY ./requirements/prod.txt ./requirements.txt
RUN pip install -r requirements.txt
COPY . .
ENV PYTHONPATH=./flask
RUN pytest ./flask/test
CMD ["uwsgi", "http.ini"]