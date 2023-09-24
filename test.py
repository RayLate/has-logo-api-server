from db.db import *
import requests
import os
# rows = get_all(filter={"total_runtime":0})

for row in os.listdir('/data/2023-09-19'):
    print(row)
    requests.get('http://127.0.0.1:5000/task?folder_path=/data/2023-09-19/{}'.format(row))

print(len(os.listdir('/data/2023-09-19')))