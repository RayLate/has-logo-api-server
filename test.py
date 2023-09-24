from requests import post
import os
import time
folders = os.listdir('/data/has-logo-queue')
start = time.time()
for folder in folders:
    post(f'http://127.0.0.1:5000/{folder}')
    t_end = time.time()
    print(f'{folder}\t{t_end - start}')

t_final = time.time()
print(f'{len(folders)} domain took {t_final - start} with an average of {(t_final - start)/len(folders)}')