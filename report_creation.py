from datetime import datetime
import json
import requests
import os
import time


users_url = "https://jsonplaceholder.typicode.com/users"
todos_url = "https://jsonplaceaholder.typicode.com/todos"
folder_name = "reports"

responses = requests.get(users_url), requests.get(todos_url)

users_data = json.loads(responses[0].text)
tasks_data = json.loads(responses[1].text)


def api_availability(*urls):
    # check connection to urls
    for url in urls:
        try:
            requests.get(url)
            print(f"Successfully connected to {url}")
        except requests.exceptions.ConnectionError:
            print(f"An error occured during connection to {url}")
            raise SystemExit


def short_name(task_name):
    if len(task_name) > 50:
        return f"{task_name[:50]}...\n"
    else:
        return f"{task_name}\n"


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


class User():
    def __init__(self, users_data, tasks_data):
        self.id = users_data['id']
        self.name = users_data['name']
        self.username = users_data['username']
        self.email = users_data['email']
        self.phone = users_data['phone']
        self.website = users_data['website']
        self.company_name = users_data['company']['name']
        self.completed_tasks = []
        self.unfinished_tasks = []

        for task in tasks_data:
            if self.id == task['userId']:
                if task['completed']:
                    self.completed_tasks.append(short_name(task['title']))
                else:
                    self.unfinished_tasks.append(short_name(task['title']))

        if not self.completed_tasks:
            self.completed_tasks.append(f"{self.name} has no completed tasks")
        if not self.unfinished_tasks:
            self.unfinished_tasks .append(f"{self.name} has no unfinished tasks")

    def report_creation(self):
        api_availability(users_url, todos_url)  # check connection to urls
        self.report = f"{self.name}.txt"
        if os.path.exists(self.report):  # if file exist, creating a new one
            change_time = os.path.getmtime(self.report)
            last_change = time.strftime('%Y-%m-%dT%H-%m-%S', time.localtime(change_time))
            os.rename(self.report, f'{self.report[:-4]}_{last_change}.txt')

        self.user_info = f"""{self.name} <{self.email}>
Time of creation: {time.strftime('%Y-%m-%d %H:%m', time.localtime())}
{self.company_name}\n
Completed tasks:\n
{"".join(self.completed_tasks)}
Unfinished tasks:\n
{"".join(self.unfinished_tasks)} """
        try:  # with out context manager
            file = open(self.report_name, "w", encoding="utf-8")
            file.write(self.user_info)
            file.close()
            print(f"Report for {self.name} created")
        except IOError:
            print("IOError")
            path = os.path.join(os.path.abspath(os.path.dirname(__file__)), user_file_name)
            os.remove(path)

if __name__ == "__main__":
    create_folder("oop")
    for user in users_data:
        User(user, tasks_data).report_creation()
