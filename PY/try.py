import tkinter as tk


root = tk.Tk()
root.title("My Tkinter App")
root.geometry("400x400")

name_var = tk.StringVar()
password_var = tk.StringVar()
message = tk.StringVar()
message1 = tk.StringVar()




def submit_data():
    name = name_var.get().strip()
    password = password_var.get().strip()

    if not name == "Livesh" or not password == "1234":
        message.set("Invalid username or password.")
        message1.set("")
        return

    message.set("User logged in successfully!")
    message1.set(f"Welcome, {name}!")



Name = tk.Frame(root)
Name.pack()
tk.Label(Name, text="Name : ").grid(row=0, column=0)
tk.Entry(Name, textvariable=name_var).grid(row=0, column=1, padx=10, pady=10)

Password = tk.Frame(root)
Password.pack()
tk.Label(Password, text="Password : ").grid(row=0, column=0)
tk.Entry(Password, textvariable=password_var, show="*").grid(row=0, column=1, padx=10, pady=10)

Login = tk.Frame(root)
Login.pack()
tk.Button(Login, text="Login", command=submit_data).grid(row=0, column=0, padx=10, pady=10)

tk.Label(root, textvariable=message, fg="red").pack(pady=10)
tk.Label(root, textvariable=message1, fg="red").pack(pady=10)

root.mainloop()

