# DJANGO TRUECALLER

Steps to run the API
## Install dependencies
```
pip3 install requirements.txt
```

## Runserver
```
python3 manage.py runserver
```
## Test the API
```
Route: http://localhost:8000/signup/
Request Type: POST
Data: 

    {
        "username":"werdtyuejhv",
        "email":"qewq@dqs.dd",
        "password":"qwertyuiop",
        "phone":"77778787887"
    }
```

```
Route: http://localhost:8000/login/
Request Type: POST
Data: 

    {
        "username":"werdtyuejhv",
        "password":"qwertyuiop"
    }
```
### JWT AUTH
You will receive a JWT Auth Token after signUp and signIn.
Include the JWT token in headers as a Bearer Token for all private requests
```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwidXNlcm5hbWUiOiJhbmt1ciJ9.eQicFQy2nYric9Gl2mhqOH4l8An7B_Kf2CKoJmZrPcA
```

### To view all the contacts
```
Public Route: http://localhost:8000/contact/
Request Type: GET
```

### To mark a contact as SPAM
```
Private Route: http://localhost:8000/spam/
Request Type: POST
Data:
    {
        "phone": "9988689898"
    }
```

### To search a contact by name
```
Private Route: http://localhost:8000/search_name?name=Ankur
Request Type: GET
```

### To search a contact by phone
```
Private Route: http://localhost:8000/search_phone?phone=8887655679
Request Type: GET
```
