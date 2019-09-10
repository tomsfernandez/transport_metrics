FROM python:3.7-alpine3.9
WORKDIR app
RUN apk add build-base
RUN pip install schedule pymongo requests
COPY . .
ENTRYPOINT ["python","-u","scraper.py"]