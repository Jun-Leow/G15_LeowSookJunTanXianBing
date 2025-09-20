import tkinter as tk
from tkinter import *
from tkinter import messagebox, ttk
import json
import os
from datetime import datetime, timedelta,date
from calendar import monthrange
from tkcalendar import DateEntry

DATA_FILE = "timetable.json"

class Timetable:
    def __init__(self, root, timetable_manager=None, current_user="guest"):
        self.root = root
        self.current_user = current_user
        self.timetable = []  #current user's event list
        self.time_slots = [
            "8:00-9:00", "9:00-10:00", "10:00-11:00", "11:00-12:00",
            "12:00-13:00", "13:00-14:00", "14:00-15:00", "15:00-16:00",
            "16:00-17:00", "17:00-18:00", "18:00-19:00", "19:00-20:00"
        ]
        self.color = {
            "Class": "#3498db", "Event": "#2ecc71",
            "Appointment": "#9b59b6", "Meeting": "#e74c3c", "Personal": "#f39c12"
        }
        self.current_view = "weekly"
        self.current_date = datetime.now()

        #UI references
        self.course = None
        self.date_var = None
        self.time_var = None
        self.location = None
        self.category_var = None
        self.participants_list = None
        self.timetable_frame = None
        self.canvas = None
        self.canvas_window = None
        self.date_label = None

    def load_all_data(self):
        #Read the whole json (return dict), if not exist return {}
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, dict):
                        return data
            except Exception:
                return {}
        return {}

    def save_all_data(self, data_dict):
        #Save the whole dict to file
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data_dict, f, indent=4, ensure_ascii=False)

    def load_timetable(self):
        data = self.load_all_data()
        my_events = data.get(self.current_user, [])
        #check participants
        for uid, events in data.items():
            if uid != self.current_user:
                for e in events:
                    if self.current_user in e.get("participants", []):
                        my_events.append(e)
        self.timetable = my_events
        #normalize participants
        for e in self.timetable:
            p = e.get("participants", [])
            if isinstance(p, str):
                e["participants"] = [x.strip() for x in p.split(",") if x.strip()]
                                     
    def save_timetable(self):
        #Update JSON with current user's timetable
        data = self.load_all_data()
        data[self.current_user] = self.timetable
        self.save_all_data(data)

    def load_users(self):
        #Read users.json and return user list
        if os.path.exists("users.json"):
            try:
                with open("users.json", "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, dict):
                        return data.get("users", [])
                    elif isinstance(data, list):
                        return data
            except Exception:
                return []
        return []
    
    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def timetable_screen(self):
        width = 800
        height = 650
        self.root.title("Timetable & Calendar")
        self.center_window(width, height)
        self.root.configure(bg="#f5f7fa")

        #icon
        try:
            icon_image = tk.PhotoImage(file='tarumt.png')
            self.root.iconphoto(False, icon_image)
        except:
            pass

        #main container
        main_frame = Frame(self.root, bg="#f5f7fa")
        main_frame.pack(fill=BOTH, expand=True, padx=8, pady=8)
        main_frame.rowconfigure(3, weight=1)
        main_frame.columnconfigure(0, weight=1)

        #Title row
        title_frame = Frame(main_frame, bg="#2c3e50", height=44)
        title_frame.grid(row=0, column=0, sticky="nsew", pady=(0,6))

        Label(title_frame, text="Your Timetable & Calendar",
              font=("Arial", 16, "bold"), fg="white", bg="#2c3e50").pack(side=LEFT, padx=10)
       
        Button(title_frame, text="❌ Exit", 
            bg="#e74c3c", fg="white", 
            command=self.exit, relief=FLAT, padx=10, pady=5).pack(side=RIGHT, padx=10, pady=6)

        Button(title_frame, text="📅 Today", 
            bg="#3498db", fg="white", 
            command=self.go_to_today, relief=FLAT, padx=10, pady=5).pack(side=RIGHT, padx=10, pady=6)
        
        #Input area (row 1)
        input_frame = Frame(main_frame, bg="#ecf0f1", relief=SOLID, bd=1)
        input_frame.grid(row=1, column=0, sticky="ew", pady=(0,6))
        input_frame.columnconfigure(0, weight=1)
        #row 1 (name/category/date)
        first_row = Frame(input_frame, bg="#ecf0f1")
        first_row.pack(fill=X, padx=6, pady=6)
        Label(first_row, text="Name:", bg="#ecf0f1").grid(row=0, column=0, sticky=W)
        self.course = Entry(first_row, width=20)
        self.course.grid(row=1, column=0, padx=4)
        Label(first_row, text="Category:", bg="#ecf0f1").grid(row=0, column=1, sticky=W)
        self.category_var = StringVar(value="Class")
        ttk.Combobox(first_row, textvariable=self.category_var, values=list(self.color.keys()),
                     width=12, state="readonly").grid(row=1, column=1, padx=4)
        Label(first_row, text="Date:", bg="#ecf0f1").grid(row=0, column=2, sticky=W)
        self.date_var = DateEntry(first_row, width=12, date_pattern="yyyy-mm-dd",mindate=date.today())
        self.date_var.grid(row=1, column=2, padx=4)

        #row 2 (time/location/participants/add)
        second_row = Frame(input_frame, bg="#ecf0f1")
        second_row.pack(fill=X, padx=6, pady=(0,8))
        Label(second_row, text="Time:", bg="#ecf0f1").grid(row=0, column=0, sticky=W)
        self.time_var = StringVar(value="Select Time")
        ttk.Combobox(second_row, textvariable=self.time_var, values=self.time_slots,
                     width=12, state="readonly").grid(row=1, column=0, padx=4)
        Label(second_row, text="Location:", bg="#ecf0f1").grid(row=0, column=1, sticky=W)
        self.location = Entry(second_row, width=18)
        self.location.grid(row=1, column=1, padx=4)

        Label(second_row, text="Participants:", bg="#ecf0f1").grid(row=0, column=2, sticky=W)
        users = self.load_users()
        user_id = [u["id"] for u in users]

        participants_frame = Frame(second_row, bg="#ecf0f1")
        participants_frame.grid(row=1, column=2, padx=4, pady=2, sticky=W)
        Label(second_row, text="(Hold Ctrl to select multiple)", 
        bg="#ecf0f1", fg="gray", font=("Arial", 8)).grid(row=2, column=2, padx=4, sticky=W)

        self.participants_list = Listbox(participants_frame, selectmode=EXTENDED, height=4, width=18, exportselection=False)
        self.participants_list.pack(side=LEFT, fill=BOTH)
        for uid in user_id:
            self.participants_list.insert(END, uid)
        p_scroll = Scrollbar(participants_frame, orient=VERTICAL, command=self.participants_list.yview)
        p_scroll.pack(side=RIGHT, fill=Y)
        self.participants_list.config(yscrollcommand=p_scroll.set)

       
        Label(second_row, text="(Hold Ctrl to select multiple)", 
      bg="#ecf0f1", fg="gray", font=("Arial", 8)).grid(row=2, column=2, padx=4, sticky=W)

# ✅ Category Legend
         # Category legend 放在右上角
        legend_frame = Frame(self.root, bg="#ecf0f1")
        legend_frame.pack(side=TOP, anchor="ne", padx=10, pady=5)

        Label(legend_frame, text="Category Colors:", bg="#ecf0f1", font=("Arial", 9, "bold")).pack(side=LEFT, padx=(0, 6))

        for cat, col in self.color.items():
            item = Frame(legend_frame, bg="#ecf0f1")
            item.pack(side=LEFT, padx=4)
            Canvas(item, width=14, height=14, bg=col, highlightthickness=1,
                   highlightbackground="black").pack(side=LEFT, padx=2)
            Label(item, text=cat, bg="#ecf0f1").pack(side=LEFT)
   
        Button(second_row, text="➕ Add Event", 
            bg="#27ae60", fg="white", 
            command=self.add_class, relief=FLAT, padx=10, pady=5).grid(row=1, column=3, padx=8)
        
        # navigation row (view + date)
        nav_frame = Frame(main_frame, bg="#f5f7fa")
        nav_frame.grid(row=2, column=0, sticky="ew", pady=(0,6))
        nav_frame.columnconfigure(0, weight=1)
        view_frame = Frame(nav_frame, bg="#f5f7fa")
        view_frame.pack(side=LEFT)
        view_var = StringVar(value=self.current_view)
        for text, value in [("Daily","daily"),("Weekly","weekly"),("Monthly","monthly")]:
            Radiobutton(view_frame, text=text, variable=view_var, value=value,
                        bg="#f5f7fa", command=lambda v=value: self.change_view(v)).pack(side=LEFT, padx=6)
        nav_btn_frame = Frame(nav_frame, bg="#f5f7fa")
        nav_btn_frame.pack(side=RIGHT)
        Button(nav_btn_frame, text="⬅️", 
            command=self.previous_date, relief=FLAT, padx=5).pack(side=LEFT, padx=4)

        self.date_label = Label(nav_btn_frame, text="", bg="#f5f7fa", font=("Arial",10,"bold"))
        self.date_label.pack(side=LEFT, padx=6)

        Button(nav_btn_frame, text="➡️", 
            command=self.next_date, relief=FLAT, padx=5).pack(side=LEFT, padx=4)
       
        #display area (row 3)
        display_container = Frame(main_frame, bg="#dbe8f5", relief=SOLID, bd=1)
        display_container.grid(row=3, column=0, sticky="nsew")
        display_container.rowconfigure(0, weight=1)
        display_container.columnconfigure(0, weight=1)

        #canvas + scroll
        scroll = Scrollbar(display_container, orient=VERTICAL)
        scroll.grid(row=0, column=1, sticky="ns")
        self.canvas = Canvas(display_container, bg="white", yscrollcommand=scroll.set)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        scroll.config(command=self.canvas.yview)

        self.timetable_frame = Frame(self.canvas, bg="white")
        self.canvas_window = self.canvas.create_window((0,0), window=self.timetable_frame, anchor="nw")
        self.timetable_frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)

        #load data + show UI
        self.load_timetable()
        self.update_date_label()
        self.refresh_timetable()

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_canvas_configure(self, event):
        #make frame same width as canvas
        try:
            self.canvas.itemconfig(self.canvas_window, width=event.width)
        except Exception:
            pass

    def add_class(self):
        name = self.course.get().strip()
        category = self.category_var.get()
        event_date = self.date_var.get_date().strftime("%Y-%m-%d")
        time = self.time_var.get()
        location = self.location.get().strip()

        if not name or not category or not event_date or time == "Select Time" or not location:
            messagebox.showerror("Error", "All fields are required")
            return

        #check conflict (same date + time)
        for e in self.timetable:
            if e["class_date"] == event_date and e["time"] == time:
                messagebox.showerror("Conflict", f"An event already exists at {event_date} {time}.")
                return

        selected_idx = self.participants_list.curselection()
        selected_participants = [self.participants_list.get(i) for i in selected_idx]
        participants = [self.current_user] + selected_participants
        #remove duplicates but keep order
        seen = set()
        participants = [p for p in participants if not (p in seen or seen.add(p))]

        data = {
            "course_name": name,
            "category": category,
            "class_date": event_date,
            "time": time,
            "location": location,
            "participants": participants,
            "added_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        self.timetable.append(data)
        self.save_timetable()
        self.refresh_timetable()

        #reset form
        self.course.delete(0, END)
        self.location.delete(0, END)
        self.participants_list.selection_clear(0, END)
        self.time_var.set("Select Time")
        self.category_var.set("Class")
        messagebox.showinfo("Success", "Event added successfully!")

    def show_event_details(self, event):
        top = Toplevel(self.root)
        top.title("Event Details")
        top.geometry("360x380")
        top.resizable(False, False)

        try:
            icon_image = tk.PhotoImage(file='tarumt.png')
            top.iconphoto(False, icon_image)
        except:
            pass

        frame = Frame(top, bg="white", relief=SOLID, bd=1)
        frame.pack(fill=BOTH, expand=True, padx=8, pady=8)
        participants_str = ", ".join(event.get("participants", [])) if isinstance(event.get("participants", []), list) else str(event.get("participants", ""))
        text = (f"Name: {event.get('course_name')}\n\n"
                f"Category: {event.get('category')}\n\n"
                f"Date: {event.get('class_date')}\n\n"
                f"Time: {event.get('time')}\n\n"
                f"Location: {event.get('location')}\n\n"
                f"Participants: {participants_str}\n\n"
                f"Added: {event.get('added_date')}")
        Label(frame, text=text, justify=LEFT, bg="white").pack(fill=BOTH, expand=True, padx=6, pady=6)
        btn_frame = Frame(frame, bg="white")
        btn_frame.pack(pady=6)
        Button(btn_frame, text="✏️ Edit", 
            bg="#f39c12", fg="white", 
            command=lambda e=event: [top.destroy(), self.edit_event(self.timetable.index(e), e)], 
            relief=FLAT, padx=10, pady=5).pack(side=LEFT, padx=6)

        Button(btn_frame, text="🗑️ Delete", 
            bg="#e74c3c", fg="white", 
            command=lambda: [top.destroy(), self.delete_event(event)], 
            relief=FLAT, padx=10, pady=5).pack(side=LEFT, padx=6)
        
    def edit_event(self, index, old_data):
        edit = Toplevel(self.root)
        edit.title("Edit Event")
        edit.geometry("420x520")
        edit.resizable(False, False)

        try:
            icon_image = tk.PhotoImage(file='tarumt.png')
            edit.iconphoto(False, icon_image)
        except:
            pass

        container = Frame(edit, bg="#f5f7fa")
        container.pack(fill=BOTH, expand=True, padx=8, pady=8)

        Label(container, text="Name:").pack(anchor=W, padx=6, pady=(4,0))
        name_entry = Entry(container)
        name_entry.insert(0, old_data.get("course_name",""))
        name_entry.pack(fill=X, padx=6, pady=2)

        Label(container, text="Category:").pack(anchor=W, padx=6, pady=(6,0))
        category_var = StringVar(value=old_data.get("category","Class"))
        ttk.Combobox(container, textvariable=category_var, values=list(self.color.keys()), state="readonly").pack(fill=X, padx=6, pady=2)

        Label(container, text="Date:").pack(anchor=W, padx=6, pady=(6,0))
        date_var = DateEntry(container, date_pattern="yyyy-mm-dd")
        try:
            date_var.set_date(datetime.strptime(old_data.get("class_date",""), "%Y-%m-%d"))
        except Exception:
            pass
        date_var.pack(fill=X, padx=6, pady=2)

        Label(container, text="Time:").pack(anchor=W, padx=6, pady=(6,0))
        time_var = StringVar(value=old_data.get("time","Select Time"))
        ttk.Combobox(container, textvariable=time_var, values=self.time_slots, state="readonly").pack(fill=X, padx=6, pady=2)

        Label(container, text="Location:").pack(anchor=W, padx=6, pady=(6,0))
        location_entry = Entry(container)
        location_entry.insert(0, old_data.get("location",""))
        location_entry.pack(fill=X, padx=6, pady=2)

        Label(container, text="Participants:").pack(anchor=W, padx=6, pady=(6,0))
        users = self.load_users()
        user_id = [u["id"] for u in users]
        participants_list_edit = Listbox(container, selectmode=EXTENDED, height=6, exportselection=False)
        participants_list_edit.pack(fill=X, padx=6, pady=2)
        for uid in user_id:
            participants_list_edit.insert(END, uid)
        existing = old_data.get("participants", [])
        if isinstance(existing, str):
            existing = [x.strip() for x in existing.split(",") if x.strip()]
        for i, uid in enumerate(user_id):
            if uid in existing:
                participants_list_edit.selection_set(i)

        def save_changes():
            name = name_entry.get().strip()
            category = category_var.get()
            date = date_var.get_date().strftime("%Y-%m-%d")
            time = time_var.get()
            location = location_entry.get().strip()
            selected_idx = participants_list_edit.curselection()
            participants = [participants_list_edit.get(i) for i in selected_idx]
            participants = [self.current_user] + participants
            #remove duplicates while keeping order
            seen = set()
            participants = [p for p in participants if not (p in seen or seen.add(p))]

            if not name or not category or not date or time == "Select Time" or not location or not participants:
                messagebox.showerror("Error", "All fields are required")
                return

            #conflict check (ignore the event currently being edited)
            for i, e in enumerate(self.timetable):
                if i != index and e["class_date"] == date and e["time"] == time:
                    messagebox.showerror("Conflict", f"An event already exists at {date} {time}.")
                    return

            new_data = {
                "course_name": name,
                "category": category,
                "class_date": date,
                "time": time,
                "location": location,
                "participants": participants,
                "added_date": old_data.get("added_date", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            }
            self.timetable[index] = new_data
            self.save_timetable()
            self.refresh_timetable()
            edit.destroy()
            messagebox.showinfo("Success", "Event updated successfully!")

        Button(container, text="💾 Save Changes",bg="#27ae60", fg="white",relief=FLAT, padx=10, pady=5,command=save_changes).pack(pady=8)
        
    def delete_event(self, event):
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this event?"):
            self.timetable = [e for e in self.timetable if e != event]
            self.save_timetable()
            self.refresh_timetable()
            messagebox.showinfo("Deleted", "Event removed")

    #---------------- navigation ----------------
    def change_view(self, v):
        self.current_view = v
        self.update_date_label()
        self.refresh_timetable()

    def previous_date(self):
        if self.current_view == "daily":
            self.current_date -= timedelta(days=1)
        elif self.current_view == "weekly":
            self.current_date -= timedelta(weeks=1)
        elif self.current_view == "monthly":
            year = self.current_date.year
            month = self.current_date.month - 1
            if month == 0:
                month = 12; year -= 1
            self.current_date = self.current_date.replace(year=year, month=month)
        self.update_date_label()
        self.refresh_timetable()

    def next_date(self):
        if self.current_view == "daily":
            self.current_date += timedelta(days=1)
        elif self.current_view == "weekly":
            self.current_date += timedelta(weeks=1)
        elif self.current_view == "monthly":
            year = self.current_date.year
            month = self.current_date.month + 1
            if month == 13:
                month = 1; year += 1
            self.current_date = self.current_date.replace(year=year, month=month)
        self.update_date_label()
        self.refresh_timetable()

    def go_to_today(self):
        self.current_date = datetime.now()
        self.update_date_label()
        self.refresh_timetable()

    def update_date_label(self):
        if self.current_view == "daily":
            self.date_label.config(text=self.current_date.strftime("%A, %B %d, %Y"))
        elif self.current_view == "weekly":
            start = self.current_date - timedelta(days=self.current_date.weekday())
            end = start + timedelta(days=6)
            self.date_label.config(text=f"{start.strftime('%b %d')} - {end.strftime('%b %d, %Y')}")
        else:
            self.date_label.config(text=self.current_date.strftime("%B %Y"))

    def refresh_timetable(self):
        #clear old widgets
        for w in self.timetable_frame.winfo_children():
            w.destroy()
        if self.current_view == "daily":
            self.show_daily(self.timetable)
        elif self.current_view == "weekly":
            self.show_weekly_grid(self.timetable)
        else:
            self.show_monthly_grid(self.timetable)

    def show_daily(self, timetable):
        header = Frame(self.timetable_frame, bg="#34495e", height=30)
        header.pack(fill=X)
        Label(header, text="Time", fg="white", bg="#34495e", width=14).pack(side=LEFT)
        Label(header, text="Event", fg="white", bg="#34495e").pack(side=LEFT, fill=X, expand=True)

        today = self.current_date.strftime("%Y-%m-%d")
        if today == datetime.now().strftime("%Y-%m-%d"):
            Label(header, text="Time (Today)", fg="white", bg="#34495e", width=14).pack(side=LEFT)
        else:
            Label(header, text="Time", fg="white", bg="#34495e", width=14).pack(side=LEFT)

        Label(header, text="Event", fg="white", bg="#34495e").pack(side=LEFT, fill=X, expand=True)
        
        for i, slot in enumerate(self.time_slots):
            row = Frame(self.timetable_frame, bg="#ecf0f1" if i % 2 == 0 else "white", height=36, relief=SOLID, bd=1)
            row.pack(fill=X)
            Label(row, text=slot, width=14, bg=row.cget("bg")).pack(side=LEFT)
            evs = [e for e in timetable if e["class_date"] == today and e["time"] == slot]
            if evs:
                ev = evs[0]
                Button(row, text=ev["course_name"], bg=self.color.get(ev["category"], "#7f8c8d"),
                       fg="white", relief=FLAT, command=lambda e=ev: self.show_event_details(e)).pack(side=LEFT, fill=X, expand=True)

    def show_weekly_grid(self, timetable):
        start = self.current_date - timedelta(days=self.current_date.weekday())
        days = [start + timedelta(days=i) for i in range(7)]

        # header row
        for c in range(8):
            self.timetable_frame.grid_columnconfigure(c, weight=1, uniform="col")
        Label(self.timetable_frame, text="Time", bg="#34495e", fg="white", relief=SOLID).grid(row=0, column=0, sticky="nsew")
        for i, d in enumerate(days, start=1):
            Label(self.timetable_frame, text=d.strftime("%a\n%d"), bg="#34495e", fg="white", relief=SOLID).grid(row=0, column=i, sticky="nsew")

    # time slots
        for r, slot in enumerate(self.time_slots, start=1):
            Label(self.timetable_frame, text=slot, relief=SOLID, anchor="w").grid(row=r, column=0, sticky="nsew")
            self.timetable_frame.grid_rowconfigure(r, weight=1, uniform="row")
            for c, d in enumerate(days, start=1):
                day_str = d.strftime("%Y-%m-%d")
            # today highlight
                bg = "#ffeaa7" if d.date() == datetime.now().date() else "white"
                cell = Frame(self.timetable_frame, relief=SOLID, bd=1, bg=bg)
                cell.grid(row=r, column=c, sticky="nsew")
            # find events
                evs = [e for e in timetable if e["class_date"] == day_str and e["time"] == slot]
                if evs:
                    ev = evs[0]
                    Button(cell, text=ev["course_name"], bg=self.color.get(ev["category"], "#7f8c8d"),
                        fg="white", relief=FLAT, wraplength=120,
                        command=lambda e=ev: self.show_event_details(e)).pack(fill=BOTH, expand=True, padx=2, pady=2)

    def show_monthly_grid(self, timetable):
        year, month = self.current_date.year, self.current_date.month
        days_in_month = monthrange(year, month)[1]
        first_day = datetime(year, month, 1).weekday()  # Monday=0

        for c in range(7):
            self.timetable_frame.grid_columnconfigure(c, weight=1, uniform="mcol")
        for r in range(7):
            self.timetable_frame.grid_rowconfigure(r, weight=1, uniform="mrow")

        weekdays = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
        for i, wd in enumerate(weekdays):
            Label(self.timetable_frame, text=wd, bg="#34495e", fg="white", relief=SOLID).grid(row=0, column=i, sticky="nsew")

        day = 1
        row_idx = 1
        col_idx = first_day
        while day <= days_in_month:
            cell = Frame(self.timetable_frame, relief=SOLID, bd=1)
            cell.grid(row=row_idx, column=col_idx, sticky="nsew")

        # highlight today
            bg = "#ffeaa7" if datetime(year, month, day).date() == datetime.now().date() else "white"
            Label(cell, text=str(day), anchor="ne", bg=bg).pack(fill=X)

            day_str = f"{year}-{month:02d}-{day:02d}"
            evs = [e for e in timetable if e["class_date"] == day_str]
            for ev in evs[:3]:
                Button(cell, text=ev["course_name"], bg=self.color.get(ev["category"], "#7f8c8d"),
                    fg="white", relief=FLAT, command=lambda e=ev: self.show_event_details(e)).pack(fill=X, padx=2, pady=1)

            day += 1
            col_idx += 1
            if col_idx == 7:
                col_idx = 0
                row_idx += 1

    def exit(self):
        self.root.destroy()
        from home import HomeScreen
        home_root = tk.Tk()
        home_root.geometry('800x500')
        home_root.title('TARUMT Student Assistant App')
        
        try:
            icon_image = tk.PhotoImage(file='tarumt.png')
            home_root.iconphoto(False, icon_image)
        except:
            pass
        
        home_screen = HomeScreen(home_root)
        home_screen.show()
        
        home_root.mainloop()

def main(user_id="guest"):
    root = tk.Tk()
    app = Timetable(root, None, user_id)
    app.load_timetable()
    app.timetable_screen()

    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit the application?"):
            root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()