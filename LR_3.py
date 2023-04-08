# Задание 1
import http.client
import json

def operate(data: str, left: int):
  d = json.loads(data)
  if d['operation'] == 'div':
    return left / d['number']
  if d['operation'] == 'mul':
    return left * d['number']
  if d['operation'] == 'sum':
    return left + d['number']
  if d['operation'] == 'sub':
    return left - d['number']

option = 10
result = 0

conn = http.client.HTTPConnection("167.172.172.227:8000")
conn.request("GET", "/number/" + option)

response = conn.getresponse().read().decode()
result += json.loads(response)['number']
print(result)

# Задание 2
conn = http.client.HTTPConnection("167.172.172.227:8000")
conn.request("GET", "/number/?option=" + option)

response = conn.getresponse().read().decode()
result = operate(response, result)
print('Результат операции = ', result)

# Задание 3
headers = {'Content-type': 'application/x-www-form-urlencoded'}
conn.request("POST", "/number/", "option=" + option, headers)

response = conn.getresponse().read().decode()
result = operate(response, result)
print('Результат операции = ', result)

# Задание 4
headers = {'Content-type': 'application/json'}
body = {"option": option}
conn.request("PUT", "/number/", json.dumps(body), headers)

response = conn.getresponse().read().decode()
result = operate(response, result)
print('Результат операции = ', result)

# Задание 5
headers = {'Content-type': 'application/json'}
body = {"option": option}
conn.request("DELETE", "/number/", json.dumps(body), headers)

response = conn.getresponse().read().decode()
result = operate(response, result)
print('Результат операции = ', result)
