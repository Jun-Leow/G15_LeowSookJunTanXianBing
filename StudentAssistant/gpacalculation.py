import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox
import json
import os
from datetime import datetime
import copy

class GPACalculator:
    
    def __init__(self, root, current_user="guest"):
        self.root = root
        self.current_user = current_user
        self.courses = []
        self.semesters ={}
        self.current_semester ="Semester 1"
        self.semester_options = ["Semester 1", "Semester 2", "Semester 3", "Semester 4", "Semester 5", "Semester 6"]
        self.grade_points = {
            "A": 4.0, "A-": 3.7, "B+": 3.3, "B": 3.0, "B-": 2.7,
            "C+": 2.3, "C": 2.0, "C-": 1.7, "D+": 1.3, "D": 1.0, "F": 0.0
        }
        
        self.total_credit = tk.StringVar(value="0")
        self.total_point = tk.StringVar(value="0")
        self.gpa = tk.StringVar(value="0.00")
        self.cgpa = tk.StringVar(value="0.00")
        self.grade = tk.StringVar(value="A")
        self.semester_var = tk.StringVar(value="Semester 1")
        
        self.ui()
        self.load_courses()
        self.refresh_course()
    
    def get_current_user(self):
        return self.current_user
    
    def set_current_user(self, value):
        self.current_user = value
        self.load_courses()
        self.refresh_course()
    
    def get_courses(self):
        return copy.deepcopy(self.courses)
    
    def get_total_credits(self):
        return int(self.total_credit.get())
    
    def get_total_points(self):
        return float(self.total_point.get())
    
    def get_gpa(self):
        return float(self.gpa.get())
    
    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def ui(self):
        width = 800
        height = 650
        self.root.title('TARUMT Student Assistant App - GPA Calculator')
        self.center_window(width, height)
        
        #icon
        try:
            icon_image = tk.PhotoImage(file='tarumt.png')
            self.root.iconphoto(False, icon_image)
        except:
            pass
        
        self.root.configure(bg='#dbe8f5')
        
        main_frame = Frame(self.root, bg='#dbe8f5')
        main_frame.pack(fill=BOTH, expand=True, padx=20, pady=10)

        # gpa window title
        title_label = Label(main_frame, text="GPA Calculator",font=('Arial', 20, 'bold'), fg='#2c3e50', bg="#dbe8f5")
        title_label.pack(pady=20)

        #user 
        user_info = Label(main_frame, text=f"User: {self.current_user}",font=('Arial', 12, 'bold'), fg='#2c3e50', bg="#dbe8f5")
        user_info.pack(pady=5)

        semester_frame = Frame(main_frame, bg="#dbe8f5")
        semester_frame.pack(fill=X, pady=10)

        #choose semester that you want
        choose_semester = Label(semester_frame,text="Semester:",font=('Arial',10,'bold'),bg="#dbe8f5")
        choose_semester.grid(row=0, column=0, padx=5, pady=5, sticky=W)
        semester_combo = Combobox(semester_frame,textvariable=self.semester_var,values=self.semester_options,width=12,state="readonly",font=('Arial',10))
        semester_combo.grid(row=0, column=1, padx=5, pady=5)
        semester_combo.bind("<<ComboboxSelected>>", self.change_semester)

        # go to previous semester
        pre_semester = Button(semester_frame,text="<== Previous Semester",font=('Arial', 10, 'bold'),bg= "#2ecc71", fg='black',command=self.previous_semester,pady=3)
        pre_semester.grid(row=0, column=2, padx=10, pady=5)

        #view the all semester and overall
        view_semester = Button(semester_frame,text="View Semester Summary",font=('Arial',10,'bold'),bg="#9b59b6",fg='black',command=self.show_semester_summary,pady=3)
        view_semester.grid(row=0, column=3, padx=10, pady=2)

        # go to next semester
        next_semester = Button(semester_frame,text="Next Semester ==>",font=('Arial', 10, 'bold'),bg= "#2ecc71", fg='black',command=self.next_semester,pady=3)
        next_semester.grid(row=0, column=4, padx=10, pady=5)
        
        input_frame = Frame(main_frame, bg="#dbe8f5")
        input_frame.pack(fill=X, pady=10)
        
        # input course name
        course_label = Label(input_frame, text="Course Name: ",font=('Arial', 10, 'bold'), bg='#dbe8f5',fg='black')
        course_label.grid(row=0, column=0, padx=5, pady=5, sticky=W)
        self.course_name = Entry(input_frame, font=('Arial', 10), width=20)
        self.course_name.grid(row=1, column=0, padx=5, pady=5)
        
        #input credit
        credit_label = Label(input_frame, text="Credits:",font=('Arial', 10, 'bold'), bg='#dbe8f5',fg='black')
        credit_label.grid(row=0, column=1, padx=5, pady=5, sticky=W)
        self.credits = Spinbox(input_frame, from_=1, to=10, font=('Arial', 10), width=8)
        self.credits.grid(row=1, column=1, padx=5, pady=5)
        self.credits.delete(0, END)
        self.credits.insert(0, "3")
        
        # input grade
        grade_label = Label(input_frame, text="Grade:", font=('Arial', 10, 'bold'), bg='#dbe8f5',fg='black')
        grade_label.grid(row=0, column=2, padx=5, pady=5, sticky=W)
        grade_list = Combobox(input_frame,textvariable=self.grade,values=list(self.grade_points.keys()),width=5)
        grade_list.config(font=('Arial', 10))
        grade_list.grid(row=1, column=2, padx=5, pady=5)
        
        #add course
        add_btn = Button(input_frame, text="Add Course", font=('Arial', 10, 'bold'),bg='#3498db', fg='black', command=self.add_course)
        add_btn.grid(row=1, column=3, padx=10, pady=5)

        #edit course
        edit_btn = Button(input_frame,text="Edit Selected Course",font=('Arial',10,'bold'),bg="#f39c12", fg='black', command=self.edit_selected, padx=10)
        edit_btn.grid(row=1, column=4, padx=10, pady=5)

        #course list frame
        list_container = Frame(main_frame, bg='#dbe8f5')
        list_container.pack(fill=BOTH, expand=True, pady=10)

        #header
        header_frame = Frame(list_container, bg='#3498db')
        header_frame.pack(fill=X)
        
        headers = ["Course Name", "Credits", "Grade", "Grade Points","Semester"]
        column_widths = [20, 8, 8, 12,12]
        
        for i, (header, width) in enumerate(zip(headers, column_widths)):
            if i == 0: #id
                label = Label(header_frame, text=header.ljust(width), #put the word from left and no any space
                             font=('Arial', 12, 'bold'), bg='#3498db', 
                             fg='black', padx=0, anchor='w')# w is west. write from left first
                label.pack(side=LEFT, padx=(10, 0))
            elif i == len(headers) - 1: #semester
                label = Label(header_frame, text=header.rjust(width), #put the word from right and no any space
                             font=('Arial', 12, 'bold'), bg='#3498db', 
                             fg='black', padx=0, anchor='e')#e is east. write from right
                label.pack(side=RIGHT, padx=(0, 10))
            else:
                label = Label(header_frame, text=header.center(width), 
                             font=('Arial', 12, 'bold'), bg='#3498db', 
                             fg='black', padx=0, anchor='center')
                label.pack(side=LEFT, expand=True, fill=X)
        
        #list
        list_frame = Frame(list_container, bg='#dbe8f5')
        list_frame.pack(fill=BOTH, expand=True)
        
        #course list
        self.course_list = Listbox(list_frame, font=('Courier New', 10),height=8, selectmode=SINGLE) #only can choose one
        
        #can see the below course 
        scrollbar = Scrollbar(list_frame)
        scrollbar.pack(side=RIGHT, fill=Y)
        
        self.course_list.pack(side=LEFT, fill=BOTH, expand=True)
        self.course_list.config(yscrollcommand=scrollbar.set) #scrollbar can control list
        scrollbar.config(command=self.course_list.yview) #list can control scrollbar, put scrollbar and course list together
        
        # every data
        result_frame = Frame(main_frame, bg='#dbe8f5')
        result_frame.pack(fill=X, pady=10)

        #your now semester gpa
        gpa_calc = Label(result_frame,text="Current Semester GPA:",font=('Arial', 12, 'bold'), bg="#dbe8f5")
        gpa_calc.grid(row=0, column=0, padx=10, pady=5, sticky=W)
        self.gpa_display = Label(result_frame,textvariable=self.gpa,font=('Arial', 12, 'bold'), fg="#3498db",bg="#dbe8f5")
        self.gpa_display.grid(row=0, column=1, padx=10, pady=5, sticky=W)

        #cgpa 
        cgpa_calc = Label(result_frame,text="Current Semester CGPA:",font=('Arial', 12, 'bold'), bg="#dbe8f5")
        cgpa_calc.grid(row=0, column=2, padx=10, pady=5, sticky=W)
        self.cgpa_display = Label(result_frame,textvariable=self.cgpa,font=('Arial', 12, 'bold'), fg="#3498db",bg="#dbe8f5")
        self.cgpa_display.grid(row=0, column=3, padx=10, pady=5, sticky=W)
        
        #total credit
        credit_label = Label(result_frame, text="Total Credits:",font=('Arial', 12, 'bold'), bg='#dbe8f5')
        credit_label.grid(row=1, column=0, padx=10, pady=5, sticky=W)
        total_credits = Label(result_frame, textvariable=self.total_credit,font=('Arial', 12, 'bold'), fg="#34495e", bg='#dbe8f5')
        total_credits.grid(row=1, column=1, padx=10, pady=5, sticky=W)
        
        #grade point
        points_label = Label(result_frame, text="Total Grade Points:",font=('Arial', 12, 'bold'), bg='#dbe8f5')
        points_label.grid(row=1, column=2, padx=10, pady=5, sticky=W)
        total_points = Label(result_frame, textvariable=self.total_point,font=('Arial', 12, 'bold'), fg="#34495e", bg='#dbe8f5')
        total_points.grid(row=1, column=3, padx=10, pady=5, sticky=W)
        
        #button frame
        buttons_frame = Frame(main_frame, bg='#dbe8f5')
        buttons_frame.pack(pady=10)
        
        #back button
        back_btn = Button(buttons_frame, text="Exit", font=('Arial', 12, 'bold'), bg='white', fg='black', command=self.exit)
        back_btn.grid(row=0, column=0, padx=5)
        
        #calculate GPA button
        calc_btn = Button(buttons_frame, text="Calculate GPA", font=('Arial', 12, 'bold'), bg='light green', fg='black', command=self.calculate_gpa)
        calc_btn.grid(row=0, column=1, padx=5)
        
        #clear all button
        clear_btn = Button(buttons_frame, text="Clear All", font=('Arial', 12, 'bold'), bg="#f57b56", fg='black', command=self.clear_all)
        clear_btn.grid(row=0, column=2, padx=5)
        
        #delete selected button
        delete_btn = Button(buttons_frame, text="Delete Selected", font=('Arial', 12, 'bold'), bg="#f6fb90", fg='black', command=self.delete_selected)
        delete_btn.grid(row=0, column=3, padx=5)

    def load_courses(self):
        self.courses = []
        self.semesters = {}
        
        if os.path.exists('courses.json'):
            try:
                with open('courses.json', 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    self.courses = data.get(self.current_user, [])

                    for course in self.courses:
                        semester = course.get('semester','Semester 1')
                        if semester not in self.semesters:
                            self.semesters[semester] = []
                        self.semesters[semester].append(course)

                    self.courses = self.semesters.get(self.current_semester,[])
            except (json.JSONDecodeError, IOError):
                self.courses = []
                self.semesters = {}
        else:
            self.courses = []
            self.semesters = {}
    
    def save_courses(self):
        try:
            #combine all course in one semester
            all_course = []
            for semester_course in self.semesters.values():
                if isinstance(semester_course,list):
                    all_course.extend(semester_course)

            data = {}
            if os.path.exists('courses.json'):
                with open('courses.json', 'r', encoding='utf-8') as file:
                    try:
                        data = json.load(file)
                    except json.JSONDecodeError:
                        data = {}
            
            data[self.current_user] = all_course
            
            with open('courses.json', 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
        
        except IOError as e:
            messagebox.showerror("Error:", f"Failed to save course data: {str(e)}")
    
    #refresh course
    def refresh_course(self):
          self.course_list.delete(0, END)
          for course in self.semesters.get(self.current_semester, []):
            format_course = f"{course['course']:<20}{course['credits']:>12}{course['grade']:>16}{course['points']:>24.1f}{course['semester']:>20}"
            self.course_list.insert(END, format_course)
    
    #add course
    def add_course(self):
        course = self.course_name.get().strip()
        credit_value = self.credits.get()
        grade_value = self.grade.get()
        
        if not course or not credit_value or not grade_value:
            messagebox.showerror("Error", "Please fill in all fields.")
            return
        
        if len(course) > 20:
            messagebox.showerror("Error", "Course name cannot more than 20 characters.")
            return
        
        #to validate the course name is exist or not in the same semester
        for existing_course in self.semesters.get(self.current_semester, []):
            if existing_course['course'].lower() == course.lower():
                messagebox.showerror("Duplicate Course",f"Course '{course}' already exists in this semester")
                return
        
        if not credit_value:
            messagebox.showerror("Error", "Please enter credit hours")
            self.credits.focus()
            return
        
        if self.current_semester not in self.semesters:
            self.semesters[self.current_semester] = []

        
        try:
            credit_num = int(credit_value)
            if credit_num <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Credits must be a positive integer")
            self.credits.focus()
            return
        
        if credit_num >=20:
            messagebox.showerror("Error", "Credits must be between 1-20")
            self.credits.focus()
            return
        
        if grade_value not in self.grade_points:
            messagebox.showerror("Error", "Please select a valid grade")
            return
        
        #calculate grade point
        points = self.grade_points[grade_value] * credit_num
        
        course_data = {
            "course": course,
            "credits": credit_num,
            "grade": grade_value,
            "points": points,
            "semester": self.current_semester,
            "added_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        #update semester data
        if self.semester_var.get() not in self.semesters:
            self.semesters[self.semester_var.get()]=[]
        self.semesters[self.semester_var.get()].append(course_data)

        self.save_courses()
        self.courses = self.semesters[self.current_semester]  

        self.refresh_course()
        
        #clear input
        self.course_name.delete(0, END)
        self.credits.delete(0, END)
        self.credits.insert(0, "3")
        self.grade.set("A")
        self.course_name.focus()

        self.calculate_gpa()

    def edit_selected(self):
        select = self.course_list.curselection() #the id that u choose
        if not select:
            messagebox.showwarning("Warning", "Please select a course to edit")
            return
        
        index = select[0]
        if 0 <= index < len(self.courses):
            course_edit = self.courses[index]

            #edit window
            edit_window = Toplevel(self.root)
            edit_window.title("Edit Course")
            edit_window.geometry("400x250")
            edit_window.configure(bg="#dbe8f5")
            edit_window.transient(self.root) #this window will at the above of the main window
            edit_window.grab_set() # use this window first , cannot use the main window

            #center the window
            screen_width = edit_window.winfo_screenwidth()
            screen_height = edit_window.winfo_screenheight()
            x = (screen_width - 400) // 2
            y = (screen_height - 250) // 2
            edit_window.geometry(f'400x250+{x}+{y}')

            try:
                icon_image = tk.PhotoImage(file='tarumt.png')
                edit_window.iconphoto(False, icon_image)  
            except:
                pass

            #edit window title
            edit_title = Label(edit_window,text="Edit Course",font=('Arial', 14, 'bold'), fg="#2c3e50",bg="#dbe8f5")
            edit_title.pack(pady=10)

            #course name
            name_frame = Frame(edit_window, bg="#dbe8f5")
            name_frame.pack(fill=X, padx=20, pady=5)

            course_name = Label(name_frame,text="Course Name:",font=('Arial', 10), bg="#dbe8f5")
            course_name.pack(side=LEFT)
            name_var = StringVar(value=course_edit['course'])
            name_entry = Entry(name_frame, textvariable=name_var, font=('Arial', 10))
            name_entry.pack(side=RIGHT, fill=X, padx=(10, 0))
            name_entry.focus()

            #credit
            credit_frame = Frame(edit_window, bg="#dbe8f5")
            credit_frame.pack(fill=X, padx=20, pady=5)

            credit_hour = Label(credit_frame,text="Credit:",font=('Arial', 10), bg="#dbe8f5")
            credit_hour.pack(side=LEFT)
            credit_var = StringVar(value=str(course_edit['credits']))
            credit_spin = Spinbox(credit_frame, from_=1, to=10, textvariable=credit_var,font=('Arial', 10), width=8)
            credit_spin.pack(side=RIGHT, padx=(10, 0))

            #grade
            grade_frame = Frame(edit_window, bg="#dbe8f5")
            grade_frame.pack(fill=X, padx=20, pady=5)

            grade = Label(grade_frame,text="Grade:",font=('Arial', 10), bg="#dbe8f5")
            grade.pack(side=LEFT)
            grade_var = StringVar(value=course_edit['grade']) #use grade var to store grade
            # can dropdown the list of different grade
            grade_combo = Combobox(grade_frame, textvariable=grade_var,values=list(self.grade_points.keys()),width=5, font=('Arial', 10), state="readonly") 
            grade_combo.pack(side=RIGHT, padx=(10, 0)) #dropdown on right

            #semester
            semester_frame = Frame(edit_window, bg="#dbe8f5")
            semester_frame.pack(fill=X, padx=20, pady=5)

            semester = Label(semester_frame,text="Semester:",font=('Arial', 10), bg="#dbe8f5")
            semester.pack(side=LEFT)
            semester_var = StringVar(value=course_edit.get('semester', 'Semester 1'))
            semester_combo = Combobox(semester_frame, textvariable=semester_var,values=self.semester_options,width=12, font=('Arial', 10), state="readonly")
            semester_combo.pack(side=RIGHT, padx=(10, 0))

            def save_change():
                new_course_name = name_var.get().strip()
                if not new_course_name:
                    messagebox.showerror("Error", "Course name cannot be empty")
                    return
                
                if len(new_course_name) > 20:
                    messagebox.showerror("Error", "Course name cannot exceed 20 characters.")
                    return
                
                try:
                    new_credit = int(credit_var.get())
                    if new_credit <= 0:
                        raise ValueError
                except ValueError:
                    messagebox.showerror("Error", "Credits must be a positive integer")
                    return
                
                if grade_var.get() not in self.grade_points:
                    messagebox.showerror("Error", "Please select a valid grade")
                    return
                
                #calculate new point
                new_point = self.grade_points[grade_var.get()]*new_credit

                #new semester
                new_semester = semester_var.get()

                #check if move to another semester
                original_semester = course_edit.get('semester', self.current_semester)

                #update course data
                course_edit['course'] = new_course_name
                course_edit['credits'] = new_credit
                course_edit['grade'] = grade_var.get()
                course_edit['points'] = new_point
                course_edit['semester'] = new_semester
                course_edit['modified_date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                #move the course when the semester is change
                if original_semester != new_semester:
                    #remove the course from the original semester
                    if original_semester in self.semesters:
                        for i,course in enumerate(self.semesters[original_semester]):
                            #find have or not
                            if course.get("added_date") == course_edit.get("added_date"):
                                self.semesters[original_semester].pop(i)#get it and remove it
                                break

                    #add to new semester
                    if new_semester not in self.semesters:
                        self.semesters[new_semester] = []
                    self.semesters[new_semester].append(course_edit)

                    #remove if current semester is not the new semester
                    if self.current_semester != new_semester:
                        self.courses.pop(index)
                self.save_courses()
                self.refresh_course()
                self.calculate_gpa()
                edit_window.destroy()
                messagebox.showinfo("Success", "Course updated successfully")

            save = Button(edit_window,text="Save Change", font=('Arial', 10),bg= "#3498db", fg='white', command=save_change)
            save.pack(pady=10)

    #change the semester
    def change_semester(self, event=None):
        self.current_semester = self.semester_var.get()
        self.courses = self.semesters.get(self.current_semester, [])
        self.refresh_course()
        self.calculate_gpa()

    def previous_semester(self):
        #save the semester data first
        self.save_courses()

        #find semester index
        current_index = self.semester_options.index(self.current_semester)

        #check have previous semester or not
        if current_index > 0:
            prev_semester = self.semester_options[current_index - 1]
            self.semester_var.set(prev_semester)
            self.change_semester()
            messagebox.showinfo("Previous Semester", f"Now viewing {prev_semester}")
        else:
            messagebox.showinfo("Info", "You are already in the first semester")
    
    # calculate gpa in the semester
    def calculate_gpa(self):
        semester_credits = 0
        semester_points = 0.0
        
        for course in self.courses:
            semester_credits += course["credits"]
            semester_points += course["points"]
        
        self.total_credit.set(str(semester_credits))
        self.total_point.set(f"{semester_points:.1f}")
        
        if semester_credits > 0:
            semester_gpa = semester_points / semester_credits
            self.gpa.set(f"{semester_gpa:.2f}")
            
            if semester_gpa >= 3.5:
                self.gpa_display.config(fg='green')
            elif semester_gpa >= 2.0:
                self.gpa_display.config(fg='blue')
            else:
                self.gpa_display.config(fg='red')
        else:
            self.gpa.set("0.00")
            self.gpa_display.config(fg='black')

        #calculate cgpa
        total_credits = 0
        total_points = 0.0

        for semester_courses in self.semesters.values(): #all semester
            for course in semester_courses: #course in one semester
                total_credits += course["credits"]
                total_points += course["points"]
        
        if total_credits > 0:
            cgpa = total_points / total_credits
            self.cgpa.set(f"{cgpa:.2f}")
        else:
            self.cgpa.set("0.0")

    #go to next semester
    def next_semester(self):
        #save the semester data first
        self.save_courses()

        #find semester index
        current_index = self.semester_options.index(self.current_semester)

        #check have next semester or not
        if current_index < len(self.semester_options) -1:
            next_semester = self.semester_options[current_index+1]
            self.semester_var.set(next_semester)
            self.change_semester()
            messagebox.showinfo("Next Semester", f"Now viewing {next_semester}")
        else:
            messagebox.showinfo("Info", "You are already in the final semester")
    
    # calculate gpa in the semester
    def calculate_gpa(self):
        semester_credits = 0
        semester_points = 0.0
        
        for course in self.courses:
            semester_credits += course["credits"]
            semester_points += course["points"]
        
        self.total_credit.set(str(semester_credits))
        self.total_point.set(f"{semester_points:.1f}")
        
        if semester_credits > 0:
            semester_gpa = semester_points / semester_credits
            self.gpa.set(f"{semester_gpa:.2f}")
            
            if semester_gpa >= 3.5:
                self.gpa_display.config(fg='green')
            elif semester_gpa >= 2.0:
                self.gpa_display.config(fg='blue')
            else:
                self.gpa_display.config(fg='red')
        else:
            self.gpa.set("0.00")
            self.gpa_display.config(fg='black')

        #calculate cgpa
        total_credits = 0
        total_points = 0.0

        for semester_courses in self.semesters.values(): #all semester
            for course in semester_courses: #course in one semester
                total_credits += course["credits"]
                total_points += course["points"]
        
        if total_credits > 0:
            cgpa = total_points / total_credits
            self.cgpa.set(f"{cgpa:.2f}")
        else:
            self.cgpa.set("0.00")

    def delete_selected(self):
        select = self.course_list.curselection()
        if not select:
            messagebox.showwarning("Warning", "Please select a course to delete")
            return
        
        index = select[0]
        if 0 <= index < len(self.courses):
            #remove from current semester list
            delete_course = self.courses[index]
            self.courses.pop(index)

            #remove from semester storage
            semester = delete_course.get('semester',self.current_semester)
            if semester in self.semesters:
                for i, course in enumerate(self.semesters[semester]):
                    if (course['course'] == delete_course['course'] and course['grade'] == delete_course['grade'] and course['credits'] == delete_course['credits']):
                        self.semesters[semester].pop(i)
                        break
            
            self.save_courses()
            self.refresh_course()
            self.calculate_gpa()
            messagebox.showinfo("Success", "Course deleted successfully")
    
    def clear_all(self):
         if not self.courses:
            messagebox.showinfo("Info", "No courses to clear")
            return
         
         if messagebox.askyesno("Confirm", "Are you sure you want to clear all courses?"):
            #clear list 
            semester = self.current_semester
            if semester in self.semesters:
                self.semesters[semester] = []
            self.courses = []
            self.save_courses()
            self.refresh_course()
            self.calculate_gpa()
            messagebox.showinfo("Success", "All courses cleared for this semester")

    #show all semester and overall
    def show_semester_summary(self):
        if not self.semesters:
            messagebox.showinfo("Semester Summary", "No semester data found.")
            return
        
        summary_window = Toplevel(self.root)
        summary_window.title("Semester Summary")
        summary_window.geometry("600x500")
        summary_window.configure(bg="#dbe8f5")
        summary_window.transient(self.root)
        summary_window.grab_set()

        #center the window
        screen_width = summary_window.winfo_screenwidth()
        screen_height = summary_window.winfo_screenheight()
        x = (screen_width - 600) // 2
        y = (screen_height - 500) // 2
        summary_window.geometry(f'600x500+{x}+{y}')

        try:
            icon_image = tk.PhotoImage(file='tarumt.png')
            summary_window.iconphoto(False, icon_image)  
        except:
            pass

        #title
        title_frame = Frame(summary_window,bg= "#2980b9")
        title_frame.pack(fill=X, pady=(0, 10))
        
        title_label = Label(title_frame, text="Semester Summary", font=('Arial', 18, 'bold'), fg='white',bg= "#2980b9", pady=15)
        title_label.pack()

        #content frame
        content_frame = Frame(summary_window, bg="#dbe8f5")
        content_frame.pack(fill=BOTH, expand=True, padx=20, pady=10)

        #scrollbar
        scrollbar = Scrollbar(content_frame)
        scrollbar.pack(side=RIGHT,fill=Y)

        summary_text = Text(content_frame, wrap=WORD, yscrollcommand=scrollbar.set,font=("Courier New", 11), bg="white", fg="black")
        summary_text.pack(fill=BOTH, expand=True)
        scrollbar.config(command=summary_text.yview)

        total_credits_all = 0
        total_points_all = 0.0

        for semester, courses in self.semesters.items():
            if not isinstance(courses, list) or not courses:
                continue
         
            summary_text.insert(END,"="*23 + f" {semester} " +"="*24 +"\n")

            semester_credits = 0
            semester_points = 0.0

            # summary header
            summary_text.insert(END, f"{'Course Name':<35}  {'Credits':<18}  {'Grade':<16}  {'Points':<8}\n", "header")
            summary_text.insert(END, "-" * 59 + "\n")

            for course in courses:
                name = course.get("course", "N/A")
                credits = course.get("credits", 0)
                grade = course.get("grade", "N/A")
                points = course.get("points", 0.0)

                semester_credits += credits
                semester_points += points

                summary_text.insert(END,f"{name:<25}{credits:<10}{grade:<10}{points:<10.1f}\n")

            semester_gpa = semester_points / semester_credits if semester_credits > 0 else 0.0

            summary_text.insert(END, "-" * 59 + "\n")
            summary_text.insert(END, f"   ➡ Total Credits: {semester_credits}   |   Semester GPA: {semester_gpa:.2f}\n", "summary")
            summary_text.insert(END," "+"\n")

            total_credits_all += semester_credits
            total_points_all += semester_points

        cgpa = total_points_all / total_credits_all if total_credits_all > 0 else 0.0

        #overall
        summary_text.insert(END, "\n" + "=" * 59 + "\n")
        summary_text.insert(END, f"📊 Overall Total Credits: {total_credits_all}\n", "overall")
        summary_text.insert(END, f"📊 Overall Total Grade Points: {total_points_all:.1f}\n", "overall")
        summary_text.insert(END, f"📊 CGPA: {cgpa:.2f}", "overall")
        summary_text.insert(END, "\n" + "=" * 59 + "\n")

        summary_text.tag_config("sem_title", font=('Arial', 13, 'bold'), foreground="#2980b9")
        summary_text.tag_config("header", font=('Arial', 11, 'bold'), foreground="black")
        summary_text.tag_config("summary", font=('Arial', 11, 'bold'), foreground="#27ae60")
        summary_text.tag_config("overall", font=('Arial', 12, 'bold'), foreground="#e67e22")

        summary_text.config(state=DISABLED) #user cannot edit the content
     
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

def main(current_user="guest"):
    root = tk.Tk()
    app = GPACalculator(root, current_user)
    
    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit the application?"):
            root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()