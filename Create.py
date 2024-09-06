#! python3
import os
import sqlite3
import hashlib 
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as msgbx

scriptdir = os.path.dirname(os.path.abspath(__file__))
path = 'docs/accounts.db'
db_path = os.path.join(scriptdir, path)
os.makedirs(os.path.dirname(db_path), exist_ok=True)
CON = sqlite3.connect(db_path)

file = "docs/MYLOGO.png"
pt = os.path.join(scriptdir, file)
os.makedirs(os.path.dirname(pt), exist_ok=True)

class accountFrame(tk.Frame):
    
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg="black")
        self.parent = parent
        self.parent.configure(bg="black")  # Set root window background to black
        self.parent.resizable(False, False)
        self.password = tk.StringVar()
        self.username = tk.StringVar()
        self.inval = tk.StringVar()
        self.hasher = hashlib.sha256()
        self.con = CON
        self.cur = self.con.cursor()
        
        if os.path.exists(pt):
            try:
                self.photo = tk.PhotoImage(file=pt)
                self.parent.iconphoto(False, self.photo)
            except tk.TclError as e:
                pass
        
        self.initComponents()
    
    def submit(self):
        user = self.username.get()
        word = self.password.get()
        if not user:
            user = "defaultUser"
        if not word:
            word = "1111"
        try:
            if user == "defaultUser":
                msgbx.showerror("Username Incorrect", "Must input a valid Username. PLEASE TRY AGAIN.")
                self.parent.destroy()
                self.rec()
                return 
        except:
            raise Exception("Error No. 516")  
        try:
            if len(word) < 5:
                msgbx.showerror("Password Incorrect", "Passcode must be at least 5 digits long. PLEASE TRY AGAIN.")
                self.parent.destroy()
                self.rec()
                return
        except:
            raise Exception("Error No. 414")
        self.hasher.update(word.encode('utf-8'))
        valHash = self.hasher.digest()
        PHash = str(valHash)
        try:
            learn = self.inval.get()
            if learn == "Select a Language:":
                raise Exception()
        except Exception as e:
            print(e)
            msgbx.showerror("Pick a Language", "You must pick a language from the Drop-Down-Menu on the Create Account page.")
            self.parent.destroy()
            self.rec()
            return
        self.cur.execute("CREATE TABLE IF NOT EXISTS accounts(username TEXT PRIMARY KEY, password BLOB, language TEXT)")
        self.cur.execute("SELECT username FROM accounts")
        data = self.cur.fetchall()
        for row in data:
            if user in row:
                msgbx.showerror("UserName Error", "Username is already in use. Please pick a different one.")
                self.parent.destroy()
                self.rec()
                return
        self.cur.execute("INSERT OR IGNORE INTO accounts(username, password, language) VALUES(?, ?, ?)", (user, PHash, learn))
        self.con.commit()
        self.cur.close()
        self.con.close()
        msgbx.showinfo("Account Creation", "Your account has been created successfully.")
        self.parent.destroy()
        self.learn = learn
        return self.learn

    def initComponents(self):
        self.pack(fill=tk.BOTH, expand=True)
        self.configure(bg="black")

        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TFrame', background='black')
        style.configure('TLabel', background='black', foreground='blue', font=('Helvetica', 12))
        style.configure('TEntry', fieldbackground='#333333', foreground='white', font=('Helvetica', 12))
        style.configure('TButton', background='#4CAF50', foreground='white', font=('Helvetica', 12, 'bold'))
        style.map('TButton', background=[('active', '#45a049')])
        style.configure('TOptionMenu', background='#333333', foreground='white', font=('Helvetica', 12))

        main_frame = ttk.Frame(self, style='TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        ttk.Label(main_frame, text="Welcome to the KIDS KAN KODE Website!", 
                  font=('Helvetica', 18, "bold"), foreground="#4CAF50").pack(pady=(0, 10))
        ttk.Label(main_frame, text="Create Your Account Below", 
                  font=('Helvetica', 14)).pack(pady=(0, 30))

        frame = ttk.Frame(main_frame, style='TFrame')
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="Username:").grid(row=0, column=0, sticky="w", pady=5)
        username_entry = ttk.Entry(frame, textvariable=self.username, width=30)
        username_entry.grid(row=0, column=1, sticky="ew", pady=5)
        username_entry.focus_set()

        ttk.Label(frame, text="Passcode:").grid(row=1, column=0, sticky="w", pady=5)
        passcode_entry = ttk.Entry(frame, textvariable=self.password, show="*", width=30)
        passcode_entry.grid(row=1, column=1, sticky="ew", pady=5)

        username_entry.bind("<Return>", lambda event: passcode_entry.focus_set())

        ttk.Label(frame, text="Select a Language:").grid(row=2, column=0, sticky="w", pady=(20,5))
        oplist = ["Python", "Java", "JavaScript", "HTML/CSS", "Terminal/Powershell", "CSharp"]
        self.inval.set("Select a Language")
        language_menu = ttk.OptionMenu(frame, self.inval, self.inval.get(), *oplist)
        language_menu.grid(row=2, column=1, sticky="ew", pady=(20,5))

        submit_button = ttk.Button(main_frame, text="Create Account", command=self.submit)
        submit_button.pack(pady=(30, 0))

    def rec(self):
        root = tk.Tk()
        root.title("KIDS KAN KODE")
        root.geometry("550x500+600+200")
        root.configure(bg="black")
        a = accountFrame(root)
        b = self.username.get()
        a.username.set(b)
        root.mainloop()

    def __str__(self):
        return self.learn

def start():
    root = tk.Tk()
    root.title("KIDS KAN KODE")
    root.geometry("525x330+600+200")
    root.configure(bg="black")
    accountFrame(root)
    root.mainloop()

if __name__ == "__main__":
    start()