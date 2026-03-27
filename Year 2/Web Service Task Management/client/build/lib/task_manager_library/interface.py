# from \client  run:  pipenv run python -m task_manager_library.interface


from colorama import Fore, Style, init

from .project_api import get_users_by_project, get_tasks_by_project, get_project_by_id
from .task_api import get_users_by_task,get_task_by_id
from .user_api import get_tasks_by_user,get_user_by_id,get_project_by_user
from .aggregations import get_progress_by_tasks, get_total_hours_by_user



init(autoreset=True)

def project_interface(project):
    users = get_users_by_project(project)
    tasks = get_tasks_by_project(project)
    progress = get_progress_by_tasks(tasks)

    print(f"{Fore.MAGENTA}{Style.BRIGHT}\n{'═' * 40}")
    print(f"📁 {Fore.CYAN}{Style.BRIGHT}PROJECT INTERFACE".center(40))
    print(f"{Fore.MAGENTA}{'═' * 40}{Style.RESET_ALL}")

    print(f"{Fore.YELLOW}🆔 ID:           {Style.RESET_ALL}{project.id}")
    print(f"{Fore.YELLOW}📌 Name:         {Style.RESET_ALL}{project.name}")
    print(f"{Fore.YELLOW}🏗️ Type:         {Style.RESET_ALL}{project.project_type}")
    print(f"{Fore.YELLOW}📊 Status:       {Style.RESET_ALL}{project.project_status}")

    print(f"\n{Fore.GREEN}👥 Users:        {Style.RESET_ALL}{len(users)}")
    print(f"{Fore.GREEN}📝 Tasks:        {Style.RESET_ALL}{len(tasks)}")

    color = Fore.GREEN if progress == 100 else Fore.BLUE if progress >= 50 else Fore.RED
    print(f"{color}📈 Progress:     {progress}%{Style.RESET_ALL}")

    print(f"{Fore.MAGENTA}{'═' * 40}{Style.RESET_ALL}")

def task_interface(task):
    users = get_users_by_task(task)

    print(f"{Fore.MAGENTA}{Style.BRIGHT}\n📝 TASK DETAILS\n{'='*50}")

    print(f"{Fore.YELLOW}🆔 ID:            {Style.RESET_ALL}{task.id}")
    print(f"{Fore.YELLOW}📛 Name:          {Style.RESET_ALL}{task.name}")
    print(f"{Fore.YELLOW}📍 Location:      {Style.RESET_ALL}{task.location}")

    print(f"{Fore.CYAN}📅 Start Date:    {Style.RESET_ALL}{task.start_date.strftime('%Y-%m-%d')}")
    end_date = task.end_date.strftime('%Y-%m-%d') if task.end_date else "N/A"
    print(f"{Fore.CYAN}📆 End Date:      {Style.RESET_ALL}{end_date}")

    print(f"{Fore.BLUE}📌 Status:        {Style.RESET_ALL}{task.status}")
    print(f"{Fore.BLUE}⚠️  Priority:      {Style.RESET_ALL}{task.priority}")

    print(f"{Fore.GREEN}💰 Actual Cost:   {Style.RESET_ALL}{task.actual_cost or 0} CHF")
    print(f"{Fore.GREEN}📊 Budget:        {Style.RESET_ALL}{task.budget or 0} CHF")

    project_name = get_project_by_id(task.project_id).name if task.project_id else "N/A"
    print(f"{Fore.LIGHTMAGENTA_EX}🏗️  Project:       {Style.RESET_ALL}{project_name}")
    print(f"{Fore.LIGHTMAGENTA_EX}⏱️  Work Hours:    {Style.RESET_ALL}{task.work_hours}")
    print(f"{Fore.LIGHTMAGENTA_EX}👥 Users Assigned: {Style.RESET_ALL}{len(users)}")

    print(f"{'='*50}\n")

def user_interface(user):
    print(f"{Fore.CYAN}{Style.BRIGHT}👤 USER Interface")
    print(f"{Fore.YELLOW}🆔 ID:         {Style.RESET_ALL}{user.id}")
    print(f"{Fore.YELLOW}📛 Name:       {Style.RESET_ALL}{user.name}")
    print(f"{Fore.YELLOW}👨‍👩‍👦 Surname:   {Style.RESET_ALL}{user.last_name}")
    print(f"{Fore.YELLOW}📡 Username:   {Style.RESET_ALL}@{user.username}")
    print(f"{Fore.MAGENTA}{'-' * 45}")

    projects = get_project_by_user(user)
    print(f"{Fore.GREEN}📁 Projects Assigned: {Style.RESET_ALL}")
    for p in projects:
        print(f"   - {p.name}")
    if not projects:
        print("   - No projects assigned")

    print(f"{Fore.MAGENTA}{'-' * 45}")

    tasks = get_tasks_by_user(user)
    print(f"{Fore.BLUE}📝 Tasks Assigned: {Style.RESET_ALL}")
    for t in tasks:
        print(f"   - {t.name}")
    if not tasks:
        print("   - No tasks assigned")

    total_hours = get_total_hours_by_user(user)
    print(f"{Fore.CYAN}{'-' * 45}")
    print(f"{Fore.LIGHTYELLOW_EX}⏱️ Total Work Hours: {Style.BRIGHT}{total_hours:.2f} hours")   # Da mettere a posto, ora calcola il totale lavorato sulle task ma da tutte le persone
    print(f"{Fore.CYAN}{'=' * 45}\n")


if __name__ == '__main__':

    project = get_project_by_id(4)
    task = get_task_by_id(1)
    user = get_user_by_id(1)
    project_interface(project)
    task_interface(task)
    user_interface(user)