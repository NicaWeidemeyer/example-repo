# ========= Importing external modules =========
from datetime import datetime

# ========= Functions =========
def load_users():
    """
    Reads from user.txt file, creates dictionary with key=username
    and value=password pair and returns users
    """
    users = {}
    try:  # Defensive programming in case file doesn't exist
        with open("user.txt", "r", encoding="utf-8") as file:
            for line in file:
                username, password = line.strip().split(", ")
                users[username] = password
    except FileNotFoundError:
        print("Error. user.txt file could not be found.\n")
    return users


def login(users):
    """
    Continuously asks user to log in, validates username and
    password, only exits when both correct, returns username
    """
    while True:
        username = input("Enter your username: ")  # Case-sensitive
        password = input("Enter your password: ")  # Case-sensitive
        if username not in users:
            print("Username not found. Please try again.\n")
        elif users[username] != password:
            print("Incorrect password. Please try again.\n")
        else:
            print("Login was successful!\n")
            return username
        

def reg_user(users):
    """
    Registers a new user, makes sure username does not already
    exist, confirms the password choice, appends new user
    information to user.txt, updates users dictionary
    """
    while True:  # Username validation loop
        new_username = input("Please enter a new username: ")
        if new_username in users:
            print("This username already exists. "
                  "Please choose another one.\n")
            continue
        new_password = input("Please enter a new password: ")
        confirm_password = input("Please confirm the password: ")
        if new_password != confirm_password:  # Typo checking
            print("Passwords do not match. Please try again.\n")
            continue
        # If passwords match
        with open("user.txt", "a", encoding="utf-8") as file:
            file.write(f"\n{new_username}, {new_password}")
        users[new_username] = new_password  # Update dictionary
        print("New user was registered successfully!\n")
        break


def add_task(users):
    """
    Allows user to add a new task into the system, validates that
    assigned user exists and due date format, sets current date
    as date assigned, sets completion "No" as default
    """
    while True:  # User validation loop
        task_user = input(
            "Enter the username the task is assigned to: "
            )
        if task_user in users:
            break
        else:
            print(
                "User does not exist. Please enter a valid username.\n"
                )
    task_title = input("Enter the title of the task: ")
    task_description = input("Enter the task description: ")
    while True:  # Date validation loop
        task_due_date = input(
            "Enter the due date of the task (e.g. 22 Dec 2025): "
            )
        try:
            datetime.strptime(task_due_date, "%d %b %Y") # str to object
            break  # Exit loop if date format is valid
        except ValueError:
            print("Invalid date format. Please use e.g. 22 Dec 2025.\n")
    task_date_assigned = datetime.now().strftime("%d %b %Y")  # obj to str
    task_completed = "No"
    with open("tasks.txt", "a", encoding="utf-8") as file:
        file.write(
            f"{task_user}, {task_title}, {task_description}, "
            f"{task_date_assigned}, {task_due_date}, {task_completed}\n"
        )
    print("The new task was added successfully!\n")


def view_all():
    """
    Checks whether tasks and tasks.txt exist, reads all tasks
    from tasks.txt, displays them in an easy-to-read format
    """
    print("--------- ALL TASKS ---------\n")  # Outside loop
    try:  # Defensive programming in case file doesn't exist
        with open("tasks.txt", "r", encoding="utf-8") as file:
            found = False  # Flag to track if any tasks exist
            for line in file:
                task = line.strip().split(", ")
                found = True  # Update flag
                print(f"Assigned to: {task[0]}")
                print(f"Task title: {task[1]}")
                print(f"Task description: {task[2]}")
                print(f"Date assigned: {task[3]}")
                print(f"Due date: {task[4]}")
                print(f"Task completed: {task[5]}\n")
        if not found:
            print("No tasks were found.\n")  # Flag stays False
    except FileNotFoundError:
        print("No tasks were found. tasks.txt does not exist yet.\n")


def view_mine(logged_in_user, users):
    """
    Checks whether tasks and tasks.txt exist, reads all tasks
    from tasks.txt, filters tasks for the logged-in user,
    displays them in an easy-to-read and numbered format,
    lets user mark complete and edit tasks
    """  
    try:  # Defensive programming in case file doesn't exist
        # Read all tasks from tasks.txt
        with open("tasks.txt", "r", encoding="utf-8") as file:
            tasks = [line.strip().split(", ") for line in file]

            # Create indexed list of logged-in user tasks
            user_tasks = []
            for task_index, task in enumerate(tasks):
                if task[0] == logged_in_user:
                    user_tasks.append((task_index, task))
            if not user_tasks:
                print("You have no tasks assigned to you.\n")
                return
            
            # Display logged-in user tasks with numbers
            print("--------- MY TASKS ---------\n")  # Outside loop
            task_number = 1  # Start counting from 1
            for task_index, task in user_tasks:
                print(f"Task number: {task_number}")
                print(f"Assigned to: {task[0]}")
                print(f"Task title: {task[1]}")
                print(f"Task description: {task[2]}")
                print(f"Date assigned: {task[3]}")
                print(f"Due date: {task[4]}")
                print(f"Task completed: {task[5]}\n")
                task_number += 1  # Move to next number

            # Recursive function to get a valid task number
            def get_valid_task_number():
                try:
                    user_choice = int(input(
                        "Enter the task number to select task "
                        "or -1 to return to menu: "
                    ))
                except ValueError:  # Non-integer inputs
                    print("Invalid input. Please enter a number.\n")
                    return get_valid_task_number()  # Recursive call
                if user_choice == -1:  # Base case/stops recursion
                    return -1
                elif 1 <= user_choice <= len(user_tasks):  # Valid inputs
                    return user_choice
                else:  # Inputs outside range
                    print("Invalid task number. Please try again.\n")
                    return get_valid_task_number()  # Recursive case
            
            # Get user_choice using the recursive function
            user_choice = get_valid_task_number()
            if user_choice == -1:
                return
            
            # Get the selected task
            task_index = user_tasks[user_choice - 1][0]
            selected_task = tasks[task_index]
            if selected_task[5] == "Yes":
                print("This task was completed and cannot be edited.\n")
                return
            
            # Let user choose to mark complete or edit task
            user_action = input(
                """Please select one of the following options:
            c - mark task as complete
            e - edit task
            : """
            ).lower()  # Case-insensitive

            # Mark task complete
            if user_action == "c":
                selected_task[5] = "Yes"
                print("Task was marked as complete!\n")

            # Edit task (username)
            elif user_action == "e":
                edit_user = input(
                    "Would you like to edit the assigned user? Yes/No: "
                ).lower()  # Case-insensitive
                if edit_user == "yes":
                    new_user = input("Enter new username: ")
                    if new_user in users:  # Validate new_user
                        selected_task[0] = new_user
                    else:
                        print(
                            "User does not exist and username "
                            "could not be changed.\n"
                        )
                
                # Edit task (due date)
                edit_date = input(
                    "Would you like to edit the due date? Yes/No: "
                ).lower()  # Case-insensitive
                if edit_date == "yes":
                    while True:
                        new_date = input(
                            "Enter a new due date (e.g. 22 Dec 2025): "
                        )
                        try:
                            # str to obj
                            datetime.strptime(new_date, "%d %b %Y")
                            selected_task[4] = new_date
                            break
                        except ValueError:
                            print(
                                "Invalid date format. "
                                "Please use e.g. 22 Dec 2025.\n"
                            )
                print("Task was successfully updated!\n")

            else:
                print("Invalid option. Please try again.\n")
                return
            
            # Save into/rewrite task.txt
            with open ("tasks.txt", "w", encoding="utf-8") as file:
                for task in tasks:
                    file.write(", ".join(task) + "\n")
    
    except FileNotFoundError:
        print("No tasks were found. tasks.txt does not exist yet.\n")


def view_completed():
    """
    Checks whether tasks and tasks.txt exist, reads all tasks
    from tasks.txt, filters tasks for completion "Yes",
    displays them in an easy-to-read format
    """  
    try:  # Defensive programming in case file doesn't exist
        with open("tasks.txt", "r", encoding="utf-8") as file:
            print("--------- COMPLETED TASKS ---------\n")
            found = False  # Flag to track if completed tasks exist
            for line in file:
                task = line.strip().split(", ")
                if task[5] == "Yes":
                    found = True  # Update flag
                    print(f"Assigned to: {task[0]}")
                    print(f"Task title: {task[1]}")
                    print(f"Task description: {task[2]}")
                    print(f"Date assigned: {task[3]}")
                    print(f"Due date: {task[4]}")
                    print(f"Task completed: {task[5]}\n")
        if not found:
            print("No completed tasks were found.\n")  # Flag stays False
    except FileNotFoundError:
        print("No completed tasks were found. "
              "tasks.txt does not exist yet.\n")


def delete_task():
    """
    Asks for title of task to be deleted, reads all tasks from
    tasks.txt, filters for title, rewrites file without deleted task
    """
    task_title = input(
        "Enter the title of the task you want to delete: "
        )
    remaining_tasks = []  # List to store remaining tasks
    deleted = False  # Flag to track whether task was removed
    try:  # Defensive programming in case file doesn't exist
        with open("tasks.txt", "r", encoding="utf-8") as file:
            for line in file:
                task = line.strip().split(", ")  # List to find title
                if task[1] != task_title:
                    remaining_tasks.append(line.rstrip("\n"))  # Keep task
                else:
                    deleted = True  # Update flag
        
        # Rewrite file
        with open("tasks.txt", "w", encoding="utf-8") as file:
            for task_line in remaining_tasks:  # String for task line
                file.write(task_line + "\n")  # Add newline
        if deleted:
            print("Task was successfully deleted.\n")
        else:
            print("Task was not found.\n")
    except FileNotFoundError:
        print("Tasks file does not exist yet.\n")


def gen_reports():
    """
    Creates task_overview.txt and user_overview.txt, with statistics
    about tasks created in task_manager.py
    """
    # Load users and tasks
    try:  # Defensive programming in case file doesn't exist
        with open("user.txt", "r", encoding="utf-8") as file:
            users = [line.strip().split(", ")[0] for line in file]
        with open("tasks.txt", "r", encoding="utf-8") as file:
            tasks = [line.strip().split(", ") for line in file]
    except FileNotFoundError:
        print("Files were not found and reports cannot be generated.\n")
        return
    
    # Variables/counters for task statistics
    total_tasks = len(tasks)
    completed_tasks = 0
    incomplete_tasks = 0
    overdue_tasks = 0
    today = datetime.today()

    # Task statistics calculations
    for task in tasks:
        completed = task[5]
        due_date = datetime.strptime(task[4], "%d %b %Y")  # str to obj
        if completed == "Yes":
            completed_tasks += 1
        else:
            incomplete_tasks += 1
            if due_date < today:
                overdue_tasks += 1
    
    # Incomplete and overdue percentages
    if total_tasks > 0:  # Cannot divide by 0/no existing tasks
        incomplete_perc = (incomplete_tasks / total_tasks) * 100
    else:
        incomplete_perc = 0
    if total_tasks > 0:  # Cannot divide by 0/no existing tasks
        overdue_perc = (overdue_tasks / total_tasks) * 100
    else:
        overdue_perc = 0

    # Write task_overview.txt
    with open("task_overview.txt", "w", encoding="utf-8") as file:
        file.write(f"Total tasks: {total_tasks}\n")
        file.write(f"Completed tasks: {completed_tasks}\n")
        file.write(f"Incomplete tasks: {incomplete_tasks}\n")
        file.write(f"Overdue tasks: {overdue_tasks}\n")
        file.write(
            f"Share of incomplete tasks: {incomplete_perc:.2f}%\n"
            )
        file.write(
            f"Share of overdue tasks: {overdue_perc:.2f}%\n"
        )
    
    # Start user_overview.txt file
    with open("user_overview.txt", "w", encoding="utf-8") as file:
        file.write(f"Total users: {len(users)}\n")
        file.write(f"Total tasks: {total_tasks}\n")

        # Variables/counters for user statistics
        for user in users:
            user_tasks = 0
            user_completed = 0
            user_incomplete = 0
            user_overdue = 0

            # Loop through tasks and count tasks for each user
            for task in tasks:
                if task[0] == user:
                    user_tasks += 1
                    # str to obj
                    due_date = datetime.strptime(task[4], "%d %b %Y")
                    if task[5] == "Yes":
                        user_completed += 1
                    else:
                        user_incomplete += 1
                        if due_date < today:
                            user_overdue += 1
            
            # Incomplete and overdue percentages
            if total_tasks > 0:  # Cannot divide by 0/no existing tasks
                perc_assigned = (user_tasks / total_tasks) * 100
            else:
                perc_assigned = 0
            if user_tasks > 0:  # Cannot divide by 0/no existing tasks
                perc_completed = (user_completed / user_tasks) * 100
                perc_incomplete = (user_incomplete / user_tasks) * 100
                perc_overdue = (user_overdue / user_tasks) * 100
            else:
                perc_completed = 0
                perc_incomplete = 0
                perc_overdue = 0

            # Continue writing user_overview.txt
            file.write(f"\nUser: {user}\n")
            file.write(f"Number of tasks assigned: {user_tasks}\n")
            file.write(
                f"Share of tasks assigned: {perc_assigned:.2f}%\n"
                )
            file.write(
                f"Share of completed tasks: {perc_completed:.2f}%\n"
                )
            file.write(
                f"Share of incomplete tasks: {perc_incomplete:.2f}%\n"
                )
            file.write(
                f"Share of overdue tasks: {perc_overdue:.2f}%\n"
                )
    
    print("Reports were generated successfully!")


def display_statistics():
    """
    Displays task and user statistics from tasks_overview.txt
    and user_overview.txt, generates the reports if needed,
    prints them in an easy-to-read format
    """
    try:  # Defensive programming in case files don#t exist
        with open("task_overview.txt", "r", encoding="utf-8") as file:
            task_statistics = file.read()
        with open("user_overview.txt", "r") as file:
            user_statistics = file.read()
    except FileNotFoundError:
        gen_reports()
        with open("task_overview.txt", "r", encoding="utf-8") as file:
            task_statistics = file.read()
        with open("user_overview.txt", "r", encoding="utf-8") as file:
            user_statistics = file.read()
    
    # Print reports in an easy-to-read format
    print("--------- TASK OVERVIEW ---------\n")
    print(task_statistics)
    print("\n--------- USER OVERVIEW ---------\n")
    print(user_statistics)


# ========= Login Section =========
users = load_users()
logged_in_user = login(users)


# ========= Menu Loop =========
while True:
    # Admin menu
    if logged_in_user == "admin":
        menu = input(
            """Please select one of the following options:
        r - register a user
        a - add task
        va - view all tasks
        vm - view my tasks
        vc - view completed tasks
        del - delete tasks
        ds - display statistics
        gr - generate reports
        e - exit
        : """
        ).lower()  # Case-insensitive

    # Normal user menu
    else:
        menu = input(
            """Please select one of the following options:
        a - add task
        va - view all tasks
        vm - view my tasks
        e - exit
        : """
        ).lower()  # Case-insensitive

    # All possible admin or user choices
    if menu == "r":  # Only admin
        if logged_in_user == "admin":
            reg_user(users)
        else:
            print("Only admin is allowed to register new users.\n")
    elif menu == "a":
        add_task(users)
    elif menu == "va":
        view_all()
    elif menu == "vm":
        view_mine(logged_in_user, users)
    elif menu == "vc":
        view_completed()
    elif menu == "del":
        delete_task()
    elif menu == "ds":  # Only admin
        if logged_in_user == "admin":
            display_statistics()
        else:
            print("Only admin is allowed to view statistics.\n")
    elif menu == "gr":  # Only admin
        if logged_in_user == "admin":
            gen_reports()
        else:
            print("Only admin can generate reports.\n")
    elif menu == "e":
        print("Thank you for using task manager. Goodbye!")
        exit()
    else:
        print("Invalid input. Please try again.\n")