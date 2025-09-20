import tkinter as tk
from tkinter import *
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import time
import os
import json

current_user = None

class User:
    def __init__(self,data_file="users.json"):
        self._data_file = data_file
        self._users = []
        self.load_users()
    
    def load_users(self):
        try:
            if os.path.exists(self._data_file): #check the user exist or not
                with open(self._data_file, 'r', encoding='utf-8') as file: #if exist, read the data
                    self._users = json.load(file)
            else:
                self._users = []
        except (json.JSONDecodeError, IOError) as e:
            messagebox.showerror("Error", f"Failed to load user data: {str(e)}")
            self._users = []
    
    def validate_user(self, user_id, password):
        for user in self._users:
            if user['id'] == user_id and user['password'] == password:
                return True
        return False
    
class ImportantScreen:
    def __init__(self, root):
        self.root = root
        self.frame = None
    
    def clear_screen(self):#clear screen
        for widget in self.root.winfo_children(): #loop all element
            widget.destroy()#remove element
    
    def add_background(self, image_path=None):
        try:
            if image_path and os.path.exists(image_path):
                background_image = tk.PhotoImage(file=image_path)
                background_label = tk.Label(self.root, image=background_image)
                background_label.place(x=0, y=0, relwidth=1, relheight=1)
                background_label.lower()
                self.root.background_image = background_image
            else:
                self.root.configure(bg="#f0f0f0")
        except Exception as e:
            print(f"Background adding error: {e}")
            self.root.configure(bg="#f0f0f0")

class WelcomeScreen(ImportantScreen): #inherit from importantscreen
    def show(self):
        self.clear_screen()
        self.add_background('C:/Users/User/Downloads/StudentAssistant/background_tarumt.png')
        
        main_frame = tk.Frame(self.root, bg="white", padx=20, pady=20)
        main_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        welcome_label = tk.Label(
            main_frame, 
            text="WELCOME TO", 
            font=('Helvetica', 18, 'bold'),
            bg="white",
            fg="#333333"
        )
        welcome_label.pack()
        
        school_app_label = tk.Label(
            main_frame, 
            text="STUDENT ASSISTANT APP", 
            font=('Helvetica', 20, 'bold'),
            bg="white",
            fg="#0066cc"
        )
        school_app_label.pack(pady=(5, 5))

        try:
            image = tk.PhotoImage(file='book.png')
            image_label = tk.Label(main_frame, image=image, bg="#f0f0f0")
            image_label.image = image
            image_label.pack(pady=20)
        except Exception as e:
            print(f"Image load error: {e}")

        get_started = tk.Button(
            main_frame,
            text="GET STARTED",
            command=self.get_started,
            bg="#0066cc",
            fg="white",
            activebackground="#004d99",
            font=('Arial', 12, 'bold'),
            bd=0,
            width=15,
            padx=10,
            pady=5
        )
        get_started.pack()
    
    def get_started(self):
        login_screen = LoginScreen(self.root)
        login_screen.show()

class LoginScreen(ImportantScreen):
    def __init__(self, root):
        super().__init__(root)
        self.user = User()

    def show(self):
        self.clear_screen()
        self.add_background('C:/Users/User/Downloads/StudentAssistant/background_tarumt.png')

        login_frame = tk.Frame(self.root, bg="white", padx=20, pady=20)
        login_frame.place(relx=0.5, rely=0.5, anchor="center")

        heading = tk.Label(login_frame, text='Login', bg="white", font=('Arial', 16, 'bold'))
        heading.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        tk.Label(login_frame, text="Student ID:", bg="white").grid(row=1, column=0, sticky="e", pady=5)
        self.stud_id = tk.Entry(login_frame, bd=5)
        self.stud_id.grid(row=1, column=1, pady=5, padx=10)

        tk.Label(login_frame, text="Password:", bg="white").grid(row=2, column=0, sticky="e", pady=5)
        self.stud_pass = tk.Entry(login_frame, bd=5, show="*")
        self.stud_pass.grid(row=2, column=1, pady=5, padx=10)

        login_btn = tk.Button(login_frame, text="Login", command=self.login, bd=6, width=15, bg="#3E8EDE")
        login_btn.grid(row=3, columnspan=2, pady=10)
    
    def login(self):
        global current_user

        user_id = self.stud_id.get().strip()
        password = self.stud_pass.get()

        if not user_id:
            messagebox.showerror("Error", "Student ID cannot be empty!")
            return
        
        if not password:
            messagebox.showerror("Error", "Password cannot be empty!")
            return
        
        if len(user_id) != 7 or not user_id.isdigit():
            messagebox.showerror("Error", "Student ID must be 7 digits!")
            return
        
        if self.user.validate_user(user_id, password):
            current_user = user_id
            messagebox.showinfo("Login Successful", f"Welcome {user_id}")
            home_screen = HomeScreen(self.root)
            home_screen.show()
        else:
            messagebox.showerror("Login Failed", "Invalid Student ID or Password")

class HomeScreen(ImportantScreen):
    def show(self):
        self.clear_screen()
        self.root.configure(bg='#f0f8ff')

        main_frame = Frame(self.root, bg='#f0f8ff')
        main_frame.pack(fill=BOTH, expand=True)

        navbar = Frame(main_frame, width=800, height=60, bg='light blue')
        navbar.pack(fill=X)

        tarumt_label = Label(navbar, text="TARUMT ", font=('Arial', 20, 'bold'), fg='#2c3e50', bg='light blue')
        tarumt_label.place(x=20, y=15)

        app_label = Label(navbar, text="Student Assistant", font=('Arial', 12), fg='#2c3e50', bg='light blue')
        app_label.place(x=140, y=24)

        datetimeLabel = Label(navbar, font=('Arial', 11), fg='#2c3e50', bg='light blue')
        datetimeLabel.place(relx=0.95, rely=0.5, anchor=E)

        self.job =None

        def update_datetime():
            current_time = time.strftime('%Y-%m-%d %I:%M:%S %p')
            datetimeLabel.config(text=current_time)
            self.job = datetimeLabel.after(1000, update_datetime)

        update_datetime()

        content_frame = Frame(self.root, width=800, height=440, bg='#f0f8ff')
        content_frame.place(x=0, y=60)

        welcome_label = Label(content_frame, text="✨ Welcome to Student Assistant ✨",font=('Arial', 24, 'bold'), fg='#2c3e50', bg='#f0f8ff')
        welcome_label.place(relx=0.5, y=40, anchor=CENTER)

        button_frame = Frame(content_frame, bg='#f0f8ff')
        button_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        def gpa_calculator():
            if self.job:
                datetimeLabel.after_cancel(self.job)
            self.root.destroy()
            import gpacalculation
            gpacalculation.main(current_user)

        gpa_btn = Button(button_frame, text="📊 GPA Calculator", font=('Arial', 14, 'bold'),bg="#afcde0", fg='#2c3e50', width=20, height=2, relief=RAISED, bd=3, command=gpa_calculator)
        gpa_btn.pack(pady=10)

        def timetable():
            if self.job:
                datetimeLabel.after_cancel(self.job)
            self.root.destroy()
            import timetable
            timetable.main(current_user)

        time_btn = Button(button_frame, text="📅 Timetable", font=('Arial', 14, 'bold'),bg="#8fbbe7", fg='#2c3e50', width=20, height=2, relief=RAISED, bd=3, command=timetable)
        time_btn.pack(pady=10)

        def logout():
            global current_user
            current_user = None
            welcome_screen = WelcomeScreen(self.root)
            welcome_screen.show()

        logout_btn = Button(button_frame, text="🚪Logout", font=('Arial', 14, 'bold'),bg="#81a3e6", fg='#2c3e50', width=20, height=2, relief=RAISED, bd=3, command=logout)
        logout_btn.pack(pady=10)

root = tk.Tk()
root.geometry('800x500')
root.title('TARUMT Student Assistant App')

try:
    icon_image = tk.PhotoImage(file='tarumt.png')
    root.iconphoto(False, icon_image)  
except:
    pass

#start with welcome screen
welcome_screen = WelcomeScreen(root)
welcome_screen.show()
    
def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit the application?"):
        root.destroy()
        exit()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()