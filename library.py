import sqlite3
from tkinter import *
from tkinter import messagebox
from datetime import datetime
from datetime import timedelta
import queries
import threading

class Library:
    connection = sqlite3.connect("library.db", check_same_thread=False)
    cursor = connection.cursor()
    
    @classmethod
    def connectionClose(cls):
        return cls.connection.close()

    def __init__(self,root):
        self.root = root
        # self.root.geometry("1920x1080")
        self.root.attributes('-fullscreen', True)
        self.root.title("Cyber Worm")
        self.root.iconbitmap("C:/Python/EMS/logo.ico")
        self.root.configure(bg="#005b96")

        self.counterOfData = 0
        
        ### Get the date and time ###
        self.todayInfo = datetime.now().replace(microsecond=0)
        self.fullDate = self.todayInfo.strftime("%Y-%m-%d %H:%M:%S")
        self.future = timedelta(minutes=0.6)
        self.deadlineDate = self.todayInfo + self.future
        ### Set Entries' Default Value ###
        self.defaultBorrowedDate = StringVar()
        self.defaultBorrowedDate.set(f"{self.fullDate}")

        self.defaultDeadline = StringVar()
        self.defaultDeadline.set(f"{self.deadlineDate}")
        ### Set Entries' Default Value ###

        # Title
        titleLabel = Label(self.root, text="LIBRARY MANAGEMENT SYSTEM (LMS)", font=('Arial', 30, 'bold'), bg='#005b96', fg='red')
        titleLabel.place(relx=0.2, rely=0.02)

        ################################################################## Exist Books Frame ##################################################################
        self.showBooksFrame = LabelFrame(self.root, text="Exist Books", bg='#005b96', fg='red', font=('Arial', 14, 'bold'))#, width=1200, height=350)
        self.showBooksFrame.place(relx=0.01, rely=0.1)    
    
        self.booksList = queries.showBooks()
        self.scrbar = Scrollbar(self.showBooksFrame)
        self.scrbar.pack(side=RIGHT, fill=Y)
        self.myList = Listbox(self.showBooksFrame, yscrollcommand=self.scrbar.set, width=110, height=15, bg='#005b96', fg='white', font=('Arial', 12, 'bold'))

        for rowBooksList in enumerate(self.booksList, 1):
                self.myList.insert(END, str(rowBooksList))

        self.myList.pack(side=LEFT)
        self.scrbar.config(command=self.myList.yview)
        ################################################################## Exist Books Frame ##################################################################

        ######################################################## Lend Book and Show Borrowed List Frame ########################################################
        self.lendBookFrame = LabelFrame(self.root, text="Lend", bg='#005b96', fg='red', font=('Arial', 12, 'bold'), width=450, height=720)
        self.lendBookFrame.place(relx=0.68, rely=0.1)

        self.borrowerLabel = Label(self.lendBookFrame, text="Borrower Name:", bg='#005b96', fg='white', font=('Arial', 12, 'bold'))
        self.borrowerLabel.place(relx=0.05, rely=0.03)
        self.borrowerEntry = Entry(self.lendBookFrame, border=5, bg='white', width=40)
        self.borrowerEntry.place(relx=0.4, rely=0.03)

        self.borrowerPhoneLabel = Label(self.lendBookFrame, text="Borrower Phone:", bg='#005b96', fg='white', font=('Arial', 12, 'bold'))
        self.borrowerPhoneLabel.place(relx=0.05, rely=0.1)
        self.borrowerPhoneEntry = Entry(self.lendBookFrame, border=5, bg='white', width=40)
        self.borrowerPhoneEntry.place(relx=0.4, rely=0.1)

        self.borrowedDateLabel = Label(self.lendBookFrame, text="Borrowed Date:", bg='#005b96', fg='white', font=('Arial', 12, 'bold'))
        self.borrowedDateLabel.place(relx=0.05, rely=0.17)
        self.borrowedDateEntry = Entry(self.lendBookFrame, textvariable=self.defaultBorrowedDate, border=5, bg='white', width=40)
        self.borrowedDateEntry.place(relx=0.4, rely=0.17)

        self.deadlineLabel = Label(self.lendBookFrame, text="Deadline:", bg='#005b96', fg='white', font=('Arial', 12, 'bold'))
        self.deadlineLabel.place(relx=0.05, rely=0.24)
        self.deadlineEntry = Entry(self.lendBookFrame, textvariable=self.defaultDeadline, border=5, bg='white', width=40)
        self.deadlineEntry.place(relx=0.4, rely=0.24)

        self.rowIDLabel = Label(self.lendBookFrame, text="Book's ID:", bg='#005b96', fg='white', font=('Arial', 12, 'bold'))
        self.rowIDLabel.place(relx=0.05, rely=0.31)
        self.rowIDEntry = Entry(self.lendBookFrame, border=5, bg='white', width=40)
        self.rowIDEntry.place(relx=0.4, rely=0.31)

        self.borrowedBooksFrame = LabelFrame(self.root, text="Borrowed Books", bg='#005b96', fg='red', font=('Arial', 12, 'bold'), width=1000, height=350)
        self.borrowedBooksFrame.place(relx=0.01, rely=0.55)

        self.borrowList = queries.showBorrowed()
        self.scrbarLend = Scrollbar(self.borrowedBooksFrame)
        self.scrbarLend.pack(side=RIGHT, fill=Y)
        self.myLendList = Listbox(self.borrowedBooksFrame, yscrollcommand=self.scrbarLend.set, width=110, height=15, bg='#005b96', fg='white', font=('Arial', 12, 'bold'))

        for rowBorrowList in enumerate(self.borrowList, 1):
                self.myLendList.insert(END, str(rowBorrowList))
        
        self.myLendList.pack(side=LEFT)
        self.scrbarLend.config(command=self.myLendList.yview)

        def getTime():
            presentTime = datetime.now().replace(microsecond=0)
            return presentTime
        
        def timeToTime():
            rightNow = getTime()
            timer = threading.Timer(1.0, timeToTime)
            timer.start()

            if rightNow == self.deadlineDate:
                self.cursor.execute(f"SELECT name FROM books WHERE ROWID='{self.rowIDEntry.get()}'")
                bookName = self.cursor.fetchall()
                print("*"*50)
                self.cursor.execute(f"UPDATE books SET borrowedStatus='False' WHERE ROWID='{self.rowIDEntry.get()}'")
                self.connection.commit()
                print("FALSE OLDU")
                print("*"*50)
                self.cursor.execute(f"""SELECT borrowedStatus FROM books WHERE ROWID="{self.rowIDEntry.get()}" """)
                allBorrowedStatus = self.cursor.fetchall()
                for i in allBorrowedStatus:
                    for j in i:
                        if j == 'False':
                            print("*"*50)
                            self.cursor.execute(f"DELETE FROM borrowedBooks WHERE borrowedBookName='{bookName[0][0]}'")
                            self.connection.commit()
                            print("SİLİNDİ")
                            print("*"*50)
                            timer.cancel()
                            print("TIMER IS CANCELLED")
        def lendTo():
            try:
                self.cursor.execute(f"UPDATE books SET borrowedStatus='True' WHERE ROWID='{self.rowIDEntry.get()}'")
                self.connection.commit()
                print("TRUE OLDU")

                self.cursor.execute(f"SELECT name FROM books WHERE ROWID='{self.rowIDEntry.get()}'")
                bookName = self.cursor.fetchall()
                
                self.cursor.execute(f"""SELECT borrowedStatus FROM books WHERE ROWID="{self.rowIDEntry.get()}" """)
                allBorrowedStatus = self.cursor.fetchall()

                for check in allBorrowedStatus:
                    for clearData in check:
                        if clearData == 'True':
                            if self.counterOfData == 0:
                                self.cursor.execute(f"INSERT INTO borrowedBooks VALUES('{self.borrowerEntry.get()}', '{self.borrowerPhoneEntry.get()}', '{bookName[0][0]}', '{self.borrowedDateEntry.get()}', '{self.deadlineEntry.get()}')")
                                self.connection.commit()
                                print("EKLENDİ")
                                self.counterOfData = 1
                                timeToTime()
                            else:
                                return messagebox.showerror("System Message", "A book can only be loaned once. You can request the book from the borrower.")

            except sqlite3.OperationalError:
                return messagebox.showerror("System Message", """You may not have entered the "Book's ID".""")
            except IndexError:
                return messagebox.showerror("System Message", """The "Book's ID" you entered may not be valid.""")

        lendToButton = Button(self.lendBookFrame, text="Lend to", fg='red', font=('Arial', 10, 'bold') ,width=50, height=4, command=lendTo)
        lendToButton.place(relx=0.05, rely=0.37)
        ######################################################## Lend Book and Show Borrowed List Frame ########################################################
        
        ############################################################# Refresh Button #############################################################
        def refresh():
            self.__init__(root)

        refreshButton = Button(self.lendBookFrame, text="Refresh", fg='red', font=('Arial', 10, 'bold') ,width=50, height=4, command=refresh)
        refreshButton.place(relx=0.05, rely=0.50)
        ############################################################# Refresh Button #############################################################

        self.borrowerLabel = Label(self.lendBookFrame, text="Buraya el ile kayıt silme işlemini yapabilirsiniz.", bg='#005b96', fg='red', font=('Arial', 14, 'bold'))
        self.borrowerLabel.place(relx=0.02, rely=0.8)

if __name__ == "__main__":
    root = Tk()
    rootObject = Library(root)
    root.mainloop()
    Library.connectionClose()
