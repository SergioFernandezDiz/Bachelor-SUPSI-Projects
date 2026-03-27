# from \client run: python -m task_manager_library.statistic

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from .modules import *
from .task_api import list_tasks_all_priorities,list_tasks_all_status
from .project_api import get_tasks_by_project,get_project_by_id
from collections import Counter
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd
import random



def view_hours_task_project(project: Project, width=10, height=6):
    tasks = get_tasks_by_project(project)
    tasks = [t for t in tasks if t.work_hours > 0]

    labels = [t.name for t in tasks]
    sizes = [t.work_hours for t in tasks]
    colors = plt.cm.tab20.colors[:len(tasks)]

    fig, ax = plt.subplots(figsize=(width * 1.05, height * 0.95))

    fig.subplots_adjust(top=0.88, bottom=0.32)

    wedges, texts, autotexts = ax.pie(
        sizes,
        labels=None,
        colors=colors,
        startangle=140,
        radius=1.6,
        autopct='%1.1f%%',
        pctdistance=0.6,
        textprops={'fontsize': 12}
    )

    ax.legend(
        handles=wedges,
        labels=labels,
        loc='lower center',
        bbox_to_anchor=(0.5, -0.4),
        fontsize=9,
        title="Tasks",
        title_fontsize=10,
        ncol=2
    )

    ax.set_title(f"Hours task for project {project.id}", fontsize=16, fontweight='bold')
    ax.axis('equal')

    return fig


def view_tasks_status_project(project: Project, width=10, height=5, font_scale=3.0):
    tasks = get_tasks_by_project(project)
    all_status = list_tasks_all_status()
    task_status = Counter(task.status for task in tasks)
    counts = [task_status.get(status, 0) for status in all_status]

    fig, ax = plt.subplots(figsize=(width, height))
    colors = ['skyblue', 'green', 'gray']
    bars = ax.bar(all_status, counts, color=colors[:len(all_status)], edgecolor='black')
    #bars = ax.bar(all_status, counts, color='skyblue', edgecolor='black')

    ax.set_title(f"Task Status for Project {project.id}", fontsize=14 * font_scale)
    ax.set_ylabel("Count", fontsize=12 * font_scale)
    ax.tick_params(axis='x', labelsize=10 * font_scale)
    ax.tick_params(axis='y', labelsize=10 * font_scale)
    ax.yaxis.get_major_locator().set_params(integer=True)
    ax.grid(axis='y', linestyle='--', alpha=0.4)

    return fig


def view_tasks_priority_project(project: Project, width=10, height=5, font_scale=3.0):
    tasks = get_tasks_by_project(project)
    all_priority= list_tasks_all_priorities()
    task_priority = Counter(task.priority for task in tasks)
    counts = [task_priority.get(priority, 0) for priority in all_priority]

    fig, ax = plt.subplots(figsize=(width, height))
    bars = ax.bar(all_priority, counts, color='salmon', edgecolor='black')


    ax.set_title(f"Task Priority for Project {project.id}", fontsize=14 * font_scale)
    ax.set_ylabel("Count", fontsize=12 * font_scale)
    ax.tick_params(axis='x', labelsize=10 * font_scale)
    ax.tick_params(axis='y', labelsize=10 * font_scale)
    ax.yaxis.get_major_locator().set_params(integer=True)
    ax.grid(axis='y', linestyle='--', alpha=0.4)

    return fig

# graphical user interface
def show_project_summary_gui(project: Project):
    window = tk.Tk()
    window.title(f"Task summary for project {project.id}")
    window.state('zoomed')

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    plot_width = screen_width / 120
    plot_height = screen_height / 200
    font_scale = screen_width / 1920

    pie_fig = view_hours_task_project(project, width=plot_width * 1.3, height=plot_height * 2.3)
    status_fig = view_tasks_status_project(project, width=plot_width, height=plot_height, font_scale=font_scale)
    priority_fig = view_tasks_priority_project(project, width=plot_width, height=plot_height, font_scale=font_scale)

    container = tk.Frame(window)
    container.pack(fill='both', expand=True)

    if pie_fig:
        pie_canvas = FigureCanvasTkAgg(pie_fig, master=container)
        pie_canvas.draw()
        pie_canvas.get_tk_widget().grid(row=0, column=0, rowspan=2, sticky='nsew', padx=20, pady=20)

    if status_fig:
        status_canvas = FigureCanvasTkAgg(status_fig, master=container)
        status_canvas.draw()
        status_canvas.get_tk_widget().grid(row=0, column=1, sticky='nsew', padx=20, pady=10)

    if priority_fig:
        priority_canvas = FigureCanvasTkAgg(priority_fig, master=container)
        priority_canvas.draw()
        priority_canvas.get_tk_widget().grid(row=1, column=1, sticky='nsew', padx=20, pady=10)

    container.grid_rowconfigure(0, weight=1)
    container.grid_rowconfigure(1, weight=1)
    container.grid_columnconfigure(0, weight=2)
    container.grid_columnconfigure(1, weight=1)

    tk.Button(window, text="Close", font=("Arial", int(12 * font_scale)), command=window.destroy).pack(pady=10)

    window.mainloop()

def show_gantt_gui(project):
    try:
        tasks = get_tasks_by_project(project)
    except Exception as e:
        print(f"{Fore.RED}❌ Tasks not found: {project.id}: {e}{Style.RESET_ALL}")
        return

    if not tasks:
        print(f"{Fore.YELLOW}⚠️ No tasks found for project {project.id}.{Style.RESET_ALL}")
        return

    df = pd.DataFrame([
        {
            "Task": task.name,
            "Start": task.start_date,
            "Finish": task.end_date or task.start_date,
            "Color": f"rgba({random.randint(50, 200)}, {random.randint(100, 255)}, {random.randint(150, 255)}, 0.9)"
        }
        for task in tasks if task.start_date
    ])

    fig = px.timeline(
        df,
        x_start="Start",
        x_end="Finish",
        y="Task",
        title=f"Gantt Chart for Project {project.id}",
        color="Task",
        color_discrete_sequence=df["Color"].tolist()
    )

    fig.update_yaxes(autorange="reversed", showticklabels=False)
    fig.update_layout(
        plot_bgcolor="#fff",
        paper_bgcolor="#f9f9f9",
        font=dict(family="Arial", size=14),
        title_x=0.5,
        margin=dict(l=100, r=40, t=60, b=60),
        dragmode=False,
        xaxis_fixedrange=True,
        yaxis_fixedrange=True
    )

    fig.update_traces(
        marker_line_color="black",
        marker_line_width=0.6,
        selector=dict(type="bar")
    )

    fig.show()





if __name__ == "__main__":
    project = get_project_by_id(90)
    #view_hours_task_project(project).show()
    #view_tasks_status_project(project).show()
    #view_tasks_priority_project(project).show()
    #show_project_summary_gui(project)
    show_gantt_gui(project)