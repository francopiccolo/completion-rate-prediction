# completion-rate-prediction
To clone the repo:
```shell script
git clone git@github.com:francopiccolo/completion-rate-prediction.git
cd completion-rate-prediction
```
Then copy the data completion_rate.csv to ./flask/data/

To build docker images for flask, redis and nginx:
```shell script
docker-compose build
```
To run docker containers:
```shell script
docker-compose up
```
After that you should be able to access the Swagger documented API in:
http://localhost:80

To run API stress test:
```shell script
python locustfile.py
```
Which will enable to go to http://localhost:8089/ to simulate the tests.

To test with Postman import the collection on ./flask/test/data/postman_collection.json