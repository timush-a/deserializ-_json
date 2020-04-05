from datetime import datetime
import json
import requests
import os
import time


users_url = "https://jsonplaceholder.typicode.com/users"
todos_url = "https://jsonplaceholder.typicode.com/todos"
folder_name = "reports"


def api_availability(*urls):
    # check connection to urls
    for url in urls:
        try:
            requests.get(url)
            print(f"Successfully connected to {url}")
        except requests.exceptions.ConnectionError:
            print(f"An error occured during connection to {url}")
            raise SystemExit


def create_folder(folder_name: str):
    # creating directory in current directory
    parent_dir = os.getcwd()
    path = os.path.join(parent_dir, folder_name)
    try:
        os.mkdir(path)
        return print(f"{folder_name} in {parent_dir} created")
    except OSError:
        print("Folder already exists in ", parent_dir)
    os.chdir(path)


def rename_old_txt_file(file_name):
    # if file exist, creating a new one, rename the old file
    if os.path.exists(file_name):
        change_time = os.path.getmtime(file_name)
        last_change = time.strftime('%Y-%m-%dT%H-%m-%S', time.localtime(change_time))
        os.rename(file_name, f'{file_name[:-4]}_{last_change}.txt')


def shorten_task_name(task_name):
    # shorten the task name if len > 50
    if len(task_name) > 50:
        return f"{task_name[:50]}...\n"
    else:
        return f"{task_name}\n"


def reports_creation(users_url: str, todos_url: str, folder_name: str):
    """
    Creating reports for each user in the specified directory.
    Uses 2 API (users_url, todos_url) which return JSON files.
    """

    api_availability(users_url, todos_url)

# reports will be created in this folder
    create_folder(str(folder_name))


# receiving data and deserialization
    users_data_response = requests.get(users_url)
    tasks_data_responce = requests.get(todos_url)

    users = json.loads(users_data_response.text)
    tasks = json.loads(tasks_data_responce.text)

# collecting user information, and users tasks
    for user in users:
        user_info = []
        user_info.append(user['name'])  # user name
        user_info.append(f" <{user['email']}> ")  # user email
        user_info.append(f"{time.strftime('%Y-%m-%d %H:%m', time.localtime())}\n")  # creation time
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

        user_info.append("".join(comp_task))
        user_info.append("\nOutstanding tasks:\n")
        user_info.append("".join(outst_task))

        user_file = f"{user['username']}.txt"
        rename_old_txt_file(user_file)  # if file exist, creating a new one

        try:  # with out context manager
            file = open(user_file, "w", encoding="utf-8")
            file.write("".join(user_info))
            file.close()
            print(f"Report for {user['name']} created")
        except IOError:
            print("IOError")
            path = os.path.join(os.path.abspath(os.path.dirname(__file__)), user_file_name)
            os.remove(path)

if __name__ == "__main__":
    reports_creation(users_url, todos_url, folder_name)
