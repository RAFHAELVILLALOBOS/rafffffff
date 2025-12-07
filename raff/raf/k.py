import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import os, sys
import json
import requests
import webbrowser
from PIL import Image, ImageTk
from io import BytesIO
from playsound import playsound
import threading

# For PyInstaller EXE compatibility
def resource_path(relative_path):
    
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Load saved workouts from JSON
def load_workouts():
    
    return json.load(open("workouts.json")) if os.path.exists("workouts.json") else []

# Save workouts to workouts.json
def save_workouts(data):
    
    with open("workouts.json", "w") as file:
        json.dump(data, file, indent=4)

# custom exercise or dropdown value
def get_exercise():

    return custom_exercise_entry.get().strip() or exercise_var.get()


#--------SOUND FUNCTIONS---------#

#Play sound without freezing the UI
def play_sound_async(sound_file):
    
    def _play():
        try:
            playsound(resource_path(sound_file))
        except Exception as e:
            print("Sound error:", e)

    threading.Thread(target=_play, daemon=True).start()
    

#---------ADD / DONE / DELETE-----------#

# Add new workout entry
def add_workout():
    
    n = name_entry.get().strip()
    e = get_exercise()
    c = count_entry.get().strip()
    r = reps_entry.get().strip()
    d = date_entry.get().strip()
    t = time_entry.get().strip().upper()
    l = level_var.get()

    if not (n and e and c and r and d and t):
        return

    try:
        datetime.strptime(d, "%d-%m-%Y")
        datetime.strptime(t, "%I:%M%p")
    except:
        return

    tree.insert("", "end", values=(n, e, c, r, f"{d} {t}", l, "Pending"))

    for entry in (name_entry, custom_exercise_entry, count_entry, reps_entry, date_entry, time_entry):
        entry.delete(0, tk.END)

    level_combo.set("Beginner")
    exercise_combo.set("Push-ups")

    save_workouts([tree.item(i, "values") for i in tree.get_children()])

 # Mark selected row as Done
def mark_done():
   
    for i in tree.selection():
        v = tree.item(i, "values")
        tree.item(i, values=(v[0], v[1], v[2], v[3], v[4], v[5], "Done"))

    save_workouts([tree.item(i, "values") for i in tree.get_children()])

# Delete selected workout
def delete_workout():
    
    for i in tree.selection():
        tree.delete(i)
    save_workouts([tree.item(i, "values") for i in tree.get_children()])


#--------NOTIFICATION---------#

# Check if any workout time is due every 10s
def check_notifications():
  
    now = datetime.now()

    for i in tree.get_children():
        v = tree.item(i, "values")

        try:
            workout_time = datetime.strptime(v[4], "%d-%m-%Y %I:%M%p")

            if workout_time <= now and v[6] == "Pending":
                play_sound_async("buddy.wav")
                messagebox.showinfo("Workout Reminder", f"Time to start: {v[1]} ({v[5]})")

        except:
            pass

    root.after(10000, check_notifications)


#--------ANALYTICS (VIDEOS)----------#

 # Open YouTube workout tutorial 
def show_analytics():
  
    sel = tree.selection()

    if not sel:
        messagebox.showinfo("Analytics", "Please select a workout.")
        return

    exercise = tree.item(sel[0], "values")[1]

    videos = {
        "Push-ups": "https://www.youtube.com/watch?v=IODxDxX7oi4",
        "Jumping Jacks": "https://www.youtube.com/watch?v=c4DAnQ6DtF8",
        "Squats": "https://www.youtube.com/watch?v=aclHkVaku9U",
        "Plank": "https://www.youtube.com/watch?v=pSHjTRCQxIw"
    }

    if exercise in videos:
        webbrowser.open(videos[exercise])
    else:
        messagebox.showinfo("Analytics", f"No video available for {exercise}")


#----------THEME SYSTEM----------#

# Toggle dark/light theme
def toggle_theme(*_):
    
    bg, fg = ("#2e2e2e", "#ffffff") if theme_var.get() == "Dark" else ("#f0f0f0", "#000000")

    root.config(bg=bg)

    def apply_theme(w):
        try:
            w.config(bg=bg, fg=fg)
        except:
            pass
        for child in w.winfo_children():
            apply_theme(child)

    apply_theme(root)

    style = ttk.Style()
    style.theme_use("default")
    style.configure("Treeview", background=bg, foreground=fg, fieldbackground=bg)
    style.configure("Treeview.Heading", background=bg, foreground=fg)


#---------BACKGROUND IMAGE----------#

# Load and set background image
def set_background_image(url):
 
    try:
        img = Image.open(BytesIO(requests.get(url).content)).resize((775, 500), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(img)

        canvas = tk.Canvas(root, width=775, height=500, highlightthickness=0)
        canvas.place(x=0, y=0, relwidth=1, relheight=1)
        canvas.create_image(0, 0, anchor="nw", image=photo)
        canvas.image = photo

        for w in root.winfo_children():
            if w != canvas:
                w.lift()

    except Exception as e:
        print("Image load failed:", e)


#----------MAIN WINDOW----------#

root = tk.Tk()
root.title("WORKOUT PLAN")
root.geometry("775x500")
root.iconbitmap(resource_path("HAHA.ico"))

theme_var = tk.StringVar(value="Light")
level_var = tk.StringVar(value="Beginner")
exercise_var = tk.StringVar(value="Push-ups")

set_background_image("https://olympiagym.com.au/wp-content/uploads/2022/06/IMG_1171.jpg")



#--------TOP BAR (THEME SELECTOR)----------#

ttk.Combobox(root, textvariable=theme_var, values=["Light", "Dark"], width=10, state="readonly")\
    .grid(row=0, column=3, sticky="e", padx=10)
theme_var.trace_add("write", toggle_theme)

tk.Label(root, text="WORKOUT PLAN", font=("Helvetica", 16, "bold")).grid(row=1, column=0, columnspan=4, pady=10)



#---------INPUT FIELDS------------#

tk.Label(root, text="Name:").grid(row=2, column=0, sticky="e")
name_entry = tk.Entry(root, width=20)
name_entry.grid(row=2, column=1, sticky="w")

tk.Label(root, text="Exercise:").grid(row=3, column=0, sticky="e")
exercise_frame = tk.Frame(root)
exercise_frame.grid(row=3, column=1, sticky="w")

custom_exercise_entry = tk.Entry(exercise_frame, width=20)
custom_exercise_entry.pack(side="left")

exercise_combo = ttk.Combobox(
    exercise_frame, textvariable=exercise_var,
    values=["Push-ups", "Jumping Jacks", "Squats", "Plank"],
    state="readonly", width=16
)
exercise_combo.pack(side="left")

tk.Label(root, text="Count:").grid(row=4, column=0, sticky="e")
count_entry = tk.Entry(root, width=20)
count_entry.grid(row=4, column=1, sticky="w")

tk.Label(root, text="Reps:").grid(row=5, column=0, sticky="e")
reps_entry = tk.Entry(root, width=20)
reps_entry.grid(row=5, column=1, sticky="w")

tk.Label(root, text="Date (DD-MM-YYYY):").grid(row=6, column=0, sticky="e")
date_entry = tk.Entry(root, width=20)
date_entry.grid(row=6, column=1, sticky="w")

tk.Label(root, text="Time (AM/PM):").grid(row=7, column=0, sticky="e")
time_entry = tk.Entry(root, width=20)
time_entry.grid(row=7, column=1, sticky="w")

tk.Label(root, text="Level:").grid(row=8, column=0, sticky="e")
level_combo = ttk.Combobox(
    root, textvariable=level_var,
    values=["Beginner", "Intermediate", "Advanced"],
    state="readonly", width=18
)
level_combo.grid(row=8, column=1, sticky="w")



#----------TABLE-----------#

cols = ("Name", "Exercise", "Count", "Reps", "Date/Time", "Level", "Status")
tree = ttk.Treeview(root, columns=cols, show="headings", height=10)

for c in cols:
    tree.heading(c, text=c)
    tree.column(c, width=107, anchor="center")

tree.grid(row=9, column=0, columnspan=4, padx=10, pady=10)

# Load saved workouts
for workout in load_workouts():
    if isinstance(workout, dict):
        workout = tuple(workout.values())
    tree.insert("", "end", values=workout)


#-----------BUTTONS--------------#

btn_frame = tk.Frame(root)
btn_frame.grid(row=10, column=0, columnspan=4, pady=10)

tk.Button(btn_frame, text="ADD WORKOUT", command=add_workout).pack(side="left", padx=5)
tk.Button(btn_frame, text="MARK DONE", command=mark_done).pack(side="left", padx=5)
tk.Button(btn_frame, text="DELETE", command=delete_workout).pack(side="left", padx=5)
tk.Button(btn_frame, text="ANALYTICS", command=show_analytics).pack(side="left", padx=5)

#-----------RUN APP--------------#

toggle_theme()
check_notifications()
root.mainloop()
