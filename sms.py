from tkinter import *  # Import all necessary modules from tkinter
import time  # Import time module to handle time-related tasks
import ttkthemes  # Import ttkthemes for themed Tkinter widgets
from tkinter import (
    ttk,
    messagebox,
    filedialog,
)  # Import specific components from tkinter
import pymysql  # Import pymysql to handle MySQL database connections
import pandas  # Import pandas for handling data manipulation


# Function to handle the exit functionality with confirmation
def iexit():
    result = messagebox.askyesno("Confirm", "Do you want to exit?")
    if result:  # If the user confirms, close the application
        root.destroy()
    else:  # Otherwise, do nothing
        pass


# Function to export student data to a CSV file
def export_data():
    url = filedialog.asksaveasfilename(
        defaultextension=".csv"
    )  # Prompt user to select save location and name for CSV file
    indexing = studentTable.get_children()  # Get all the student data from the table
    newlist = []
    for index in indexing:  # Iterate through each row in the table
        content = studentTable.item(index)  # Extract the data of that row
        datalist = content["values"]
        newlist.append(datalist)  # Append the extracted data to the list

    # Convert the list of student data into a pandas DataFrame and save it as a CSV file
    table = pandas.DataFrame(
        newlist,
        columns=[
            "Id",
            "Name",
            "Mobile",
            "Email",
            "Address",
            "Gender",
            "DOB",
            "Added Date",
            "Added Time",
        ],
    )
    table.to_csv(url, index=False)
    messagebox.showinfo("Success", "Data is saved successfully")


# Function to create a new window for adding, updating, or searching students
def toplevel_data(title, button_text, command):
    global idEntry, phoneEntry, nameEntry, emailEntry, addressEntry, genderEntry, dobEntry, screen
    screen = Toplevel()  # Create a new top-level window
    screen.title(title)  # Set the title of the window
    screen.grab_set()  # Make this window modal (disables other windows)
    screen.resizable(False, False)  # Disable resizing of the window

    # Create labels and entry widgets for each student attribute
    idLabel = Label(screen, text="Id", font=("times new roman", 20, "bold"))
    idLabel.grid(row=0, column=0, padx=30, pady=15, sticky=W)
    idEntry = Entry(screen, font=("roman", 15, "bold"), width=24)
    idEntry.grid(row=0, column=1, pady=15, padx=10)

    nameLabel = Label(screen, text="Name", font=("times new roman", 20, "bold"))
    nameLabel.grid(row=1, column=0, padx=30, pady=15, sticky=W)
    nameEntry = Entry(screen, font=("roman", 15, "bold"), width=24)
    nameEntry.grid(row=1, column=1, pady=15, padx=10)

    phoneLabel = Label(screen, text="Phone", font=("times new roman", 20, "bold"))
    phoneLabel.grid(row=2, column=0, padx=30, pady=15, sticky=W)
    phoneEntry = Entry(screen, font=("roman", 15, "bold"), width=24)
    phoneEntry.grid(row=2, column=1, pady=15, padx=10)

    emailLabel = Label(screen, text="Email", font=("times new roman", 20, "bold"))
    emailLabel.grid(row=3, column=0, padx=30, pady=15, sticky=W)
    emailEntry = Entry(screen, font=("roman", 15, "bold"), width=24)
    emailEntry.grid(row=3, column=1, pady=15, padx=10)

    addressLabel = Label(screen, text="Address", font=("times new roman", 20, "bold"))
    addressLabel.grid(row=4, column=0, padx=30, pady=15, sticky=W)
    addressEntry = Entry(screen, font=("roman", 15, "bold"), width=24)
    addressEntry.grid(row=4, column=1, pady=15, padx=10)

    genderLabel = Label(screen, text="Gender", font=("times new roman", 20, "bold"))
    genderLabel.grid(row=5, column=0, padx=30, pady=15, sticky=W)
    genderEntry = Entry(screen, font=("roman", 15, "bold"), width=24)
    genderEntry.grid(row=5, column=1, pady=15, padx=10)

    dobLabel = Label(screen, text="D.O.B", font=("times new roman", 20, "bold"))
    dobLabel.grid(row=6, column=0, padx=30, pady=15, sticky=W)
    dobEntry = Entry(screen, font=("roman", 15, "bold"), width=24)
    dobEntry.grid(row=6, column=1, pady=15, padx=10)

    # Create a button that will execute the passed command when clicked
    student_button = ttk.Button(screen, text=button_text, command=command)
    student_button.grid(row=7, columnspan=2, pady=15)

    # If the window is for updating a student, populate the fields with the selected student's data
    if title == "Update Student":
        indexing = studentTable.focus()  # Get the focused row in the table
        content = studentTable.item(indexing)  # Retrieve the data of the selected row
        listdata = content["values"]
        # Insert the data into the respective entry fields
        idEntry.insert(0, listdata[0])
        nameEntry.insert(0, listdata[1])
        phoneEntry.insert(0, listdata[2])
        emailEntry.insert(0, listdata[3])
        addressEntry.insert(0, listdata[4])
        genderEntry.insert(0, listdata[5])
        dobEntry.insert(0, listdata[6])


# Function to update a student's data in the database
def update_data():
    query = "update student set name=%s, mobile=%s, email=%s, address=%s, gender=%s, dob=%s, date=%s, time=%s where id=%s"
    # Execute the update query with the values from the entry fields
    mycursor.execute(
        query,
        (
            nameEntry.get(),
            phoneEntry.get(),
            emailEntry.get(),
            addressEntry.get(),
            genderEntry.get(),
            dobEntry.get(),
            date,
            currenttime,
            idEntry.get(),
        ),
    )
    con.commit()  # Commit the changes to the database
    messagebox.showinfo(
        "Success", f"Id {idEntry.get()} is modified successfully", parent=screen
    )
    screen.destroy()  # Close the update window
    show_student()  # Refresh the table to show the updated data


# Function to fetch and display all student data in the table
def show_student():
    query = "select * from student"  # SQL query to select all students
    mycursor.execute(query)
    fetched_data = mycursor.fetchall()  # Fetch all rows from the database
    studentTable.delete(*studentTable.get_children())  # Clear the table
    for data in fetched_data:  # Insert each student's data into the table
        studentTable.insert("", END, values=data)


# Function to delete a selected student from the database
def delete_student():
    indexing = studentTable.focus()  # Get the focused row in the table
    content = studentTable.item(indexing)
    content_id = content["values"][0]  # Extract the student ID from the selected row
    query = "delete from student where id=%s"
    mycursor.execute(query, content_id)  # Execute the delete query
    con.commit()  # Commit the changes
    messagebox.showinfo("Deleted", f"Id {content_id} is deleted successfully")
    show_student()  # Refresh the table to show remaining data


# Function to search for students based on various criteria
def search_data():
    query = "select * from student where id=%s or name=%s or email=%s or mobile=%s or address=%s or gender=%s or dob=%s"
    # Execute the search query using the values from the entry fields
    mycursor.execute(
        query,
        (
            idEntry.get(),
            nameEntry.get(),
            emailEntry.get(),
            phoneEntry.get(),
            addressEntry.get(),
            genderEntry.get(),
            dobEntry.get(),
        ),
    )
    studentTable.delete(*studentTable.get_children())  # Clear the table
    fetched_data = mycursor.fetchall()  # Fetch the search results
    for data in fetched_data:  # Insert the search results into the table
        studentTable.insert("", END, values=data)


# Function to add a new student to the database
def add_data():
    # Check if any entry field is empty
    if (
        idEntry.get() == ""
        or nameEntry.get() == ""
        or phoneEntry.get() == ""
        or emailEntry.get() == ""
        or addressEntry.get() == ""
        or genderEntry.get() == ""
        or dobEntry.get() == ""
    ):
        messagebox.showerror("Error", "All Fields are required", parent=screen)
    else:
        try:
            query = "insert into student values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            # Execute the insert query with the values from the entry

            mycursor.execute(
                query,
                (
                    idEntry.get(),
                    nameEntry.get(),
                    phoneEntry.get(),
                    emailEntry.get(),
                    addressEntry.get(),
                    genderEntry.get(),
                    dobEntry.get(),
                    date,
                    currenttime,
                ),
            )
            con.commit()
            result = messagebox.askyesno(
                "Confirm",
                "Data added successfully. Do you want to clean the form?",
                parent=screen,
            )
            if result:
                idEntry.delete(0, END)
                nameEntry.delete(0, END)
                phoneEntry.delete(0, END)
                emailEntry.delete(0, END)
                addressEntry.delete(0, END)
                genderEntry.delete(0, END)
                dobEntry.delete(0, END)
            else:
                pass
        except:
            messagebox.showerror("Error", "Id cannot be repeated", parent=screen)
            return

        query = "select *from student"
        mycursor.execute(query)
        fetched_data = mycursor.fetchall()
        studentTable.delete(*studentTable.get_children())
        for data in fetched_data:
            studentTable.insert("", END, values=data)


def connect_database():
    def connect():
        global mycursor, con
        try:
            con = pymysql.connect(
                host=hostEntry.get(),
                user=usernameEntry.get(),
                password=passwordEntry.get(),
            )
            mycursor = con.cursor()
        except:
            messagebox.showerror("Error", "Invalid Details", parent=connectWindow)
            return

        try:
            query = "create database studentmanagementsystem"
            mycursor.execute(query)
            query = "use studentmanagementsystem"
            mycursor.execute(query)
            query = (
                "create table student(id int not null primary key, name varchar(30),mobile varchar(10),email varchar(30),"
                "address varchar(100),gender varchar(20),dob varchar(20),date varchar(50), time varchar(50))"
            )
            mycursor.execute(query)
        except:
            query = "use studentmanagementsystem"
            mycursor.execute(query)
        messagebox.showinfo(
            "Success", "Database Connection is successful", parent=connectWindow
        )
        connectWindow.destroy()
        addstudentButton.config(state=NORMAL)
        searchstudentButton.config(state=NORMAL)
        updatestudentButton.config(state=NORMAL)
        showstudentButton.config(state=NORMAL)
        exportstudentButton.config(state=NORMAL)
        deletestudentButton.config(state=NORMAL)

    connectWindow = Toplevel()
    connectWindow.grab_set()
    connectWindow.geometry("470x250+730+230")
    connectWindow.title("Database Connection")
    connectWindow.resizable(0, 0)

    hostnameLabel = Label(connectWindow, text="Host Name", font=("arial", 20, "bold"))
    hostnameLabel.grid(row=0, column=0, padx=20)

    hostEntry = Entry(connectWindow, font=("roman", 15, "bold"), bd=2)
    hostEntry.grid(row=0, column=1, padx=40, pady=20)

    usernameLabel = Label(connectWindow, text="User Name", font=("arial", 20, "bold"))
    usernameLabel.grid(row=1, column=0, padx=20)

    usernameEntry = Entry(connectWindow, font=("roman", 15, "bold"), bd=2)
    usernameEntry.grid(row=1, column=1, padx=40, pady=20)

    passwordLabel = Label(connectWindow, text="Password", font=("arial", 20, "bold"))
    passwordLabel.grid(row=2, column=0, padx=20)

    passwordEntry = Entry(connectWindow, font=("roman", 15, "bold"), bd=2)
    passwordEntry.grid(row=2, column=1, padx=40, pady=20)

    connectButton = ttk.Button(connectWindow, text="CONNECT", command=connect)
    connectButton.grid(row=3, columnspan=2)


count = 0
text = ""


def slider():
    global text, count
    if count == len(s):
        count = 0
        text = ""
    text = text + s[count]
    sliderLabel.config(text=text)
    count += 1
    sliderLabel.after(300, slider)


def clock():
    global date, currenttime
    date = time.strftime("%d/%m/%Y")
    currenttime = time.strftime("%H:%M:%S")
    datetimeLabel.config(text=f"   Date: {date}\nTime: {currenttime}")
    datetimeLabel.after(1000, clock)


# GUI Part
root = ttkthemes.ThemedTk()

root.get_themes()

root.set_theme("radiance")

root.geometry("1174x680+0+0")
root.resizable(0, 0)
root.title("Student Management System")

datetimeLabel = Label(root, font=("times new roman", 18, "bold"))
datetimeLabel.place(x=5, y=5)
clock()
s = "Student Management System"  # s[count]=t when count is 1
sliderLabel = Label(root, font=("arial", 28, "italic bold"), width=30)
sliderLabel.place(x=200, y=0)
slider()

connectButton = ttk.Button(root, text="Connect database", command=connect_database)
connectButton.place(x=980, y=0)

leftFrame = Frame(root)
leftFrame.place(x=50, y=80, width=300, height=600)

logo_image = PhotoImage(file="student.png")
logo_Label = Label(leftFrame, image=logo_image)
logo_Label.grid(row=0, column=0)

addstudentButton = ttk.Button(
    leftFrame,
    text="Add Student",
    width=25,
    state=DISABLED,
    command=lambda: toplevel_data("Add Student", "Add", add_data),
)
addstudentButton.grid(row=1, column=0, pady=15)

searchstudentButton = ttk.Button(
    leftFrame,
    text="Search Student",
    width=25,
    state=DISABLED,
    command=lambda: toplevel_data("Search Student", "Search", search_data),
)
searchstudentButton.grid(row=2, column=0, pady=15)

deletestudentButton = ttk.Button(
    leftFrame, text="Delete Student", width=25, state=DISABLED, command=delete_student
)
deletestudentButton.grid(row=3, column=0, pady=15)

updatestudentButton = ttk.Button(
    leftFrame,
    text="Update Student",
    width=25,
    state=DISABLED,
    command=lambda: toplevel_data("Update Student", "Update", update_data),
)
updatestudentButton.grid(row=4, column=0, pady=15)

showstudentButton = ttk.Button(
    leftFrame, text="Show Student", width=25, state=DISABLED, command=show_student
)
showstudentButton.grid(row=5, column=0, pady=15)

exportstudentButton = ttk.Button(
    leftFrame, text="Export data", width=25, state=DISABLED, command=export_data
)
exportstudentButton.grid(row=6, column=0, pady=15)

exitButton = ttk.Button(leftFrame, text="Exit", width=25, command=iexit)
exitButton.grid(row=7, column=0, pady=15)

rightFrame = Frame(root)
rightFrame.place(x=350, y=80, width=820, height=600)

scrollBarX = Scrollbar(rightFrame, orient=HORIZONTAL)
scrollBarY = Scrollbar(rightFrame, orient=VERTICAL)

studentTable = ttk.Treeview(
    rightFrame,
    columns=(
        "Id",
        "Name",
        "Mobile",
        "Email",
        "Address",
        "Gender",
        "D.O.B",
        "Added Date",
        "Added Time",
    ),
    xscrollcommand=scrollBarX.set,
    yscrollcommand=scrollBarY.set,
)

scrollBarX.config(command=studentTable.xview)
scrollBarY.config(command=studentTable.yview)

scrollBarX.pack(side=BOTTOM, fill=X)
scrollBarY.pack(side=RIGHT, fill=Y)

studentTable.pack(expand=1, fill=BOTH)

studentTable.heading("Id", text="Id")
studentTable.heading("Name", text="Name")
studentTable.heading("Mobile", text="Mobile No")
studentTable.heading("Email", text="Email Address")
studentTable.heading("Address", text="Address")
studentTable.heading("Gender", text="Gender")
studentTable.heading("D.O.B", text="D.O.B")
studentTable.heading("Added Date", text="Added Date")
studentTable.heading("Added Time", text="Added Time")

studentTable.column("Id", width=50, anchor=CENTER)
studentTable.column("Name", width=200, anchor=CENTER)
studentTable.column("Email", width=300, anchor=CENTER)
studentTable.column("Mobile", width=200, anchor=CENTER)
studentTable.column("Address", width=300, anchor=CENTER)
studentTable.column("Gender", width=100, anchor=CENTER)
studentTable.column("D.O.B", width=200, anchor=CENTER)
studentTable.column("Added Date", width=200, anchor=CENTER)
studentTable.column("Added Time", width=200, anchor=CENTER)

style = ttk.Style()

style.configure(
    "Treeview",
    rowheight=40,
    font=("arial", 12, "bold"),
    fieldbackground="white",
    background="white",
)
style.configure("Treeview.Heading", font=("arial", 14, "bold"), foreground="red")

studentTable.config(show="headings")

root.mainloop()
