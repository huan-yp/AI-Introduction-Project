import requests

def creat(data):
    url = f'http://127.0.0.1:5000/creattable/{data['table']}'
    response = requests.post(url, json=data)
    print(response.text)

def post(data):
    url = f'http://127.0.0.1:5000/{data['table']}'
    response = requests.post(url, json=data)
    print(response.text)

def put(data):
    url = f"http://127.0.0.1:5000/put/{data['table']}/{data['key']}"
    response = requests.put(url, json=data)
    print(response.text)

def get_by_key(table,key):
    url = f"http://127.0.0.1:5000/by_key/{table}/{key}"
    response = requests.get(url)
    print(response.text)

def get_by_table(table,key):
    url = f"http://127.0.0.1:5000/by_table/{table}"
    response = requests.get(url)
    print(response.text)

data1={
    'table':'成绩',
    'key':str(1),
    'value':[str(1),'20240101','20240101']
}
post(data1)
creat(data1)
post(data1)
# data1={
#         'value':['成绩','20240101','20240101','999','99']
#     }
#post(data1)
