#! /usr/bin/python3

from datetime import datetime, timedelta
import json
import os
from pathlib import Path

class Journal:
    __BASE_DIR = Path(__file__).parent

    def __init__(self) -> None:
        with open(self.__BASE_DIR / 'tasks.json', 'a+') as f:
            pass
        with open(self.__BASE_DIR / 'tasks.json') as f:
            self.tasks = json.load(f)

    def reload_json(self):
        with open(self.__BASE_DIR / 'tasks.json') as f:
            self.tasks = json.load(f)

    def redump_json(self):
        with open(self.__BASE_DIR / 'tasks.json', 'w') as f:
            json.dump(self.tasks, f, indent=2)

    def add_task(self, task_name, dtime=None):
        if dtime == None:
            dtime = datetime.now()
        self.tasks.append([str(dtime), task_name])
        self.redump_json()

    def print_todays_tasks(self):
        print("Time\t\tTime Took\tTask")
        print("````\t\t`````````\t````")
        for i in range(len(self.tasks)):
            task = self.tasks[i]
            task_time = datetime.fromisoformat(task[0])
            if i == len(self.tasks)-1:
                time_took = "Incomplete"
            else:
                next_task = self.tasks[i+1]
                next_task_time = datetime.fromisoformat(next_task[0])
                time_took = next_task_time - task_time
                time_took = f"{int(time_took.total_seconds()//60):02d} minutes"

            print(f"{task_time.strftime('%I:%M:%S %p')}\t{time_took}\t{task[1]}")


journal = Journal()
prompt_num = 0
while True:
    try:
        os.system('clear')
        print("Press Enter to change prompt. CTRL+C to exit\n")
        journal.print_todays_tasks()
        print()
        if prompt_num == 0:
            ans = input("Enter a new task: ")
            if ans == '':
                prompt_num = 1
                continue
            journal.add_task(ans)
        elif prompt_num == 1:
            ans = input("Edit previous task? [Y/n] ")
            prompt_num = 2
            if ans.lower() == 'y':
                time_for_last_task = int(input(
                    "Time spend in last recorded task(in minutes): "))
                dtime_for_next_task = datetime.fromisoformat(journal.tasks[-1][0]) + timedelta(minutes=time_for_last_task)
                print(dtime_for_next_task)
                while True:
                    time_remaining = divmod((datetime.now() - dtime_for_next_task).total_seconds(), 60)
                    print(f"Time remaining: {int(time_remaining[0])}min {int(time_remaining[1])}s")
                    new_task = input("Task name: ")
                    time_required = input("Time required(Press Enter for rest of time): ")
                    journal.add_task(new_task, dtime_for_next_task)
                    if time_required == '': break
                    dtime_for_next_task += timedelta(minutes=int(time_required))
        elif prompt_num == 2:
            ans = input("Delete Journal? [Y/n]")
            prompt_num = 0
            if ans == 'y':
                journal.tasks = []
                journal.redump_json()
    except KeyboardInterrupt:
        print("\nExiting Journal...")
        exit()