from datetime import datetime
import json
import requests
import os
import time


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
    last_change_time = time.strftime('%Y-%m-%dT-%H-%M', time.localtime(change_time))
    return last_change_time


# if file exist, creating a new one, rename the old file
def rename_old_txt_file(file_name):
    if os.path.exists(file_name):
        src = os.path.realpath(file_name)
        time = last_change(file_name)
        os.rename(file_name, file_name[:-4] + "_" + time + ".txt")


while True:
    # API availability check
    try:
        users_data_response = requests.get("https://json.medrating.org/users")
        tasks_data_responce = requests.get("https://json.medrating.org/todos")
    except requests.exceptions.ConnectionError:
        print("Error, the script did not complete the task")
        print("Check your internet connection")
        raise SystemExit

    # receiving data and deserialization
    users_data_response = requests.get("https://json.medrating.org/users")
    tasks_data_responce = requests.get("https://json.medrating.org/todos")

    users = json.loads(users_data_response.text)
    tasks = json.loads(tasks_data_responce.text)

    # current time
    now = datetime.now()
    cr_time = now.strftime("%d.%m.%Y %H:%M")

    # collecting user information, and users tasks
    for user in users:
        user_info = []
        user_info.append(user['name'])  # user name
        user_info.append("{0}{1}{2}".format(' <', user['email'], '> '))  # user email
        user_info.append(cr_time + "\n")  # creation time
        user_info.append(user['company']['name'] + "\n\n")  # company name
        user_info.append("Завершенные задачи:\n")

    # sorting tasks, formatting and append to user_info
        comp_task = []
        outst_task = []

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
        user_info.append("Оставшиеся задачи:\n")
        user_info.append("".join(outst_task))

    # additional check for names : "Mr", "Mrs",
        if user['name'].startswith('Mrs.') or user['name'].startswith('Ms.'):
            user_file_name = "".join("{}.txt".format((user['name']).split()[1]))
        else:
            user_file_name = "{}.txt".format((user['name']).split()[0])

        rename_old_txt_file(user_file_name)  # if file exist, creating a new one

        try:  # with out context manager
            file = open('{}'.format(user_file_name), 'w', encoding='utf-8')
            file.write("".join(user_info))
            file.close()
        except IOError:
            print("IOError")
            path = os.path.join(os.path.abspath(os.path.dirname(__file__)), user_file_name)
            os.remove(path)
    time.sleep(60)
