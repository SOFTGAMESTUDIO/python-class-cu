from tkinter import *
from tkinter import ttk


def show_details_page(name, roll_no, age):
    detail_window = Toplevel(root)
    detail_window.title("Student Details")
    detail_window.geometry("400x250")

    ttk.Label(detail_window, text="Student Information", font=("Arial", 14, "bold")).pack(pady=10)

    ttk.Label(detail_window, text=f"Name: {name}").pack(anchor="w", padx=20, pady=5)
    ttk.Label(detail_window, text=f"Roll No: {roll_no}").pack(anchor="w", padx=20, pady=5)
    ttk.Label(detail_window, text=f"Age: {age}").pack(anchor="w", padx=20, pady=5)

    ttk.Button(detail_window, text="Close", command=detail_window.destroy).pack(pady=15)




def submit_data():
    name = name_var.get().strip()
    roll_no = roll_var.get().strip()
    age = age_var.get().strip()

    if not name or not roll_no or not age:
        message.set("Please fill all fields.")
        return

    message.set("")
    show_details_page(name, roll_no, age)


root = Tk()
root.title("Student Form")
root.geometry("420x300")

name_var = StringVar()
roll_var = StringVar()
age_var = StringVar()
message = StringVar()

frame = ttk.Frame(root, padding=20)
frame.pack(fill="both", expand=True)

ttk.Label(frame, text="Enter Student Details", font=("Arial", 14, "bold")).pack()


ttk.Label(frame, text="Name:").grid(row=1, column=0, sticky="w", pady=5)
ttk.Entry(frame, textvariable=name_var, width=30).grid(row=1, column=1, pady=5)

ttk.Label(frame, text="Roll No:").grid(row=2, column=0, sticky="w", pady=5)
ttk.Entry(frame, textvariable=roll_var, width=30).grid(row=2, column=1, pady=5)

ttk.Label(frame, text="Age:").grid(row=3, column=0, sticky="w", pady=5)
ttk.Entry(frame, textvariable=age_var, width=30).grid(row=3, column=1, pady=5)

ttk.Button(frame, text="Submit", command=submit_data).grid(row=4, column=0, columnspan=2, pady=15)

ttk.Label(frame, textvariable=message, foreground="red").grid(row=5, column=0, columnspan=2)

root.mainloop()