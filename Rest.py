import requests
import json
base = 'https://skyline-queries-default-rtdb.firebaseio.com/'

    
def post(url,data):
    resturl = base+url+'.json'
    r = requests.post(resturl, data)
    return json.loads(r.text)

def get(url):
    resturl = base+url+'.json'
    r = requests.get(resturl)
    return json.loads(r.text)


def delete(url):
    resturl = base+url+'.json'
    r = requests.delete(resturl)
    return json.loads(r.text)


def put(url,data):
    resturl = base+url+'.json'
    print(resturl)
    r = requests.put(resturl, data)
    return json.loads(r.text)

def load(url):
    resturl = base+url+'.json'
    r = requests.get(resturl)
    return json.loads(r.text)
