from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import json
import os

app = Flask(__name__)

def load_tasks():
    filename = "tasks.json"
    try:
        with open(filename, "r", encoding='utf-8') as file:
            tasks = json.load(file)
    except FileNotFoundError:
        tasks = []
        save_tasks(tasks)
    return tasks


def save_tasks(tasks):
    with open(f"tasks.json", "w") as file:
        json.dump(tasks, file)


@app.route('/')
def index():
    tasks = load_tasks()
    return render_template('index.html', tasks=tasks)


@app.route('/add_task', methods=['POST'])
def add_task():
    title = request.form['title']
    if title:
        tasks = load_tasks()
        tasks.append({"title": title, "done": False})
        save_tasks( tasks)
    return redirect(url_for('index'))


@app.route('/remove_task/<int:index>')
def remove_task(index):
    tasks = load_tasks()
    if 0 <= index < len(tasks):
        removed_task = tasks.pop(index)
        save_tasks( tasks)
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
