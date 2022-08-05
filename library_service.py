import mysql.connector
import datetime
from datetime import timedelta


class MySQLConnector:
    @staticmethod
    def get_connection():
        conn = mysql.connector.connect(host="localHost",
                                       user="root",
                                       password="root",
                                       database="college_library")
        return conn

    @staticmethod
    def close_connection(connection):
        if connection:
            connection.close()


class LibraryService:

    @staticmethod
    def student_registration_details(name, email, id, password):
        conn = MySQLConnector.get_connection()
        cursor = conn.cursor()
        query = "insert into student_details (name, email, id, password) \
                values ( '" + name + "', '" + email + "', " + str(id) + ",'" + password + "')"
        cursor.execute(query)
        conn.commit()
        return "student registered successfully"

    @staticmethod
    def check_authority(student_id, password):
        conn = MySQLConnector.get_connection()
        cursor = conn.cursor()
        query = "select id, password from student_details"
        cursor.execute(query)
        data = cursor.fetchall()
        conn.commit()
        if (student_id, password) in data:
            return True
        else:
            return False

    @staticmethod
    def register_book(book_id, title, author, quantity, status):
        conn = MySQLConnector.get_connection()
        cursor = conn.cursor()
        query = "insert into books_detail (book_id, title, author, quantity, status) \
        values ( " + str(book_id) + ", '" + title + "', '" + author + "'," + str(quantity) + ", '" + status + "')"
        cursor.execute(query)
        conn.commit()
        return "Book registered successfully"

    @staticmethod
    def registered_book_details():
        conn = MySQLConnector.get_connection()
        cursor = conn.cursor()
        query = "SELECT * FROM books_detail"
        cursor.execute(query)
        data = cursor.fetchall()
        return data

    @staticmethod
    def remove_book(book_id):
        conn = MySQLConnector.get_connection()
        cursor = conn.cursor()
        query = "DELETE FROM books_detail where book_id = " + str(book_id)
        cursor.execute(query)
        conn.commit()
        return print("Book with id = " + str(book_id) + " remove successfully")

    @staticmethod
    def get_book(book_id, student_name):
        conn = MySQLConnector.get_connection()
        cursor = conn.cursor()
        query = "SELECT status, quantity FROM books_detail where book_id = " + str(book_id)
        cursor.execute(query)
        data = cursor.fetchone()
        status = data[0]
        quantity = data[1]
        print(status, quantity)
        if status == 'available' and quantity > 0:
            query = "UPDATE books_detail SET quantity = (quantity-1) where book_id = " + str(book_id)
            cursor.execute(query)
            conn.commit()
            issued_date = datetime.datetime.now().date()
            due_date = issued_date + timedelta(days=30)
            query = "INSERT INTO book_status (book_id, issued_to_name, issued_date, due_date) \
                     VALUES (" + str(book_id) + ",'" + student_name + "', \
                     str_to_date('" + str(issued_date) + "','%Y-%m-%d'), \
                     str_to_date('" + str(due_date) + "','%Y-%m-%d'))"
            cursor.execute(query)
            print(query)
            cursor.execute(query)
            conn.commit()
            return "Book issued successfully, return before " + str(due_date) + " to avoid charges"
        else:
            return "Book not available"

    @staticmethod
    def return_books(book_id):
        conn = MySQLConnector.get_connection()
        cursor = conn.cursor()
        query = "UPDATE books_detail SET quantity = (quantity+1) where book_id = " + str(book_id)
        cursor.execute(query)
        conn.commit()
        query = "SELECT issued_date FROM book_status where book_id = " + str(book_id)
        cursor.execute(query)
        issued_date = cursor.fetchone()[0]
        print(issued_date)
        return_date = datetime.datetime.now().date()
        print(return_date)
        query = "UPDATE book_status SET return_date = str_to_date('" + \
                str(return_date) + "' ,'%Y-%m-%d') where book_id = " + str(book_id)
        cursor.execute(query)
        conn.commit()
        total_day = return_date - issued_date
        print(total_day)
        if total_day > timedelta(days=30):
            message = "Your book return day is overdue plz pay late fee"
        else:
            message = "You successfully return book"
        return message

