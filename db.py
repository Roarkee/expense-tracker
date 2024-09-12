import sqlite3


class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cur = self.conn.cursor()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS expenses             
            (
            date DATE, 
            description TEXT,
            category TEXT, 
            price REAL)""")
        self.conn.commit()
    
    def fetchRecords(self, query):
        self.cur.execute(query)
        rows=self.cur.fetchall( )
        return rows
    
    def insertRecords(self, category, description, price, date ):
        self.cur.execute("INSERT INTO expenses values (?,?,?,?)", (category, description,price, date))
        self.conn.commit()

    def deleteRecords(self, id):
        self.cur.execute("DELETE FROM expenses where rowid=?", (id))
        self.conn.commit()

    def updateRecords(self, category, description, price, date, rid):
        self.cur.execute("UPDATE expenses SET category=?, description=?, price=?, date=? WHERE rowid=?", (category,description,price,date,rid))
        self.conn.commit()
    
    
    def __del__(self):
        self.conn.close()
        