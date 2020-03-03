import json
import requests
from datetime import datetime
import os


# API availability check
try:
    users_data_response = requests.get("https://json.medrating.org/users")
    tasks_data_responce = requests.get("https://json.medrating.org/todos")
except requests.exceptions.ConnectionError:
    print("Error, the script did not complete the task")
    print("Check yor internet connection")
    raise SystemExit


# creating directory, changing current directrory
def create_folder(directory_name):
    parent_dir = os.getcwd()
    path = os.path.join(parent_dir, directory_name)
    try:
        os.mkdir(path)
    except OSError:
        print("Folder already exists in ", parent_dir)
    os.chdir(path)

create_folder("tasks")

now = datetime.now()
date_time = now.strftime("%d.%m.%Y %H:%M")


# receiving data and deserialization
users_data_response = requests.get("https://json.medrating.org/users")
tasks_data_responce = requests.get("https://json.medrating.org/todos")

users = json.loads(users_data_response.text)
tasks = json.loads(tasks_data_responce.text)


# add user name, email address, report creation time, company adress
for i in range(len(users)):
    user_info = ""
    user_info += "{0}{1}{2}{3}".format(
        users[i]['name'],                                  # user name
        '{0}{1}{2}'.format('<', users[i]['email'], '>'),   # user email
        date_time + "\n\n",                                # creation time
        "Competed tasks\n"                                 # company adress
                                                             )

if users[i]['id'] == tasks[i]['userId']:
        for a in range(tasks[i]['id']):
            print(a)
