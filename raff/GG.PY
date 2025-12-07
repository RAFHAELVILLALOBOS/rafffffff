import tkinter as tk
from tkinter import ttk
from datetime import datetime
import os
import json


def get_exercise():
    return custom_exercise_entry.get().strip() or exercise_var.get()

def add_workout():
    n, e, d, l = name_entry.get().strip(), get_exercise(), date_entry.get().strip(), level_var.get()
    if not n or not e or not d: return
    try: datetime.strptime(d, "%d-%m-%Y")
    except: return
    tree.insert("", "end", values=(n, e, d, l, "Pending"))
    name_entry.delete(0, tk.END); custom_exercise_entry.delete(0, tk.END)
    date_entry.delete(0, tk.END); level_var.set("Beginner"); exercise_var.set("Push-ups")

def mark_done():
    for i in tree.selection():
        v = tree.item(i, "values")
        tree.item(i, values=(v[0], v[1], v[2], v[3], "Done"))

def delete_workout():
    for i in tree.selection(): tree.delete(i)

def toggle_theme(*_):
    bg, fg = ("#2e2e2e", "#fff") if theme_var.get() == "Dark" else ("#f0f0f0", "#000")
    root.configure(bg=bg)
    for w in root.winfo_children():
        try: w.configure(bg=bg, fg=fg)
        except: pass

root = tk.Tk()
root.title("WORKOUT PLANNER")
root.geometry("775x500")
theme_var = tk.StringVar(value="Light")
level_var = tk.StringVar(value="Beginner")
exercise_var = tk.StringVar(value="Push-ups")

tk.Label(root, text="Theme:").grid(row=0, column=0, sticky="e")
tk.OptionMenu(root, theme_var, "Light", "Dark", command=toggle_theme).grid(row=0, column=1, sticky="w")

tk.Label(root, text="WORKOUT PLANNER", font=("Helvetica", 16, "bold")).grid(row=1, column=0, columnspan=4, pady=10)

tk.Label(root, text="Name:").grid(row=2, column=0, sticky="e", padx=(10,0))
name_entry = tk.Entry(root, width=20)
name_entry.grid(row=2, column=1, sticky="w", padx=(0,0))

tk.Label(root, text="Exercise:").grid(row=3, column=0, sticky="e", padx=(10,0))
tk.OptionMenu(root, exercise_var, "Push-ups", "Jumping Jacks", "Squats", "Plank").grid(row=3, column=1, sticky="e")
custom_exercise_entry = tk.Entry(root, width=20)
custom_exercise_entry.grid(row=3, column=1, sticky="w")  

tk.Label(root, text="Date (DD-MM-YYYY):").grid(row=4, column=0, sticky="e", padx=(10,0))
date_entry = tk.Entry(root, width=20)
date_entry.grid(row=4, column=1, sticky="w")

tk.Label(root, text="Level:").grid(row=5, column=0, sticky="e", padx=(10,0))
tk.OptionMenu(root, level_var, "Beginner", "Intermediate", "Advanced").grid(row=5, column=1, sticky="w")

cols = ("Name", "Exercise", "Date", "Level", "Status")
tree = ttk.Treeview(root, columns=cols, show="headings", height=10)
for c in cols: tree.heading(c, text=c); tree.column(c, width=150)
tree.grid(row=6, column=0, columnspan=4, padx=10, pady=10)

btn_frame = tk.Frame(root)
btn_frame.grid(row=8, column=0, columnspan=4, pady=10)
tk.Button(btn_frame, text="ADD WORKOUT", command=add_workout, activebackground="#4CAF50").pack(side="left", padx=5)
tk.Button(btn_frame, text="MARK DONE", command=mark_done, activebackground="#2196F3").pack(side="left", padx=5)
tk.Button(btn_frame, text="DELETE", command=delete_workout, activebackground="#f44336").pack(side="left", padx=5)

toggle_theme()
root.mainloop()