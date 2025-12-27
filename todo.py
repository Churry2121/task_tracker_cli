# This application should run from the command line interface (CLI)
# Add, update, and delete tasks
# Mark a task as in progress or done
# List all tasks that are done, not done, and in progress.
import json, os, argparse

json_file = 'entries.json'

def load_tasks(): #load/open file to be read
    if os.path.exists(json_file):
        with open(json_file, 'r') as f:
            return json.load(f)
    else: 
        return [] #if file does not exist return an empty list

def add_tasks(name, desc, progress):
    new_entry = {
        'name': name,
        'description': desc,
        'progress': progress
    }

    #1. read the existing file
    data = load_tasks()
    data.append(new_entry) #add the new task

    with open(json_file, 'w') as file: #'a' adds to the end of the file while erasing what's already there, thus use 'w'. Creates a new file if file doesn't exist
        # Use json.dump() to serialize the Python dictionary to JSON format and write to the file
        json.dump(data, file, indent=4)
    print(f"Added task: {name}")

def delete_task(name_to_delete):
    data = load_tasks()

    # Find and remove the task by name
    original_length = len(data)

    #rebuild data keeping only tasks that don't match the name to delete
    data = [task for task in data if task['name'] != name_to_delete]
    
    # recreate the file without name_to_delete
    if len(data) < original_length:
        with open(json_file, 'w') as file:
            json.dump(data, file, indent=4)
        print(f"Deleted task: {name_to_delete}")
    else:
        print(f"Warning: Task '{name_to_delete}' not found.")

def update_tasks(name_to_update):
    data = load_tasks()
    task_found = False

    for task in data:
        if task['name'] == name_to_update:
            task_found = True
            new_name = input("Enter new name for the task (optional): ")
            new_desc = input("Enter new description of the task (optional): ")
            new_progress = input("Enter the progress of the task (optional): ")

            if new_name:
                task['name'] = new_name
            if new_desc:
                task['description'] = new_desc
            if new_progress:
                task['progress'] = new_progress

            break
    
    if task_found:
        with open(json_file, 'w') as file:
            json.dump(data, file, indent=4) #turning the new data (Python object) into JSON format and writes it directly into the file.
        print('Task updated successfully')
    else:
        print(f'Warning: Task {name_to_update} was not found')
    
def list_tasks():
    data = load_tasks()

    if not data:
        print("No tasks found.")
        return

    print('\n==========Tasks==========')
    for i, task in enumerate(data, 1): #enumerate(object, start_index=1)
        print(f"{i}. {task['name']}")
        print(f"   Description: {task['description']}")
        print(f"   Progress: {task['progress']}")
        print()

def list_done_tasks():
    data = load_tasks()

    data = [task for task in data if task['progress'] == 'done']

    print('\n=======Tasks that are done=======')
    for i, task in enumerate(data, 1):
        print(f"{i}. {task['name']}")
        print(f"   Description: {task['description']}")
        print(f"   Progress: {task['progress']}")
        print()

def list_not_done_tasks():
    data = load_tasks()

    data = [task for task in data if task['progress'] == 'not done']

    print('\n=====Tasks that are not done=====')
    for i, task in enumerate(data, 1):
        print(f"{i}. {task['name']}")
        print(f"   Description: {task['description']}")
        print(f"   Progress: {task['progress']}")
        print()

def list_in_progress_tasks():
    data = load_tasks()

    data = [task for task in data if task['progress'] == 'in progress']

    print('\n====Tasks that are in progress====')
    for i, task in enumerate(data, 1):
        print(f"{i}. {task['name']}")
        print(f"   Description: {task['description']}")
        print(f"   Progress: {task['progress']}")
        print()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--name', help="task's name")
    parser.add_argument('-d', '--description', help='add a description for your task')
    parser.add_argument('-p', '--progress', help='in progress || done || not done')
    parser.add_argument('-de', '--delete', help='type in the name of the task you want to delete')
    parser.add_argument('-l', '--list', action='store_true', help='list all your tasks')
    parser.add_argument('-do', '--done', action='store_true', help='type in -l and -do to list all done tasks')
    parser.add_argument('-ndo', '--notDone', action='store_true', help='type in -l and -ndo to list all tasks that are not done')
    parser.add_argument('-inp', '--inProgress', action='store_true', help='type in -l and -inp to list all tasks that are in progress')
    parser.add_argument('-u', '--update')
    
    args = parser.parse_args()

    if args.name:
        if not args.description or not args.progress:
            print("Error: --name requires both --description and --progress")
        else:
            add_tasks(args.name, args.description, args.progress)
    elif args.delete:
        delete_task(args.delete)
    elif args.update:
        update_tasks(args.update)
    elif args.list:
        if args.done:
            list_done_tasks()
        elif args.notDone:
            list_not_done_tasks()
        elif args.inProgress:
            list_in_progress_tasks()
        else:
            list_tasks()
    else:
        print("No action specified. Use -h for help.")
    