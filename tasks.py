import requests
import time

async def make_api_request(a):
	print('updated')
	print('-'*20+' start')
	url = f'http://127.0.0.1:5001/predict?folder_path={a}'
	response = requests.get(url,timeout=None)
	# print(response.json())
	print('-'*20+' end')
	return {'status':'complete'}

def dummy_task(a):

	print(f'doing {a}')
	time.sleep(5)
	print('complete')

	return {'status':'complete'}