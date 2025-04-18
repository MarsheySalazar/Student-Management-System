import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from PIL import Image, ImageTk

from dbbackend import addStdRec, dataUpdate, deleteRec, searchData, viewData

# Main Application
root = tk.Tk()
root.title("Student Management System")
root.configure(bg="#f0f4f8")

# Header Image
try:
    img = Image.open("header.png")
    img = img.resize((800, 150), Image.Resampling.LANCZOS)
    photo = ImageTk.PhotoImage(img)
    img_label = tk.Label(root, image=photo, bg="#f0f4f8")
    img_label.image = photo
    img_label.grid(row=0, column=0, columnspan=2, pady=(10, 0))
except:
    pass

# Title
appLabel = tk.Label(root, text="Student Management System", fg="#004d66", bg="#f0f4f8", font=("Sylfaen", 28, "bold"))
appLabel.grid(row=1, column=0, columnspan=2, pady=20)

# Form Fields
fields = [
    ("School", 2),
    ("Student ID", 3),
    ("First Name", 4),
    ("Last Name", 5),
    ("Date of Birth", 6),
    ("Age", 7),
    ("Gender", 8),
    ("Mobile", 9)
]

entries = {}
for field, row in fields:
    label = tk.Label(root, text=field + ":", bg="#f0f4f8", anchor='w', font=("Helvetica", 11))
    label.grid(row=row, column=0, sticky='e', padx=(40, 10), pady=8)
    entry = tk.Entry(root, width=35)
    entry.grid(row=row, column=1, padx=(0, 40), pady=8, sticky='w')
    entries[field.lower().replace(" ", "") + "entry"] = entry

# Buttons
button_frame = tk.Frame(root, bg="#f0f4f8")
button_frame.grid(row=10, column=0, columnspan=2, pady=20)

buttons = [
    ("Add Student", lambda: addStudent()),
    ("View Data", lambda: openDataWindow()),
    ("Update", lambda: updateStudent()),
    ("Delete", lambda: deleteStudent()),
    ("Clear", lambda: clearEntries())
]

for idx, (text, command) in enumerate(buttons):
    btn = tk.Button(button_frame, text=text, command=command, width=15, bg="#007acc", fg="white")
    btn.grid(row=0, column=idx, padx=6)

# Search Section
search_frame = tk.LabelFrame(root, text="Search Student", padx=10, pady=10, bg="#f0f4f8")
search_frame.grid(row=11, column=0, columnspan=2, padx=20, pady=10, sticky="ew")

search_field = ttk.Combobox(search_frame, values=["School", "Student ID", "First Name", "Last Name", "Mobile"], width=20)
search_field.grid(row=0, column=0, padx=10)
search_entry = tk.Entry(search_frame, width=30)
search_entry.grid(row=0, column=1, padx=10)
search_button = tk.Button(search_frame, text="Search", command=lambda: searchStudent())
search_button.grid(row=0, column=2, padx=10)

# Function Definitions
def addStudent():
    data = (
        entries['schoolentry'].get(),
        entries['studentidentry'].get(),
        entries['firstnameentry'].get(),
        entries['lastnameentry'].get(),
        entries['dateofbirthentry'].get(),
        entries['ageentry'].get(),
        entries['genderentry'].get(),
        entries['mobileentry'].get()
    )
    if not all(data):
        messagebox.showerror("Error", "All fields are required!")
        return
    addStdRec(*data)
    clearEntries()
    messagebox.showinfo("Success", "Student record added successfully")

def openDataWindow():
    data_window = tk.Toplevel(root)
    data_window.title("Student Records")
    tree = ttk.Treeview(data_window)
    tree["columns"] = ("id", "school", "std_id", "firstname", "lastname", "dob", "age", "gender", "mobile")
    for col in tree["columns"]:
        tree.heading(col, text=col.capitalize())
    tree.column("#0", width=0, stretch=tk.NO)
    tree.column("id", width=40)
    tree.column("school", width=120)
    tree.column("std_id", width=100)
    tree.column("firstname", width=100)
    tree.column("lastname", width=100)
    tree.column("dob", width=100)
    tree.column("age", width=50)
    tree.column("gender", width=80)
    tree.column("mobile", width=100)
    tree.pack(fill="both", expand=True)
    for student in viewData():
        tree.insert("", tk.END, values=student)

def searchStudent():
    search_by = search_field.get()
    search_term = search_entry.get()
    if not search_by or not search_term:
        messagebox.showwarning("Warning", "Please select a field and enter a term.")
        return
    results = searchData(search_term, search_by.replace(" ", ""))
    if results:
        openDataWindow()
    else:
        messagebox.showinfo("Info", "No matching records found.")

def updateStudent():
    student_id = simpledialog.askinteger("Input", "Enter Student ID to update:")
    if not student_id:
        return
    data = (
        entries['schoolentry'].get(),
        entries['studentidentry'].get(),
        entries['firstnameentry'].get(),
        entries['lastnameentry'].get(),
        entries['dateofbirthentry'].get(),
        entries['ageentry'].get(),
        entries['genderentry'].get(),
        entries['mobileentry'].get(),
        student_id
    )
    if not all(data[:-1]):
        messagebox.showerror("Error", "All fields are required!")
        return
    dataUpdate(*data)
    clearEntries()
    messagebox.showinfo("Success", "Student record updated successfully")

def deleteStudent():
    student_id = simpledialog.askinteger("Input", "Enter ID to delete:")
    if not student_id:
        return
    if messagebox.askyesno("Confirm", "Are you sure you want to delete this student?"):
        deleteRec(student_id)
        messagebox.showinfo("Success", "Student record deleted successfully")

def clearEntries():
    for entry in entries.values():
        entry.delete(0, tk.END)

root.mainloop()