from datetime import datetime
import os
import time
import json
import requests


users_url = "https://json.medrating.org/users"
todos_url = "https://json.medrating.org/todos"
folder_name = "reports"

responses = requests.get(users_url), requests.get(todos_url)

users_data = json.loads(responses[0].text)
tasks_data = json.loads(responses[1].text)


class ReportFunctions():
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
            print(f"Folder ({folder_name}) already exist in ", parent_dir)
        os.chdir(path)

    def create_report(self: "user"):
        ReportFunctions.api_availability(users_url, todos_url)
        self.report = f"{self.name}.txt"
        if os.path.exists(self.report):  # if file exist, creating a new one
            change_time = os.path.getmtime(self.report)
            last_change = time.strftime('%Y-%m-%dT%H-%m-%S', time.localtime(change_time))
            os.rename(self.report, f'{self.report[:-4]}_{last_change}.txt')
        with open(self.report, "w", encoding="utf-8") as file:
                file.write(self.user_info)
                print(f"Report for {self.name} created")


class ReportStructure(ReportFunctions):
    # collecting data from JSON file
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
                    self.completed_tasks.append(ReportFunctions.short_name(task['title']))
                else:
                    self.unfinished_tasks.append(ReportFunctions.short_name(task['title']))

        if not self.completed_tasks:
            self.completed_tasks.append(f"{self.name} has no completed tasks")
        if not self.unfinished_tasks:
            self.unfinished_tasks .append(f"{self.name} has no unfinished tasks")

        self.user_info = (
            f"{self.name} <{self.email}> "
            f"{time.strftime('%Y-%m-%d %H:%m', time.localtime())}"
            f"\n{self.company_name}\n"
            f"\nCompleted tasks:\n"
            f"{''.join(self.completed_tasks)}"
            f"\nUnfinished tasks:\n"
            f"{''.join(self.unfinished_tasks)}"
        )


if __name__ == "__main__":
    ReportFunctions.create_folder("reports")
    for user in users_data:
        ReportStructure(user, tasks_data).create_report()
