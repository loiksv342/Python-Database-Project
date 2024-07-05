import pyodbc

print()
database_name = input("Enter your database name: ").strip()
# table_name = input("Na jakiej tabeli chcesz wykonywać operacje?")
server_name = 'loiks'
conn_str = (
    'DRIVER={SQL Server};'
    f'SERVER={server_name};'
    f'DATABASE={database_name};'
    'Trusted_Connection=yes;'  # Użyj autoryzacji Windows
)

try:
    conn = pyodbc.connect(conn_str)
    print("Connection done!")
except pyodbc.Error as ex:
    sqlstate = ex.args[1]
    print(f"Connection error: {sqlstate}")
    exit()

# Utwórz kursor
cursor = conn.cursor()

# Zapytanie SQL

sql_query = input("Enter your query: ")

try:
    # Wykonaj zapytanie
    cursor.execute(sql_query)

    # Pobierz wszystkie wiersze
    rows = cursor.fetchall()

    # Wyświetl wyniki
    for row in rows:
        print(row)

except pyodbc.Error as ex:
    print(f"Błąd wykonania zapytania: {ex}")

# Zamknij kursor i połączenie
cursor.close()
conn.close()
