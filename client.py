import requests
import time

resp = requests.post('http://127.0.0.1:5000/email')
resp_data = resp.json()
print(resp_data)
task_id = resp_data.get('task_id')
print(task_id)
#

resp = requests.get(f'http://127.0.0.1:5000/email/{task_id}')
print(resp.json())
time.sleep(10)

resp = requests.get(f'http://127.0.0.1:5000/email/{task_id}')
print(resp.json())
