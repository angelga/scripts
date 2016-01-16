import requests

r = requests.post("", json={'first_name': '', 'last_name': '', 'email': '', 'phone': '', 'cover_letter': '', 'urls': ['', '']})

print(r.status_code, r.reason)
print(r.text)
