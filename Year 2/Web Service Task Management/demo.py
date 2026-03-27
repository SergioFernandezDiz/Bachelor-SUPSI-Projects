from task_manager_library import *
from colorama import Fore, Style
from datetime import datetime


def choose_section():
    print("📂 What would you like to manage?")
    print(f"1. 👤 {Fore.BLUE}{Style.BRIGHT}Users{Style.RESET_ALL}")
    print(f"2. 📝 {Fore.BLUE}{Style.BRIGHT}Tasks{Style.RESET_ALL}")
    print(f"3. 🏗️ {Fore.BLUE}{Style.BRIGHT}Projects{Style.RESET_ALL}")
    print(f"0. ❎ {Fore.RED}{Style.BRIGHT}Exit{Style.RESET_ALL}")
    return input("Choice: ").strip()

def select_user():
    while True:
        nickname = input("🔐 Enter your nickname: ").strip()
        users = get_users()
        for user in users:
            if user.username == nickname:
                print(f"\n✅ Welcome {user.name} {user.last_name}!\n")
                return user
        print("❌ User not found. Please try again.\n")

def show_shared_users(current_user):
    print("\n👥 Shared Tasks - Users in common with you:")

    tasks = get_tasks_by_user(current_user)
    shared_users = []

    for task in tasks:
        users = get_users_by_task(task)
        for user in users:
            if user.id != current_user.id:
                found = False
                for u in shared_users:
                    if u.id == user.id:
                        found = True
                        break
                if not found:
                    shared_users.append(user)

    if shared_users:
        print("✅ Users who share tasks with you:")
        for user in shared_users:
            print(f"   - {user.name} {user.last_name} (ID: {user.id})")
    else:
        print(f"{Fore.YELLOW}⚠️ No users share any task with you.{Style.RESET_ALL}")

def user_actions_menu(current_user):
    while True:
        print("\n👤 User Menu:")
        print(f"1. 🔗 {Fore.BLUE}{Style.BRIGHT}Show users who share tasks with you{Style.RESET_ALL}")
        print(f"0. 🔙 {Fore.YELLOW}{Style.BRIGHT} Back to main menu{Style.RESET_ALL}")

        choice = input("Choice: ").strip()

        if choice == "1":
            show_shared_users(current_user)
        elif choice == "0":
            break
        else:
            print(f"❌ {Fore.RED}Invalid choice.\n{Style.RESET_ALL}")

def project_action_menu(current_user):
    while True:
        print("\n🏗️ Project Menu:")
        print(f"1. 📋 {Fore.BLUE}{Style.BRIGHT}List all projects{Style.RESET_ALL}")
        print(f"2. 🔍 {Fore.BLUE}{Style.BRIGHT}View project details{Style.RESET_ALL}")
        print(f"3. 📊 {Fore.BLUE}{Style.BRIGHT}Show project statistics{Style.RESET_ALL}")
        print(f"4. 🗑️ {Fore.BLUE}Delete a project{Style.RESET_ALL}")
        print(f"5. ➕ {Fore.BLUE}{Style.BRIGHT}Create new project{Style.RESET_ALL}")
        print(f"6. ✏️ {Fore.BLUE}{Style.BRIGHT}Update a project{Style.RESET_ALL}")
        print(f"7. 📈 {Fore.BLUE}Show Gantt chart for a project{Style.RESET_ALL}")
        print(f"0. 🔙 {Fore.YELLOW}{Style.BRIGHT}Back to main menu{Style.RESET_ALL}")

        choice = input("Choice: ").strip()

        if choice == "1":
            projects = get_project_by_user(current_user)
            if not projects:
                print(f"{Fore.YELLOW}⚠️ You are not assigned to any projects.{Style.RESET_ALL}")
            else:
                print(f"{Fore.GREEN}📁 Your Projects:{Style.RESET_ALL}")
                for p in projects:
                    print(f" - [{p.id}] {p.name}-> role ({p.user_role})")

        elif choice == "2":
            while True:
                try:
                    project_id = int(input("Enter project ID to show statistics: ").strip())
                except ValueError:
                    print(f"{Fore.RED}❌ Project ID must be an integer.{Style.RESET_ALL}")
                    continue

                try:
                    project = get_project_by_id(project_id)
                except Exception as e:
                    print(f"{Fore.RED}❌ {str(e)}{Style.RESET_ALL}")
                    continue

                user_projects = get_project_by_user(current_user)
                found = False
                for p in user_projects:
                    if p.id == project_id:
                        project_interface(project)
                        found = True
                        break

                if found:
                    break
                else:
                    print(f"{Fore.RED}❌ You're not assigned to a project with ID {project_id}.{Style.RESET_ALL}")

        elif choice == "3":
            while True:
                try:
                    project_id = int(input("Enter project ID to show statistics: ").strip())
                except ValueError:
                    print(f"{Fore.RED}❌ Project ID must be an integer.{Style.RESET_ALL}")
                    continue

                try:
                    project = get_project_by_id(project_id)
                except Exception as e:
                    print(f"{Fore.RED}❌ {str(e)}{Style.RESET_ALL}")
                    continue

                user_projects = get_project_by_user(current_user)
                found = False
                for p in user_projects:
                    if p.id == project_id:
                        show_project_summary_gui(project)
                        found = True
                        break

                if found:
                    break
                else:
                    print(f"{Fore.RED}❌ You're not assigned to a project with ID {project_id}.{Style.RESET_ALL}")

        elif choice == "4":
            while True:
                try:
                    project_id = input("Enter project ID to delete: ").strip()
                except ValueError:
                    print(f"{Fore.RED}❌ Project ID must be an integer.{Style.RESET_ALL}")
                    continue

                project_id = int(project_id)

                try:
                    project = get_project_by_id(project_id)
                except Exception as e:
                    print(f"{Fore.RED}❌ {str(e)}{Style.RESET_ALL}")
                    continue
                users = get_users_by_project(project)

                is_admin = False
                for user in users:
                    if user.id == current_user.id and user.role.lower() == "admin":
                        is_admin = True
                        break

                if not is_admin:
                    print(f"{Fore.RED}❌ You must be an ADMIN of this project to delete it.{Style.RESET_ALL}")
                    break

                try:
                    delete_project(project_id)
                    print(f"{Fore.GREEN}✅ Project ID {project_id} deleted successfully.{Style.RESET_ALL}")
                except Exception as e:
                    print(f"{Fore.RED}❌ Failed to delete project: {e}{Style.RESET_ALL}")
                break

        elif choice == "5":
            print(f"\n{Fore.BLUE}🆕 Creating a new project...{Style.RESET_ALL}")

            name = input("Project name: ").strip()

            valid_types = list_projects_all_types()
            print(f"{Fore.CYAN}Available types:{Style.RESET_ALL} {', '.join(valid_types)}")
            project_type = input("Choose project type: ").strip()

            valid_statuses = list_projects_all_status()
            print(f"{Fore.CYAN}Available statuses:{Style.RESET_ALL} {', '.join(valid_statuses)}")
            project_status = input("Choose project status: ").strip()

            new_project = Project(name=name, project_type=project_type, project_status=project_status)

            try:
                created_project = create_project(new_project)
            except Exception as e:
                print(f"{Fore.RED}❌ {str(e)}{Style.RESET_ALL}")
                continue

            assign_user_to_project(current_user, created_project, role="Admin")
            print(f"{Fore.GREEN}✅ Project '{created_project.name}' created with ID {created_project.id}.{Style.RESET_ALL}")
            print(f"{Fore.GREEN}👤 You are assigned as ADMIN.{Style.RESET_ALL}")

        elif choice == "6":
            while True:
                try:
                    project_id = int(input("Enter project ID to show statistics: ").strip())
                except ValueError:
                    print(f"{Fore.RED}❌ Project ID must be an integer.{Style.RESET_ALL}")
                    continue

                try:
                    project = get_project_by_id(project_id)
                except Exception as e:
                    print(f"{Fore.RED}❌ {str(e)}{Style.RESET_ALL}")
                    continue

                users = get_users_by_project(project)

                is_admin = False
                for user in users:
                    if user.id == current_user.id and user.role.lower() == "admin":
                        is_admin = True
                        break

                if not is_admin:
                    print(f"{Fore.RED}❌ You must be an ADMIN of this project to update it.{Style.RESET_ALL}")
                    break

                print(f"{Fore.CYAN}Leave any field empty to keep current value.{Style.RESET_ALL}")

                new_name = input(f"New name [{project.name}]: ").strip()
                valid_types = list_projects_all_types()
                print(f"{Fore.CYAN}Available types:{Style.RESET_ALL} {', '.join(valid_types)}")
                new_type = input(f"New type [{project.project_type}]: ").strip()

                valid_statuses = list_projects_all_status()
                print(f"{Fore.CYAN}Available statuses:{Style.RESET_ALL} {', '.join(valid_statuses)}")
                new_status = input(f"New status [{project.project_status}]: ").strip()

                updated_project = Project(
                    project_id=project_id,
                    name=new_name if new_name else project.name,
                    project_type=new_type if new_type else project.project_type,
                    project_status=new_status if new_status else project.project_status
                )

                try:
                    result = update_project(updated_project)
                    print(f"{Fore.GREEN}✅ Project '{result.name}' updated successfully.{Style.RESET_ALL}")
                except Exception as e:
                    print(f"{Fore.RED}❌ Failed to update project: {e}{Style.RESET_ALL}")
                break

        elif choice == "7":
            projects = get_project_by_user(current_user)
            if not projects:
                print(f"{Fore.YELLOW}⚠️ No projects found.{Style.RESET_ALL}")
                return

            print(f"{Fore.CYAN}Project IDs:{Style.RESET_ALL} {', '.join(str(t.id) for t in projects)}")
            try:
                project_id = input("Enter project ID to view Gantt: ").strip()
                project_id = int(project_id)
                project = get_project_by_id(project_id)
                show_gantt_gui(project)
            except Exception as e:
                print(f"{Fore.RED}❌ Possible Project without Tasks: {e}{Style.RESET_ALL}")


        elif choice == "0":
            break
        else:
            print(f"{Fore.RED}❌ Invalid choice.{Style.RESET_ALL}")

def task_actions_menu(current_user):
    while True:
        print(f"\n📝 Task Menu:")
        print(f"1. 📋 {Fore.BLUE}List your tasks{Style.RESET_ALL}")
        print(f"2. 🔍 {Fore.BLUE}View task details{Style.RESET_ALL}")
        print(f"3. ➕ {Fore.BLUE}Create new task{Style.RESET_ALL}")
        print(f"4. ✏️ {Fore.BLUE}Update a task{Style.RESET_ALL}")
        print(f"5. 🗑️ {Fore.BLUE}Delete a task{Style.RESET_ALL}")
        print(f"0. 🔙 {Fore.YELLOW}Back to main menu{Style.RESET_ALL}")

        choice = input("Choice: ").strip()

        if choice == "1":
            tasks = get_tasks_by_user(current_user)
            if not tasks:
                print(f"{Fore.YELLOW}⚠️ You are not assigned to any tasks.{Style.RESET_ALL}")
            else:
                print(f"{Fore.GREEN}📝 Your Tasks:{Style.RESET_ALL}")
                for t in tasks:
                    print(f" - [{t.id}] {t.name}")

        elif choice == "2":
            tasks = get_tasks_by_user(current_user)
            try:
                task_id = int(input("Enter task ID to show details: ").strip())
            except ValueError:
                print(f"{Fore.RED}❌ Task ID must be an integer.{Style.RESET_ALL}")
                continue

            task_id = int(task_id)
            found = False
            for t in tasks:
                if t.id == task_id:
                    try:
                        task = get_task_by_id(task_id)
                        task_interface(task)
                        found = True
                        break
                    except Exception as e:
                        print(f"{Fore.RED}❌ {str(e)}{Style.RESET_ALL}")
                        break
            if not found:
                print(f"{Fore.RED}❌ You are not assigned to a task with ID {task_id}.{Style.RESET_ALL}")

        elif choice == "3":
            print(f"\n{Fore.BLUE}➕ Creating a new task...{Style.RESET_ALL}")

            while True:
                name = input("Task name: ").strip()
                if name:
                    break
                print(f"{Fore.RED}❌ Name is required.{Style.RESET_ALL}")

            while True:
                location = input("Location: ").strip()
                if location:
                    break
                print(f"{Fore.RED}❌ Location is required.{Style.RESET_ALL}")

            while True:
                start_str = input("Start date (YYYY-MM-DD): ").strip()
                try:
                    start_date = datetime.strptime(start_str, "%Y-%m-%d")
                    break
                except ValueError:
                    print(f"{Fore.RED}❌ Invalid start date format.{Style.RESET_ALL}")

            while True:
                end_str = input("End date (YYYY-MM-DD, optional): ").strip()
                if not end_str:
                    end_date = None
                    break
                try:
                    end_date = datetime.strptime(end_str, "%Y-%m-%d")
                    break
                except ValueError:
                    print(f"{Fore.RED}❌ Invalid end date format.{Style.RESET_ALL}")

            priorities = list_tasks_all_priorities()
            print(f"{Fore.CYAN}Available priorities:{Style.RESET_ALL} {', '.join(priorities)}")
            priority = input("Choose priority: ").strip()


            statuses = list_tasks_all_status()
            print(f"{Fore.CYAN}Available statuses:{Style.RESET_ALL} {', '.join(statuses)}")
            status = input("Choose status: ").strip()


            user_projects = get_project_by_user(current_user)
            if not user_projects:
                print(f"{Fore.YELLOW}⚠️ You are not assigned to any projects. Cannot create task.{Style.RESET_ALL}")
                continue

            project = None
            while True:
                print(f"{Fore.CYAN}Available project IDs:{Style.RESET_ALL} {', '.join(str(p.id) for p in user_projects)}")
                proj_id_input = input("Enter project ID to assign task to: ").strip()
                if proj_id_input.isdigit():
                    pid = int(proj_id_input)
                    for p in user_projects:
                        if p.id == pid:
                            project = p
                            break
                    if project:
                        break
                print(f"{Fore.RED}❌ Invalid or unauthorized project ID.{Style.RESET_ALL}")

            while True:
                work_hours_input = input("Enter your work hours (optional): ").strip()
                if not work_hours_input:
                    work_hours = 0
                    break
                try:
                    work_hours = float(work_hours_input)
                    break
                except ValueError:
                    print(f"{Fore.RED}❌ Work hours must be a number.{Style.RESET_ALL}")

            task = Task(
                name=name,
                location=location,
                start_date=start_date,
                end_date=end_date,
                status=status,
                priority=priority,
                project_id=project.id
            )

            try:
                created_task = create_task(task)
                assign_user_to_task(current_user,created_task,work_hours)
                print(f"{Fore.GREEN}✅ Task '{created_task.name}' created and assigned to you.{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.RED}❌ Failed to create task: {e}{Style.RESET_ALL}")

        elif choice == "4":
            tasks = get_tasks_by_user(current_user)
            if not tasks:
                print(f"{Fore.YELLOW}⚠️ You are not assigned to any tasks.{Style.RESET_ALL}")
                continue

            print(f"{Fore.CYAN}Your Task IDs:{Style.RESET_ALL} {', '.join(str(t.id) for t in tasks)}")

            while True:
                task_id_input = input("Enter task ID to update: ").strip()
                if not task_id_input.isdigit():
                    print(f"{Fore.RED}❌ Invalid input. Please enter a number.{Style.RESET_ALL}")
                    continue

                task_id = int(task_id_input)
                task = next((t for t in tasks if t.id == task_id), None)
                if not task:
                    print(f"{Fore.RED}❌ Task ID {task_id} not assigned to you.{Style.RESET_ALL}")
                    continue
                try:
                    task = get_task_by_id(task_id)
                    break
                except Exception as e:
                    print(f"{Fore.RED}❌ {str(e)}{Style.RESET_ALL}")
                    continue

            print(f"{Fore.CYAN}Leave fields empty to keep current values.{Style.RESET_ALL}")

            new_name = input(f"New name [{task.name}]: ").strip() or task.name

            new_location = input(f"New location [{task.location}]: ").strip() or task.location

            while True:
                new_start = input(f"New start date [{task.start_date.strftime('%Y-%m-%d')}]: ").strip()
                if not new_start:
                    new_start_date = task.start_date
                    break
                try:
                    new_start_date = datetime.strptime(new_start, "%Y-%m-%d")
                    break
                except ValueError:
                    print(f"{Fore.RED}❌ Invalid date format. Use YYYY-MM-DD.{Style.RESET_ALL}")

            while True:
                default_end = task.end_date.strftime('%Y-%m-%d') if task.end_date else ""
                new_end = input(f"New end date [{default_end}]: ").strip()
                if not new_end:
                    new_end_date = task.end_date
                    break
                try:
                    new_end_date = datetime.strptime(new_end, "%Y-%m-%d")
                    break
                except ValueError:
                    print(f"{Fore.RED}❌ Invalid date format. Use YYYY-MM-DD.{Style.RESET_ALL}")

            statuses = list_tasks_all_status()
            print(f"{Fore.CYAN}Available statuses:{Style.RESET_ALL} {', '.join(statuses)}")
            new_status = input(f"New status [{task.status}]: ").strip()
            if new_status == "":
                new_status = task.status



            priorities = list_tasks_all_priorities()
            print(f"{Fore.CYAN}Available priorities:{Style.RESET_ALL} {', '.join(priorities)}")
            new_priority = input(f"New priority [{task.priority}]: ").strip()
            if not new_priority:
                new_priority = task.priority

            updated_task = Task(
                task_id=task.id,
                name=new_name,
                location=new_location,
                start_date=new_start_date,
                end_date=new_end_date,
                status=new_status,
                priority=new_priority,
                project_id = int(task.project_id)

            )

            try:
                result = update_task(updated_task)
                print(f"{Fore.GREEN}✅ Task '{result.name}' updated successfully.{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.RED}❌ Failed to update task: {e}{Style.RESET_ALL}")

        elif choice == "5":
            tasks = get_tasks_by_user(current_user)
            if not tasks:
                print(f"{Fore.YELLOW}⚠️ You are not assigned to any tasks.{Style.RESET_ALL}")
                continue

            print(f"{Fore.CYAN}Your Task IDs:{Style.RESET_ALL} {', '.join(str(t.id) for t in tasks)}")

            while True:
                task_id = input("Enter task ID to delete: ").strip()
                if not task_id.isdigit():
                    print(f"{Fore.RED}❌ Invalid input. Must be a number.{Style.RESET_ALL}")
                    continue
                task_id = int(task_id)
                task = None
                for t in tasks:
                    if t.id == task_id:
                        task = t
                        break
                if not task:
                    print(f"{Fore.RED}❌ Task with ID {task_id} not found or not assigned to you.{Style.RESET_ALL}")
                    continue

                try:
                    delete_task(task_id)
                    print(f"{Fore.GREEN}✅ Task '{task.name}' (ID {task_id}) deleted successfully.{Style.RESET_ALL}")
                except Exception as e:
                    print(f"{Fore.RED}❌ Failed to delete task: {e}{Style.RESET_ALL}")
                break

        elif choice == "0":
            break
        else:
            print(f"{Fore.RED}❌ Invalid choice.{Style.RESET_ALL}")

if __name__ == '__main__':
    user = select_user()

    while True:
        section = choose_section()
        if section == "1":
            user_actions_menu(user)
        elif section == "2":
            task_actions_menu(user)
        elif section == "3":
            project_action_menu(user)
        elif section == "0":
            print("Exiting...")
            break
        else:
            print("❌ Invalid choice.\n")

