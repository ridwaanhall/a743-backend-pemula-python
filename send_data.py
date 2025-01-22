import requests

url = 'http://127.0.0.1:8000/notes/'

notes = [
    {"title": "Note 1", "body": "This is the body of note 1.", "tags": ["tag1", "tag2"]},
    {"title": "Note 2", "body": "This is the body of note 2.", "tags": ["tag3", "tag4"]},
    {"title": "Note 3", "body": "This is the body of note 3.", "tags": ["tag5", "tag6"]},
    {"title": "Note 4", "body": "This is the body of note 4.", "tags": ["tag7", "tag8"]},
    {"title": "Note 5", "body": "This is the body of note 5.", "tags": ["tag9", "tag10"]},
    {"title": "Note 6", "body": "This is the body of note 6.", "tags": ["tag11", "tag12"]},
    {"title": "Note 7", "body": "This is the body of note 7.", "tags": ["tag13", "tag14"]},
    {"title": "Note 8", "body": "This is the body of note 8.", "tags": ["tag15", "tag16"]},
    {"title": "Note 9", "body": "This is the body of note 9.", "tags": ["tag17", "tag18"]},
    {"title": "Note 10", "body": "This is the body of note 10.", "tags": ["tag19", "tag20"]}
]

for note in notes:
    response = requests.post(url, json=note)
    print(response.status_code, response.json())
