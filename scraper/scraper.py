import schedule
import time
from pymongo import MongoClient
import os

mongo_host = os.environ['MONGO_HOST']
mongo_port = os.environ['MONGO_PORT']
mongo_db = os.environ['MONGO_DB']
mongo_collection = os.environ['MONGO_COLLECTION']

print(f"Connecting to Mongo en {mongo_host}:{mongo_port}")
client = MongoClient(f"{mongo_host}:{mongo_port}")
print(f"Connected succesfully")
collection = client[mongo_db][mongo_collection]

def api_call():
  import time
  import requests
  op_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
  print(f"{op_time} - Calling BA API")
  response = requests.get("https://apitransporte.buenosaires.gob.ar/colectivos/vehiclePositions?client_id=a6f6a0e6a4944509a9f0ee04e5b576ef&client_secret=1CE72344c7B04b3F96A3FE0b27F42b3c&json=1")
  if response.status_code != 200:
    print(f"{op_time} - Call to BA API wasnt succesfull... Skipping")
    return
  op_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
  print(f"{op_time} - Call to BA API succesfull")
  data = response.json()["_entity"]
  for d in data:
    del d['_id']
  collection.insert_many(data)
  op_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
  print(f"{op_time} - Dumped points")


schedule.every(30).seconds.do(api_call)

while True:
  schedule.run_pending()
  time.sleep(1)