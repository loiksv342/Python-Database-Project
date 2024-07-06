from tkinter import *
import pyodbc

def connect():
    servername = server_name_entry.get()
    databasename = database_name_entry.get()
    custom_query = query_entry.get().strip()

    if not custom_query:
        result_text = "No query provided."
        display_result(result_text)
        return

    conn_str = (
        f'DRIVER={{SQL Server}};'
        f'SERVER={servername};'
        f'DATABASE={databasename};'
        'Trusted_Connection=yes;'  # Use Windows authentication
    )

    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        if any(keyword in custom_query.upper() for keyword in ["INSERT", "DROP", "ALTER"]):
            cursor.execute(custom_query)
            conn.commit()
            result_text = f"{custom_query.split()[0].capitalize()} successful."
            display_result(result_text)
        else:
            cursor.execute(custom_query)
            results = cursor.fetchall()
            result_text = "\n".join(' | '.join(str(value) for value in row) for row in results)
            display_result(result_text)

        cursor.close()
        conn.close()
    except pyodbc.Error as ex:
        result_text = f"Error executing query: {ex}"
        display_result(result_text)

def display_result(result_text):
    query_text.config(state=NORMAL)
    query_text.delete(1.0, END)
    query_text.insert(END, result_text)
    query_text.config(state=DISABLED)

window = Tk()
window.title("SQL Server Connection")
window.geometry("1000x600")
window.config(bg="#2C3E50")

# Title Frame
title_frame = Frame(window, bg="#34495E")
title_frame.pack(fill=X, pady=10)

title_label = Label(title_frame, text="SQL Server - Python Connection", font=('Helvetica', 28, 'bold'), bg="#34495E",
                    fg="#ECF0F1")
title_label.pack(pady=20)

# Input Frame
input_frame = Frame(window, bg='#2C3E50')
input_frame.pack(pady=20)

# Server Name Entry
server_name_label = Label(input_frame, text="Server Name:", font=('Helvetica', 16), bg='#2C3E50', fg='#ECF0F1')
server_name_label.grid(row=0, column=0, padx=10, pady=10, sticky='e')

server_name_entry = Entry(input_frame, width=40, font=('Helvetica', 16), bg="#ECF0F1", fg="#2C3E50", relief=FLAT,
                          highlightthickness=1, highlightbackground="#95A5A6", highlightcolor="#2980B9")
server_name_entry.grid(row=0, column=1, padx=10, pady=10)

# Database Name Entry
database_name_label = Label(input_frame, text="Database Name:", font=('Helvetica', 16), bg='#2C3E50', fg='#ECF0F1')
database_name_label.grid(row=1, column=0, padx=10, pady=10, sticky='e')

database_name_entry = Entry(input_frame, width=40, font=('Helvetica', 16), bg="#ECF0F1", fg="#2C3E50", relief=FLAT,
                            highlightthickness=1, highlightbackground="#95A5A6", highlightcolor="#2980B9")
database_name_entry.grid(row=1, column=1, padx=10, pady=10)

# Query Entry
query_label = Label(input_frame, text="SQL Query:", font=('Helvetica', 16), bg='#2C3E50', fg='#ECF0F1')
query_label.grid(row=2, column=0, padx=10, pady=10, sticky='e')

query_entry = Entry(input_frame, width=40, font=('Helvetica', 16), bg="#ECF0F1", fg="#2C3E50", relief=FLAT,
                    highlightthickness=1, highlightbackground="#95A5A6", highlightcolor="#2980B9")
query_entry.grid(row=2, column=1, padx=10, pady=10)

# Connect Button
connect_btn = Button(input_frame, text="Execute Query", command=connect, width=20, font=('Helvetica', 14, 'bold'),
                     bg='#2980B9', fg='#ECF0F1', activebackground='#3498DB', activeforeground='#ECF0F1', relief=FLAT)
connect_btn.grid(row=3, columnspan=2, pady=20)

# Query Result Frame
query_frame = Frame(window, bg="#ECF0F1", bd=2, relief=FLAT)
query_frame.pack(fill=BOTH, expand=True, padx=20, pady=10)

query_text = Text(query_frame, font=('Courier', 14), wrap=WORD, bg="#ECF0F1", fg="#2C3E50", relief=FLAT, borderwidth=2,
                  highlightthickness=1, highlightbackground="#95A5A6", highlightcolor="#2980B9")
query_text.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 10))

scrollbar = Scrollbar(query_frame, command=query_text.yview)
scrollbar.pack(side=RIGHT, fill=Y)
query_text.config(yscrollcommand=scrollbar.set, state=DISABLED)

window.mainloop()
