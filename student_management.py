import sqlite3


# -------------------------------------------------
# DATABASE CONNECTION
# -------------------------------------------------

def connect_database():
    connection = sqlite3.connect("students.db")
    return connection


# -------------------------------------------------
# CREATE TABLE
# -------------------------------------------------

def create_table():
    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            gender TEXT NOT NULL,
            course TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


# -------------------------------------------------
# ADD STUDENT
# -------------------------------------------------

def add_student():
    print("\n--- Add Student ---")

    name = input("Enter student name: ")
    age = input("Enter age: ")
    gender = input("Enter gender: ")
    course = input("Enter course: ")
    email = input("Enter email: ")
    phone = input("Enter phone number: ")

    connection = connect_database()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            INSERT INTO students
            (name, age, gender, course, email, phone)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (name, age, gender, course, email, phone))

        connection.commit()

        print("Student added successfully!")

    except sqlite3.IntegrityError:
        print("Error: Email already exists.")

    finally:
        connection.close()


# -------------------------------------------------
# VIEW STUDENTS
# -------------------------------------------------

def view_students():
    print("\n--- Student List ---")

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    if not students:
        print("No students found.")
    else:
        print("-" * 100)

        print(
            f"{'ID':<5}"
            f"{'Name':<20}"
            f"{'Age':<8}"
            f"{'Gender':<10}"
            f"{'Course':<15}"
            f"{'Email':<25}"
            f"{'Phone':<15}"
        )

        print("-" * 100)

        for student in students:
            print(
                f"{student[0]:<5}"
                f"{student[1]:<20}"
                f"{student[2]:<8}"
                f"{student[3]:<10}"
                f"{student[4]:<15}"
                f"{student[5]:<25}"
                f"{student[6]:<15}"
            )

        print("-" * 100)

    connection.close()


# -------------------------------------------------
# SEARCH STUDENT
# -------------------------------------------------

def search_student():
    print("\n--- Search Student ---")

    student_id = input("Enter student ID: ")

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM students WHERE id = ?",
        (student_id,)
    )

    student = cursor.fetchone()

    if student:
        print("\nStudent Found!")
        print("ID     :", student[0])
        print("Name   :", student[1])
        print("Age    :", student[2])
        print("Gender :", student[3])
        print("Course :", student[4])
        print("Email  :", student[5])
        print("Phone  :", student[6])
    else:
        print("Student not found.")

    connection.close()


# -------------------------------------------------
# UPDATE STUDENT
# -------------------------------------------------

def update_student():
    print("\n--- Update Student ---")

    student_id = input("Enter student ID to update: ")

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM students WHERE id = ?",
        (student_id,)
    )

    student = cursor.fetchone()

    if not student:
        print("Student not found.")
        connection.close()
        return

    print("\nEnter new details:")

    name = input("Enter name: ")
    age = input("Enter age: ")
    gender = input("Enter gender: ")
    course = input("Enter course: ")
    email = input("Enter email: ")
    phone = input("Enter phone number: ")

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
            age,
            gender,
            course,
            email,
            phone,
            student_id
        ))

        connection.commit()

        print("Student updated successfully!")

    except sqlite3.IntegrityError:
        print("Error: Email already exists.")

    finally:
        connection.close()


# -------------------------------------------------
# DELETE STUDENT
# -------------------------------------------------

def delete_student():
    print("\n--- Delete Student ---")

    student_id = input("Enter student ID to delete: ")

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM students WHERE id = ?",
        (student_id,)
    )

    student = cursor.fetchone()

    if not student:
        print("Student not found.")
        connection.close()
        return

    confirmation = input(
        f"Are you sure you want to delete {student[1]}? (yes/no): "
    )

    if confirmation.lower() == "yes":

        cursor.execute(
            "DELETE FROM students WHERE id = ?",
            (student_id,)
        )

        connection.commit()

        print("Student deleted successfully!")

    else:
        print("Delete operation cancelled.")

    connection.close()


# -------------------------------------------------
# MAIN MENU
# -------------------------------------------------

def main():
    create_table()

    while True:

        print("\n")
        print("=" * 40)
        print("      STUDENT MANAGEMENT SYSTEM")
        print("=" * 40)

        print("1. Add Student")
        print("2. View Students")
        print("3. Search Student")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            add_student()

        elif choice == "2":
            view_students()

        elif choice == "3":
            search_student()

        elif choice == "4":
            update_student()

        elif choice == "5":
            delete_student()

        elif choice == "6":
            print("Thank you for using Student Management System!")
            break

        else:
            print("Invalid choice. Please try again.")


# -------------------------------------------------
# PROGRAM START
# -------------------------------------------------

if __name__ == "__main__":
    main()
