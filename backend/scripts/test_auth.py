import urllib.request, urllib.parse, json
base='http://127.0.0.1:8000'
# create user
url=base+'/api/v1/auth/register'
data={"name":"Test User","email":"test+syscheck@example.com","password":"Password123!","user_type":"client"}
req=urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers={'Content-Type':'application/json'})
try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        print('REGISTER status', resp.status)
        print(resp.read().decode())
except Exception as e:
    print('REGISTER error', e)

# token
url=base+'/api/v1/auth/token'
form=urllib.parse.urlencode({'username':'test+syscheck@example.com','password':'Password123!'}).encode()
req=urllib.request.Request(url, data=form, headers={'Content-Type':'application/x-www-form-urlencoded'})
try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        print('TOKEN status', resp.status)
        print(resp.read().decode())
except Exception as e:
    print('TOKEN error', e)
