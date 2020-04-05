from datetime import datetime, time
import json
import requests
import os
import time


users_url = "https://jsonplaceholder.typicode.com/users"
todos_url = "https://jsonplaceholder.typicode.com/todos"
folder_name = "tasks"


def create_folder(folder_name: str):
    # creating directory in current directory
    parent_dir = os.getcwd()
    path = os.path.join(parent_dir, folder_name)
    try:
        os.mkdir(path)
    except OSError:
        print("Folder already exists in ", parent_dir)
    os.chdir(path)


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


def report_creation(users_url: str, todos_url: str, folder_name: str):
    """
    Creating reports for each user in the specified directory(folder_name).
    Uses 2 API (users_url, todos_url) which return JSON files.

    Example:
    Leanne Graham <Sincere@april.biz> 04.04.2020 16:55
    Romaguera-Crona

    Completed tasks:
    et porro tempora
    quo adipisci enim quam ut ab
    illo est ratione doloremque quia maiores aut
    vero rerum temporibus dolor
    ipsa repellendus fugit nisi
    repellendus sunt dolores architecto voluptatum
    ab voluptatum amet voluptas
    accusamus eos facilis sint et aut voluptatem
    quo laboriosam deleniti aut qui
    molestiae ipsa aut voluptatibus pariatur dolor nih...
    ullam nobis libero sapiente ad optio sint

    Outstanding tasks:
    delectus aut autem
    quis ut nam facilis et officia qui
    fugiat veniam minus
    laboriosam mollitia et enim quasi adipisci quia pr...
    qui ullam ratione quibusdam voluptatem quia omnis
    illo expedita consequatur quia in
    molestiae perspiciatis ipsa
    et doloremque nulla
    dolorum est consequatur ea mollitia in culpa
    """


# reports will be created in this folder
    create_folder(str(folder_name))

# API availability check
    try:
        requests.get("https://jsonplaceholder.typicode.com/users")
        requests.get("https://jsonplaceholder.typicode.com/todos")
    except requests.exceptions.ConnectionError:
        print("Connection error, the script did not complete the task")
        print("Check your internet connection")
    raise SystemExit

# receiving data and deserialization
    users_data_response = requests.get(users_url)
    tasks_data_responce = requests.get(users_todos)

    users = json.loads(users_data_response.text)
    tasks = json.loads(tasks_data_responce.text)

# collecting user information, and users tasks
    for user in users:
        user_info = []
        user_info.append(user['name'])  # user name
        user_info.append(f" <{user['email']}> ")  # user email
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


if __name__ == "__main__":
    report_creation(users_url, todos_url, folder_name)
