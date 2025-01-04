import os
import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog
from datetime import datetime


def add_task():
    task = task_entry.get()
    if task != "":
        # Create a new frame to hold the task and its checkbox
        task_frame = tk.Frame(task_listbox)
        task_frame.pack(fill="x", pady=2)

        # Add a checkbutton for the task
        var = tk.BooleanVar()  # Variable to track the checkbox state
        checkbutton = tk.Checkbutton(task_frame, text=task, variable=var)
        checkbutton.pack(side="left", padx=5)

        # Store the task frame and its variable for future use
        tasks.append((task_frame, var))

        task_entry.delete(0, tk.END)
    else:
        pass  # Optionally show a message if the entry is empty


def delete_task():
    # Remove completed tasks
    once = True
    for task_frame, var in tasks[:]:  # Iterate over a copy of the task list
        if var.get():  # Check if the task is marked as completed
            task_text = task_frame.winfo_children()[0].cget("text")  # Get the task name
            if once:
                messagebox.showinfo("Congratulations", f"You have done a great job, and are on the right path\nYou completed: '{task_text}'")
                once = False

            task_frame.destroy()  # Remove the frame
            tasks.remove((task_frame, var))  # Remove from the task list


def save_task():
    task = task_entry.get()  # Get the task entered by the user

    # Ensure the task is not empty
    if task != "":
        # Ask the user to choose a directory to save the file
        folder = filedialog.askdirectory(title="Select Folder to Save Task")

        if folder:  # If the user selects a folder
            # Ask the user to input a custom file name
            file_name = simpledialog.askstring("Input", "Enter file name:", parent=root)

            if file_name:  # If the user provides a file name
                # Define the full file path with the user input file name
                file_path = os.path.join(folder, f"{file_name}.txt")

                # Get the current date and time for timestamp
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                # Open the file in append mode
                with open(file_path, 'a') as file:
                    # Write the task with the timestamp
                    file.write(f"[{timestamp}] Completed: {task}\n")

                print(f"Task saved to {file_path}")  # Optional confirmation for testing
            else:
                print("No file name provided.")
        else:
            print("No folder selected.")
    else:
        print("Task cannot be empty.")


def save_all_tasks():
    # Get all tasks from the tasks list (each task is stored as a tuple (task_frame, var))
    tasks_text = [task_frame.winfo_children()[0].cget("text") for task_frame, var in tasks if task_frame.winfo_children()]

    if tasks_text:  # Only save if there are tasks
        # Ask the user to choose a directory to save the file
        folder = filedialog.askdirectory(title="Select Folder to Save Tasks")

        if folder:  # If the user selects a folder
            # Define the default file name
            file_name = "tasks_list.txt"  # No need to ask for file name, this is the default

            # Define the full file path
            file_path = os.path.join(folder, file_name)

            # Get the current date and time for timestamp (optional)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Open the file in write mode
            with open(file_path, 'w') as file:
                # Write all tasks to the file with timestamp
                for task in tasks_text:
                    file.write(f"[{timestamp}] Task: {task}\n")

            print(f"All tasks saved to {file_path}")  # Optional confirmation for testing
        else:
            print("No folder selected.")
    else:
        print("No tasks to save.")

# Create the main window
root = tk.Tk()
root.title("To-Do List with Checkboxes")

# List to store tasks and their associated variables
tasks = []

# Input field and buttons
task_entry = tk.Entry(root, width=40)
task_entry.pack(pady=5)


add_button = tk.Button(root, text="Add Task", command=add_task, font=("Arial", 16, "bold"), fg="green", bg="red", width=25)
add_button.pack(pady=5)

"""img = tk.PhotoImage(file="trash.png")  # Ensure the file exists
resized_img = img.resize((20, 20))  # Set to desired size
img = ImageTk.PhotoImage(resized_img)"""

delete_button = tk.Button(root, text="Delete Completed Tasks",font=("Arial", 16, "bold"),command=delete_task, width=30,bg="blue", fg="red")
delete_button.pack(pady=5)

save_button = tk.Button(root, text="Save Task to File", font=("Arial", 16, "bold"),command=save_task, width=35)
save_button.pack(pady=5)

save_button = tk.Button(root, text="Save All Completed Tasks to File", font=("Arial", 16, "bold"),command=save_all_tasks, width=35)
save_button.pack(pady=5)


# Frame to hold tasks
task_listbox = tk.Listbox(root, height=10, width=50)
task_listbox.pack(pady=10)

# Run the application
root.mainloop()