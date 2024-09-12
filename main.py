


# if __name__=="__main__":
#     pass

import tkinter as tk
from tkinter import ttk

root = tk.Tk()
notebook = ttk.Notebook(root)
notebook.pack(expand=True)

# Create the first tab
tab1 = tk.Frame(notebook)
notebook.add(tab1, text="Tab 1")
tk.Label(tab1, text="This is the first tab").pack()

# Button to add a new tab
def add_tab():
    tab2 = tk.Frame(notebook)
    notebook.add(tab2, text="New Tab")
    tk.Label(tab2, text="This is a new tab").pack()

def remove_tab():
    # Remove the first tab (index 0)
    notebook.forget(0)

# Add buttons for adding and removing tabs
tk.Button(root, text="Add Tab", command=add_tab).pack(side=tk.LEFT)
tk.Button(root, text="Remove Tab", command=remove_tab).pack(side=tk.LEFT)

root.mainloop()
