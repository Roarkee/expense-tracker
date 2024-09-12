import tkinter as tk
from tkinter import ttk,PhotoImage,messagebox
import datetime as dt
import sqlite3
from db import *

data=Database('expenses.db')



class Expenses(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Expense Tracker")
        self.geometry("400x750")
        self.resizable(False, False)
        
        self.font=("Roboto", 17, "bold")
        self.notebook=ttk.Notebook(self)
        self.add_expense=tk.Frame(self.notebook)
        self.overview=tk.Frame(self.notebook)
        self.notebook.add(self.overview, text="Overview")
        self.notebook.add(self.add_expense, text="Add Expense")
        # self.configure(self.overview,bg="#abd5fa")
   
        name=ttk.Label(self.overview,text="Hi Pretty Boy!", foreground="black",background="#abd5fa", font=self.font)
        name.place(relx=0.25, rely=0.05, anchor=tk.CENTER)
        self.box=tk.Frame(self.overview, width=350, height=150, border=2, relief="raised",borderwidth=3, bg="#ae98cd")
        self.box.place(x=30, y=80)
        self.box.pack_propagate(False)
        self.box_name=tk.Label(self.box,text="WALLET",bg="#ae98cd",font=self.font).place(relx=0.05, rely=0.05,anchor="nw")
        self.amount_spent=tk.Label(self.box, text="Amount Spent: $     ",font=self.font,bg="#ae98cd").place(relx=0.05,rely=0.45, anchor="nw")
        self.mybalance=tk.Label(self.box,font=self.font,bg="#ae98cd",text="Balance:$     ").place(relx=0.05, rely=0.8)

        self.analysislbl=tk.Label(self.overview,text="Analysis", font=self.font).place(relx=0.1, rely=0.5)
        


        self.add_expenses()
        self.notebook.pack(expand=True, fill="both")
      
        self.mainloop()

    def saveRecords(self):
        data.insertRecords(category=self.category_box.get(),description=self.description_box.get(),price=self.price_box.get(),date=self.date_box.get())
    
    def getDate(self):
        date= dt.datetime.now()
        return date.strftime("%d-%m-%Y")
    
    def clearBox(self):
        self.category_box.delete(0, tk.END)
        self.description_box.delete(0, tk.END)
        self.price_box.delete(0, tk.END)
        self.date_box.delete(0, tk.END)

    def balance(self):
        sum=data.fetchRecords(query="SELECT sum(price) from expense")
        for x in sum:
            messagebox.showinfo("Current balance ", f"Amount spent: {x}\n Total Balance: {10000-x}")
    
    def update(self):
        data.updateRecords(category=self.category_box.get(),description=self.description_box.get(),price=self.price_box.get(),date=self.date_box.get())

    def delete(self):
        data.deleteRecords(id="rowid")
    
    
    

 
    def add_expenses(self):
        f1=tk.Frame(self.add_expense, padx=10, pady=10, bg="#123498")
        f1.grid(row=0, column=0, sticky="n")  
        f2=tk.Frame(self.add_expense, bg="#a945de")
        f2.grid(row=1, column=0, sticky="s")  
    
    
        tk.Label(f2, text="CATEGORY", font=self.font).grid(row=0, column=0, sticky="w")
        tk.Label(f2, text="DESCRIPTION", font=self.font).grid(row=1, column=0, sticky="w")
        tk.Label(f2, text="PRICE", font=self.font).grid(row=2, column=0, sticky="w")
        tk.Label(f2, text="DATE PURCHASED", font=self.font).grid(row=3, column=0, sticky="w")

        self.category_box = tk.Entry(f2, font=("Arial", 17))
        self.category_box.grid(row=0, column=1, sticky="ew", padx=(10, 0))
        self.description_box = tk.Entry(f2, font=("Arial", 17))
        self.description_box.grid(row=1, column=1, sticky="ew", padx=(10, 0))
        self.price_box = tk.Entry(f2, font=("Arial", 17))
        self.price_box.grid(row=2, column=1, sticky="ew", padx=(10, 0))
        self.date_box = tk.Entry(f2, font=("Arial", 17))
        self.date_box.grid(row=3, column=1, sticky="ew", padx=(10, 0))
       
        savebtn=tk.Button(f2,
                          text="SAVE",
                          bg="#abcdef",
                          fg="#123456",
                          font=("Nunito", 16, "italic"),
                          command=self.saveRecords
                            )   
        clearbtn=tk.Button( f2,
                           text="CLEAR",
                          bg="#abcdef",
                          fg="#123456",
                          font=("Nunito", 16, "italic"),
                          command=self.clearBox)
        
        
        updatebtn=tk.Button(f2,
                             text="UPDATE",
                          bg="#abcdef",
                          fg="#123456",
                          font=("Nunito", 16, "italic"),
                        #   command=
                          )
        
        datebtn=tk.Button(f2,
                          text="CURRENT DATE",
                          bg="#abcdef",
                          fg="#123456",
                          font=("Nunito", 16, "italic"),
                          command=self.getDate)
        
        deletebtn=tk.Button(f2,
                            text="DELETE",
                          bg="#abcdef",
                          fg="#123456",
                          font=("Nunito", 16, "italic"),
                        #   command=
                          )
        savebtn.grid(row=0,column=2)
        updatebtn.grid(row=1, column=2)
        clearbtn.grid(row=2,column=2)
        deletebtn.grid(row=0,column=3)
        datebtn.grid(row=1,column=3)
        

        

        
        

Expenses()
    



    

