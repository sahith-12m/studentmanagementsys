import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3


# =========================
# DATABASE
# =========================

def connect_db():
    return sqlite3.connect("students.db")


def create_table():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            gender TEXT NOT NULL,
            course TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            phone TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# =========================
# CLEAR INPUT FIELDS
# =========================

def clear_fields():
    name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    gender_combo.set("")
    course_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)


# =========================
# ADD STUDENT
# =========================

def add_student():

    name = name_entry.get().strip()
    age = age_entry.get().strip()
    gender = gender_combo.get().strip()
    course = course_entry.get().strip()
    email = email_entry.get().strip()
    phone = phone_entry.get().strip()

    if not name or not age or not gender or not course or not email or not phone:
        messagebox.showwarning(
            "Missing Information",
            "Please fill all fields."
        )
        return

    if not age.isdigit():
        messagebox.showerror(
            "Invalid Age",
            "Age must be a number."
        )
        return

    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO students
            (name, age, gender, course, email, phone)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (name, int(age), gender, course, email, phone))

        conn.commit()

        messagebox.showinfo(
            "Success",
            "Student added successfully."
        )

        clear_fields()
        display_students()

    except sqlite3.IntegrityError:
        messagebox.showerror(
            "Error",
            "Email already exists."
        )

    finally:
        conn.close()


# =========================
# DISPLAY STUDENTS
# =========================

def display_students():

    for item in student_table.get_children():
        student_table.delete(item)

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, age, gender, course, email, phone
        FROM students
        ORDER BY id DESC
    """)

    students = cursor.fetchall()

    for student in students:
        student_table.insert("", tk.END, values=student)

    conn.close()


# =========================
# SELECT STUDENT
# =========================

def select_student(event):

    selected = student_table.focus()

    if not selected:
        return

    values = student_table.item(selected, "values")

    clear_fields()

    name_entry.insert(0, values[1])
    age_entry.insert(0, values[2])
    gender_combo.set(values[3])
    course_entry.insert(0, values[4])
    email_entry.insert(0, values[5])
    phone_entry.insert(0, values[6])


# =========================
# UPDATE STUDENT
# =========================

def update_student():

    selected = student_table.focus()

    if not selected:
        messagebox.showwarning(
            "Select Student",
            "Please select a student from the table."
        )
        return

    values = student_table.item(selected, "values")
    student_id = values[0]

    name = name_entry.get().strip()
    age = age_entry.get().strip()
    gender = gender_combo.get().strip()
    course = course_entry.get().strip()
    email = email_entry.get().strip()
    phone = phone_entry.get().strip()

    if not name or not age or not gender or not course or not email or not phone:
        messagebox.showwarning(
            "Missing Information",
            "Please fill all fields."
        )
        return

    if not age.isdigit():
        messagebox.showerror(
            "Invalid Age",
            "Age must be a number."
        )
        return

    conn = connect_db()
    cursor = conn.cursor()

    try:

        cursor.execute("""
            UPDATE students
            SET name = ?,
                age = ?,
                gender = ?,
                course = ?,
                email = ?,
                phone = ?
            WHERE id = ?
        """, (
            name,
            int(age),
            gender,
            course,
            email,
            phone,
            student_id
        ))

        conn.commit()

        messagebox.showinfo(
            "Success",
            "Student updated successfully."
        )

        clear_fields()
        display_students()

    except sqlite3.IntegrityError:
        messagebox.showerror(
            "Error",
            "Email already exists."
        )

    finally:
        conn.close()


# =========================
# DELETE STUDENT
# =========================

def delete_student():

    selected = student_table.focus()

    if not selected:
        messagebox.showwarning(
            "Select Student",
            "Please select a student."
        )
        return

    values = student_table.item(selected, "values")
    student_id = values[0]

    confirmation = messagebox.askyesno(
        "Delete Student",
        f"Are you sure you want to delete {values[1]}?"
    )

    if not confirmation:
        return

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM students WHERE id = ?",
        (student_id,)
    )

    conn.commit()
    conn.close()

    messagebox.showinfo(
        "Deleted",
        "Student deleted successfully."
    )

    clear_fields()
    display_students()


# =========================
# SEARCH STUDENT
# =========================

def search_student():

    search_text = search_entry.get().strip()

    for item in student_table.get_children():
        student_table.delete(item)

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, age, gender, course, email, phone
        FROM students
        WHERE name LIKE ?
           OR course LIKE ?
           OR email LIKE ?
    """, (
        "%" + search_text + "%",
        "%" + search_text + "%",
        "%" + search_text + "%"
    ))

    students = cursor.fetchall()

    for student in students:
        student_table.insert("", tk.END, values=student)

    conn.close()


# =========================
# MAIN WINDOW
# =========================

create_table()

root = tk.Tk()

root.title("Student Management System")
root.geometry("1100x650")
root.resizable(False, False)

root.configure(bg="#f4f6f8")


# =========================
# TITLE
# =========================

title = tk.Label(
    root,
    text="Student Management System",
    font=("Arial", 24, "bold"),
    bg="#1f4e78",
    fg="white",
    pady=15
)

title.pack(fill=tk.X)


# =========================
# FORM FRAME
# =========================

form_frame = tk.Frame(
    root,
    bg="#f4f6f8",
    padx=20,
    pady=20
)

form_frame.pack(fill=tk.X)


# Name

tk.Label(
    form_frame,
    text="Name",
    font=("Arial", 11),
    bg="#f4f6f8"
).grid(row=0, column=0, padx=10, pady=8, sticky="w")

name_entry = tk.Entry(
    form_frame,
    width=25,
    font=("Arial", 11)
)

name_entry.grid(row=0, column=1, padx=10, pady=8)


# Age

tk.Label(
    form_frame,
    text="Age",
    font=("Arial", 11),
    bg="#f4f6f8"
).grid(row=0, column=2, padx=10, pady=8, sticky="w")

age_entry = tk.Entry(
    form_frame,
    width=25,
    font=("Arial", 11)
)

age_entry.grid(row=0, column=3, padx=10, pady=8)


# Gender

tk.Label(
    form_frame,
    text="Gender",
    font=("Arial", 11),
    bg="#f4f6f8"
).grid(row=1, column=0, padx=10, pady=8, sticky="w")

gender_combo = ttk.Combobox(
    form_frame,
    width=23,
    values=["Male", "Female", "Other"],
    state="readonly"
)

gender_combo.grid(row=1, column=1, padx=10, pady=8)


# Course

tk.Label(
    form_frame,
    text="Course",
    font=("Arial", 11),
    bg="#f4f6f8"
).grid(row=1, column=2, padx=10, pady=8, sticky="w")

course_entry = tk.Entry(
    form_frame,
    width=25,
    font=("Arial", 11)
)

course_entry.grid(row=1, column=3, padx=10, pady=8)


# Email

tk.Label(
    form_frame,
    text="Email",
    font=("Arial", 11),
    bg="#f4f6f8"
).grid(row=2, column=0, padx=10, pady=8, sticky="w")

email_entry = tk.Entry(
    form_frame,
    width=25,
    font=("Arial", 11)
)

email_entry.grid(row=2, column=1, padx=10, pady=8)


# Phone

tk.Label(
    form_frame,
    text="Phone",
    font=("Arial", 11),
    bg="#f4f6f8"
).grid(row=2, column=2, padx=10, pady=8, sticky="w")

phone_entry = tk.Entry(
    form_frame,
    width=25,
    font=("Arial", 11)
)

phone_entry.grid(row=2, column=3, padx=10, pady=8)


# =========================
# BUTTONS
# =========================

button_frame = tk.Frame(
    root,
    bg="#f4f6f8"
)

button_frame.pack(pady=5)


add_button = tk.Button(
    button_frame,
    text="Add Student",
    width=15,
    bg="#198754",
    fg="white",
    font=("Arial", 10, "bold"),
    command=add_student
)

add_button.grid(row=0, column=0, padx=5)


update_button = tk.Button(
    button_frame,
    text="Update",
    width=15,
    bg="#0d6efd",
    fg="white",
    font=("Arial", 10, "bold"),
    command=update_student
)

update_button.grid(row=0, column=1, padx=5)


delete_button = tk.Button(
    button_frame,
    text="Delete",
    width=15,
    bg="#dc3545",
    fg="white",
    font=("Arial", 10, "bold"),
    command=delete_student
)

delete_button.grid(row=0, column=2, padx=5)


clear_button = tk.Button(
    button_frame,
    text="Clear",
    width=15,
    bg="#6c757d",
    fg="white",
    font=("Arial", 10, "bold"),
    command=clear_fields
)

clear_button.grid(row=0, column=3, padx=5)


# =========================
# SEARCH
# =========================

search_frame = tk.Frame(
    root,
    bg="#f4f6f8"
)

search_frame.pack(pady=15)


tk.Label(
    search_frame,
    text="Search:",
    font=("Arial", 11, "bold"),
    bg="#f4f6f8"
).pack(side=tk.LEFT, padx=5)


search_entry = tk.Entry(
    search_frame,
    width=35,
    font=("Arial", 11)
)

search_entry.pack(side=tk.LEFT, padx=5)


search_button = tk.Button(
    search_frame,
    text="Search",
    width=12,
    bg="#6f42c1",
    fg="white",
    font=("Arial", 10, "bold"),
    command=search_student
)

search_button.pack(side=tk.LEFT, padx=5)


show_all_button = tk.Button(
    search_frame,
    text="Show All",
    width=12,
    bg="#212529",
    fg="white",
    font=("Arial", 10, "bold"),
    command=display_students
)

show_all_button.pack(side=tk.LEFT, padx=5)


# =========================
# TABLE
# =========================

table_frame = tk.Frame(root)

table_frame.pack(
    fill=tk.BOTH,
    expand=True,
    padx=20,
    pady=10
)


columns = (
    "ID",
    "Name",
    "Age",
    "Gender",
    "Course",
    "Email",
    "Phone"
)


student_table = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings",
    height=10
)


for column in columns:

    student_table.heading(
        column,
        text=column
    )

    student_table.column(
        column,
        width=120,
        anchor=tk.CENTER
    )


student_table.column("ID", width=50)
student_table.column("Name", width=150)
student_table.column("Email", width=200)


student_table.pack(
    side=tk.LEFT,
    fill=tk.BOTH,
    expand=True
)


# Scrollbar

scrollbar = ttk.Scrollbar(
    table_frame,
    orient=tk.VERTICAL,
    command=student_table.yview
)

student_table.configure(
    yscrollcommand=scrollbar.set
)

scrollbar.pack(
    side=tk.RIGHT,
    fill=tk.Y
)


# Select row

student_table.bind(
    "<ButtonRelease-1>",
    select_student
)


# =========================
# START
# =========================

display_students()

root.mainloop()
