import json
import requests
from datetime import datetime
import os
import time


# API availability check
try:
    users_data_response = requests.get("https://json.medrating.org/users")
    tasks_data_responce = requests.get("https://json.medrating.org/todos")
except requests.exceptions.ConnectionError:
    print("Error, the script did not complete the task")
    print("Check yor internet connection")
    raise SystemExit


# creating directory in current directory
def create_folder(directory_name):
    parent_dir = os.getcwd()
    path = os.path.join(parent_dir, directory_name)
    try:
        os.mkdir(path)
    except OSError:
        print("Folder already exists in ", parent_dir)
    os.chdir(path)

create_folder("tasks")


# receiving data and deserialization
users_data_response = requests.get("https://json.medrating.org/users")
tasks_data_responce = requests.get("https://json.medrating.org/todos")

users = json.loads(users_data_response.text)
tasks = json.loads(tasks_data_responce.text)

# current time
now = datetime.now()
date_time = now.strftime("%d.%m.%Y %H:%M")


# last modified time of file
def last_change_time(file_name):
    changed = os.path.getmtime(file_name)
    pp_changed = time.strftime('%Y-%m-%dT-%H-%M', time.localtime(changed))
    return pp_changed


# collecting user information, and save it to string
for user in users:
    user_info = []
    user_info.append(user['name'])                                   # user name
    user_info.append("{0}{1}{2}".format(' <', user['email'], '> '))  # user email
    user_info.append(date_time + "\n")                               # report creation time
    user_info.append(user['company']['name'] + "\n\n")               # company name
    user_info.append("Завершенные задачи\n")

    comp_task = []
    outst_task = []
# sorting tasks, formatting and append to user_info
    for user_task in tasks:
        if user['id'] == user_task['userId']:
            if user_task['completed']:
                if len(user_task['title']) > 50:
                    comp_task.append((user_task['title'])[:50] + "..." + "\n")
                else:
                    comp_task.append(user_task['title'] + "\n")
            else:
                if len(user_task['title']) > 50:
                    outst_task.append((user_task['title'])[:50] + "..." + "\n")
                else:
                    outst_task.append(user_task['title'] + "\n")

    user_info.append("".join(comp_task) + "\n")
    user_info.append("Оставшиеся задачи\n")
    user_info.append("".join(outst_task))
# if file exist, creating a new one, rename the old file
# additional check for names : "Mr", "Mrs",
    if user['name'].startswith('Mrs.') or user['name'].startswith('Ms.'):
        user_file_name = " ".join("{}.txt".format((user['name']).split()[1]))
    else:
        user_file_name = "{}.txt".format((user['name']).split()[0])
    if os.path.exists(user_file_name):
        src = os.path.realpath(user_file_name)
        a = last_change_time(user_file_name)
        os.rename(user_file_name, user_file_name[:-4] + "_" + a + ".txt")
    try:
        file = open('{}'.format(user_file_name), 'w', encoding='utf-8')
        file.write("".join(user_info))
        file.close()
    except IOError:
        print("IOError")
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), user_file_name)
        os.remove(path)
