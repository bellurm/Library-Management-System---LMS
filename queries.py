import sqlite3

connection = sqlite3.connect("library.db")
cursor = connection.cursor()

def showBooks():
    cursor.execute("SELECT * FROM books")
    return cursor.fetchall()

def showBorrowed():
    cursor.execute("SELECT * FROM borrowedBooks")
    return cursor.fetchall()
