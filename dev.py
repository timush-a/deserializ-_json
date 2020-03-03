import json
import requests
from datetime import datetime
from os import getcwd, mkdir, path, chdir


directory_name = "tasks"
parent_dir = getcwd()
path = path.join(parent_dir, directory_name)


try:
    mkdir(path)
except OSError:
    print('Folder already exists in ', parent_dir)

chdir(path)
now = datetime.now()
date_time = now.strftime("%d.%m.%Y %H:%M")


users_data_response = requests.get("https://json.medrating.org/users")
tasks_data_responce = requests.get("https://json.medrating.org/todos")


users = json.loads(users_data_response.text)
tasks = json.loads(tasks_data_responce.text)


# add user name, email address, report creation time, company adress

user_info = ""
for i in range(len(users)):
    user_info += "{0}{1}{2}{3}".format(
        users[i]['name'],                                   # user name
        '{0}{1}{2}'.format('<', users[i]['email'], '>'),    # user email
        date_time + '\n\n',                                 # creation time
        'Competed tasks\n'                                  # company adress
                                       )
    if users[i]['id'] == tasks[i]['userId']:
        for a in range(tasks[i]['id']):
            print(a)



