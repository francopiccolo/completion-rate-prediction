FROM python:3.7
WORKDIR /completion-rate
COPY ./requirements/prod.txt ./requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD ["uwsgi", "http.ini"]