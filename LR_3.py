# Задание 1
import http.client
import json


conn = http.client.HTTPConnection("167.172.172.227:8000")
conn.request("GET", "/number/10")

r1 = conn.getresponse().read().decode()
number1 = json.loads(r1)
print(number1['number'])


# Задание 2
conn = http.client.HTTPConnection("167.172.172.227:8000")
conn.request("GET", "/number/?option=10")

r2 = conn.getresponse().read().decode()
number2 = json.loads(r2)
print(number2['operation'], number2['number'])
res1 = int(number1['number'] / number2['number'])
print('Результат операции = ', res1)

# Задание 3
headers = {'Content-type': 'application/x-www-form-urlencoded'}
conn.request("POST", "/number/", "option=10", headers)

r3 = conn.getresponse().read().decode()
number3 = json.loads(r3)
print(number3['operation'], number3['number'])
res2 = int(res1 * number3['number'])
print('Результат операции = ', res2)

# Задание 4
headers = {'Content-type': 'application/json'}
body = {"option": 10}
conn.request("PUT", "/number/", json.dumps(body), headers)

r4 = conn.getresponse().read().decode()
number4 = json.loads(r4)
print(number4['operation'], number4['number'])
res3 = int(res2 + number4['number'])
print('Результат операции = ', res3)

# Задание 5
headers = {'Content-type': 'application/json'}
body = {"option": 10}
conn.request("DELETE", "/number/", json.dumps(body), headers)

r5 = conn.getresponse().read().decode()
number5 = json.loads(r5)
print(number5['operation'], number5['number'])
res4 = int(res3 - number5['number'])
print('Результат операции = ', res4)
