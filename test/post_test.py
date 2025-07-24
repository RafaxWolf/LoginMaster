import requests

rank = {
    "usuario":"akomisad",
    "rank":"normal"
}

print(requests.post("http://192.168.253.130:5000/type_verify",json=rank).text)