import json, urllib.request
users = urllib.request.urlopen("https://json.medrating.org/users").read()
users_txt = open('users.txt', 'w')
users_txt.write(str(json.loads(users)))


todos = urllib.request.urlopen("https://json.medrating.org/todos").read()
todos_txt = open('todos.txt', 'w')
todos_txt.write(str(json.loads(todos)))



