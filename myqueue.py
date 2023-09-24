from flask import Flask, request
import requests
import redis
from rq import Queue
from tasks import make_api_request, dummy_task

import time


app = Flask(__name__)
app.name='queue server'
r=redis.Redis()
q=Queue(connection=r)


@app.route("/")
def get_health():
	return "Server is Live"


@app.route("/task")
def add_task():

	if request.args.get("folder_path"):
		job = q.enqueue(make_api_request,request.args.get("folder_path"))
		q_len=len(q)

		return f"the task {job.id} is added into the task queue at {job.enqueued_at}. {q_len} task in queue" 

	if request.args.get('test'):
		job = q.enqueue(dummy_task,request.args.get("test"))
		q_len=len(q)
		print(f"the task {job.id} is added into the task queue at {job.enqueued_at}. {q_len} task in queue")

		return f"the task {job.id} is added into the task queue at {job.enqueued_at}. {q_len} task in queue" 

	return "search_param error"


if __name__ == "__main__":
	app.run(host='0.0.0.0',port=5000)
