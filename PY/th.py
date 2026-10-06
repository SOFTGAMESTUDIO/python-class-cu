import tkinter as tk

root = tk.Tk()
root.iconbitmap(r'logo.png')
root.title("My Tkinter App")
root.geometry("400x400")


frame1 = tk.Frame(root)
frame1.pack()
tk.Button(frame1, text="Button 1").pack()

frame2 = tk.Frame(root)
frame2.pack()
tk.Button(frame2, text="Button 2").grid(row=0, column=0)

tk.Button(root, text="Button 3").place(x=180, y=200)


root.mainloop()