import tkinter as tk
#help(tk)

def view_task( tasks):
    if tasks:
        print("Here are your tasks:")
        for task in tasks:
            print(task,"")
    else:
        print("No tasks:")


def add_task(tasks):
    user_task = input("Please give a task to add: ")
    tasks.append(user_task)

def delete_task(tasks):
    user_task = input("Please give a task to delete: ")
    if user_task in tasks:
        tasks.remove(user_task)
    else:
        print("No such task:")





def main():
    tasks = []
    print("Welcome to you To-Do-ListYou have the choice of the following options:")
    print("0. View Task")
    print("1. Add Task")
    print("2. Delete Task")
    print("3. Options")
    print("4. Exit")

    while True:

        choice = input("Enter your choice: ")
        if choice == "0":
            view_task(tasks)
        elif choice == "1":
            add_task(tasks)
        elif choice == "2":
            delete_task(tasks)
        elif choice == "3":
            print("0. View Task")
            print("1. Add Task")
            print("2. Delete Task")
            print("3. Options")
            print("4. Exit")
        elif choice == "4":
            print("Thank you for using To-Do-List. Bye")
            break

    '''root = tk.Tk()
    root.title("To-Do List Application")

    task_listbox = tk.Listbox(root, height=10, width=50)
    task_listbox.pack(pady=10)

    task_entry = tk.Entry(root, width=52)
    task_entry.pack(pady=5)

    add_button = tk.Button(root, text="Add Task", width=48, command=add_task)
    add_button.pack(pady=5)

    delete_button = tk.Button(root, text="Delete Task", width=48, command=delete_task)
    delete_button.pack(pady=5)
    root.mainloop()'''
if __name__ == "__main__":
    main()