from datetime import datetime
import json
import requests
import os
import time


# API availability check
try:
    requests.get("https://jsonplaceholder.typicode.com/users")
    requests.get("https://jsonplaceholder.typicode.com/todos")
except requests.exceptions.ConnectionError:
    print("Error, the script did not complete the task")
    print("Check your internet connection")
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


# reports will be created in this folder
create_folder("tasks")


# last modified time of file
def last_change(file_name):
    change_time = os.path.getmtime(file_name)
    last_change_time = time.strftime('%Y-%m-%dT%H:%m:%s', time.localtime(change_time))
    return last_change_time


# if file exist, creating a new one, rename the old file
def rename_old_txt_file(file_name):
    if os.path.exists(file_name):
        time = last_change(file_name)
        os.rename(file_name, f'{file_name[:-4]}_{time}.txt')


# shorten the task name
def shorten_task_name(task_name):
    if len(task_name) > 50:
        return f"{task_name[:50]}...\n"
    else:
        return f"{task_name}\n"


# receiving data and deserialization
users_data_response = requests.get("https://jsonplaceholder.typicode.com/users")
tasks_data_responce = requests.get("https://jsonplaceholder.typicode.com/todos")

users = json.loads(users_data_response.text)
tasks = json.loads(tasks_data_responce.text)

# current time
now = datetime.now()
cr_time = now.strftime("%d.%m.%Y %H:%M")

# collecting user information, and users tasks
for user in users:
    user_info = []
    user_info.append(user['name'])  # user name
    user_info.append(f"<{user['email']}>")  # user email
    user_info.append(f"{cr_time}\n")  # creation time
    user_info.append(f"{user['company']['name']}\n\n")  # company name
    user_info.append('Completed tasks:\n')

# sorting tasks, formatting and append to user_info
    comp_task = []
    outst_task = []

    for user_task in tasks:
        if user['id'] == user_task['userId']:
            if user_task['completed']:
                comp_task.append(shorten_task_name(user_task['title']))
            else:
                outst_task.append(shorten_task_name(user_task['title']))

    user_info.append("".join(comp_task) + "\n")
    user_info.append("Outstanding tasks:\n")
    user_info.append("".join(outst_task))

    user_file_name = f"{user['username']}.txt"

    rename_old_txt_file(user_file_name)  # if file exist, creating a new one

    try:  # with out context manager
        file = open(f'{user_file_name}', 'w', encoding='utf-8')
        file.write("".join(user_info))
        file.close()
        print('Report created')
    except IOError:
        print("IOError")
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), user_file_name)
        os.remove(path)
