# TARUMT Student Assistant App
This is a helper app for TARUMT students. It has these features:

- Login and logout
- GPA calculator (can handle many semesters and CGPA)
- Timetable (day, week, month views, add/edit/delete events)
- Share events with other users

## What You Need

- Python 3.7 or above
- Tkinter (for GUI）
- tkcalendar (for pick a dates)
- PIL (Pillow, for pictures)

## Install

Type this in your terminal or command prompt:

```bash
pip install tkcalendar Pillow
```

## Files in Project

```
TARUMT_Student_Assistant/
│
├── home.py              # Main file, login and home
├── gpacalculation.py    # GPA calculator
├── timetable.py         # Timetable functions
├── users.json           # User accounts data
├── courses.json         # Courses and grades data
├── timetable.json       # Timetable events data
├── tarumt.png           # App icon
├── book.png             # Welcome page picture 
└── background_tarumt.png # Login background 
```


## How to Start

1. Put all files in the same folder.  
2. Run this command:

```bash
python home.py
```

(You can also run `gpacalculation.py` or `timetable.py`, but it’s better to start with `home.py`)


## Test Accounts

These accounts are in `users.json`:

| Student ID | Password  |
|------------|-----------|
| 2407011    | 12345678  |
| 2407012    | 12345678  |
| 2407013    | 12345678  |
| 2407014    | 12345678  |
| 2407015    | 12345678  |


## Features

### 🏠 Home Page
- Shows current user and date/time
- Buttons to GPA calculator and timetable

### 📊 GPA Calculator
- Add courses for many semesters
- Shows GPA and CGPA
- Edit or delete courses
- Export semester summary

### 📅 Timetable
- View by day, week, month
- Add, edit, delete events
- Can invite other users
- Detects conflicts


## 🖼 Pictures

Put these in the same folder:  
- `tarumt.png` — App icon  
- `book.png` — Welcome picture  
- `background_tarumt.png` — Login background  

App still works if missing, just no pictures.


## FAQ

### 1. Error: `No module named 'tkcalendar'`
Run:
```bash
pip install tkcalendar
```

### 2. Error: `No module named 'PIL'`
Run:
```bash
pip install Pillow
```

### 3. Timetable or course not showing?
Check `timetable.json` and `courses.json` exist and are correct.
