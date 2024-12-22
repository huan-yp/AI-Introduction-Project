import requests


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
    
for i in range(1):
    data1={
        'table':'成绩',
        'key':str(i+1),
        'value':[str(i),'20240101','20240101',str(i),str(i+1)]
    }
    put(data1)
# data1={
#         'value':['成绩','20240101','20240101','999','99']
#     }
#post(data1)
