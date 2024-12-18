import requests


def post(data):
    url = 'http://127.0.0.1:5000'
    response = requests.post(url, json=data)
    print(response.text)

def put(data):
    url = f"http://127.0.0.1:5000/put/{data['id']}"
    response = requests.put(url, json=data)
    print(response.text)

def get_by_key(key):
    url = f"http://127.0.0.1:5000/by_key/key"
    response = requests.get(url)
    print(response.text)

def get_by_id(id):
    url = f"http://127.0.0.1:5000/by_id/id"
    response = requests.get(url)
    print(response.text)
    
# for i in range(10):
#     data1={
#         'value':['成绩','20240101','20240101',str(i),str(i+1)]
#     }
#     post(data1)
data1 = {
    'id': 4,
    'value':['成绩', '20240101', '20240101', 999, 99]
}
post(data1)
