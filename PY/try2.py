import tkinter as tk


root = tk.Tk()
root.title("My Tkinter App")
root.geometry("400x400")

First_No = tk.StringVar()
Second_No = tk.StringVar()
message = tk.StringVar()



def submit_data():
    FirstNo = First_No.get().strip()
    SecondNo = Second_No.get().strip()

    if not FirstNo or not SecondNo :
        message.set("Fill Both Fields")
        return

    temp = int(FirstNo) + int(SecondNo)
    message.set(f"Addition {FirstNo} & {SecondNo} is : {temp}")




FirstNo = tk.Frame(root)
FirstNo.pack()
tk.Label(FirstNo, text="First No : ").grid(row=0, column=0)
tk.Entry(FirstNo, textvariable=First_No).grid(row=0, column=1, padx=10, pady=10)

Password = tk.Frame(root)
Password.pack()
tk.Label(Password, text="Second No : ").grid(row=0, column=0)
tk.Entry(Password, textvariable=Second_No).grid(row=0, column=1, padx=10, pady=10)

Addition = tk.Frame(root)
Addition.pack()
tk.Button(Addition, text="Addition", command=submit_data).grid(row=0, column=0, padx=10, pady=10)

tk.Label(root, textvariable=message, fg="red").pack(pady=10)


root.mainloop()

