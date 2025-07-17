import os
from datetime import timedelta, date
from dotenv import load_dotenv
import mysql.connector


load_dotenv()

try:
    # Connect to MySQL database
    db = mysql.connector.connect(
        host=os.getenv("db_HOST"),
        user=os.getenv("db_USER"),
        password=os.getenv("db_PASSWORD"),
    )
    cursor = db.cursor()

    # Create database if it doesn't exist
    cursor.execute("CREATE DATABASE IF NOT EXISTS library_management")
    cursor.execute("USE library_management")

    # Create BOOKS table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS BOOKS (
        book_id VARCHAR(150) PRIMARY KEY,
        book_title VARCHAR(200),
        quantity INT
    )
    """)

    # Create USERS table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS USERS (
        ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100),
        user_id VARCHAR(150),
        book_id VARCHAR(150),
        book_title VARCHAR(200),
        borrow DATE NOT NULL,
        return_due DATE,
        FOREIGN KEY(book_id) REFERENCES BOOKS(book_id)
    )
    """)

except mysql.connector.Error as err:
    print("Error",err)
    exit()

def borrow_book():
    try:
        name = input("Enter your name: ")
        user_id = input("Enter your id: ")

        cursor.execute("SELECT * FROM BOOKS WHERE quantity>0")
        books = cursor.fetchall()
        if not books:
            print("No books available.\n")
            return

        print("--AVAILABLE BOOKS--")
        for book in books:
            print(f"{book[0]} : {book[1]}")
        num_books=int(input("ENTER NUMBER OF BOOKS YOU WISH TO BORROW--")
        borrowed=[]
        if num_books>10:
                      print("YOU CANNOT BORROW MORE THAN 10 BOOKS")
        for i in range(num_books)
                      
        book_id = input("Enter your book id to borrow: ")
        cursor.execute("SELECT book_title FROM BOOKS WHERE book_id=%s AND available=TRUE", (book_id,))
        res = cursor.fetchone()

        if not res:
            print("No such available book.\n")
            return

        book_title = res[0]
        borrow = date.today()
        return_due = borrow + timedelta(days=7)

        cursor.execute("""
            INSERT INTO USERS(name, user_id, book_id, book_title, borrow, return_due)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (name, user_id, book_id, book_title, borrow, return_due))

        cursor.execute("UPDATE BOOKS SET quantity= quantiti - 1  book_id = %s", (book_id,))
    db.commit()
    print(f"\nBorrowed {book_title} (ID: {book_id}). Return by {return_due}.\n")
except Exception as e:
    print("Error", e)
        
def return_book():
    try:
        name = input("Enter your name: ")
        user_id = input("Enter your user-id to return the book: ")

        cursor.execute("""
            SELECT id, book_title, book_id, borrow, return_due 
            FROM USERS WHERE user_id = %s AND return_due IS NOT NULL
        """, (user_id,))
        records = cursor.fetchall()

        if not records:
            print("No borrowed books found.\n")
            return

        print("\n--- Your Borrowed Books ---")
        for record in records:
            id_, book_title, book_id, borrow, return_due = record
            print(f"\nBook ID     : {book_id}")
            print(f"Title       : {book_title}")
            print(f"Borrowed On : {borrow}")
            print(f"Return Due  : {return_due}")

            cursor.execute("UPDATE BOOKS SET available = TRUE WHERE book_id = %s", (book_id,))
            cursor.execute("UPDATE USERS SET return_due = NULL WHERE id = %s", (id_,))
            db.commit()
            print("Book returned successfully.\n")
    except Exception as e:
        print("Error", e)

def add_book():
    try:
        admin_pass = input("Enter admin password: ")
        if admin_pass != "admin123":
            print("Access Denied. Incorrect password.\n")
            return

        title = input("Enter book title: ")
        book_id = input("Enter unique Book ID: ")

        cursor.execute("SELECT * FROM BOOKS WHERE book_id = %s", (book_id,))
        show = cursor.fetchone()
        if show:
            print("Book ID already exists.\n")
            return

        cursor.execute(
            "INSERT INTO BOOKS(book_id, book_title, available) VALUES (%s, %s, TRUE)",
            (book_id, title)
        )
        db.commit()
        print("Book added successfully.\n")
    except Exception as e:
        print("Error adding book:", e)

def show_data():
    try:
        check = input("Enter admin password--: ")
        if check != "admin123":
            print("ACCESS DENIED")
            return

        query = """
            SELECT BOOKS.book_id, BOOKS.book_title, BOOKS.available, 
                   USERS.name, USERS.borrow, USERS.return_due
            FROM BOOKS
            LEFT JOIN USERS ON BOOKS.book_id = USERS.book_id
        """
        cursor.execute(query)
        files = cursor.fetchall()

        print("\n --- Library Book Status ---\n")
        for s in files:
            book_id, title, available, name, borrow, return_due = s
            print(f"Book ID     : {book_id}")
            print(f"Title       : {title}")
            print(f"Available   : {'Yes' if available else 'No'}")
            if not available and name:
                print(f"   Borrowed By : {name}")
                print(f"   Borrowed On : {borrow}")
                print(f"   Return Due  : {return_due}")
            print()
    except Exception as e:
        print("Error", e)

def main():
    while True:
        print("\n---- Library Management System ----")
        print("1. Borrow Book")
        print("2. Return Book")
        print("3. Add Book (For Admin Only)")
        print("4. Show All Book Records (For Admin Only)")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            borrow_book()
        elif choice == '2':
            return_book()
        elif choice == '3':
            add_book()
        elif choice == '4':
            show_data()
        elif choice == '5':
            print("Exiting the system. Have a nice day!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    try:
        main()
    finally:
        cursor.close()
        db.close()

