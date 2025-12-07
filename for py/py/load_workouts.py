import json
import os
import tkinter as tk
from tkinter import messagebox, simpledialog, font

WORKOUT_FILE = "workouts.json"

def load_workouts():
    
    if not os.path.exists(WORKOUT_FILE):
        return {}
    try:
        with open(WORKOUT_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            # ensure it's a dict
            if isinstance(data, dict):
                return data
            return {}
    except (json.JSONDecodeError, OSError):
        # corrupted file or read error -> ignore and start fresh
        return {}

def save_workouts(workouts):
    """Save workouts to JSON file."""
    try:
        with open(WORKOUT_FILE, "w", encoding="utf-8") as f:
            json.dump(workouts, f, indent=2, ensure_ascii=False)
    except OSError as e:
        messagebox.showerror("Save error", f"Could not save workouts: {e}")

class WorkoutApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🏋️ Workout Plan App")
        self.root.geometry("500x400")
        self.center_window(500, 400)
        self.root.resizable(False, False)

        # Fonts
        self.title_font = font.Font(family="Helvetica", size=18, weight="bold")
        self.list_font = font.Font(family="Helvetica", size=12)
        self.btn_font = font.Font(family="Helvetica", size=10, weight="bold")

        # Title label
        title_label = tk.Label(root, text="🏋️ Workout Plan App", font=self.title_font, fg="#2E86C1")
        title_label.pack(pady=(15, 10))

        # Frame for listbox and scrollbar
        list_frame = tk.Frame(root)
        list_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        # Scrollbar
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Listbox
        self.listbox = tk.Listbox(
            list_frame,
            width=50,
            height=12,
            font=self.list_font,
            yscrollcommand=scrollbar.set,
            selectmode=tk.SINGLE
        )
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.listbox.yview)

        # Load workouts and refresh
        self.workouts = load_workouts()
        self.refresh_listbox()

        # Button frame
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=15)

        # Buttons of style
        btn_params = {
            "width": 12,
            "font": self.btn_font,
            "bg": "#2874A6",
            "fg": "white",
            "activebackground": "#1B4F72",
            "activeforeground": "white",
            "bd": 0,
            "relief": "ridge"
        }

        tk.Button(btn_frame, text="Add Workout", command=self.add_workout, **btn_params).grid(row=0, column=0, padx=8)
        tk.Button(btn_frame, text="Remove Workout", command=self.remove_workout, **btn_params).grid(row=0, column=1, padx=8)
        tk.Button(btn_frame, text="View Daily Plan", command=self.view_daily_plan, **btn_params).grid(row=0, column=2, padx=8)
        tk.Button(btn_frame, text="Exit", command=root.quit, **btn_params).grid(row=0, column=3, padx=8)

    def center_window(self, width, height):
        self.root.update_idletasks()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def refresh_listbox(self):
        self.listbox.config(state=tk.NORMAL)
        self.listbox.delete(0, tk.END)
        if not self.workouts:
            self.listbox.insert(tk.END, "No workouts found.")
            # keep listbox enabled so user can still scroll/click buttons
        else:
            for name, details in self.workouts.items():
                self.listbox.insert(tk.END, f"{name}: {details}")

    def add_workout(self):
        name = simpledialog.askstring("Add Workout", "Enter workout name:")
        if not name:
            return
        name = name.strip()
        if name in self.workouts:
            messagebox.showwarning("Warning", "Workout already exists.")
            return
        details = simpledialog.askstring("Add Workout", "Enter workout details (e.g., reps, sets):")
        if not details:
            return
        self.workouts[name] = details.strip()
        save_workouts(self.workouts)
        self.refresh_listbox()
        messagebox.showinfo("Success", f"Added workout '{name}'.")

    def remove_workout(self):
        selected = self.listbox.curselection()
        if not selected:
            messagebox.showwarning("Warning", "Select a workout to remove.")
            return
        # If the listbox shows placeholder "No workouts found.", handle that
        item_text = self.listbox.get(selected[0])
        if item_text == "No workouts found.":
            messagebox.showwarning("Warning", "No workouts to remove.")
            return
        workout = item_text.split(":")[0].strip()
        if workout in self.workouts:
            if messagebox.askyesno("Confirm", f"Remove workout '{workout}'?"):
                del self.workouts[workout]
                save_workouts(self.workouts)
                self.refresh_listbox()
                messagebox.showinfo("Removed", f"Removed workout '{workout}'.")

    def view_daily_plan(self):
        if not self.workouts:
            messagebox.showinfo("Daily Plan", "No workouts to show.")
            return
        plan = "\n".join(f"{i+1}. {name} - {details}" for i, (name, details) in enumerate(self.workouts.items()))
        messagebox.showinfo("Your Daily Workout Plan", plan)

if __name__ == "__main__":
    root = tk.Tk()
    app = WorkoutApp(root)
    # show a welcome/info box shortly after the window opens
    root.after(100, lambda: messagebox.showinfo("Welcome", "Welcome to Workout Plan App!\nUse 'Add Workout' to start."))
    root.mainloop()
