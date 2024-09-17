import tkinter as tk
from tkinter import ttk
import datetime as dt
from db import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

data=Database('expenses.db')



class Expenses(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Expense Tracker")
        self.geometry("750x750")
        self.resizable(False, False)
        
        self.font=("Roboto", 14, "bold")
        self.notebook=ttk.Notebook(self)
        self.add_expense=tk.Frame(self.notebook)
        self.overview=tk.Frame(self.notebook)
        self.notebook.add(self.overview, text="Overview")
        self.notebook.add(self.add_expense, text="Add Expense")
        # self.configure(self.overview,bg="#abd5fa")
   
        name=ttk.Label(self.overview,text="Hi Pretty Boy!", foreground="black",background="#abd5fa", font=("Ebrima", 20, "bold"))
        name.place(x=30, y=30)
        self.box=tk.Frame(self.overview, width=350, height=150, border=2, relief="raised",borderwidth=3, bg="#ae98cd")
        self.box.place(x=30, y=80)
        self.box.pack_propagate(False)
        self.box_name=tk.Label(self.box,text="WALLET",bg="#ae98cd",font=self.font).place(relx=0.05, rely=0.05,anchor="nw")

        self.amount_spent=tk.Label(self.box, text="Amount Spent: $     ",font=self.font,bg="#ae98cd")
        self.amount_spent.place(relx=0.05,rely=0.45, anchor="nw")

        self.mybalance=tk.Label(self.box,font=self.font,bg="#ae98cd",text="Balance:$     ")
        self.mybalance.place(relx=0.05, rely=0.8)

        self.analysislbl=tk.Label(self.overview,text="Analysis", font=self.font).place(relx=0.05, rely=0.34)
        self.diagramlabel=tk.Label(self.overview)
        self.diagramlabel.place(relx=0.05, rely=0.37)
        
        self.selected_id=0
        self.count=0

       
        self.add_expenses()
        self.get_records()
        self.balance()
        self.create_piechart()
        
      
        self.notebook.pack(expand=True, fill="both")
        
        self.mainloop()

    



    def saveRecords(self):
        self.price=float(self.price_box.get())
        data.insertRecords(category=self.category_box.get(),description=self.description_box.get(),price=self.price,date=self.date_box.get())
        
        self.refreshdata()
        self.balance()
        self.clearBox()
        

    def getDate(self):
        date= dt.datetime.now().strftime("%B %d %Y")
        self.cur_datevar.set(f"{date}")
    
    def clearBox(self):
        self.category_box.delete(0, tk.END)
        self.description_box.delete(0, tk.END)
        self.price_box.delete(0, tk.END)
        self.date_box.delete(0, tk.END)

    def balance(self):
        sum=data.fetchRecords(query="SELECT sum(price) from expenses")
        print(sum)
        for i in sum:
            for j in i:
                if j is None:
                    j=0
                # messagebox.showinfo("Current balance ", f"Amount spent: {j}\n Total Balance: {10000-j}")
                self.amount_spent.config(text=f"Amount Spent: ${j}")
                self.mybalance.config(text=f"Balance: ${10000-j}")
                
    
    def update(self):
        selected=self.tv.focus()
        data.updateRecords(category=self.category_box.get(),description=self.description_box.get(),price=self.price_box.get(),date=self.date_box.get(),rid=self.selected_id)
        self.tv.item(selected,text="",values=(self.category_box.get(), self.description_box.get(), self.price_box.get(), self.date_box.get(),self.selected_id))

        self.clearBox() 
        self.balance()
        self.tv.after(400, self.refreshdata)   
    
        
    def delete(self):

        data.deleteRecords(self.selected_id)
        self.balance()
        self.refreshdata()

    def refreshdata(self):
        for item in self.tv.get_children():
            self.tv.delete(item)
        self.get_records()


    def get_records(self):
        self.count=0
        for record in data.fetchRecords(query="SELECT rowid, * FROM expenses"):
            self.tv.insert(parent="", iid=self.count, index=0, values=(record[0],record[3],record[2],record[4],record[1]))
            self.count+=1
        self.tv.after(400, self.refreshdata)

    def record_select(self,event):

        selected=self.tv.focus()
        selected_value=self.tv.item(selected, "values")
        if selected_value:
            self.selected_id=selected_value[0]
            self.category_var.set(selected_value[1])
            self.description_var.set(selected_value[2])
            self.price_var.set(selected_value[3])
            self.cur_datevar.set(str(selected_value[4]))


    def create_piechart(self):
        boss=data.fetchRecords(query="select category, sum(price) from expenses group by category")
        if boss:
            category=[item[0] for item in boss]
            price=[item[1] for item in boss]

            fig, ax=plt.subplots()
            ax.pie(price,labels=category, autopct='%1.1f%%', startangle=90)
            ax.axis("equal")

            canvas = FigureCanvasTkAgg(fig, master=self.diagramlabel)
            canvas.draw()
            canvas.get_tk_widget().pack(expand=True, fill="both")
        else:
            # If no data, display a message
            no_data_label = tk.Label(self.diagramlabel, text="No data available to display", font=("Arial", 14))
            no_data_label.place(relx=0.1, rely=0.6)




    

    def exit(self):
        self.destroy()
    
 
    def add_expenses(self):
        #This is the frame for the expenses tab i created in init
        #my init method was getting too long for my liking so i decided to write this here instead and call it 
        #in the init method. 


        #this is to make the widgets that would later be placed in take equal space
        #here that is f1 and f2
        self.add_expense.grid_rowconfigure(0, weight=1)
        self.add_expense.grid_rowconfigure(1, weight=1)
        self.add_expense.grid_columnconfigure(0, weight=1)

        #creating two frames 
        #one for the buttons and textboxes and the other for displaying the info
        f1=tk.Frame(self.add_expense, bg="red")
        f1.grid(row=0, column=0, sticky="nsew")  
        f2=tk.Frame(self.add_expense, bg="#affffe")
        f2.grid(row=1, column=0, sticky="nsew")  

        f2.rowconfigure(0, weight=1)
        f2.rowconfigure(1, weight=1)
        f2.rowconfigure(2, weight=1)
        f2.rowconfigure(3, weight=1)
        f2.columnconfigure(2,weight=1)
        f2.columnconfigure(3, weight=1)
        
        self.cur_datevar=tk.StringVar()
        self.price_var=tk.DoubleVar()
        self.category_var=tk.StringVar()
        self.description_var=tk.StringVar()
      
        tk.Label(f2, text="CATEGORY", font=self.font).grid(row=0, column=0, sticky="w", padx=(10,0))
        tk.Label(f2, text="DESCRIPTION", font=self.font).grid(row=1, column=0, sticky="w", padx=(10,0))
        tk.Label(f2, text="PRICE", font=self.font).grid(row=2, column=0, sticky="w", padx=(10,0))
        tk.Label(f2, text="DATE PURCHASED", font=self.font).grid(row=3, column=0, sticky="w", padx=(10,0))

        #category text box
        self.category_box = tk.Entry(f2, font=("Arial", 17),textvariable=self.category_var)
        self.category_box.grid(row=0, column=1, sticky="ew", padx=(10, 0))
        #description text box
        self.description_box = tk.Entry(f2, font=("Arial", 17),textvariable=self.description_var)
        self.description_box.grid(row=1, column=1, sticky="ew", padx=(10, 0))
        #price textbox
        self.price_box = tk.Entry(f2, font=("Arial", 17),textvariable=self.price_var)
        self.price_box.grid(row=2, column=1, sticky="ew", padx=(10, 0))
        #date textbox
        self.date_box = tk.Entry(f2, font=("Arial", 17),textvariable=self.cur_datevar)
        self.date_box.grid(row=3, column=1, sticky="ew", padx=(10, 0))
       
        savebtn=tk.Button(f2,
                          text="SAVE",
                          bg="#abcdef",
                          fg="#123456",
                          font=("Nunito", 12, "italic"),
                          command=self.saveRecords
                            )   
        clearbtn=tk.Button( f2,
                           text="CLEAR",
                          bg="#abcdef",
                          fg="#123456",
                          font=("Nunito", 12, "italic"),
                          command=self.clearBox)
        
        
        updatebtn=tk.Button(f2,
                             text="UPDATE",
                          bg="#abcdef",
                          fg="#123456",
                          font=("Nunito", 12, "italic"),
                          command=self.update
                          )
        
        datebtn=tk.Button(f2,
                          text="CURRENT DATE",
                          bg="#abcdef",
                          fg="#123456",
                          font=("Nunito", 12, "italic"),
                          command=self.getDate)
        
        deletebtn=tk.Button(f2,
                            text="DELETE",
                          bg="#abcdef",
                          fg="#123456",
                          font=("Nunito", 12, "italic"),
                          command=self.delete
                          )
        exitbtn=tk.Button(f2,
                          text="EXIT",
                          bg="#abcdef",
                          fg="#123498",
                          font=("Nunito", 12, "italic"),
                          command=self.exit
                          )
        savebtn.grid(row=0,column=2,padx=(10,0),sticky="ew")
        updatebtn.grid(row=1, column=2, padx=(10,0),sticky="ew")
        clearbtn.grid(row=2,column=2, padx=(10,0),sticky="ew")
        deletebtn.grid(row=0,column=3, padx=(10,0),sticky="ew")
        datebtn.grid(row=3,column=2, padx=(10,0),sticky="ew")
        exitbtn.grid(row=1,column=3, padx=(10,0),sticky="ew")

        self.tv=ttk.Treeview(f1)
        self.tv['columns']=( 'id', 'Category', 'Description', 'Price','Date')
        self.tv.column("#0", width=0, stretch=tk.NO)
        self.tv.column("id", anchor="center", width=50)
        self.tv.column("Category", anchor="center", width=80)
        self.tv.column("Description", anchor="center", width=200)
        self.tv.column("Price", anchor="center", width=70)
        self.tv.column("Date", anchor="center", width=90)

        self.tv.heading("id", text="ID")
        self.tv.heading("Category", text="CATEGORY")
        self.tv.heading("Description", text="DESCRIPTION")
        self.tv.heading("Price", text="PRICE")
        self.tv.heading("Date", text="DATE")

        self.tv.bind("<ButtonRelease-1>", self.record_select)

        scrollbar=ttk.Scrollbar(f1, orient="vertical", command=self.tv.yview)
        self.tv.configure(yscrollcommand=scrollbar.set(first=0.01, last=0.5))
        scrollbar.pack(side="right",fill="y")
        self.tv.pack(expand=True, fill="both")

        
        

    



    

