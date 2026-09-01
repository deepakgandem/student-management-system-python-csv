import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os


# ==========================================================
# CSV STUDENT MANAGEMENT SYSTEM
# STAGE 6
# ADD + VIEW + SEARCH + UPDATE + DELETE
# MODERN DARK BLUE + WHITE UI
# ==========================================================


# ==========================================================
# CSV SETTINGS
# ==========================================================

CSV_FILE = "students.csv"


# ==========================================================
# CREATE CSV FILE
# ==========================================================

def create_csv():

    if not os.path.exists(CSV_FILE):

        with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:

            writer = csv.writer(file)

            writer.writerow([
                "ID",
                "Name",
                "Phone",
                "Course",
                "Fee"
            ])


# ==========================================================
# COLORS
# ==========================================================

BG_COLOR = "#EAF2F8"
HEADER_COLOR = "#17365D"
BUTTON_COLOR = "#1F4E78"
BUTTON_HOVER = "#163A5C"
BUTTON_TEXT = "#FFFFFF"
ENTRY_BG = "#FFFFFF"
TEXT_COLOR = "#17202A"
TABLE_HEADER = "#5B9BD5"
TABLE_ROW = "#FFFFFF"
SELECT_COLOR = "#D6EAF8"


# ==========================================================
# CSV HELPER FUNCTIONS
# ==========================================================


# ----------------------------------------------------------
# READ ALL STUDENTS
# ----------------------------------------------------------

def read_students():

    create_csv()

    students = []

    try:

        with open(
            CSV_FILE,
            "r",
            newline="",
            encoding="utf-8"
        ) as file:

            reader = csv.DictReader(file)

            for row in reader:

                students.append(row)

    except Exception as error:

        messagebox.showerror(
            "CSV Error",
            str(error)
        )

    return students


# ----------------------------------------------------------
# WRITE ALL STUDENTS
# ----------------------------------------------------------

def write_students(students):

    try:

        with open(
            CSV_FILE,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            fieldnames = [
                "ID",
                "Name",
                "Phone",
                "Course",
                "Fee"
            ]

            writer = csv.DictWriter(
                file,
                fieldnames=fieldnames
            )

            writer.writeheader()

            writer.writerows(students)

        return True

    except Exception as error:

        messagebox.showerror(
            "CSV Error",
            str(error)
        )

        return False


# ----------------------------------------------------------
# GET NEXT STUDENT ID
# ----------------------------------------------------------

def get_next_id():

    students = read_students()

    if len(students) == 0:
        return 1

    ids = []

    for student in students:

        try:

            ids.append(
                int(student["ID"])
            )

        except (ValueError, KeyError):
            pass

    if len(ids) == 0:
        return 1

    return max(ids) + 1


# ==========================================================
# GUI FUNCTIONS
# ==========================================================


# ----------------------------------------------------------
# CLEAR FIELDS
# ----------------------------------------------------------

def clear_fields():

    entry_name.delete(0, tk.END)

    entry_phone.delete(0, tk.END)

    entry_course.delete(0, tk.END)

    entry_fee.delete(0, tk.END)

    entry_search.delete(0, tk.END)

    tree.selection_remove(
        tree.selection()
    )


# ----------------------------------------------------------
# ADD STUDENT
# ----------------------------------------------------------

def add_student():

    name = entry_name.get().strip()

    phone = entry_phone.get().strip()

    course = entry_course.get().strip()

    fee = entry_fee.get().strip()


    # Check empty fields

    if (
        name == ""
        or phone == ""
        or course == ""
        or fee == ""
    ):

        messagebox.showwarning(
            "Input Error",
            "Please enter all student details."
        )

        return


    # Check fee

    try:

        fee_value = float(fee)

    except ValueError:

        messagebox.showwarning(
            "Input Error",
            "Fee must be a number."
        )

        return


    # Get next ID

    next_id = get_next_id()


    # Create student record

    student = {
        "ID": str(next_id),
        "Name": name,
        "Phone": phone,
        "Course": course,
        "Fee": f"{fee_value:.2f}"
    }


    # Read existing students

    students = read_students()


    # Add new student

    students.append(student)


    # Save CSV

    if write_students(students):

        messagebox.showinfo(
            "Success",
            "Student added successfully!"
        )

        clear_fields()

        view_students()


# ----------------------------------------------------------
# VIEW STUDENTS
# ----------------------------------------------------------

def view_students():

    # Clear table

    for item in tree.get_children():

        tree.delete(item)


    students = read_students()


    # Display students

    for student in students:

        tree.insert(
            "",
            tk.END,
            values=(
                student["ID"],
                student["Name"],
                student["Phone"],
                student["Course"],
                student["Fee"]
            )
        )


    total_label.config(
        text=f"Total Students: {len(students)}"
    )


# ----------------------------------------------------------
# SEARCH STUDENT
# ----------------------------------------------------------

def search_student():

    search_text = (
        entry_search
        .get()
        .strip()
        .lower()
    )


    # If search is empty

    if search_text == "":

        view_students()

        return


    # Clear table

    for item in tree.get_children():

        tree.delete(item)


    students = read_students()

    results = []


    # Search name, phone and course

    for student in students:

        name = student["Name"].lower()

        phone = student["Phone"].lower()

        course = student["Course"].lower()


        if (
            search_text in name
            or search_text in phone
            or search_text in course
        ):

            results.append(student)


    # Display results

    for student in results:

        tree.insert(
            "",
            tk.END,
            values=(
                student["ID"],
                student["Name"],
                student["Phone"],
                student["Course"],
                student["Fee"]
            )
        )


    total_label.config(
        text=f"Search Results: {len(results)}"
    )


# ----------------------------------------------------------
# SELECT STUDENT
# ----------------------------------------------------------

def select_student(event):

    selected = tree.focus()


    if selected == "":

        return


    values = tree.item(
        selected,
        "values"
    )


    if not values:

        return


    # Name

    entry_name.delete(
        0,
        tk.END
    )

    entry_name.insert(
        0,
        values[1]
    )


    # Phone

    entry_phone.delete(
        0,
        tk.END
    )

    entry_phone.insert(
        0,
        values[2]
    )


    # Course

    entry_course.delete(
        0,
        tk.END
    )

    entry_course.insert(
        0,
        values[3]
    )


    # Fee

    entry_fee.delete(
        0,
        tk.END
    )

    entry_fee.insert(
        0,
        values[4]
    )


# ----------------------------------------------------------
# UPDATE STUDENT
# ----------------------------------------------------------

def update_student():

    selected = tree.focus()


    if selected == "":

        messagebox.showwarning(
            "Update",
            "Please select a student from the table."
        )

        return


    values = tree.item(
        selected,
        "values"
    )


    if not values:

        return


    student_id = str(values[0])


    name = entry_name.get().strip()

    phone = entry_phone.get().strip()

    course = entry_course.get().strip()

    fee = entry_fee.get().strip()


    # Check empty fields

    if (
        name == ""
        or phone == ""
        or course == ""
        or fee == ""
    ):

        messagebox.showwarning(
            "Input Error",
            "Please enter all student details."
        )

        return


    # Check fee

    try:

        fee_value = float(fee)

    except ValueError:

        messagebox.showwarning(
            "Input Error",
            "Fee must be a number."
        )

        return


    students = read_students()

    student_found = False


    # Find student

    for student in students:

        if str(student["ID"]) == student_id:

            student["Name"] = name

            student["Phone"] = phone

            student["Course"] = course

            student["Fee"] = f"{fee_value:.2f}"

            student_found = True

            break


    if not student_found:

        messagebox.showerror(
            "Update Error",
            "Student not found."
        )

        return


    # Save updated data

    if write_students(students):

        messagebox.showinfo(
            "Success",
            "Student updated successfully!"
        )

        clear_fields()

        view_students()


# ----------------------------------------------------------
# DELETE STUDENT
# ----------------------------------------------------------

def delete_student():

    selected = tree.focus()


    if selected == "":

        messagebox.showwarning(
            "Delete",
            "Please select a student from the table."
        )

        return


    values = tree.item(
        selected,
        "values"
    )


    if not values:

        return


    student_id = str(values[0])

    student_name = values[1]


    # Confirm deletion

    answer = messagebox.askyesno(
        "Confirm Delete",
        f"Do you want to delete {student_name}?"
    )


    if not answer:

        return


    students = read_students()


    # Remove selected student

    new_students = []

    deleted = False


    for student in students:

        if str(student["ID"]) == student_id:

            deleted = True

        else:

            new_students.append(student)


    if not deleted:

        messagebox.showerror(
            "Delete Error",
            "Student not found."
        )

        return


    # Re-index IDs

    for index, student in enumerate(
        new_students,
        start=1
    ):

        student["ID"] = str(index)


    # Save CSV

    if write_students(new_students):

        messagebox.showinfo(
            "Success",
            "Student deleted successfully!\n\n"
            "Student IDs have been re-indexed."
        )

        clear_fields()

        view_students()


# ==========================================================
# BUTTON STYLE
# ==========================================================

def create_button(
    parent,
    text,
    width,
    command
):

    button = tk.Button(

        parent,

        text=text,

        width=width,

        font=("Arial", 11, "bold"),

        bg=BUTTON_COLOR,

        fg=BUTTON_TEXT,

        activebackground=BUTTON_HOVER,

        activeforeground=BUTTON_TEXT,

        relief="flat",

        bd=0,

        padx=10,

        pady=8,

        cursor="hand2",

        command=command
    )


    # Hover effect

    button.bind(
        "<Enter>",
        lambda event:
        button.config(
            bg=BUTTON_HOVER
        )
    )


    button.bind(
        "<Leave>",
        lambda event:
        button.config(
            bg=BUTTON_COLOR
        )
    )


    return button


# ==========================================================
# START PROGRAM
# ==========================================================

print("=" * 60)

print(
    "       CSV STUDENT MANAGEMENT SYSTEM"
)

print("=" * 60)

print()

print(
    "[START] Program is running..."
)

print(
    "[1] Creating CSV file..."
)


# Create CSV

create_csv()


print(
    "[2] CSV file is ready."
)

print(
    "[3] Loading student records..."
)


# ==========================================================
# MAIN WINDOW
# ==========================================================

root = tk.Tk()


root.title(
    "GK Infotech Solutions - Student Management System"
)


root.geometry(
    "1100x750"
)


root.minsize(
    900,
    650
)


root.configure(
    bg=BG_COLOR
)


# ==========================================================
# TITLE HEADER
# ==========================================================

header_frame = tk.Frame(

    root,

    bg=HEADER_COLOR,

    height=85
)


header_frame.pack(
    fill="x"
)


header_frame.pack_propagate(
    False
)


title_label = tk.Label(

    header_frame,

    text="STUDENT MANAGEMENT SYSTEM",

    font=(
        "Arial",
        24,
        "bold"
    ),

    bg=HEADER_COLOR,

    fg="white"
)


title_label.pack(
    pady=23
)


# ==========================================================
# INPUT FRAME
# ==========================================================

input_frame = tk.Frame(

    root,

    bg=BG_COLOR
)


input_frame.pack(
    pady=15
)


# ==========================================================
# STUDENT NAME
# ==========================================================

tk.Label(

    input_frame,

    text="Student Name:",

    font=(
        "Arial",
        12,
        "bold"
    ),

    bg=BG_COLOR,

    fg=TEXT_COLOR

).grid(

    row=0,

    column=0,

    padx=10,

    pady=8,

    sticky="e"
)


entry_name = tk.Entry(

    input_frame,

    width=35,

    font=(
        "Arial",
        12
    ),

    bg=ENTRY_BG,

    fg=TEXT_COLOR,

    relief="solid",

    bd=1
)


entry_name.grid(

    row=0,

    column=1,

    padx=10,

    pady=8
)


# ==========================================================
# PHONE
# ==========================================================

tk.Label(

    input_frame,

    text="Phone Number:",

    font=(
        "Arial",
        12,
        "bold"
    ),

    bg=BG_COLOR,

    fg=TEXT_COLOR

).grid(

    row=1,

    column=0,

    padx=10,

    pady=8,

    sticky="e"
)


entry_phone = tk.Entry(

    input_frame,

    width=35,

    font=(
        "Arial",
        12
    ),

    bg=ENTRY_BG,

    fg=TEXT_COLOR,

    relief="solid",

    bd=1
)


entry_phone.grid(

    row=1,

    column=1,

    padx=10,

    pady=8
)


# ==========================================================
# COURSE
# ==========================================================

tk.Label(

    input_frame,

    text="Course:",

    font=(
        "Arial",
        12,
        "bold"
    ),

    bg=BG_COLOR,

    fg=TEXT_COLOR

).grid(

    row=2,

    column=0,

    padx=10,

    pady=8,

    sticky="e"
)


entry_course = tk.Entry(

    input_frame,

    width=35,

    font=(
        "Arial",
        12
    ),

    bg=ENTRY_BG,

    fg=TEXT_COLOR,

    relief="solid",

    bd=1
)


entry_course.grid(

    row=2,

    column=1,

    padx=10,

    pady=8
)


# ==========================================================
# FEE
# ==========================================================

tk.Label(

    input_frame,

    text="Fee:",

    font=(
        "Arial",
        12,
        "bold"
    ),

    bg=BG_COLOR,

    fg=TEXT_COLOR

).grid(

    row=3,

    column=0,

    padx=10,

    pady=8,

    sticky="e"
)


entry_fee = tk.Entry(

    input_frame,

    width=35,

    font=(
        "Arial",
        12
    ),

    bg=ENTRY_BG,

    fg=TEXT_COLOR,

    relief="solid",

    bd=1
)


entry_fee.grid(

    row=3,

    column=1,

    padx=10,

    pady=8
)


# ==========================================================
# BUTTON FRAME
# ==========================================================

button_frame = tk.Frame(

    root,

    bg=BG_COLOR
)


button_frame.pack(
    pady=12
)


# ==========================================================
# ADD BUTTON
# ==========================================================

add_button = create_button(

    button_frame,

    "ADD STUDENT",

    15,

    add_student
)


add_button.grid(

    row=0,

    column=0,

    padx=6
)


# ==========================================================
# VIEW BUTTON
# ==========================================================

view_button = create_button(

    button_frame,

    "VIEW STUDENTS",

    15,

    view_students
)


view_button.grid(

    row=0,

    column=1,

    padx=6
)


# ==========================================================
# UPDATE BUTTON
# ==========================================================

update_button = create_button(

    button_frame,

    "UPDATE",

    15,

    update_student
)


update_button.grid(

    row=0,

    column=2,

    padx=6
)


# ==========================================================
# DELETE BUTTON
# ==========================================================

delete_button = create_button(

    button_frame,

    "DELETE",

    15,

    delete_student
)


delete_button.grid(

    row=0,

    column=3,

    padx=6
)


# ==========================================================
# CLEAR BUTTON
# ==========================================================

clear_button = create_button(

    button_frame,

    "CLEAR",

    15,

    clear_fields
)


clear_button.grid(

    row=0,

    column=4,

    padx=6
)


# ==========================================================
# SEARCH FRAME
# ==========================================================

search_frame = tk.Frame(

    root,

    bg=BG_COLOR
)


search_frame.pack(
    pady=10
)


tk.Label(

    search_frame,

    text="Search Student:",

    font=(
        "Arial",
        12,
        "bold"
    ),

    bg=BG_COLOR,

    fg=TEXT_COLOR

).pack(

    side="left",

    padx=8
)


entry_search = tk.Entry(

    search_frame,

    width=35,

    font=(
        "Arial",
        12
    ),

    bg=ENTRY_BG,

    fg=TEXT_COLOR,

    relief="solid",

    bd=1
)


entry_search.pack(

    side="left",

    padx=8
)


search_button = create_button(

    search_frame,

    "SEARCH",

    12,

    search_student
)


search_button.pack(

    side="left",

    padx=5
)


# ==========================================================
# TABLE FRAME
# ==========================================================

table_frame = tk.Frame(

    root,

    bg=BG_COLOR
)


table_frame.pack(

    fill="both",

    expand=True,

    padx=25,

    pady=10
)


# ==========================================================
# TREEVIEW STYLE
# ==========================================================

style = ttk.Style()


try:

    style.theme_use("clam")

except tk.TclError:

    pass


style.configure(

    "Treeview",

    background=TABLE_ROW,

    foreground=TEXT_COLOR,

    rowheight=32,

    fieldbackground=TABLE_ROW,

    font=(
        "Arial",
        11
    )
)


style.configure(

    "Treeview.Heading",

    background=TABLE_HEADER,

    foreground="white",

    font=(
        "Arial",
        11,
        "bold"
    ),

    relief="flat"
)


style.map(

    "Treeview",

    background=[
        (
            "selected",
            SELECT_COLOR
        )
    ],

    foreground=[
        (
            "selected",
            TEXT_COLOR
        )
    ]
)


# ==========================================================
# VERTICAL SCROLLBAR
# ==========================================================

vertical_scrollbar = ttk.Scrollbar(

    table_frame,

    orient="vertical"
)


vertical_scrollbar.pack(

    side="right",

    fill="y"
)


# ==========================================================
# HORIZONTAL SCROLLBAR
# ==========================================================

horizontal_scrollbar = ttk.Scrollbar(

    table_frame,

    orient="horizontal"
)


horizontal_scrollbar.pack(

    side="bottom",

    fill="x"
)


# ==========================================================
# STUDENT TABLE
# ==========================================================

tree = ttk.Treeview(

    table_frame,

    columns=(

        "ID",

        "Name",

        "Phone",

        "Course",

        "Fee"

    ),

    show="headings",

    yscrollcommand=
    vertical_scrollbar.set,

    xscrollcommand=
    horizontal_scrollbar.set
)


vertical_scrollbar.config(

    command=tree.yview
)


horizontal_scrollbar.config(

    command=tree.xview
)


# ==========================================================
# TABLE HEADINGS
# ==========================================================

tree.heading(

    "ID",

    text="ID"
)


tree.heading(

    "Name",

    text="Student Name"
)


tree.heading(

    "Phone",

    text="Phone Number"
)


tree.heading(

    "Course",

    text="Course"
)


tree.heading(

    "Fee",

    text="Fee"
)


# ==========================================================
# COLUMN WIDTHS
# ==========================================================

tree.column(

    "ID",

    width=70,

    anchor="center"
)


tree.column(

    "Name",

    width=250,

    anchor="center"
)


tree.column(

    "Phone",

    width=180,

    anchor="center"
)


tree.column(

    "Course",

    width=250,

    anchor="center"
)


tree.column(

    "Fee",

    width=150,

    anchor="center"
)


tree.pack(

    fill="both",

    expand=True
)


# ==========================================================
# TABLE CLICK EVENT
# ==========================================================

tree.bind(

    "<ButtonRelease-1>",

    select_student
)


# ==========================================================
# TOTAL STUDENTS LABEL
# ==========================================================

total_label = tk.Label(

    root,

    text="Total Students: 0",

    font=(
        "Arial",
        13,
        "bold"
    ),

    bg=BG_COLOR,

    fg=HEADER_COLOR
)


total_label.pack(

    pady=12
)


# ==========================================================
# LOAD STUDENTS
# ==========================================================

view_students()


# ==========================================================
# START GUI
# ==========================================================

root.mainloop()

