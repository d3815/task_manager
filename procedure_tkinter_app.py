#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from tkinter import *
from tkinter import messagebox
import datetime
import sqlite3


def update_today_list_frame():

    for widget in today_task_frame.winfo_children():
        widget.destroy()

    today_task_list = show_today_task()
    task_count = Label(today_task_frame, text='Всего задач : {}'.format(len(today_task_list)))
    task_count.pack(side=TOP)

    task_canvas = Canvas(today_task_frame)
    task_list_scrollbar = Scrollbar(today_task_frame, orient="vertical", command=task_canvas.yview)
    frame = Frame()

    for i in today_task_list:
        lab_title = Label(frame, text=str.upper(i[1]))
        lab_title.pack()
        lab_desc = Label(frame, text=str.capitalize(i[2]))
        lab_desc.pack()
        lab_date = Label(frame, text=i[3])
        lab_date.pack()
        lab_priority = Label(frame, text='Приоритет {}'.format(i[4]))
        lab_priority.pack()
        btn_del = Button(frame, text='Удалить задачу', command=lambda i=i: delete_task(i[0]))
        btn_del.pack()

    task_canvas.create_window(0, 0, anchor='nw', window=frame)
    task_canvas.update_idletasks()
    task_canvas.configure(scrollregion=task_canvas.bbox('all'), yscrollcommand=task_list_scrollbar.set)
    task_canvas.pack(fill='both', expand=True, side='left')
    task_list_scrollbar.pack(side=RIGHT, fill=Y)


def delete_task(task_id):
    sql_delete_task = 'DELETE FROM Tasks WHERE task_id = {}'.format(task_id)
    sql_request(sql_delete_task)
    update_task_list_frame()
    update_today_list_frame()


def sql_request(request, contex_fetchall=False):
    conn = sqlite3.connect('mydatabase.db')
    cur = conn.cursor()
    sql_create = "CREATE TABLE IF NOT EXISTS Tasks (task_id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, " \
                 "description TEXT, due TEXT, priority INTEGER)"
    cur.execute(sql_create)
    cur.execute(request)

    if contex_fetchall:
        context = cur.fetchall()
        return context
    else:
        conn.commit()

    conn.close()


def show_today_task():
    time_today = datetime.datetime.today()
    sql_show_today_task = "Select * FROM Tasks WHERE due = '{}-{}-{}'".format(time_today.day, time_today.month,
                                                                              str(time_today.year)[-2:])
    # сделать нормальное форматирование строки с датой выше
    context = sql_request(sql_show_today_task, contex_fetchall=True)
    return context


def show_all_task():
    sql_show_all_tasks = 'SELECT * FROM Tasks ORDER BY due, priority'
    context = sql_request(sql_show_all_tasks, contex_fetchall=True)
    return context


def delete_window_context():
    title.delete(first=0, last=500)
    desc.delete(first=0, last=500)
    date.delete(first=0, last=20)
    priority.delete(first=0, last=20)


def add_task():
    if title.get() and desc.get() and priority.get():
        loc_title = title.get()
        loc_desc = desc.get()
        if date.get():
            loc_date = date.get()
        else:
            loc_date = None
        loc_priority = priority.get()

        sql_update = "INSERT INTO Tasks(title, description, due, priority) VALUES " \
                     "('{0}', '{1}', '{2}', '{3}')".format(loc_title, loc_desc, loc_date, loc_priority)
        sql_request(sql_update)

        delete_window_context()
        update_task_list_frame()
        update_today_list_frame()
        title.focus()
    else:
        messagebox.showinfo('Failed', 'Введены некорректные данные')


def update_task_list_frame():

    for widget in all_task_frame.winfo_children():
        widget.destroy()

    task_list = show_all_task()
    task_count = Label(all_task_frame, text='Всего задач : {}'.format(len(task_list)))
    task_count.pack(side=TOP)
    task_canvas = Canvas(all_task_frame)
    task_list_scrollbar = Scrollbar(all_task_frame, orient="vertical", command=task_canvas.yview)
    frame = Frame()

    for i in task_list:
        lab_title = Label(frame, text=str.upper(i[1]))
        lab_title.pack()
        lab_desc = Label(frame, text=str.capitalize(i[2]))
        lab_desc.pack()
        lab_date = Label(frame, text=i[3])
        lab_date.pack()
        lab_priority = Label(frame, text='Приоритет {}'.format(i[4]))
        lab_priority.pack()
        btn_del = Button(frame, text='Удалить задачу', command=lambda i=i: delete_task(i[0]))
        btn_del.pack()

    task_canvas.create_window(0, 0, anchor='nw', window=frame)
    task_canvas.update_idletasks()
    task_canvas.configure(scrollregion=task_canvas.bbox('all'), yscrollcommand=task_list_scrollbar.set)
    task_canvas.pack(fill='both', expand=True, side='left')
    task_list_scrollbar.pack(side=RIGHT, fill=Y)


root = Tk()

root.title('Task Manager')
w = root.winfo_screenwidth() // 4
h = root.winfo_screenheight() // 4
root.geometry('800x280+{}+{}'.format(w, h))
root.resizable(width=False, height=False)

new_task_frame = Frame(root)
today_task_frame = Frame(root)
all_task_frame = Frame(root)

new_task = Label(new_task_frame, text="Новая задача")
new_task.pack(side=TOP)

title_label = Label(new_task_frame, text='Название задачи')
title_label.pack(side=TOP)

title = Entry(new_task_frame, width=15)
title.focus()
title.pack(side=TOP)

desc_label = Label(new_task_frame, text='Описание задачи')
desc_label.pack(side=TOP)
desc = Entry(new_task_frame, width=15)
desc.pack(side=TOP)

date_label = Label(new_task_frame, text='Сроки')
date_label.pack(side=TOP)
date = Entry(new_task_frame, width=15)
date.pack(side=TOP)

priority_label = Label(new_task_frame, text='Приоритет')
priority_label.pack(side=TOP)

priority = Entry(new_task_frame, width=15)
priority.pack(side=TOP)

btn = Button(new_task_frame, text="Добавить", command=add_task)
btn.pack(side=TOP)

new_task_frame.pack(side=LEFT, ipadx=10)
all_task_frame.pack(side=LEFT, ipadx=10)
today_task_frame.pack(side=LEFT, ipadx=10)

update_task_list_frame()
update_today_list_frame()

root.mainloop()
