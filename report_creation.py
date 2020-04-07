from datetime import datetime
import json, requests
import os, time, pprint


users_url = "https://jsonplaceholder.typicode.com/users"
todos_url = "https://jsonplaceholder.typicode.com/todos"
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


def shorten_task_name(task_name):
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

create_folder("oop")


class User():
    def __init__(self, users_data):
        self.id = users_data['id']
        self.name = users_data['name']
        self.username = users_data['username']
        self.email = users_data['email']
        self.phone = users_data['phone']
        self.website = users_data['website']
        self.company_name = users_data['company']['name']
        
    def get_tasks(self, tasks_data):
        self.completed_tasks = []
        self.unfinished_tasks = []
        for task in tasks_data:
            if self.user_id == task['userId']:
                if task['completed']:
                    self.completed_tasks.append(shorten_task_name(task['title']))
                else:
                    self.unfinished_tasks.append(shorten_task_name(task['title']))
        

    def rename_old_txt_file(file_name):
        # if file exist, creating a new one, rename the old file
        if os.path.exists(file_name):
            change_time = os.path.getmtime(file_name)
            last_change = time.strftime('%Y-%m-%dT%H-%m-%S', time.localtime(change_time))
            os.rename(file_name, f'{file_name[:-4]}_{last_change}.txt')

       
    def report_creation():
        self.report_name = f"{self.user_name}.txt"
        rename_old_txt_file(self.report_name)  # if file exist, creating a new one
        self.user_info = f"""{self.name} <{self.email}> 
                                        {time.strftime('%Y-%m-%d %H:%m', time.localtime())}\n
                                        {self.company_name}\n\n
                                        Completed tasks:\n
                                        {"".join(self.completed_tasks)}
                                        \nUnfinished tasks:\n
                                        {"".join(self.unfinished_tasks)}
                                        """
        try:  # with out context manager
            file = open(self.report_name, "w", encoding="utf-8")
            file.write(self.user_info)
            file.close()
            print(f"Report for {self.name} created")
        except IOError:
            print("IOError")
            path = os.path.join(os.path.abspath(os.path.dirname(__file__)), user_file_name)
            os.remove(path)
